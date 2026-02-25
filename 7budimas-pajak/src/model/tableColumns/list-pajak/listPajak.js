import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import RouterButton from "@/src/components/ui/RouterButton.vue";
import T from "@/src/components/ui/table/T.vue";


const columnHelper = createColumnHelper();


export const ListPajakColumn = [
    columnHelper.display({
        id: "no",
        header: () => h("div", { class: "tw-pl-3", innerText: "No" }),
        cell: (info) => h(T, { innerText: info.row.index + 1 }),
    }),


    columnHelper.accessor((row) => row.no_faktur_pajak, {
        id: "no_faktur_pajak",
        header: "No Faktur Pajak",
        cell: (info) => h("div", {
            class: "table-cell-medium",
            innerText: info.getValue(),
        }),
    }),

    columnHelper.accessor((row) => row.no_faktur, {
        id: "no_faktur",
        header: "No Faktur",
        cell: (info) => h("div", {
            class: "table-cell-medium",
            innerText: info.getValue(),
        }),
    }),
    columnHelper.accessor((row) => row.principal, {
        id: "principal",
        header: "Principal",
        cell: (info) => h("div", {
            class: "table-cell-lg",
            innerText: info.getValue(),
        }),
    }),
    columnHelper.accessor((row) => row.tanggal_order, {
        id: "tanggal_order",
        header: "Tanggal Order",
        cell: (info) => h("div", {
            class: "table-cell-medium",
            innerText: info.getValue(),
        }),
    }),
    columnHelper.accessor((row) => row.customer, {
        id: "customer",
        header: "Customer",
        cell: (info) => h("div", {
            class: "table-cell-medium",
            innerText: info.getValue(),
        }),
    }),
    columnHelper.accessor((row) => row.npwp, {
        id: "npwp",
        header: "NPWP",
        cell: (info) => h("div", {
            class: "table-cell-medium",
            innerText: info.getValue(),
        }),
    }),
    columnHelper.accessor((row) => row.nilai_faktur, {
        id: "nilai_faktur",
        header: "Nilai Faktur",
        cell: (info) => h("div", {
            class: "table-cell-medium",
            innerText: info.getValue(),
        }),
    }),
    columnHelper.display({
        id: "action",
        header: () => h("div", { class: "tw-pl-2", innerText: "Action" }),
        cell: (info) => {
            const { no_faktur } = info.row.original;
            return h("div", { class: "tw-px-4 tw-text-center " }, [
                h(
                    RouterButton,
                    {
                        to: `/list-pajak/detail-list-pajak/${no_faktur}`,
                        class: "tw-px-4 tw-py-2 tw-bg-blue-500 tw-text-white tw-rounded-md hover:tw-bg-blue-600",
                    },
                    "Detail"
                ),
            ]);
        },
    }),
];
