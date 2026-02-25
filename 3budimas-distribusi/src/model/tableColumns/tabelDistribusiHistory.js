import {createColumnHelper} from "@tanstack/vue-table";
import {h} from "vue";

const columnHelper = createColumnHelper();

export const tabelDistribusiHistory = [
    columnHelper.accessor((row) => row.id, {
        id: "id",
        enableSorting: false,
        cell: (info) =>
            h("span", {
                class: "tw-w-10 tw-flex tw-justify-center",
                innerText: info.row.index + 1,
            }),
        header: () =>
            h("span", {
                class: "tw-w-10 tw-flex tw-justify-center",
                innerText: "No",
            }),
    }),
    columnHelper.accessor((row) => row.no_faktur, {
        id: "no_faktur",
        cell: (info) =>
            h("span", {
                class: "table-cell-small",
                innerText: info.getValue(),
            }),
        header: "Nomor Faktur",
    }),
    columnHelper.accessor((row) => row.status_order, {
        id: "status_order",
        cell: (info) =>
            h("span", {
                class: "table-cell-lg",
                innerText: info.getValue()
                === 10 ? "Rescheduled" : "Shipping",
            }),
        header: "Status",
    }),
    columnHelper.accessor((row) => row.tanggal_terkirim, {
        id: "tanggal_terkirim",
        cell: (info) =>
            h("span", {
                class: "table-cell-small",
                innerText: info.getValue(),
            }),
        header: "Tanggal Pengiriman",
    }),
    columnHelper.accessor((row) => row.kode_rute, {
        id: "kode_rute",
        cell: (info) =>
            h("div", {class: "table-cell-small", innerText: info.getValue()}),
        header: "Rute",
    }),
    columnHelper.accessor((row) => row.nama_armada, {
        id: "nama_armada",
        cell: (info) =>
            h("div", {class: "table-cell-small", innerText: info.getValue()}),
        header: "Armada",
    }),
];
