import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import T from "@/src/components/ui/table/T.vue";
import { parseCurrency } from "@/src/lib/utils";

const columnHelper = createColumnHelper();

export const listLogPenggunaanPromoColumn = [
    columnHelper.display({
        id: "no",
        header: h("div", { class: "tw-pl-3", innerText: "No" }),
        cell: (info) => h(T, { innerText: info.row.index + 1 }),
    }),
    columnHelper.accessor((row) => row.no_faktur, {
        id: "no_faktur",
        header: h("div", { innerText: "No. Faktur" }),
        cell: (info) =>
            h("div", {
                class: "table-cell-lg",
                innerText: info.getValue(),
            }),
    }),
    columnHelper.accessor((row) => row.kode_promo, {
        id: "kode_promo",
        header: h("div", { innerText: "Kode Promo" }),
        cell: (info) =>
            h("div", {
                class: "table-cell-lg",
                innerText: info.getValue(),
            }),
    }),
    columnHelper.accessor((row) => row.nama_promo, {
        id: "nama_promo",
        header: h("div", { innerText: "Nama Promo" }),
        cell: (info) =>
            h("div", {
                class: "table-cell-lg",
                innerText: info.getValue(),
            }),
    }),
    columnHelper.accessor((row) => row.principal, {
        id: "principal",
        header: h("div", { innerText: "Principal" }),
        cell: (info) =>
            h("div", {
                class: "table-cell-lg",
                innerText: info.getValue(),
            }),
    }),
    columnHelper.accessor((row) => row.nominal_promo, {
        id: "nominal_promo",
        header: h("div", { innerText: "Nominal Promo" }),
        cell: (info) =>
            h("div", {
                class: "table-cell-lg",
                innerText: parseCurrency(info.getValue()),
            }),
    }),
    columnHelper.accessor((row) => row.status_penggunaan, {
        id: "status_penggunaan",
        header: h("div", { innerText: "Status Penggunaan" }),
        cell: (info) =>
            h("div", {
                class: "table-cell-lg",
                innerText: info.getValue(),
            }),
    }),
];