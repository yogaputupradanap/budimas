import {createColumnHelper} from "@tanstack/vue-table";
import {h} from "vue";
import Button from "@/src/components/ui/Button.vue";

const columnHelper = createColumnHelper();

export const listPreviewCoa = (shomModal, handledelete, showDetailCoa) => [
    columnHelper.accessor((row) => row.row_num, {
        id: "no",
        header: "No",
        cell: (info) =>
            h("div", {
                class: "table-cell-lg",
                innerText: info.getValue(),
            }),
    }),
    columnHelper.accessor((row) => row.nama_perusahaan, {
        id: "nama_perusahaan",
        header: "Nama Perusahaan",
        cell: (info) => {
            return h("div", {
                class: "table-cell-medium",
                innerText: info.getValue(),
            });
        },
    }),
    columnHelper.accessor((row) => row.nomor_akun, {
        id: "nomor_akun",
        header: "Nomor Akun",
        cell: (info) => {
            return h("div", {
                class: "table-cell-medium",
                innerText: info.getValue(),
            });
        },
    }), columnHelper.accessor((row) => row.nama_akun, {
        id: "nama_akun",
        header: "Nama Akun",
        cell: (info) => {
            return h("div", {
                class: "table-cell-medium",
                innerText: info.getValue(),
            });
        },
    }),
    columnHelper.accessor((row) => row.nama_kategori, {
        id: "nama_kategori",
        header: "Kategory",
        cell: (info) => {
            return h("div", {
                class: " table-cell-medium",
                innerText: info.getValue(),
            });
        },
    }),
    columnHelper.accessor((row) => row.action, {
        id: "action",
        header: "Action",
        cell: (info) => {
            return h(
                "div",
                {class: "table-cell-medium tw-flex tw-gap-2"}, // flex biar rapi
                [
                    h(Button, {
                        class: "tw-bg-green-500 tw-text-white tw-px-3 tw-py-1 tw-rounded",
                        icon: "mdi mdi-eye",
                        trigger: () => showDetailCoa(info.row.original),
                    }),
                    h(Button, {
                        class: "tw-bg-blue-500 tw-text-white tw-px-3 tw-py-1 tw-rounded",
                        icon: "mdi mdi-pencil",
                        trigger: () => shomModal(info.row.original),
                    }),
                    h(Button, {
                        class: "tw-bg-red-500 tw-text-white tw-px-3 tw-py-1 tw-rounded",
                        icon: "mdi mdi-trash-can-outline",
                        trigger: () => handledelete(info.row.original),
                    }),
                ]
            )
        },
    }),

];
