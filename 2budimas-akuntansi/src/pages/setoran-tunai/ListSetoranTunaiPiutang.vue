<script setup>
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import {listSetoranTunaiPiutangColumn} from "@/src/model/tableColumns/setoran-tunai/listSetoranTunai";
import {setoranService} from "@/src/services/setoran";
import {usePagination} from "@/src/lib/usePagination";
import {useFiltering} from "@/src/lib/useFiltering";
import {useSorting} from "@/src/lib/useSorting";
import ServerTable from "@/src/components/ui/table/ServerTable.vue";
import {ref} from "vue";
import Label from "@/src/components/ui/Label.vue";
import SelectInput from "@/src/components/ui/formInput/SelectInput.vue";
import VueDatePicker from "@vuepic/vue-datepicker";
import Button from "@/src/components/ui/Button.vue";
// import { useOthers } from "@/src/store/others";
import {useUser} from "@/src/store/user";
import {$swal} from "@/src/components/ui/SweetAlert.vue";
import {useFetchPaginateV2} from "@/src/lib/useFetchPaginateV2";

// const others = useOthers();
const user = useUser();
const sales = ref();
const statusSetoran = ref();
const periodeAwal = ref(null);
const periodeAkhir = ref(null);
const selectedStatus = ref(1);
const advancedFilters = ref([])
const statusOptions = [
  {
    name: "Kasir",
    value: 1,
  },
]

const {endpoints} = setoranService;
const {onPaginationChange, pagination} = usePagination();
const {onColumnFilterChange, globalFilters} = useFiltering();
const {onSortingChange, sorting} = useSorting();
const [data, count, loading, totalPage, key] = useFetchPaginateV2(
    `/api/akuntansi/get-list-konfirmasi-setoran-tunai?`,
    {
      pagination,
      sorting,
      globalFilters,
      initialSortColumn: "draft_tanggal_input",
      advancedFilters: advancedFilters,
      isRunOnMounted: true,
    }
);

const reset = () => {
  periodeAwal.value = null;
  periodeAkhir.value = null;
};

const searchQuery = () => {
  if (periodeAwal.value > periodeAkhir.value) {
    $swal.error(
        "Periode Awal tidak boleh lebih besar dari Periode Akhir",
    )
    return;
  }
  advancedFilters.value = [
    {
      column: "periode_awal",
      value: periodeAwal.value,
    },
    {
      column: "periode_akhir",
      value: periodeAkhir.value,
    },
  ];

}
</script>

<template>
  <FlexBox full flex-col>
    <SlideRightX
        class="slide-container tw-z-10"
        :duration-enter="0.6"
        :duration-leave="0.6"
        :delay-in="0.1"
        :delay-out="0.1"
        :initial-x="-40"
        :x="40">
      <Card no-subheader>
        <template #header>Form Pencarian Piutang</template>
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
                  v-model="selectedStatus"
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
            <div class="tw-flex tw-gap-2">
              <Button
                  :trigger="reset"
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
        class="slide-container"
        :duration-enter="0.6"
        :duration-leave="0.6"
        :delay-in="0.2"
        :delay-out="0.2"
        :initial-x="-40"
        :x="40">
      <Card no-subheader>
        <template #header>List Tagihan</template>
        <template #content>
          <ServerTable
              :columns="listSetoranTunaiPiutangColumn"
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
              :total-data="count"/>
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>
