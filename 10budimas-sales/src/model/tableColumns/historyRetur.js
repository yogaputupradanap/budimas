import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import { parseCurrency } from "../../lib/utils";

const columnHelper = createColumnHelper();
export const HistoryReturColumns = [
  columnHelper.accessor((row) => row.no_order, {
    id: "noOrder",
    cell: (info) =>
      h("div", { class: "tw-w-24 tw-text-center tw-break-all", innerText: info.getValue() }),
    header: () => h('div', {class: 'tw-w-24 tw-text-center', innerText: "Nota Order"}),
  }),
  columnHelper.accessor((row) => row.kode, {
    id: "kodeCustomer",
    cell: (info) =>
      h("div", { class: "tw-w-28", innerText: info.getValue() }),
    header: () => "kode customer",
  }),
  columnHelper.accessor((row) => row.nama, {
    id: "namaCustomer",
    cell: (info) =>
      h("div", { class: "tw-w-44", innerText: info.getValue() }),
    header: () => "nama customer",
  }),
  columnHelper.accessor((row) => row.nama_principal, {
    id: "namaPrincipal",
    cell: (info) =>
      h("div", { class: "tw-w-44", innerText: info.getValue() }),
    header: () => "nama principal",
  }),
  columnHelper.accessor((row) => row.total_penjualan, {
    id: "totalBayar",
    cell: (info) =>
      h("div", {
        class: "tw-w-24",
        innerText: "Rp. " + parseCurrency(info.getValue()),
      }),
    header: () => "total retur",
  }),
  columnHelper.accessor((row) => row.tanggal_order, {
    id: "tanggalOrder",
    cell: (info) =>
      h("div", { class: "tw-w-24", innerText: info.getValue() }),
    header: () => "tanggal order",
  }),
];
