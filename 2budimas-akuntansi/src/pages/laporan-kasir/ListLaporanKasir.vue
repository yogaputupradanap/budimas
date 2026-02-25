<script setup>
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import Table from "@/src/components/ui/table/Table.vue";
import { listLaporanKasirColumn } from "@/src/model/tableColumns/laporan-kasir/listLaporanKasirColumn";
import { setoranService } from "@/src/services/setoran";
import { usePagination } from "@/src/lib/usePagination";
import { useFiltering } from "@/src/lib/useFiltering";
import { useSorting } from "@/src/lib/useSorting";
import { useFetchPaginate } from "@/src/lib/useFetchPaginate";
import ServerTable from "@/src/components/ui/table/ServerTable.vue";
import { computed, inject, onMounted, ref } from "vue";
import Label from "@/src/components/ui/Label.vue";
import Skeleton from "@/src/components/ui/Skeleton.vue";
import VueDatePicker from "@vuepic/vue-datepicker";
import Button from "@/src/components/ui/Button.vue";
import { useTableSearch } from "@/src/lib/useTableSearch";
// import { useOthers } from "@/src/store/others";
import { useUser } from "@/src/store/user";
import { getTodayDate } from "@/src/lib/utils";

// const others = useOthers();
const user = useUser();
const periodeAwal = ref(getTodayDate());
const periodeAkhir = ref(getTodayDate());

const { endpoints } = setoranService;
const { onPaginationChange, pagination } = usePagination();
const { onColumnFilterChange, globalFilters } = useFiltering();
const { onSortingChange, sorting } = useSorting();
const [data, count, loading, totalPage, key] = useFetchPaginate(
  `${endpoints.listLaporanKasir}`,
  {
    pagination,
    sorting,
    globalFilters,
    initialSortColumn: "tanggal",
    additionalParams: {
      id_cabang: user?.user?.value?.id_cabang,
    },
  }
);

// all methods and properties that needed for table filtering
const fieldPool = [periodeAwal, periodeAkhir];
const queryEntries = computed(() => [
  ["periode_awal=", periodeAwal.value],
  ["periode_akhir=", periodeAkhir.value],
]);

const options = {
  initialColumnName: "tanggal",
  checkFieldFilterFunc: (val) => val[1] === undefined || val[1] === null,
  filterFunction: (val) => val[1] !== undefined && val[1] !== null,
  asArgument: true,
};

const [
  clientData,
  button,
  searchLoading,
  isServerTable,
  clientKey,
  searchQuery,
] = useTableSearch(
  endpoints.listLaporanKasir,
  fieldPool,
  queryEntries,
  options
);

const reset = () => {
  periodeAwal.value = getTodayDate();
  periodeAkhir.value = getTodayDate();
  isServerTable.value = true;
};
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
        <template #header>Filter Laporan Kasir</template>
        <template #content>
          <FlexBox full flexCol itEnd class="md:tw-flex-row">
            <FlexBox full>
              <Label label="Periode Awal">
                <VueDatePicker
                  v-model="periodeAwal"
                  model-type="yyyy-MM-dd"
                  format="yyyy-MM-dd"
                  :clearable="false"
                  :enable-time-picker="false"
                  placeholder="yyyy-MM-dd"
                  auto-apply />
              </Label>
              <Label label="Periode Akhir">
                <VueDatePicker
                  v-model="periodeAkhir"
                  model-type="yyyy-MM-dd"
                  format="yyyy-MM-dd"
                  :clearable="false"
                  :enable-time-picker="false"
                  placeholder="yyyy-MM-dd"
                  auto-apply />
              </Label>
            </FlexBox>
            <FlexBox full jusEnd>
              <Button
                :trigger="reset"
                icon="mdi mdi-reload"
                class="tw-h-[38px] tw-w-full xl:tw-w-32 tw-bg-red-500">
                Reset
              </Button>
              <Button
                :loading="searchLoading"
                :trigger="searchQuery"
                :icon="button.icon"
                class="tw-h-[38px] tw-w-full xl:tw-w-32">
                Cari Data
              </Button>
            </FlexBox>
          </FlexBox>
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
        <template #header>
          <div class="tw-flex tw-justify-between tw-items-center">
            <span>List Laporan Kasir</span>
          </div>
        </template>
        <template #content>
          <ServerTable
            v-if="isServerTable"
            :columns="listLaporanKasirColumn"
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
            :total-data="count" />
          <Table
            v-else
            :key="clientKey"
            :columns="listLaporanKasirColumn"
            :table-data="clientData.pages" />
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>
