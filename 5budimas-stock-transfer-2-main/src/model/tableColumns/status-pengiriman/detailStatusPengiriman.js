import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";

const columnHelper = createColumnHelper();

export const detailStatusPengirimanColumn = [
  columnHelper.display({
    id: "no",
    header: h("div", { class: "tw-pl-4", innerText: "No" }),
    cell: (info) => h("div", { class: "tw-pl-4", innerText: info.row.index + 1 }),
  }),
  columnHelper.accessor((row) => row.sku, {
    id: "sku",
    header: "SKU",
    cell: (info) => info.getValue(),
  }),
  columnHelper.accessor((row) => row.nama_produk, {
    id: "nama_produk",
    header: "Produk",
    cell: (info) => info.getValue(),
  }),
  columnHelper.accessor((row) => row.nama_principal, {
    id: "nama_principal",
    header: "Nama Principal",
    cell: (info) => info.getValue(),
  }),
  columnHelper.accessor((row) => row.uom1, {
    id: "uom1",
    header: "UOM 1",
    cell: (info) => info.getValue(),
  }),
  columnHelper.accessor((row) => row.uom2, {
    id: "UOM 2",
    header: "UOM 2",
    cell: (info) => info.getValue(),
  }),
  columnHelper.accessor((row) => row.uom3, {
    id: "UOM 3",
    header: "UOM 3",
    cell: (info) => info.getValue(),
  })
];
