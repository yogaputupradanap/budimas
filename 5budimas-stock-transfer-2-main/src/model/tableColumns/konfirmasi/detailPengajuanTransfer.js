import TableInput from "@/src/components/ui/table/TableInput.vue";
import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";

const columnHelper = createColumnHelper();

export const detailPengajuanTransferColumn = [
  columnHelper.display({
    id: "no",
    header: h("div", { class: "tw-pl-4", innerText: "No" }),
    cell: (info) =>
      h("div", { class: "tw-pl-4", innerText: info.row.index + 1 }),
  }),
  columnHelper.accessor((row) => row.nama_produk, {
    id: "nama_produk",
    header: "Produk",
    cell: (info) =>
      h("div", {
        class: "tw-w-52 md:tw-w-auto",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.accessor((row) => row.nama_principal, {
    id: "nama_principal",
    header: "Principal",
    cell: (info) =>
      h("div", {
        class: "tw-w-52 md:tw-w-auto",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.display({
    id: "uom3",
    header: "UOM 3",
    cell: (info) =>
      h(TableInput, {
        table: info.table,
        column: info.column.id,
        row: info.row.index,
        initialValue: info.row.original.carton,
        type: "number",
      }),
  }),
  columnHelper.display({
    id: "uom2",
    header: "UOM 2",
    cell: (info) =>
      h(TableInput, {
        table: info.table,
        column: info.column.id,
        row: info.row.index,
        initialValue: info.row.original.box,
        type: "number",
      }),
  }),
  columnHelper.display({
    id: "uom1",
    header: "UOM 1",
    cell: (info) =>
      h(TableInput, {
        table: info.table,
        column: info.column.id,
        row: info.row.index,
        initialValue: info.row.original.pieces,
        type: "number",
      }),
  }),
];
