<script setup>
import { getCoreRowModel, useVueTable } from "@tanstack/vue-table";
import { ref, defineProps } from "vue";
import TableHeader from "./TableHeader.vue";
import TableBody from "./TableBody.vue";
import Toolbar from "./Toolbar.vue";
import Footer from "./Footer.vue";
import Loader from "../Loader.vue";
import Empty from "../Empty.vue";

const props = defineProps({
  columns: null,
  tableData: null,
  hideFooter: Boolean,
  hideToolbar: Boolean,
  classic: Boolean,
  loading: Boolean,
  tableWidth: String,
  onPaginationChange: Function,
  onSortingChange: Function,
  onGlobalFiltersChange: Function,
  pagination: null,
  sorting: null,
  filter: null,
  pageCount: Number,
  totalData: Number,
});

const updateParentData = defineEmits(["customAction"]);

const data = ref(props.tableData);
const globalFilter = ref(props.filter.text);

const table = useVueTable({
  get data() {
    return data.value;
  },
  columns: props.columns,
  getCoreRowModel: getCoreRowModel(),
  manualPagination: true,
  manualSorting: true,
  enableGlobalFilter: true,
  onPaginationChange: props.onPaginationChange,
  onSortingChange: props.onSortingChange,
  onGlobalFilterChange: props.onGlobalFiltersChange,
  state: {
    get pagination() {
      return props.pagination;
    },
    get sorting() {
      return props.sorting;
    },
    get globalFilter() {
      return globalFilter.value;
    },
  },
  pageCount: props.pageCount,
  meta: {
    updateRow: (value, rowIndex, columnId, emits, funcId = null) => {
      const dat = { value, rowIndex, columnId, funcId };
      updateParentData(emits, dat);
    },
  },
});
</script>

<template>
  <div class="tw-w-full">
    <div class="tw-p-4 tw-flex tw-flex-col tw-gap-6">
      <Toolbar server :table="table" v-if="!hideToolbar" :filter="filter" />
      <div
        :class="[
          !tableWidth
            ? 'lg:tw-overflow-hidden tw-overflow-auto'
            : 'tw-w-[71vw] tw-min-w-full tw-overflow-x-scroll',
        ]">
        <table
          v-if="data.length"
          :class="[!tableWidth ? 'tw-w-full' : tableWidth, 'tw-min-h-auto']">
          <TableHeader :table="table" :classic="classic" />
          <TableBody
            server
            :loading="loading"
            :table="table"
            :classic="classic" />
        </table>
        <div
          class="tw-w-full tw-h-56 tw-p-6 tw-flex tw-justify-center tw-items-center tw-bg-gray-50 tw-rounded-lg"
          v-else>
          <Loader v-if="loading" />
          <Empty v-else text="Data Kosong" />
        </div>
      </div>
      <Footer :table="table" :total-data="totalData" v-if="!hideFooter" />
    </div>
  </div>
</template>

<style scoped>
/* width */
::-webkit-scrollbar {
  width: 5px;
  height: 5px;
}

::-webkit-scrollbar:hover {
  width: 10px;
}
/* Track */
::-webkit-scrollbar-track {
  background: #f1f5f9;
}

/* Handle */
::-webkit-scrollbar-thumb {
  border-radius: 15px;
  background: #cbd5e2;
}

/* Handle on hover */
::-webkit-scrollbar-thumb:hover {
  background: #afafaf;
}
</style>
