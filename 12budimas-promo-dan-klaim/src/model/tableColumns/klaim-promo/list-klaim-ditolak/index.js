import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import T from "@/src/components/ui/table/T.vue";
import RouterButton from "@/src/components/ui/RouterButton.vue";

const columnHelper = createColumnHelper();

export const listKlaimDitolakColumn = [
    columnHelper.display({
        id: "no",
        header: h("div", { class: "tw-pl-3", innerText: "No" }),
        cell: (info) => h(T, { innerText: info.row.index + 1 }),
    }),
    columnHelper.accessor((row) => row.nomor_klaim, {
        id: "no_klaim",
        header: h("div", { innerText: "No. Klaim" }),
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
    columnHelper.accessor((row) => row.nominal_klaim, {
        id: "nominal_klaim",
        header: h("div", { innerText: "Nominal Klaim" }),
        cell: (info) =>
            h("div", {
                class: "table-cell-lg",
                innerText: info.getValue(),
            }),
    }),
    columnHelper.accessor((row) => row.status_klaim, {
        id: "status_klaim",
        header: h("div", { innerText: "Status Klaim" }),
        cell: (info) =>
            h("div", {
                class: "table-cell-lg",
                innerText: info.getValue(),
            }),
    }),
    columnHelper.display({
        id: "action",
        header: "Actions",
        cell: ({ column, row, table }) => {
            return h("div", { class: "tw-flex tw-flex-col tw-space-y-2 tw-w-fit" }, [
                h(RouterButton, {
                    class: "tw-px-10 tw-py-2",
                    to: `/klaim-promo/detail/${row.original.id}`,
                }, "Detail"),
                h(RouterButton, {
                    class: "tw-px-10 tw-bg-red-500 tw-py-2",
                    to: `/klaim-promo/list-klaim-ditolak/ajukan-ulang/${row.original.id}`,
                }, "Ajukan Ulang"),
            ])
        }
    }),
];