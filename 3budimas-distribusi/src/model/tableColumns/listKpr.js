import {createColumnHelper} from "@tanstack/vue-table";
import {h} from "vue";
import Button from "@/src/components/ui/Button.vue";
import {BBadge} from "bootstrap-vue-next";
import RouterButton from "@/src/components/ui/RouterButton.vue";

const columnHelper = createColumnHelper();

export const tableListKpr = [
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

    columnHelper.accessor((row) => row.kode_kpr, {
        id: "kode_kpr",
        cell: (info) =>
            h("span", {
                class: "table-cell-small",
                innerText: info.getValue(),
            }),
        header: "No. KPR",
    }),
    columnHelper.accessor((row) => row.nama_customer, {
        id: "nama_customer",
        cell: (info) =>
            h("span", {
                class: "table-cell-small",
                innerText: info.getValue(),
            }),
        header: "Customer",
    }),
    columnHelper.accessor((row) => row.tanggal_request, {
        id: "tanggal_request",
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
    columnHelper.accessor((row) => row.status_request, {
        id: "status_request",
        cell: (info) =>
            info.getValue() === "1" ?
                h(BBadge, {
                    class: "table-cell-small tw-p-2.5 tw-me-2 w-8 tw-bg-blue-500",
                    variant: "primary",
                    innerText: "Siap Diambil",
                }) :
                h(BBadge, {
                    class: "table-cell-small tw-p-2.5 tw-me-2 w-8 tw-bg-blue-500",
                    variant: "primary",
                    innerText: "CN terbentuk",
                }),
        header: "Status",
    }),
    columnHelper.accessor((row) => row.status_request, {
        id: "action",
        enableSorting: false,

        cell: (info) =>
            info.getValue() === "1" ?
                h(RouterButton, {
                    class: "table-cell-small",
                    to: "/retur/insert-retur/" + info.row.original.id_request,
                    innerText: "Insert Retur",
                })
                :
                h(Button, {
                    class: "table-cell-small",
                    disabled: true,
                    innerText: "Retur Selesai",
                }),
        header: "Action",
    }),

];
