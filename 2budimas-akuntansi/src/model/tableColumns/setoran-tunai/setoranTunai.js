import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import RouterButton from "@/src/components/ui/RouterButton.vue";

const columnHelper = createColumnHelper();

export const listPengajuanJurnalColumn = [
  columnHelper.display({
    id: "no",
    header: h("div", { class: "tw-pl-4 md:tw-pl-4 tw-w-12 tw-text-start md:tw-w-auto", innerText: "No" }),
    cell: (info) => h("div", { class: "tw-pl-4", innerText: info.row.index + 1 }),
  }),
  columnHelper.accessor((row) => row.customer, {
    id: "customer",
    header: "Customer",
    cell: (info) => h("div", { class: "tw-w-44 md:tw-w-auto", innerText: info.getValue() }),
  }),
  columnHelper.accessor((row) => row.tagihan, {
    id: "tagihan",
    header: "Tagihan",
    cell: (info) => {
      const tagihan = info.getValue();
      return h("div", { class: "tw-w-28 md:tw-w-auto", innerText: tagihan != null ? `Rp ${tagihan.toLocaleString()}` : "-" });
    },
  }),
  columnHelper.accessor((row) => row.setoran, {
    id: "setoran",
    header: "Setoran",
    cell: (info) => {
      const setoran = info.getValue();
      return h("div", { class: "tw-w-28 md:tw-w-auto", innerText: setoran != null ? `Rp ${setoran.toLocaleString()}` : "-" });
    },
  }),
  columnHelper.accessor((row) => row.saldo, {
    id: "saldo",
    header: "Saldo",
    cell: (info) => {
      const saldo = info.getValue();
      return h("div", { class: "tw-w-28 md:tw-w-auto", innerText: saldo != null ? `Rp ${saldo.toLocaleString()}` : "-" });
    },
  }),
  columnHelper.accessor((row) => row.faktur, {
    id: "jumlah_faktur",
    header: " Faktur",
    cell: (info) => h("div", { class: "tw-w-24 md:tw-w-auto", innerText: info.getValue() }),
  }),
  columnHelper.display({
    id: "action",
    header: "Actions",
    cell: (info) => {
      const id = info.row.original.id;
      return h(RouterButton, { to: `/jurnal/detail/${id}`, class: "tw-w-32" }, () => "Detail");
    },
  }),
];
