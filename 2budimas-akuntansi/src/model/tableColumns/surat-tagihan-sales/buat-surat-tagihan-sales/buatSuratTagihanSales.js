import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import IndeterminateCheckbox from "@/src/components/ui/IndeterminateCheckbox.vue";
import T from "@/src/components/ui/table/T.vue";
import { parseCurrency } from "@/src/lib/utils";

const columnHelper = createColumnHelper();

export const buatSuratTagihanSalesColumn = [
  columnHelper.display({
    id: "no",
    header: h("div", { class: "tw-pl-3", innerText: "No" }),
    cell: (info) => h(T, { innerText: info.row.index + 1 }),
  }),
  columnHelper.accessor((row) => row.nomor_faktur, {
    id: "nomor_faktur",
    header: h("div", { innerText: "Faktur" }),
    cell: (info) =>
      h("div", {
        class: "table-cell-lg",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.accessor((row) => row.total_order, {
    id: "total_penjualan",
    header: "Total Order",
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
  columnHelper.accessor((row) => row.tgl_jatuh_tempo, {
    id: "tgl_jatuh_tempo",
    header: "Tgl Jatuh Tempo",
    cell: (info) =>
      h("div", {
        class: "table-cell-medium",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.display({
    id: "action",
    header: ({ table }) =>
      h("div", { class: "tw-px-2 tw-pt-1" }, [
        h(IndeterminateCheckbox, {
          checked: table.getIsAllRowsSelected(),
          indeterminate: table.getIsSomeRowsSelected(),
          onChange: table.getToggleAllRowsSelectedHandler(),
        }),
      ]),
    cell: ({ row }) => {
      return h("div", { class: "tw-px-2 tw-pt-1" }, [
        h(IndeterminateCheckbox, {
          checked: row.getIsSelected(),
          disabled: !row.getCanSelect(),
          onChange: row.getToggleSelectedHandler(),
        }),
      ]);
    },
  }),
];
