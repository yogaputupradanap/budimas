<script setup>
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import Table from "@/src/components/ui/table/Table.vue";
import {listSetoranTunaiColumn} from "@/src/model/tableColumns/setoran-tunai/listSetoranTunai";
import {setoranService} from "@/src/services/setoran";
import {usePagination} from "@/src/lib/usePagination";
import {useFiltering} from "@/src/lib/useFiltering";
import {useSorting} from "@/src/lib/useSorting";
import {useFetchPaginate} from "@/src/lib/useFetchPaginate";
import ServerTable from "@/src/components/ui/table/ServerTable.vue";
import {computed, ref, watchEffect } from "vue";
import Label from "@/src/components/ui/Label.vue";
import SelectInput from "@/src/components/ui/formInput/SelectInput.vue";
import VueDatePicker from "@vuepic/vue-datepicker";
import Button from "@/src/components/ui/Button.vue";
import {useTableSearch} from "@/src/lib/useTableSearch";
// import { useOthers } from "@/src/store/others";
import {useUser} from "@/src/store/user";
import {getTodayDate, statusSetoranList} from "@/src/lib/utils";

// const others = useOthers();
const user = useUser();
const sales = ref();
const statusSetoran = ref();
const periodeAwal = ref(getTodayDate());
const periodeAkhir = ref(getTodayDate());

const {endpoints} = setoranService;
const {onPaginationChange, pagination} = usePagination();
const {onColumnFilterChange, globalFilters} = useFiltering();
const {onSortingChange, sorting} = useSorting();
const [data, count, loading, totalPage, key] = useFetchPaginate(
    `${endpoints.tunai}`,
    {
      pagination,
      sorting,
      globalFilters,
      initialSortColumn: "draft_tanggal_input",
      additionalParams: {
        id_cabang: user?.user?.value?.id_cabang,
        tipe_setoran: 1, // Tambahkan ini (1 untuk Tunai)
        periode_awal: periodeAwal.value,
        periode_akhir: periodeAkhir.value,
      },
    }
);

// all methods and properties that needed for table filtering
const fieldPool = [sales, statusSetoran, periodeAwal, periodeAkhir];
const queryEntries = computed(() => [
  ["sales=", sales.value],
  ["status=", statusSetoran.value],
  ["periode_awal=", periodeAwal.value],
  ["periode_akhir=", periodeAkhir.value],
]);

const options = {
  initialColumnName: "draft_tanggal_input",
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
] = useTableSearch(endpoints.tunai, fieldPool, queryEntries, options);

const reset = () => {
  fieldPool.forEach((val) => (val.value = null));
  periodeAwal.value = getTodayDate();
  periodeAkhir.value = getTodayDate();
  isServerTable.value = true;
};

// watchEffect(() => {
//   console.log("CEK DATA API:", data.value);
//   console.log("APAKAH DATA BERBENTUK ARRAY?", Array.isArray(data.value));
// }); 
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
        <template #header>List Tagihan</template>
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
                  :options="statusSetoranList"
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
                  :loading="searchLoading"
                  :trigger="searchQuery"
                  :icon="button.icon"
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
              v-if="isServerTable"
              :columns="listSetoranTunaiColumn"
              :key="key"
              :table-data="data?.pages?.result || data?.result || []" 
              :loading="loading"
              :on-pagination-change="onPaginationChange"
              :on-global-filters-change="onColumnFilterChange"
              :on-sorting-change="onSortingChange"
              :pagination="pagination"
              :sorting="sorting"
              :filter="globalFilters"
              :page-count="totalPage"
              :total-data="count"/>
          <Table
              v-else
              :key="clientKey"
              :columns="listSetoranTunaiColumn"
              :table-data="clientData?.pages?.result || clientData?.result || clientData" />
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>
