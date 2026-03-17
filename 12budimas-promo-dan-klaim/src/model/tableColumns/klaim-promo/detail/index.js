import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import T from "@/src/components/ui/table/T.vue";

const columnHelper = createColumnHelper();

export const listDetailKlaimPromoColumn = [
    columnHelper.display({
        id: "no",
        header: h("div", { class: "tw-pl-3", innerText: "No" }),
        cell: (info) => h(T, { innerText: info.row.index + 1 }),
    }),
    columnHelper.accessor((row) => row.no_faktur, {
        id: "no_faktur",
        header: h("div", { innerText: "No Faktur" }),
        cell: (info) =>
            h("div", {
                class: "table-cell-lg",
                innerText: info.getValue(),
            }),
    }),
    columnHelper.accessor((row) => row.customer, {
        id: "customer",
        header: h("div", { innerText: "Customer" }),
        cell: (info) =>
            h("div", {
                class: "table-cell-lg",
                innerText: info.getValue(),
            }),
    }),
    columnHelper.accessor((row) => row.jumlah_klaim, {
        id: "jumlah_klaim",
        header: h("div", { innerText: "Jumlah Klaim" }),
        cell: (info) =>
            h("div", {
                class: "table-cell-lg",
                innerText: info.getValue(),
            }),
    }),
    columnHelper.accessor((row) => row.estimasi_klaim, {
        id: "estimasi_klaim",
        header: h("div", { innerText: "Estimasi Klaim" }),
        cell: (info) =>
            h("div", {
                class: "table-cell-lg",
                innerText: info.getValue(),
            }),
    }),
    columnHelper.accessor((row) => row.status, {
        id: "status",
        header: h("div", { innerText: "Status" }),
        cell: (info) =>
            h("div", {
                class: "table-cell-lg",
                innerText: info.getValue(),
            }),
    })
];