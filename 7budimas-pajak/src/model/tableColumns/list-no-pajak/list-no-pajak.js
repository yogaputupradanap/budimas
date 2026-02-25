import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import T from "@/src/components/ui/table/T.vue";

const columnHelper = createColumnHelper();

export const ListNoPajakColumn = [
    columnHelper.accessor((row) => row.row_num, {
        id: "no",
        header: () => h("div", { class: "tw-pl-3", innerText: "No" }),
        cell: (info) => h(T, { innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium" }),
    }),

    columnHelper.accessor((row) => row.no_faktur_pajak, {
        id: "no_faktur_pajak",
        header: () =>
            h("div", {
                class: "tw-pl-1",
                innerText: "No Faktur Pajak",
            }),
        cell: (info) =>
            h("div", {
                class: "table-cell-small",
                innerText: info.getValue(),
            }),
    }),
    columnHelper.accessor((row) => row.no_faktur, {
        id: "no_faktur",
        header: () =>
            h("div", {
                class: "tw-pl-1",
                innerText: "No Faktur",
            }),
        cell: (info) =>
            h("div", {
                class: "table-cell-small",
                innerText: info.getValue() ? info.getValue() : "-",
            }),
    }),

    columnHelper.accessor((row) => row.sudah_digunakan, {
        id: "sudah_digunakan",
        header: () =>
            h("div", {
                class: "table-cell-small",
                innerText: "Status Penggunaan",
            }),
        cell: (info) =>
            h("div", {
                class: "tw-pl-2",
                innerText: info.getValue() ? "Sudah Digunakan" : "Belum digunakan",
            }),
    }),

    columnHelper.accessor((row) => row.tanggal_digunakan, {
        id: "tanggal_digunakan",
        header: () =>
            h("div", {
                class: "table-cell-small",
                innerText: "Tanggal Digunakan",
            }),
        cell: (info) =>
            h("div", {
                class: "tw-pl-6",
                innerText: info.getValue() ? info.getValue() : "-",
            }),
    }),
];
