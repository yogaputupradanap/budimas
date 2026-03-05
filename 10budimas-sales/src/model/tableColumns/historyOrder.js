import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import { parseCurrency } from "../../lib/utils";

const columnHelper = createColumnHelper();
export const HistoryOrderColumns = [
  columnHelper.accessor((row) => row.no_order, {
    id: "noOrder",
    cell: (info) =>
      h("div", { class: "table-cell-lg", innerText: info.getValue() }),
    header: () =>
      h("div", { class: "tw-pl-2", innerText: "Nota Order" }),
  }),
  columnHelper.accessor((row) => row.kode, {
    id: "kodeCustomer",
    cell: (info) => {
      return h("div", { class: "tw-w-28 tw-text-xs", innerText: info.getValue() });
    },
    header: () =>
      h("div", { class: "tw-w-28 tw-text-start", innerText: "Kode Customer" }),
  }),
  columnHelper.accessor((row) => row.nama, {
    id: "namaCustomer",
    cell: (info) => {
      let text = info.getValue().toLowerCase();
      return h("div", { class: "tw-w-44 tw-text-xs", innerText: text });
    },
    header: () => "nama customer",
  }),
  columnHelper.accessor((row) => row.nama_principal, {
    id: "kodePrincipal",
    cell: (info) => {
      let text = info.getValue().toLowerCase();
      return h("div", { class: "tw-w-44 te-text-xs", innerText: text });
    },
    header: () => "nama principal",
  }),
  columnHelper.accessor((row) => row.total_penjualan, {
    id: "totalBayar",
    cell: (info) =>
      h("div", {
        class: "tw-w-28 tw-text-xs",
        innerText: "Rp. " + parseCurrency(info.getValue()),
      }),
    header: () => "total bayar",
  }),
  columnHelper.accessor((row) => row.tanggal_order, {
    id: "tanggalOrder",
    cell: (info) => h("div", { class: "tw-w-24 tw-text-xs", innerText: info.getValue() }),
    header: () => "tanggal order",
  }),
  columnHelper.accessor((row) => row.status_faktur, {
    id: "status",
    cell: (info) => {
      const status = info.getValue();
      const statusObj = {
        0: "Draft",
        1: "Pending Pembayaran",
        2: "Booked",
        3: "Di Ambil Dari Gudang",
        4: "Sedang Dikirim",
        5: "Terkirim",
        6: "Lunas",
        7: "Gagal",
        8: "Terkirim"
      };

      const statusToText = statusObj.hasOwnProperty(status)
        ? statusObj[status]
        : "On Process";

      return h("div", {
        class: "tw-w-28 tw-text-xs",
        innerText: statusToText,
      });
    },
    header: () => "status",
  }),
];
