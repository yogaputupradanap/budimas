<script setup>
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import Label from "@/src/components/ui/Label.vue";
import { BFormInput } from "bootstrap-vue-next";
import Table from "@/src/components/ui/table/Table.vue";
import Button from "@/src/components/ui/Button.vue";
import { computed, onMounted, onUnmounted, ref, watch } from "vue";
import { useUser } from "@/src/store/user";
import { useOthers } from "@/src/store/others";
import { storeToRefs } from "pinia";
import { useRoute, useRouter } from "vue-router";
import { listProdukDetailColumns } from "@/src/model/tableColumns/stock-opname/listProdukDetail";
import { stockOpnameService } from "@/src/services/stockOpname";
import { useAlert } from "@/src/store/alert";
import { formatRupiah } from "@/src/lib/utils";
import Swal from "sweetalert2";

const others = useOthers();
const route = useRoute();
const router = useRouter();
const { stockOpname } = storeToRefs(others);
onUnmounted(() => {
  stockOpname.value.produks = [];
});

onMounted(() => {
  others.getOneStockOpnameDetail(route.params.id);
});

const alert = useAlert();
const userStore = useUser();
const isServerTable = ref(false);
const loadingSubmit = ref(false);
const kode_so = ref("");
const total = computed(() => {
  return stockOpname.value.produks.reduce((acc, val) => {
    return acc + val.subtotal;
  }, 0);
});
const totalSelisih = computed(() => {
  return stockOpname.value.produks.reduce((acc, val) => {
    return acc + val.subtotal_selisih;
  }, 0);
});
const tanggal = ref("");
const principal = ref("");
const jumlah_produk = ref("");
const keterangan = ref("");
const status = ref("");
const id_cabang = userStore.user.value?.id_cabang;

const localStore = ref(null);

const stockOpnameDiterima = async () => {
  try {
    const result = await Swal.fire({
      title: "Konfirmasi Penerimaan",
      text: `Anda akan menerima Stock Opname dengan kode ${kode_so.value}. Lanjutkan?`,
      icon: "question",
      showCancelButton: true,
      confirmButtonText: "Ya, Terima",
      cancelButtonText: "Batal",
      confirmButtonColor: "#28a745",
      focusConfirm: false
    })

    if (!result.isConfirmed) {
      return;
    }

    loadingSubmit.value = true;
    const data = {
      id_stock_opname: route.params.id,
      id_user: userStore.user.value.id,
      data_produks: stockOpname.value.produks,
      id_cabang: id_cabang,
      id_perusahaan: userStore.user.value?.id_perusahaan,
    };
    await stockOpnameService.putStockOpname("diterima", data);
    await others.getAllStockOpname();
    alert.setMessage("Berhasil menerima stock opname", "success");
    router.replace("/stock-opname");
  } catch (error) {
    alert.setMessage(error, "danger");
  } finally {
    loadingSubmit.value = false;
  }
};

const stockOpnameEskalasi = async () => {
  try {
    const result = await Swal.fire({
      title: "Konfirmasi Eskalasi",
      text: `Anda akan mengeskalasi Stock Opname dengan kode ${kode_so.value}. Lanjutkan?`,
      icon: "question",
      showCancelButton: true,
      confirmButtonText: "Ya, Eskalasi",
      cancelButtonText: "Batal",
      confirmButtonColor: "#28a745",
      focusConfirm: false
    })

    if (!result.isConfirmed) {
      return;
    }

    loadingSubmit.value = true;
    const data = {
      id_stock_opname: route.params.id,
      id_user: userStore.user.value.id,
    };

    await stockOpnameService.putStockOpname("eskalasi", data);
    await others.getAllStockOpname();

    alert.setMessage("Berhasil mengeskalasi stock opname", "success");
    router.replace("/stock-opname");
  } catch (e) {
    alert.setMessage(e, "danger");
  } finally {
    loadingSubmit.value = false;
  }
}

// const stockOpnameDitolak = async () => {
//   try {
//     loadingSubmit.value = true;
//     const data = {
//       id_stock_opname: route.params.id,
//       id_user: userStore.user.value.id,
//     };
//     await stockOpnameService.putStockOpname("ditolak", data);
//     await others.getAllStockOpname();
//     alert.setMessage("Berhasil menolak stock opname", "success");
//     router.replace("/stock-opname");
//   } catch (error) {
//     alert.setMessage(error, "danger");
//   } finally {
//     loadingSubmit.value = false;
//   }
// };

