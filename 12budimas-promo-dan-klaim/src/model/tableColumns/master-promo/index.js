import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import T from "@/src/components/ui/table/T.vue";
import Button from "@/src/components/ui/Button.vue";
import RouterButton from "@/src/components/ui/RouterButton.vue";
import { formatNumber } from "@/src/lib/utils";

const columnHelper = createColumnHelper();

export const listMasterPromoColumn = [
    columnHelper.display({
        id: "no",
        header: h("div", { class: "tw-pl-3", innerText: "No" }),
        cell: (info) => h(T, { 
            innerText: info.row.index + 1 
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
    columnHelper.accessor((row) => row.terpakai, {
        id: "terpakai",
        header: h("div", { innerText: "Terpakai" }),
        cell: (info) =>
            h("div", {
                class: "table-cell-lg",
                innerText: formatNumber(info.getValue()),
            }),
    }),
    columnHelper.accessor((row) => row.terklaim, {
        id: "terklaim",
        header: h("div", { innerText: "Terklaim" }),
        cell: (info) =>
            h("div", {
                class: "table-cell-lg",
                innerText: info.getValue(),
            }),
    }),
    columnHelper.accessor((row) => row.status_promo, {
        id: "status_promo",
        header: h("div", { innerText: "Status Promo" }),
        cell: (info) =>
            h("div", {
                class: "table-cell-lg",
                innerText: info.getValue(),
            }),
    }),
    columnHelper.display({
        id: "action",
        header: "Action",
        cell: ({ column, row, table }) => {
            const showModal = () => table.options.meta.updateRow(
                row.original,
                row.index,
                column.kode_promo,
                "openRowModal"
            );

            return h("div", { class: "tw-flex tw-flex-col tw-gap-2 tw-w-min" }, [
                h(Button, {
                    trigger: showModal,
                    class: "tw-px-12 tw-py-2",
                }, "Detail"),
                h(RouterButton, {
                    to: `/master-promo/ajukan-klaim/${row.original.kode_promo}`,
                    class: " tw-py-2 tw-bg-green-500",
                }, "Ajukan Klaim")
            ]);
        },
    }),
];