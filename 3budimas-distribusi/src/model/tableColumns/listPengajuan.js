import {createColumnHelper} from "@tanstack/vue-table";
import {h} from "vue";
import RouterButton from "@/src/components/ui/RouterButton.vue";

const columnHelper = createColumnHelper();

export const tableListPengajuan = [
    columnHelper.accessor((row) => row.no, {
        id: "no",
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

    columnHelper.accessor((row) => row.nama_rute, {
        id: "rute",
        cell: (info) =>
            h("span", {
                class: "table-cell-small",
                innerText: info.getValue(),
            }),
        header: "Rute",
    }),
    columnHelper.accessor((row) => row.nama, {
        id: "customer",
        cell: (info) =>
            h("span", {
                class: "table-cell-small",
                innerText: info.getValue(),
            }),
        header: "Customer",
    }),
    columnHelper.accessor((row) => row.tanggal_request, {
        id: "tanggal",
        cell: (info) =>
            h("span", {
                class: "table-cell-medium",
                innerText: info.getValue(),
            }),
        header: "Tanggal",
    }),
    columnHelper.accessor((row) => row.jumlah_barang, {
        id: "jumlah_barang",
        cell: (info) =>
            h("span", {
                class: "table-cell-small",
                innerText: info.getValue(),
            }),
        header: "Jumlah Barang",
    }),
    columnHelper.accessor((row) => row.action, {
        id: "action",
        cell: (info) =>
            h(RouterButton, {
                class: "table-cell-small",
                to: `/retur/list-pengajuan/${info.row.original.id_request}`,
                innerText: "Cetak KPR",
            }),
        header: "Action",
    }),

];
