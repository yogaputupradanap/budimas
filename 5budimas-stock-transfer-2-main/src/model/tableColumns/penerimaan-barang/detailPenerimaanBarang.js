import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import TableInput from "@/src/components/ui/table/TableInput.vue";
import T from "@/src/components/ui/table/T.vue";

const columnHelper = createColumnHelper();

export const detailPenerimaanBarangColumn = [
  columnHelper.display({
    id: "no",
    header: h(T, () => "No"),
    cell: (info) => h(T, () => info.row.index + 1),
  }),
  columnHelper.accessor((row) => row.nama_produk, {
    id: "nama_produk",
    header: h(T, () => "Produk"),
    cell: (info) => h(T, () => info.getValue()),
  }),
  columnHelper.accessor((row) => row.jumlah_picked, {
    id: "jumlah",
    header: h(T, () => "Jumlah Order"),
    cell: (info) => h(T, () => info.getValue()),
  }),
  columnHelper.group({
    id: "uoms",
    header: h(
      "div",
      { class: "tw-w-full tw-flex tw-justify-center" },
      "jumlah order"
    ),
    columns: [
      columnHelper.accessor((row) => row.carton, {
        id: "uom1",
        header: h(T, () => "UOM 3"),
        cell: (info) => h(T, () => info.getValue()),
      }),
      columnHelper.accessor((row) => row.box, {
        id: "uom2",
        header: h(T, () => "UOM 2"),
        cell: (info) => h(T, () => info.getValue()),
      }),
      columnHelper.accessor((row) => row.pieces, {
        id: "uom3",
        header: h(T, () => "UOM 1"),
        cell: (info) => h(T, () => info.getValue()),
      }),
    ],
  }),
  columnHelper.group({
    id: "uoms-input",
    header: h(
      "div",
      { class: "tw-w-full tw-flex tw-justify-center" },
      "jumlah diterima"
    ),
    columns: [
      columnHelper.display({
        id: "uom_3",
        header: h(T, () => "UOM 3"),
        cell: (info) =>
          h(T, () =>
            h(TableInput, {
              table: info.table,
              column: info.column.id,
              row: info.row.index,
              initialValue: info.row.original.picking,
              type: "number",
            })
          ),
      }),
      columnHelper.display({
        id: "uom_2",
        header: h(T, () => "UOM 2"),
        cell: (info) =>
          h(T, () =>
            h(TableInput, {
              table: info.table,
              column: info.column.id,
              row: info.row.index,
              initialValue: info.row.original.picking,
              type: "number",
            })
          ),
      }),
      columnHelper.display({
        id: "uom_1",
        header: h(T, () => "UOM 1"),
        cell: (info) =>
          h(T, () =>
            h(TableInput, {
              table: info.table,
              column: info.column.id,
              row: info.row.index,
              initialValue: info.row.original.picking,
              type: "number",
            })
          ),
      }),
    ],
  }),
  columnHelper.display({
    id: "keterangan",
    header: h(T, () => "Keterangan"),
    cell: (info) =>
      h(T, () =>
        h(TableInput, {
          class: "tw-w-52",
          table: info.table,
          column: info.column.id,
          row: info.row.index,
          initialValue: info.row.original.picking,
          type: "text",
        })
      ),
  }),
];
