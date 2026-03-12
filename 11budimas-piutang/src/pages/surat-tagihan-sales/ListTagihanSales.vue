<script setup>
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import ServerTable from "@/src/components/ui/table/ServerTable.vue";
import { listSuratTagihanColumn } from "@/src/model/tableColumns/surat-tagihan-sales/listSuratTagihanSales";
import Label from "@/src/components/ui/Label.vue";
import SelectInput from "@/src/components/ui/formInput/SelectInput.vue";
import VueDatePicker from "@vuepic/vue-datepicker";
import Button from "@/src/components/ui/Button.vue";
import RouterButton from "@/src/components/ui/RouterButton.vue";
import { usePagination } from "@/src/lib/usePagination";
import { useFiltering } from "@/src/lib/useFiltering";
import { useSorting } from "@/src/lib/useSorting";
import { useFetchPaginate } from "@/src/lib/useFetchPaginate";
import { piutangService } from "@/src/services/piutang";
import { useOthers } from "@/src/store/others";
import { computed, ref } from "vue";
import Skeleton from "@/src/components/ui/Skeleton.vue";
import { useTableSearch } from "@/src/lib/useTableSearch";
import { format } from "date-fns";
import Table from "@/src/components/ui/table/Table.vue";

const others = useOthers();

const { baseUrl } = piutangService;
const { onPaginationChange, pagination } = usePagination();
const { onColumnFilterChange, globalFilters } = useFiltering();
const { onSortingChange, sorting } = useSorting();

const sales = ref(null);
const customer = ref(null);
const principal = ref(null);
const jatuhTempo = ref(null);

const containerKey = ref(0);

const formatJatuhTempo = computed(() => {
  if (jatuhTempo.value) {
    return format(new Date(jatuhTempo.value), "yyyy-MM-dd");
  }
  return null;
});

const fieldPool = [sales, customer, principal, jatuhTempo];
const queryEntries = computed(() => [
  ["sales=", sales.value],
  ["customer=", customer.value],
  ["principal=", principal.value],
  ["jatuh_tempo=", formatJatuhTempo.value],
]);

const options = {
  initialColumnName: "nota_tagihan",
  checkFieldFilterFunc: (val) => val[1] === null,
  filterFunction: (val) => val[1] !== null,
  asArgument: true,
};

const [data, count, loading, totalPage, key] = useFetchPaginate(`${baseUrl}?`, {
  pagination,
  sorting,
  globalFilters,
  initialSortColumn: "nota_tagihan",
});

const [
  clientData,
  button,
  searchLoading,
  isServerTable,
  clientKey,
  searchQuery,
] = useTableSearch(baseUrl, fieldPool, queryEntries, options);

const reset = () => {
  fieldPool.forEach((val) => (val.value = null));
  isServerTable.value = true;
};
</script>

<template>
  <FlexBox full flex-col :key="containerKey">
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
            <Label label="Sales">
              <Skeleton
                class="skeleton"
                v-if="others.sales.loading" />
              <SelectInput
                v-else
                v-model="sales"
                placeholder="Pilih Data"
                size="md"
                :search="true"
                :options="others.sales.list"
                text-field="nama"
                value-field="id" />
            </Label>
            <Label label="Customer">
              <Skeleton
                class="skeleton"
                v-if="others.customer.loading" />
              <SelectInput
                v-else
                v-model="customer"
                placeholder="Pilih Data"
                size="md"
                :search="true"
                :options="others.customer.list"
                text-field="nama"
                value-field="id"
                :virtual-scroll="true" />
            </Label>
            <Label label="Principal ">
              <Skeleton
                class="skeleton"
                v-if="others.principal.loading" />
              <SelectInput
                v-else
                v-model="principal"
                placeholder="Pilih Data"
                size="md"
                :search="true"
                :options="others.principal.list"
                text-field="nama"
                value-field="id" />
            </Label>
            <Label label="Tangal Jatuh Tempo">
              <VueDatePicker
                v-model="jatuhTempo"
                :enable-time-picker="false"
                placeholder="mm/dd/yyyy"
                auto-apply />
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
      class="slide-container tw-justify-end"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.2"
      :delay-out="0.2"
      :initial-x="-40"
      :x="40">
      <RouterButton
        icon="mdi mdi-plus-thick"
        class="tw-px-4 tw-py-2"
        to="/surat-tagihan-sales/buat-surat-tagihan">
        Buat Surat Tagihan
      </RouterButton>
    </SlideRightX>

    <SlideRightX
      class="slide-container tw-justify-end"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.2"
      :delay-out="0.2"
      :initial-x="-40"
      :x="40">
      <Card no-subheader>
        <template #header>List Surat Tagihan</template>
        <template #content>
          <ServerTable
            v-if="isServerTable"
            table-width="tw-w-[90vw]"
            :columns="listSuratTagihanColumn"
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
            table-width="tw-w-[90vw]"
            :key="clientKey"
            :columns="listSuratTagihanColumn"
            :table-data="clientData.pages" />
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>