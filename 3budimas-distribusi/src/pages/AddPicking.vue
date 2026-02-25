<script setup>
import SlideRightX from "../components/animation/SlideRightX.vue";
import Card from "../components/ui/Card.vue";
import Table from "../components/ui/table/Table.vue";
import StatusBar from "../components/ui/StatusBar.vue";
import { tableAddPicking } from "../model/tableColumns";
import { usePicking } from "../store/picking";
import { inject, onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import PickingList from "../components/pdf/PickingList.vue";
import { apiUrl, downloadPdf, fetchWithAuth } from "../lib/utils";
import { useKepalaCabang } from "../store/kepalaCabang";
import Button from "../components/ui/Button.vue";
import { useAlert } from "../store/alert";


const user = useKepalaCabang();
const picking = usePicking();
const tableKey = ref(0);
const route = useRoute();
const pickingInfo = ref({});
const pdfName = `kertas picking ${new Date().toLocaleString()}`;
const idCabang = user.kepalaCabangUser.id_cabang;
const id_rute = route.params.id_rute;
const produk_id = route.params.produk_id;
const id_armada = route.query.id_armada;
const id_driver = route.query.id_driver;
const delivering_date = route.query.delivering_date;
const $swal = inject("$swal");
const router = useRouter();
const alert = useAlert();
const namaPicked = user.kepalaCabangUser.nama;

const getResource = async () => {
  await picking.getRutePicking(idCabang);

  await picking.getListAddPicking(
  id_rute,
  idCabang,
  id_armada,
  id_driver,
  delivering_date
);

// await picking.getDetailListPicking();
// console.log("add detail:", picking.getDetailListPicking);
console.log("params:", route.params);

console.log("ADD PICKING DATA:", picking.listAddPicking.addPicking);

  pickingInfo.value = picking.listPicking.rutePicking.find(
  (val) => val.id_rute == id_rute
);
};

const submitPicking = async () => {
  if (
    !picking.listAddPicking.addPicking ||
    picking.listAddPicking.addPicking.length === 0
  ) {
    alert("Tidak ada data picking untuk dikirim");
    return;
  }

  const data = {
    id_rute: id_rute,
    id_armada: id_armada,
    id_driver: id_driver,
    id_cabang: idCabang,
    delivering_date: delivering_date,
    nama_picked: namaPicked,
    list_picking: picking.listAddPicking.addPicking,
  };
  try {
    const isConfirm = await $swal.confirmSubmit();
    if (!isConfirm) return;
    const res = await fetchWithAuth(
      "POST",
      `${apiUrl}/api/distribusi/submit-picking`,
      data
    );
    $swal.success(res.message || "Berhasil mengirim picking");
    router.back();
  } catch (error) {
    $swal.error(error || "Gagal mengirim picking");
    console.log(error);
  }
};

onMounted(() => {
  console.log("route params:", route.params);
  console.log("route query:", route.query);
  console.log("id_rute:", id_rute);

  getResource();
});
</script>

<template>
  <div class="tw-flex tw-flex-col tw-gap-4 lg:tw-px-4 tw-px-0">
    <PickingList
      v-if="user.kepalaCabangUser"
      v-show="false"
      :picking-list="picking.listAddPicking.addPicking"
      :info="pickingInfo"
    />
    <SlideRightX
      class=""
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-out="0.1"
      :delay-in="0.1"
      :initial-x="-40"
      :x="40">
      <Card :no-subheader="true">
        <template #header>Add Picking</template>
        <template #content>
          <div class="status-field-container-2-col">
            <StatusBar
              :loading="picking.listAddPicking.loading"
              label="Kode :"
              :value="pickingInfo?.kode || ''" />
            <StatusBar
              :loading="picking.listAddPicking.loading"
              label="Rute :"
              :value="pickingInfo?.nama_rute || ''" />
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
        <template #header>Daftar Barang</template>
        <template #content>
          <Table
            :loading="picking.listAddPicking.loading"
            :table-data="picking.listAddPicking.addPicking"
            :columns="tableAddPicking"
            :key="tableKey" />
          <div class="tw-w-full tw-flex tw-justify-end tw-space-x-2">
            <BButton
              @click="downloadPdf('picking-list', pdfName)"
              variant="success"
              class="tw-bg-blue-500 tw-border-none tw-mb-5 tw-mr-3">
              <i class="mdi mdi-printer"></i>
              &nbsp;
              <p>Cetak</p>
            </BButton>
            <Button
              :trigger="submitPicking"
              icon="mdi mdi-check"
              class="tw-bg-green-500 tw-h-fit tw-py-2 tw-px-4">
              Submit
            </Button>
          </div>
        </template>
      </Card>
    </SlideRightX>
  </div>
</template>
