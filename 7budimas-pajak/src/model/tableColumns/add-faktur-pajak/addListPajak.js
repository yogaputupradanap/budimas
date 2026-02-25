import { createColumnHelper } from "@tanstack/vue-table";
import { h, ref } from "vue";
import RouterButton from "@/src/components/ui/RouterButton.vue";
import T from "@/src/components/ui/table/T.vue";
import IndeterminateCheckbox from "@/src/components/ui/IndeterminateCheckbox.vue";


const columnHelper = createColumnHelper();

export const ListFakturPajakColumn = [
    columnHelper.display({
        id: "no",
        header: () => h("div", { class: "tw-pl-3", innerText: "No" }),
        cell: (info) => h(T, { innerText: info.row.index + 1 }),
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
            class: "table-cell-l",
            innerText: info.getValue(),
        }),
    }),

    columnHelper.display({
        id: "action",
        header: ({ table }) =>
            h("div", { class: "tw-px-2 tw-pt-1" }, [
                h(IndeterminateCheckbox, {
                    checked: table.getIsAllRowsSelected(),
                    indeterminate: table.getIsSomeRowsSelected(),
                    onChange: table.getToggleAllRowsSelectedHandler(),
                }),
            ]),
        cell: ({ row }) => {
            return h("div", { class: "tw-px-2 tw-pt-1" }, [
                h(IndeterminateCheckbox, {
                    checked: row.getIsSelected(),
                    disabled: !row.getCanSelect(),
                    onChange: row.getToggleSelectedHandler(),
                }),
            ]);
        },
    }),

];
