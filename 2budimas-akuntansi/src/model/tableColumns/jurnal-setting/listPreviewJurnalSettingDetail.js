import {createColumnHelper} from "@tanstack/vue-table";
import {h} from "vue";
import Button from "@/src/components/ui/Button.vue";

const columnHelper = createColumnHelper();

export const listPreviewJurnalSettingDetail = (handleDelete) => [
    columnHelper.accessor((row) => row.urutan, {
        id: "no",
        header: "No",
        cell: (info) =>
            h("div", {
                class: "table-cell-small",
                innerText: info.row.index + 1,
            }),
    }),
    columnHelper.accessor((row) => row.nama_modul, {
        id: "id_modul",
        header: "Modul",
        cell: (info) => {
            return h("div", {
                    class: "table-cell-medium",
                    innerText: info.getValue(),
                },
            );
        },
    }),
    columnHelper.accessor((row) => row.nama_akun, {
        id: "id_coa",
        header: "Akun COA",
        cell: (info) => {
            return h("div", {
                    class: "table-cell-medium",
                    innerText: info.getValue(),
                }
            );
        },
    }),
    columnHelper.accessor((row) => row.type, {
        id: "type",
        header: "Tipe Transaksi",
        cell: (info) => {
            return h("div", {
                    class: "table-cell-medium",
                    innerText: info.getValue() === 1 ? "Debit" : "Kredit",
                }
            );
        },
    }),
    columnHelper.accessor((row) => row.nama_kolom_view, {
        id: "id_source_data",
        header: "Source Data",
        cell: (info) => {
            return h("div", {
                    class: "table-cell-medium",
                    innerText: info.getValue(),
                }
            );
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
                        class: "tw-bg-red-500 tw-text-white tw-px-3 tw-py-1 tw-rounded",
                        icon: "mdi mdi-trash-can-outline",
                        trigger: () => handleDelete(info.row.index, info.row.original),
                    }),
                ]
            )
        },
    }),

];

export const listPreviewJurnalSettingEditDetail = (handleEdit) => [
    columnHelper.accessor((row) => row.urutan, {
        id: "no",
        header: "No",
        cell: (info) =>
            h("div", {
                class: "table-cell-small",
                innerText: info.row.index + 1,
            }),
    }),
    columnHelper.accessor((row) => row.nama_modul, {
        id: "id_modul",
        header: "Modul",
        cell: (info) => {
            return h("div", {
                    class: "table-cell-medium",
                    innerText: info.getValue(),
                },
            );
        },
    }),
    columnHelper.accessor((row) => row.nama_akun, {
        id: "id_coa",
        header: "Akun COA",
        cell: (info) => {
            return h("div", {
                    class: "table-cell-medium",
                    innerText: info.getValue(),
                }
            );
        },
    }),
    columnHelper.accessor((row) => row.type, {
        id: "type",
        header: "Tipe Transaksi",
        cell: (info) => {
            return h("div", {
                    class: "table-cell-medium",
                    innerText: info.getValue() === 1 ? "Debit" : "Kredit",
                }
            );
        },
    }),
    columnHelper.accessor((row) => row.nama_kolom_view, {
        id: "id_source_data",
        header: "Source Data",
        cell: (info) => {
            return h("div", {
                    class: "table-cell-medium",
                    innerText: info.getValue(),
                }
            );
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
                        class: "tw-bg-blue-500 tw-text-white tw-px-3 tw-py-1 tw-rounded",
                        icon: "mdi  mdi-pencil",
                        trigger: () => handleEdit(info.row.index, info.row.original),
                    }),
                ]
            )
        },
    }),

];
