import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import T from "@/src/components/ui/table/T.vue";
import RouterButton from "@/src/components/ui/RouterButton.vue";
import Button from "@/src/components/ui/Button.vue";
import { parseCurrency } from "@/src/lib/utils";

const columnHelper = createColumnHelper();

export const listKlaimPromoColumn = [
    columnHelper.display({
        id: "no",
        header: h("div", { class: "tw-pl-3", innerText: "No" }),
        cell: (info) => h(T, { innerText: info.row.index + 1 }),
    }),
    columnHelper.accessor((row) => row.nomor_klaim, {
        id: "nomor_klaim",
        header: h("div", { innerText: "No Klaim" }),
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
                innerText: parseCurrency(info.getValue()),
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
            const showModal = () => table.options.meta.updateRow(
                row.original,
                row.index,
                column.id,
                "openRowModal"
            );
            return h("div", { class: "tw-flex tw-gap-2" }, [
                // Edit button
                h(Button, {
                    class: "tw-px-3 mdi mdi-pencil",
                    disabled: row.original.status === 4,
                    trigger: showModal,
                }, ""),
                // Detail button
                h(RouterButton, {
                    class: "tw-px-3 mdi mdi-information-outline tw-bg-gray-500 hover:tw-bg-gray-600",
                    to: `/klaim-promo/detail/${row.original.id}`,
                }, ""),
            ])
        }
    }),
];