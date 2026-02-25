import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";

const columnHelper = createColumnHelper();

export const detailPengirimanStockTransferColumn = [
  columnHelper.display({
    id: "no",
    header: h("div", { class: "tw-px-4", innerText: "No" }),
    cell: (info) => h("div", { class: "tw-px-4", innerText: info.row.index + 1 }),
  }),
  columnHelper.accessor((row) => row.kode_sku, {
    id: "sku",
    header: "SKU",
    cell: (info) => h("div", {
      class: "tw-w-28 md:tw-w-auto",
      innerText: info.getValue(),
    }),
  }),
  columnHelper.accessor((row) => row.nama_produk, {
    id: "nama_produk",
    header: "Produk",
    cell: (info) => h("div", {
      class: "tw-w-44 md:tw-w-auto",
      innerText: info.getValue(),
    }),
  }),
  columnHelper.accessor((row) => row.nama_principal, {
    id: "nama_principal",
    header: "Nama Principal",
    cell: (info) => h("div", {
      class: "tw-w-44 md:tw-w-auto",
      innerText: info.getValue(),
    }),
  }),
  columnHelper.accessor((row) => row.carton, {
    id: "uom1",
    header: "UOM 1",
    cell: (info) => h("div", {
      class: "tw-w-16 md:tw-w-auto",
      innerText: info.getValue(),
    }),
  }),
  columnHelper.accessor((row) => row.box, {
    id: "UOM 2",
    header: "UOM 2",
    cell: (info) => h("div", {
      class: "tw-w-16 md:tw-w-auto",
      innerText: info.getValue(),
    }),
  }),
  columnHelper.accessor((row) => row.pieces, {
    id: "UOM 3",
    header: "UOM 3",
    cell: (info) => h("div", {
      class: "tw-w-16 md:tw-w-auto",
      innerText: info.getValue(),
    }),
  })
];
