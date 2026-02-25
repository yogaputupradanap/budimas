<script setup>
import SlideRightX from "../components/animation/SlideRightX.vue";
import Card from "../components/ui/Card.vue";

import Table from "../components/ui/table/Table.vue";
import StatusBar from "../components/ui/StatusBar.vue";
import { tableDetailPicking } from "../model/tableColumns";
import { usePicking } from "../store/picking";
import { inject, onMounted, ref, computed } from "vue";
import { apiUrl, fetchWithAuth } from "../lib/utils";
import Button from "../components/ui/Button.vue";
import { useAlert } from "../store/alert";
import { useRoute, useRouter } from "vue-router";
import { useKepalaCabang } from "@/src/store/kepalaCabang";

const user = useKepalaCabang();
const picking = usePicking();
const tableKey = ref(0);
const localStore = ref([]);
const produkInfo = ref(null);
const loadingProduk = ref(true);
const alert = useAlert();
const router = useRoute();
const idProduk = router.params.id_produk;
const idCabang = computed(() => user.kepalaCabangUser?.id_cabang);

const totalPermintaan = ref(0);
const $swal = inject("$swal");

const nav = useRouter();
const change = ({ value, rowIndex, columnId }) => {
  localStore.value = localStore.value.map((val, idx) => {
    if (rowIndex === idx) {
      return {
        ...val,
        [columnId]: value,
      };
    }

    return { ...val };
  });
};

const getProduk = async () => {
  try {
    loadingProduk.value = true;

    const url = new URL("/api/produk/get-produk", apiUrl);
    url.searchParams.set("id_produk", idProduk);
    url.searchParams.set("id_cabang", idCabang.value);

    const produk = await fetchWithAuth("GET", url.toString());

    if (!Object.keys(produk).length) throw "Informasi produk tidak ada di stok";

    produkInfo.value = { ...produk };
  } catch (error) {
    $swal.error(error);
    console.log(error);
  } finally {
    loadingProduk.value = false;
  }
};

const hitungTotalPermintaan = () => {
  if (localStore.value && localStore.value.length > 0) {
    totalPermintaan.value = localStore.value.reduce((total, item) => {
      return total + (parseInt(item.total_in_pieces) || 0);
    }, 0);
  } else {
    totalPermintaan.value = 0;
  }
};

const totalPermintaanakhir = computed(() =>
  (localStore.value || []).reduce(
    (total, item) => total + (Number(item?.total_in_pieces) || 0),
    0
  )
);

const submitPicked = async () => {
  try {
    const filterPicked = localStore.value
      .filter((val) => val.picking !== null)
      .map((val) => ({
        picking: val.picking,
        id_order_detail: val.id_order_detail,
        idProduk,
      }));

    if (!filterPicked.length) throw "Semua field jumlah picking kosong !!!";

    // Validasi: cek apakah ada picking yang melebihi total order
    for (const item of localStore.value) {
      if (item.picking !== null && item.picking !== undefined) {
        const totalOrder = parseInt(item.total_in_pieces) || 0;
        const picking = parseInt(item.picking) || 0;

        if (picking > totalOrder) {
          throw `Jumlah picking untuk toko "${item.nama_customer}" (${picking} pcs) tidak boleh lebih besar dari total order (${totalOrder} pcs)`;
        }
      }
    }

    picking.resetPickingState("listAddPicking");
    const isConfirm = await $swal.confirmEdit();
    if (!isConfirm) return;
    await fetchWithAuth(
      "POST",
      `${apiUrl}/api/distribusi/submit-produk-picking`,
      {
        id_cabang: idCabang.value,
        picking: filterPicked,
      }
    );

    await getProduk();
    $swal.success("Berhasil mengubah jumlah produk picking");
    const id_rute = router.params.id_rute;
    const id_armada = localStore.value[0].id_armada;
    const id_driver = localStore.value[0].id_driver;
    const delivering_date = localStore.value[0].delivering_date;
    await picking.getListAddPicking(
      id_rute,
      idCabang,
      id_armada,
      id_driver,
      delivering_date
    );
    nav.back();
  } catch (error) {
    $swal.error(error || "Gagal mengubah jumlah produk picking");
    console.log(error);
  }
};

const getResource = async () => {
  const id_rute = router.params.id_rute;
  const id_order_detail = router.query.id_order_detail;

  await picking.getDetailListPicking(
    idProduk,
    id_rute,
    id_order_detail
  );

  await getProduk();

  localStore.value =
    picking.listDetailPicking.detailPicking.map((item) => ({
      ...item,
      produkInfo: produkInfo.value,
    }));

  tableKey.value++;
};

onMounted(async () => {
  if (!idCabang.value) return;
  getResource();
});
</script>

<template>
  <div class="tw-flex tw-flex-col tw-gap-4 lg:tw-px-4 tw-px-0">
    <SlideRightX
      class=""
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-out="0.1"
      :delay-in="0.1"
      :initial-x="-40"
      :x="40">
      <Card :no-subheader="true">
        <template #header>View Detail Picking</template>
        <template #content>
          <div
            class="tw-grid tw-grid-cols-1 md:tw-grid-cols-3 tw-gap-4 tw-w-full tw-mb-5">
            <StatusBar
              label="Kode Produk :"
              :value="produkInfo?.kode_sku"
              :loading="loadingProduk" />
            <StatusBar
              label="Nama Produk :"
              :value="produkInfo?.nama"
              :loading="loadingProduk" />
            <StatusBar
              label="Satuan :"
              value="pieces"
              :loading="loadingProduk" />
          </div>
        </template>
      </Card>
    </SlideRightX>
    <SlideRightX
      class=""
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.2"
      :delay-out="0.2"
      :initial-x="-40"
      :x="40">
      <Card :no-subheader="true">
        <template #header>Daftar Toko</template>
        <template #content>
          <div class="tw-w-full">
            <div class="status-field-container-2-col">
              <StatusBar
                label="Total Permintaan :"
                :value="String(totalPermintaanakhir)"
                :loading="loadingProduk"
              />

              <StatusBar
                label="Stok :"
                :value="String(produkInfo?.jumlah_good ?? 0)"
                :loading="loadingProduk"
              />
            </div>
            <Table
              :key="tableKey"
              :loading="picking.listDetailPicking.loading"
              :table-data="localStore"
              :columns="tableDetailPicking"
              @change="change" />
            <div class="tw-w-full tw-flex tw-justify-end tw-pb-4">
              <Button
                :trigger="submitPicked"
                class="tw-bg-green-500 tw-w-24 tw-h-9"
                icon="mdi mdi-check">
                submit
              </Button>
            </div>
          </div>
        </template>
      </Card>
    </SlideRightX>
  </div>
</template>
