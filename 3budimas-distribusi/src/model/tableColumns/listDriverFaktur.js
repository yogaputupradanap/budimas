import TableInput from "@/src/components/ui/table/TableInput.vue";
import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
const columnHelper = createColumnHelper();

const checkKey = (field, original, tipe) => {
  const check = original.hasOwnProperty(field);
  return {
    rowValue: check ? original[field] : 0,
    tipeValue: tipe,
  };
};

export const listDriverFakturColumn = [
  columnHelper.accessor((row) => row.nama_customer, {
    id: "nama_customer",
    header: () =>
      h("div", { class: "tw-w-48 tw-text-start tw-pl-2" }, "Customer"),
    cell: (info) =>
      h("div", { class: "tw-w-48 tw-text-xs tw-pl-2" }, info.getValue()),
  }),
  columnHelper.accessor((row) => row.nomor_faktur, {
    id: "nomor_faktur",
    header: () => h("div", { class: "tw-w-40 tw-text-start" }, "Nomor Faktur"),
    cell: (info) => h("div", { class: "tw-w-40 tw-text-xs" }, info.getValue()),
  }),
  columnHelper.display({
    id: "6",
    header: "Parkir",
    cell: (info) => {
      const value = checkKey("nominal_parkir", info.row.original, 6);
      
      return h(TableInput, {
        table: info.table,
        column: info.column.id,
        row: info.row.index,
        type: "number",
        initialValue: value.rowValue,
        placeholder: "uang parkir",
      });
    },
  }),
  columnHelper.display({
    id: "7",
    header: "Bongkar",
    cell: (info) => {
      const value = checkKey("nominal_bongkar", info.row.original, 7)

      return h(TableInput, {
        table: info.table,
        column: info.column.id,
        row: info.row.index,
        type: "number",
        initialValue: value.rowValue,
        placeholder: "uang bongkar",
      });
    },
  }),
  columnHelper.display({
    id: "8",
    header: "Lainnya",
    cell: (info) => {
      const value = checkKey("nominal_lainnya", info.row.original, 8)

      return h(TableInput, {
        table: info.table,
        column: info.column.id,
        row: info.row.index,
        type: "number",
        initialValue: value.rowValue,
        placeholder: "uang lainnya",
      });
    },
  }),
  columnHelper.display({
    id: "keterangan",
    header: "Keterangan",
    cell: (info) => {
      return h(TableInput, {
        table: info.table,
        column: info.column.id,
        row: info.row.index,
        initialValue: info.row.original?.keterangan || "",
        placeholder: "keterangan",
      });
    },
  }),
];
