<script setup>
import {
  getCoreRowModel,
  useVueTable,
  getFilteredRowModel,
  getSortedRowModel,
  getPaginationRowModel,
} from "@tanstack/vue-table";
import { ref, defineProps, defineEmits } from "vue";
import TableHeader from "./TableHeader.vue";
import TableBody from "./TableBody.vue";
import Toolbar from "./Toolbar.vue";
import Footer from "./Footer.vue";
import Loader from "../Loader.vue";
import Empty from "../Empty.vue";
import { defineExpose } from "vue";

const props = defineProps({
  columns: null,
  tableData: null,
  hideFooter: Boolean,
  hideToolbar: Boolean,
  classic: Boolean,
  loading: Boolean,
  tableWidth: String,
});
const updateParentData = defineEmits(["change", "openRowModal", "removeRow"]);

const data = ref(props.tableData);
const globalFilter = ref("");
const sortColumn = ref([]);
const rowSelection = ref({});

const table = useVueTable({
  get data() {
    return data.value;
  },
  columns: props.columns,
  state: {
    get sorting() {
      return sortColumn.value;
    },
    get globalFilter() {
      return globalFilter.value;
    },
    get rowSelection() {
      return rowSelection.value;
    },
  },
  onSortingChange: (updaterOrValue) => {
    sortColumn.value =
      typeof updaterOrValue === "function"
        ? updaterOrValue(sortColumn.value)
        : updaterOrValue;
  },
  onRowSelectionChange: (updateOrValue) => {
    rowSelection.value =
      typeof updateOrValue === "function"
        ? updateOrValue(rowSelection.value)
        : updateOrValue;
  },
  getRowId: row => row.id,
  enableRowSelection: true,
  getCoreRowModel: getCoreRowModel(),
  getFilteredRowModel: !props.hideToolbar ? getFilteredRowModel() : undefined,
  getSortedRowModel: getSortedRowModel(),
  getPaginationRowModel: !props.hideFooter
    ? getPaginationRowModel()
    : undefined,
  initialState: {
    pagination: {
      pageIndex: 0,
      pageSize: props.hideFooter && props.hideToolbar ? 100 : 10,
    },
  },
  meta: {
    updateData: (rowIndex, columnId, value) => {
      const updatedData = data.value.map((dat, index) => {
        if (index === rowIndex) {
          return {
            ...dat,
            [columnId]: value,
          };
        }
        return { ...dat };
      });
      updateParentData("change", updatedData);
    },
    updateRow: (value, rowIndex, columnId, emits) => {
      const dat = { value, rowIndex, columnId };
      updateParentData(emits, dat);
    },
  },
});

const getSelectedRow = () => table.getState().rowSelection

defineExpose({
  getSelectedRow
})
</script>

<template>
  <div v-if="!loading" class="tw-w-full">
    <Empty text="Data Kosong" v-if="!data.length" />
    <div :class="['tw-p-4 tw-flex tw-flex-col tw-gap-6', tableWidth && 'tw-items-center']" v-else>
      <Toolbar :table="table" v-model="globalFilter" v-if="!hideToolbar" />
      <div
        :class="[
          !tableWidth
            ? 'xl:tw-overflow-hidden tw-overflow-auto'
            : 'tw-w-[77vw] md:tw-w-[81vw] lg:tw-w-[61vw] xl:tw-w-[69vw] 2xl:tw-w-[74vw] tw-overflow-x-scroll',
        ]">
        <table :class="!tableWidth ? 'tw-w-full' : tableWidth">
          <TableHeader :table="table" :classic="classic" />
          <TableBody :table="table" :classic="classic" />
        </table>
      </div>
      <Footer :table="table" :total-data="data.length" v-if="!hideFooter" />
    </div>
  </div>
  <div
    class="tw-w-full tw-h-56 tw-p-6 tw-flex tw-justify-center tw-items-center tw-bg-gray-50 tw-rounded-lg"
    v-else>
    <Loader />
  </div>
</template>
