<script setup>
import { onMounted, watch } from "vue";
import { useFetchPaginate } from "../lib/useFetchPaginate";
import { useFiltering } from "../lib/useFiltering";
import { usePagination } from "../lib/usePagination";
import { useSorting } from "../lib/useSorting";
import { voucherService } from "../services/voucher";
import Card from "./ui/Card.vue";
import FlexBox from "./ui/FlexBox.vue";
import RouterButton from "./ui/RouterButton.vue";
import ServerTable from "./ui/table/ServerTable.vue";

const props = defineProps(["tipeVoucher", "data", "column"]);

const { voucherApi } = voucherService;

const query = `${voucherApi}?tipe-voucher=${props.tipeVoucher}`;

const { onPaginationChange, pagination } = usePagination();
const { onColumnFilterChange, globalFilters } = useFiltering();
const { onSortingChange, sorting } = useSorting();

const [data, count, loading, totalPage, key] = useFetchPaginate(query, {
  pagination,
  sorting,
  globalFilters,
  asInitArgument: false,
});

const removeRow = (value) => {
  data.value = value;
  key.value++;
};

const refreshTable = () => {
  key.value++;
};

onMounted(refreshTable);
</script>

<template>
  <FlexBox full flex-col>
    <FlexBox full jus-end>
      <RouterButton
        icon="mdi mdi-plus"
        :to="`/voucher-${tipeVoucher}/add-voucher-${tipeVoucher}`">
        Add Voucher
      </RouterButton>
    </FlexBox>
    <Card no-subheader>
      <template #header>List Voucher</template>
      <template #content>
        <ServerTable
          @remove-row="(data) => removeRow(data)"
          table-width="tw-w-[90vw]"
          :columns="column"
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
      </template>
    </Card>
  </FlexBox>
</template>
