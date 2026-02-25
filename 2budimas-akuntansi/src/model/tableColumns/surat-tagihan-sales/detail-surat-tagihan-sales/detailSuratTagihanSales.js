import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import Button from "@/src/components/ui/Button.vue";
import T from "@/src/components/ui/table/T.vue";
import { parseCurrency } from "@/src/lib/utils";
const columnHelper = createColumnHelper();

export const detailTagihanSalesColumn = [
  columnHelper.display({
    id: "no",
    header: h("div", { class: "tw-pl-3", innerText: "No" }),
    cell: (info) => h(T, { innerText: info.row.index + 1 }),
  }),
  columnHelper.accessor((row) => row.no_faktur, {
    id: "no_faktur",
    header: h("div", { innerText: "Faktur" }),
    cell: (info) =>
      h("div", {
        class: "table-cell-lg",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.accessor((row) => row.total_penjualan, {
    id: "total_penjualan",
    header: "Total Order",
    cell: (info) =>
      h("div", {
        class: "table-cell-medium",
        innerText: parseCurrency(info.getValue()),
      }),
  }),
  columnHelper.accessor((row) => row.angsuran, {
    id: "angsuran",
    header: "Angsuran",
    cell: (info) =>
      h("div", {
        class: "table-cell-medium",
        innerText: parseCurrency(info.getValue()),
      }),
  }),
  columnHelper.accessor((row) => row.tanggal_order, {
    id: "tanggal_order",
    header: "Tanggal Order",
    cell: (info) =>
      h("div", {
        class: "table-cell-medium",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.accessor((row) => row.tanggal_jatuh_tempo, {
    id: "tanggal_jatuh_tempo",
    header: "Tgl Jatuh Tempo",
    cell: (info) =>
      h("div", {
        class: "table-cell-medium",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.display({
    id: "bukti_bayar",
    header: "Bukti Bayar",
    cell: ({ row, column, table }) => {
      const openModal = () => {
        table.options.meta.updateRow(
          row.original,
          row.index,
          column.id,
          "openRowModal"
        );
      };
      return h(
        Button,
        {
          class: "tw-px-7 tw-py-2",
          trigger: openModal,
        },
        "Lihat"
      );
    },
  }),
];
