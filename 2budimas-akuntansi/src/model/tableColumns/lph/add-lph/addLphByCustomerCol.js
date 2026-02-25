import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import { formatCurrencyAuto } from "@/src/lib/utils";

const columnHelper = createColumnHelper();

export const addLphByCustomerColumns = [
  columnHelper.display({
    id: "select",
    header: ({ table }) =>
      h("div", { class: "tw-flex tw-justify-center tw-w-full tw-mx-2" }, [
        h("input", {
          type: "checkbox",
          class: "tw-h-4 tw-w-4",
          checked: table.getIsAllRowsSelected(),
          indeterminate: table.getIsSomeRowsSelected(),
          onChange: table.getToggleAllRowsSelectedHandler(),
        }),
      ]),

    cell: ({ row }) =>
      h("div", { class: "tw-flex tw-justify-center" }, [
        h("input", {
          type: "checkbox",
          class: "tw-h-4 tw-w-4",
          checked: row.getIsSelected(),
          disabled: !row.getCanSelect(),
          indeterminate: row.getIsSomeSelected(),
          onChange: row.getToggleSelectedHandler(),
        }),
      ]),
  }),
  columnHelper.accessor((row) => row.nama_sales, {
    id: "nama_sales",
    header: "Sales",
    cell: (info) =>
      h("div", {
        class: "table-cell-medium",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.accessor((row) => row.kode_customer, {
    id: "kode_customer",
    header: "kode customer",
    cell: (info) =>
      h("div", {
        class: "table-cell-medium",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.accessor((row) => row.tanggal_faktur, {
    id: "tanggal_faktur",
    header: "tanggal faktur",
    cell: (info) =>
      h("div", {
        class: "table-cell-medium",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.accessor((row) => row.no_faktur, {
    id: "no_faktur",
    header: "no faktur",
    cell: (info) =>
      h("div", {
        class: "table-cell-medium",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.accessor((row) => row.total_penjualan, {
    id: "total_penjualan",
    header: "Total Tagihan",
    cell: (info) =>
      h("div", {
        class: "tw-text-end ",
        innerText: formatCurrencyAuto(info.getValue()),
      }),
  }),
  columnHelper.accessor((row) => row.sisa_pembayaran, {
    id: "sisa_pembayaran",
    header: "Sisa Tagihan",
    cell: (info) =>
      h("div", {
        class: "tw-text-end ",
        innerText: formatCurrencyAuto(info.getValue()),
      }),
  }),
  columnHelper.accessor((row) => row.tanggal_jatuh_tempo, {
    id: "tanggal_jatuh_tempo",
    header: "tanggal jatuh tempo",
    cell: (info) =>
      h("div", {
        class: "table-cell-medium",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.accessor((row) => row.kode_cn, {
    id: "kode_cn",
    header: "Nota Retur",
    size: 60,
    cell: (info) =>
      h("div", {
        class: "table-cell-medium ",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.accessor((row) => row.nominal_retur, {
    id: "total_retur",
    header: "Nilai Retur",
    cell: (info) =>
      h("div", {
        class: "tw-text-end ",
        innerText: formatCurrencyAuto(info.getValue()),
      }),
  }),
];

export const addLphCustomerColModal = [
  columnHelper.display({
    id: "select",
    header: ({ table }) =>
      h("div", { class: "tw-flex tw-justify-center tw-w-full tw-mx-2" }, [
        h("input", {
          type: "checkbox",
          class: "tw-h-4 tw-w-4",
          checked: table.getIsAllRowsSelected(),
          indeterminate: table.getIsSomeRowsSelected(),
          onChange: table.getToggleAllRowsSelectedHandler(),
        }),
      ]),

    cell: ({ row }) =>
      h("div", { class: "tw-flex tw-justify-center" }, [
        h("input", {
          type: "checkbox",
          class: "tw-h-4 tw-w-4",
          checked: row.getIsSelected(),
          disabled: !row.getCanSelect(),
          indeterminate: row.getIsSomeSelected(),
          onChange: row.getToggleSelectedHandler(),
        }),
      ]),
  }),
  columnHelper.accessor((row) => row.tanggal_faktur, {
    id: "tanggal_faktur",
    header: "tanggal faktur",
    cell: (info) =>
      h("div", {
        class: "table-cell-medium",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.accessor((row) => row.no_faktur, {
    id: "no_faktur",
    header: "no faktur",
    cell: (info) =>
      h("div", {
        class: "table-cell-medium",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.accessor((row) => row.total_penjualan, {
    id: "total_penjualan",
    header: "Total Tagihan",
    cell: (info) =>
      h("div", {
        class: "tw-text-end ",
        innerText: formatCurrencyAuto(info.getValue()),
      }),
  }),
  columnHelper.accessor((row) => row.sisa_pembayaran, {
    id: "sisa_pembayaran",
    header: "Sisa Tagihan",
    cell: (info) =>
      h("div", {
        class: "tw-text-end ",
        innerText: formatCurrencyAuto(info.getValue()),
      }),
  }),
  columnHelper.accessor((row) => row.tanggal_jatuh_tempo, {
    id: "tanggal_jatuh_tempo",
    header: "tanggal jatuh tempo",
    cell: (info) =>
      h("div", {
        class: "table-cell-medium",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.accessor((row) => row.kode_cn || "-", {
    id: "kode_cn",
    header: "Nota Retur",
    cell: (info) =>
      h("div", {
        class: "table-cell-medium",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.accessor((row) => row.nominal_retur, {
    id: "total_retur",
    header: "Nilai Retur",
    cell: (info) =>
      h("div", {
        class: "tw-text-end ",
        innerText: formatCurrencyAuto(info.getValue()),
      }),
  }),
];
