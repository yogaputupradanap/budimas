<script setup>
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import {listSetoranNonTunaiColumn} from "@/src/model/tableColumns/setoran-non-tunai/listSetoranNonTunai";
import {setoranService} from "@/src/services/setoran";
import {usePagination} from "@/src/lib/usePagination";
import {useFiltering} from "@/src/lib/useFiltering";
import {useSorting} from "@/src/lib/useSorting";
import ServerTable from "@/src/components/ui/table/ServerTable.vue";
import {ref, watch} from "vue";
import SelectInput from "@/src/components/ui/formInput/SelectInput.vue";
import Button from "@/src/components/ui/Button.vue";
import VueDatePicker from "@vuepic/vue-datepicker";
import {$swal} from "@/src/components/ui/SweetAlert.vue";
// import { useOthers } from "@/src/store/others";
import Label from "@/src/components/ui/Label.vue";
import {useFetchPaginateV2} from "@/src/lib/useFetchPaginateV2";
import Modal from "@/src/components/ui/Modal.vue";
import {useRouter} from "vue-router";

// const others = useOthers();

const statusSetoran = ref(4);
const periodeAwal = ref(null);
const periodeAkhir = ref(null);
const advancedFilters = ref([]);

const {endpoints} = setoranService;
const router = useRouter();
const selectedDataMutasi = ref(null);
const modalPilihDetail = ref(null);
const selectedStatusMutasi = ref(1); // Default to "Belum Terpakai"
const statusMutasiOptions = ref([
  {
    name: "Belum Terpakai",
    value: 1,
  },
  {
    name: "Sudah Terpakai",
    value: 0,
  },
  {
    name: "Semua",
    value: 2, // This option is for showing all statuses
  }
]);
const {onPaginationChange, pagination} = usePagination();
const {onColumnFilterChange, globalFilters} = useFiltering();
const {onSortingChange, sorting} = useSorting();

const [data, count, loading, totalPage, key] = useFetchPaginateV2(
    `/api/akuntansi/get-list-konfirmasi-setoran-nontunai?`,
    {
      pagination,
      sorting,
      globalFilters,
      initialSortColumn: "tanggal_mutasi",
      advancedFilters: advancedFilters,
      isRunOnMounted: true,
    }
);

const statusOptions = [
  {
    name: "Sales",
    value: 1,
  },
  {
    name: "Mutasi",
    value: 4,
  },
]

const searchQuery = () => {
  if (periodeAwal.value > periodeAkhir.value) {
    $swal.error(
        "Periode Awal tidak boleh lebih besar dari Periode Akhir",
    )
    return;
  }

  advancedFilters.value = [
    {
      column: "status",
      value: statusSetoran.value,
    },
    {
      column: "periode_awal",
      value: periodeAwal.value,
    },
    {
      column: "periode_akhir",
      value: periodeAkhir.value,
    },
    {
      column: "status_mutasi",
      value: selectedStatusMutasi.value.toString(),
    }
  ];


}


const showModal = (data) => {
  modalPilihDetail.value.show();
  selectedDataMutasi.value = data;
}

const handleByCustomer = () => {
  modalPilihDetail.value.hide();
  router.push('/setoran-non-tunai/customer/' + selectedDataMutasi.value.id_mutasi);
}

const handleBySales = () => {
  modalPilihDetail.value.hide();
  router.push('/setoran-non-tunai/sales/' + selectedDataMutasi.value.id_mutasi);
}

const resetQuery = () => {
  periodeAwal.value = null
  periodeAkhir.value = null
  selectedStatusMutasi.value = 1; // Reset to "Belum Terpakai"
  advancedFilters.value = [];
}

// watch(data, (newVal) => {
//   console.log("Isi variabel data dari useFetchPaginateV2:", newVal);
//   console.log("Tipe data:", typeof newVal);
//   if (newVal && typeof newVal === 'object') {
//     console.log("Keys yang tersedia:", Object.keys(newVal));
//   }
// }, { deep: true });
</script>

