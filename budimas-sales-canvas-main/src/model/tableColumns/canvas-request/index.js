import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import T from "@/src/components/ui/table/T.vue";
import RouterButton from "@/src/components/ui/RouterButton.vue";
import { parseCurrency } from "@/src/lib/utils";
import { parseCanvasStatus } from "@/src/lib/utils";

const columnHelper = createColumnHelper();

export const listCanvasRequestColumn = [
    columnHelper.display({
        id: "no",
        header: h("div", { class: "tw-pl-3", innerText: "No" }),
        cell: (info) => h(T, { innerText: info.row.index + 1 }),
    }),
    columnHelper.accessor((row) => row.tanggal_request, {
        id: "tanggal_request",
        header: h("div", { innerText: "Tanggal" }),
        cell: (info) =>
            h("div", {
                class: "table-cell-lg",
                innerText: info.getValue(),
            }),
    }),
    columnHelper.accessor((row) => row.total_request, {
        id: "total_request",
        header: h("div", { innerText: "Total Request" }),
        cell: (info) =>
            h("div", {
                class: "table-cell-lg",
                innerText: parseCurrency(info.getValue()),
            }),
    }),
    columnHelper.accessor((row) => row.status, {
        id: "status",
        header: h("div", { innerText: "Status" }),
        cell: (info) =>
            h("div", {
                class: "table-cell-lg",
                innerText: parseCanvasStatus(info.getValue()),
            }),
    }),
    columnHelper.display({
        id: "action",
        header: "Action",
        cell: ({ column, row, table }) => {
             return h("div", { class: "tw-flex tw-flex-col tw-gap-2 tw-w-min" }, [
                    h(RouterButton, {
                        to: `/canvas-request/${row.original.id}?tanggal_request=${row.original.tanggal_request}`,
                        class: "mdi mdi-information-outline tw-gap-2 tw-py-2 tw-px-5 tw-tracking-wide tw-bg-blue-500",
                    }, "Detail")
                ]);
            },
        }
    ),
];
