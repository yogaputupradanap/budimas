import {createColumnHelper} from "@tanstack/vue-table";
import {h} from "vue";
import {formatCurrencyAuto} from "@/src/lib/utils";

const columnHelper = createColumnHelper();

export const detailLphCol = [
    columnHelper.display({
        id: "no",
        header: () => h("div", {class: "tw-pl-3", innerText: "No"}),
        cell: (info) =>
            h("div", {class: "tw-pl-3", innerText: info.row.index + 1}),
    }),
    columnHelper.accessor((row) => row.nama_customer, {
        id: "nama_customer",
        header: "customer",
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
    columnHelper.accessor((row) => row.sisa_pembayaran, {
        id: "sisa_pembayaran",
        header: "Total Tagihan",
        cell: (info) =>
            h("div", {
                class: "table-cell-medium",
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
    columnHelper.accessor((row) => row.kode_cn || '-', {
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
                class: "table-cell-medium",
                innerText: formatCurrencyAuto(info.getValue()),
            }),
    }),
];

export const detailLphCustomerCol = [
    columnHelper.display({
        id: "no",
        header: () => h("div", {class: "tw-pl-3", innerText: "No"}),
        cell: (info) =>
            h("div", {class: "tw-pl-3", innerText: info.row.index + 1}),
    }),
    columnHelper.accessor((row) => row.nama_sales, {
        id: "nama_sales",
        header: "sales",
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
    columnHelper.accessor((row) => row.sisa_pembayaran, {
        id: "sisa_pembayaran",
        header: "Total Tagihan",
        cell: (info) =>
            h("div", {
                class: "table-cell-medium",
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
    columnHelper.accessor((row) => row.kode_cn || '-', {
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
                class: "table-cell-medium",
                innerText: formatCurrencyAuto(info.getValue()),
            }),
    }),
];
