import {createColumnHelper} from "@tanstack/vue-table";
import {h} from "vue";
import {formatCurrencyAuto} from "@/src/lib/utils";

const columnHelper = createColumnHelper();

export const listSetoranDetailTunai = [
    columnHelper.display({
        id: "no",
        header: () => h("div", {class: "tw-pl-3", innerText: "No"}),
        cell: (info) =>
            h("div", {class: "tw-pl-3", innerText: info.row.index + 1}),
    }),
    columnHelper.accessor((row) => row.nama_customer, {
        id: "nama_customer",
        header: "Nama Customer",
        cell: (info) =>
            h("div", {
                class: "table-cell-lg",
                innerText: info.getValue(),
            }),
    }),
    columnHelper.accessor((row) => row.nama_principal, {
        id: "nama_principal",
        header: "Principal",
        cell: (info) =>
            h("div", {
                class: "table-cell-medium",
                innerText: info.getValue(),
            }),
    }),
    columnHelper.accessor((row) => row.no_faktur, {
        id: "no_faktur",
        header: "No Faktur",
        cell: (info) => {
            return h("div", {
                class: "table-cell-medium",
                innerText: info.getValue(),
            });
        },
    }),
    columnHelper.accessor((row) => row.tanggal_jatuh_tempo, {
        id: "tanggal_setoh_tempo",
        header: "Tanggal Jatuh Tempo",
        cell: (info) =>
            h("div", {
                class: "table-cell-medium",
                innerText: info.getValue(),
            }),
    }),
    columnHelper.accessor((row) => row.total_penjualan - row.total_retur - row.setoran, {
        id: "tagihan",
        header: "Tagihan",
        cell: (info) =>
            h("div", {
                class: "tw-text-end",
                innerText: formatCurrencyAuto(info.getValue()),
            }),
    }),
    columnHelper.accessor((row) => row.setor_diterima_kasir, {
        id: "setor_diterima_kasir",
        header: "Diterima Kasir",
        cell: (info) =>
            h("div", {
                class: "tw-text-end",
                innerText: formatCurrencyAuto(info.getValue()),
            }),
    }),
];
