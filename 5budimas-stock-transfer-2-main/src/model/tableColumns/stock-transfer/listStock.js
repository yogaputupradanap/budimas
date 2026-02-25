import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";

const columnHelper = createColumnHelper();
export const listStockColumns = [
  columnHelper.accessor((row) => row.nama_produk, {
    id: "produk.nama",
    header: "Produk",
    cell: (info) =>
      h("div", { class: "tw-w-52 md:tw-w-auto", innerText: info.getValue() }),
  }),
  columnHelper.accessor((row) => row.sku, {
    id: "produk.kode_sku",
    header: "SKU",
    cell: (info) =>
      h("div", { class: "tw-w-20 md:tw-w-auto", innerText: info.getValue() }),
  }),
  columnHelper.accessor((row) => row.nama_cabang, {
    id: "cabang.nama",
    header: "Cabang",
    cell: (info) =>
      h("div", { class: "tw-w-52 md:tw-w-auto", innerText: info.getValue() }),
  }),

  columnHelper.accessor((row) => row.satuan, {
    id: "produk.satuan",
    header: "Satuan",
    cell: (info) =>
      h("div", { class: "tw-w-20 md:tw-w-auto", innerText: info.getValue() }),
  }),
  columnHelper.accessor((row) => row.nama_principal, {
    id: "principal.nama",
    header: "Principal",
    cell: (info) =>
      h("div", { class: "tw-w-44 md:tw-w-auto", innerText: info.getValue() }),
  }),
  columnHelper.accessor((row) => row.jumlah_good, {
    id: "stok.jumlah_good",
    header: "Jumlah",
    cell: (info) =>
      h("div", { class: "tw-w-44 md:tw-w-auto", innerText: info.getValue() }),
  }),
];