<template>
  <FlexBox full flex-col>
    <Modal ref="modalPilihDetail" id="modalPilihDetail" size="md" :centered="true">
      <SlideRightX
          :duration-enter="0.3"
          :duration-leave="0.3"
          :delay-in="0.1"
          :delay-out="0.1"
          :initial-x="-20"
          :x="20">
        <Card no-subheader>
          <template #header>
            <div class="tw-flex tw-justify-between tw-items-center">
              <span>Pilih Sumber Mutasi</span>
            </div>
          </template>
          <template #content>
            <div class="tw-space-y-4 tw-w-full">
              <Button
                  class="tw-w-full tw-py-3"
                  :trigger="handleByCustomer"
              >
                Pilih Berdasrkan Customer
              </Button>
              <Button
                  class="tw-w-full tw-py-3"
                  :trigger="handleBySales"
              >
                Pilih Berdasarkan Sales
              </Button>
            </div>
          </template>
        </Card>
      </SlideRightX>
    </Modal>
    <SlideRightX
        class="slide-container tw-z-10"
        :duration-enter="0.6"
        :duration-leave="0.6"
        :delay-in="0.1"
        :delay-out="0.1"
        :initial-x="-40"
        :x="40">
      <Card no-subheader>
        <template #header>List Konfirmasi Setoran Nontunai</template>
        <template #content>
          <div
              class="tw-grid tw-grid-cols-1 md:tw-grid-cols-4 2xl:tw-grid-cols-5 tw-gap-4 tw-items-end">
            <!-- <Label label="Sales">
              <Skeleton
                class="tw-w-full tw-h-[34px]"
                v-if="others?.sales?.loading" />
              <SelectInput
                v-else
                v-model="sales"
                placeholder="Pilih Data"
                size="md"
                :search="true"
                :options="others?.sales?.list"
                text-field="nama"
                value-field="id" />
            </Label> -->
            <Label label="Status">
              <SelectInput
                  v-model="statusSetoran"
                  placeholder="Pilih Data"
                  size="md"
                  :search="true"
                  :options="statusOptions"
                  :disabled="true"
                  text-field="name"
                  value-field="value"/>
            </Label>

            <Label label="Periode Awal">
              <VueDatePicker
                  v-model="periodeAwal"
                  model-type="yyyy-MM-dd"
                  format="yyyy-MM-dd"
                  :clearable="false"
                  :enable-time-picker="false"
                  placeholder="yyyy-MM-dd"
                  auto-apply/>
            </Label>
            <Label label="Periode Akhir">
              <VueDatePicker
                  v-model="periodeAkhir"
                  model-type="yyyy-MM-dd"
                  format="yyyy-MM-dd"
                  :clearable="false"
                  :enable-time-picker="false"
                  placeholder="yyyy-MM-dd"
                  auto-apply/>
            </Label>
            <Label label="Status Mutasi">
              <SelectInput
                  v-model="selectedStatusMutasi"
                  placeholder="Pilih Data"
                  size="md"
                  :search="true"
                  :options="statusMutasiOptions"
                  text-field="name"
                  value-field="value"/>
            </Label>
            <div class="tw-flex tw-gap-2">
              <Button
                  :trigger="resetQuery"
                  icon="mdi mdi-reload"
                  class="tw-h-[38px] tw-w-full xl:tw-w-32 tw-bg-red-500">
                Reset
              </Button>
              <Button
                  :trigger="searchQuery"
                  icon="mdi mdi-magnify"
                  class="tw-h-[38px] tw-w-full xl:tw-w-32">
                Cari Data
              </Button>
            </div>
          </div>
        </template>
      </Card>
    </SlideRightX>
    <SlideRightX
        v-if="statusSetoran === 4"
        class="slide-container"
        :duration-enter="0.6"
        :duration-leave="0.6"
        :delay-in="0.2"
        :delay-out="0.2"
        :initial-x="-40"
        :x="40">
      <Card no-subheader>
        <template #header>List Mutasi Setoran Nontunai</template>
        <template #content>
          <ServerTable
            :columns="listSetoranNonTunaiColumn(showModal)"
            :key="key"
            
            :table-data="data?.result || []" 
            
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
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>
