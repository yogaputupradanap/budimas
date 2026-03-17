import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import T from "@/src/components/ui/table/T.vue";
import Button from "@/src/components/ui/Button.vue";
import RouterButton from "@/src/components/ui/RouterButton.vue";
import { parseCurrency } from "@/src/lib/utils";

const columnHelper = createColumnHelper();

export const kasbonKlaimColumn = [
    columnHelper.display({
        id: "no",
        header: h("div", { class: "tw-pl-3", innerText: "No" }),
        cell: (info) => h(T, { innerText: info.row.index + 1 }),
    }),
    columnHelper.accessor((row) => row.kode_kasbon_klaim, {
        id: "kode_kasbon",
        header: h("div", { innerText: "Kode Kasbon" }),
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
    columnHelper.accessor((row) => row.tanggal_pengajuan, {
        id: "tanggal_pengajuan",
        header: h("div", { innerText: "Tanggal" }),
        cell: (info) =>
            h("div", {
                class: "table-cell-lg",
                innerText: info.getValue(),
            }),
    }),
    columnHelper.accessor((row) => row.nominal_kasbon_diajukan, {
        id: "nominal_kasbon_diajukan",
        header: h("div", { innerText: "Nominal Kasbon Klaim" }),
        cell: (info) =>
            h("div", {
                class: "table-cell-lg",
                innerText: parseCurrency(info.getValue()),
            }),
    }),
    columnHelper.accessor((row) => row.nominal_kasbon_disetujui, {
        id: "nominal_kasbon_disetujui",
        header: h("div", { innerText: "Nominal Klaim Dijamin" }),
        cell: (info) =>
            h("div", {
                class: "table-cell-lg",
                innerText: parseCurrency(info.getValue()),
            }),
    }),
    columnHelper.accessor((row) => row.status_kasbon, {
        id: "status_kasbon",
        header: h("div", { innerText: "Status" }),
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
             return h("div", { class: "tw-flex tw-flex-col tw-gap-2 tw-w-min" }, [
                    h(RouterButton, {
                        to: `/kasbon-klaim/detail/${row.original.id}`,
                        class: " tw-py-2 tw-bg-blue-500",
                    }, "Detail")
                ]);
            },
        }
    ),
];