watch(stockOpname.value, () => {
  kode_so.value = stockOpname.value.produks[0]?.kode_so;
  tanggal.value = stockOpname.value.produks[0]?.tanggal_so;
  principal.value = stockOpname.value.produks[0]?.nama_principal;
  jumlah_produk.value = stockOpname.value.produks?.length;
  keterangan.value = stockOpname.value.produks[0]?.ket_so;
  status.value = stockOpname.value.produks[0]?.status_so;
});
</script>

<template>
  <FlexBox full flex-col>
    <SlideRightX
      class="slide-container"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.1"
      :delay-out="0.1"
      :initial-x="-40"
      :x="40"
    >
      <Card no-subheader>
        <template #header>Detail Stock Opname</template>
        <template #content>
          <div class="form-grid-card-3-menu tw-items-end">
            <Label label="Kode Stock Opname">
              <BFormInput disabled v-model="kode_so" placeholder="Cari Nama" />
            </Label>
            <Label label="Tanggal">
              <BFormInput disabled v-model="tanggal" placeholder="Cari SKU" />
            </Label>
            <Label label="Principal">
              <BFormInput
                disabled
                v-model="principal"
                placeholder="Cari Cabang"
              />
            </Label>
            <Label label="Jumlah Produk">
              <BFormInput
                disabled
                v-model="jumlah_produk"
                placeholder="Cari Cabang"
              />
            </Label>
            <Label label="Keterangan">
              <BFormInput
                disabled
                v-model="keterangan"
                placeholder="Cari Cabang"
              />
            </Label>
            <Label label="Status">
              <BFormInput disabled v-model="status" placeholder="Cari Cabang" />
            </Label>
          </div>
        </template>
      </Card>
    </SlideRightX>

    <SlideRightX
      class="slide-container"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.3"
      :delay-out="0.1"
      :initial-x="-40"
      :x="40"
    >
      <Card no-subheader>
        <template #header>List Produk</template>
        <template #content>
          <ServerTable
            v-if="isServerTable"
            :columns="listStockColumns"
            :key="key"
            :table-data="data"
            :loading="loading"
            :on-pagination-change="onPaginationChange"
            :on-global-filters-change="onColumnFilterChange"
            :on-sorting-change="onSortingChange"
            :pagination="pagination"
            :sorting="sorting"
            :filter="globalFilters"
            :page-count="totalPage"
            :total-data="count"
          />
          <Table
            v-else
            :key="localStore || []"
            :columns="listProdukDetailColumns()"
            :loading="stockOpname.loading"
            :table-data="stockOpname.produks"
            :classic="true"
          />
          <div class="tw-flex tw-justify-end tw-w-full tw-mt-4 tw-space-x-5">
            <h3 class="tw-text-black tw-font-bold tw-text-end">
              Total Selisih {{ formatRupiah(totalSelisih) }}
            </h3>
          </div>
          <div class="tw-flex tw-justify-end tw-w-full tw-mt-4 tw-space-x-5">
            <h3 class="tw-text-black tw-font-bold tw-text-end">
              Total {{ formatRupiah(total) }}
            </h3>
          </div>
          {{ userStore.user?.id_jabatan }}
          <div
            v-if="
              status === 'under review' && userStore.user.value.id_jabatan != 9
            "
            class="tw-flex tw-justify-end tw-w-full tw-mt-4 tw-space-x-3"
          >
            <!-- <Button
              class="btn-c-danger tw-text-base tw-py-2 tw-px-5"
              icon="mdi mdi-close"
              :loading="loadingSubmit"
              :trigger="stockOpnameDitolak"
              >Tolak</Button
            > -->
            <Button
              class="btn-c-danger tw-bg-[#9747ffc4] hover:tw-bg-[#9747ff] tw-text-base tw-py-2 tw-px-5"
              icon="mdi mdi-arrow-top-right"
              :trigger="stockOpnameEskalasi"
              >Eskalasi</Button
            >
            <Button
              class="btn-c-success tw-text-base tw-py-2 tw-px-5"
              icon="mdi mdi-check"
              :loading="loadingSubmit"
              :trigger="stockOpnameDiterima"
              >Terima</Button
            >
          </div>
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>
