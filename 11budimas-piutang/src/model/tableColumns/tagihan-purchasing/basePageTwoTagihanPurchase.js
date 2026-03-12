import {createColumnHelper} from "@tanstack/vue-table";
import {h} from "vue";
import T from "@/src/components/ui/table/T.vue";
import {parseCurrency} from "@/src/lib/utils";

const columnHelper = createColumnHelper();

export const basePageTwoTagihanPurchasingColumn = [
    columnHelper.display({
        id: "no",
        header: h("div", {class: "tw-pl-3", innerText: "No"}),
        cell: (info) => h(T, {innerText: info.row.index + 1}),
    }),
    columnHelper.accessor((row) => row.no_transaksi, {
        id: "no_transaksi",
        header: "Faktur",
        cell: (info) =>
            h("div", {
                class: "table-cell-lg",
                innerText: info.getValue(),
            }),
    }),
    columnHelper.accessor((row) => row.kode_order, {
        id: "kode_order",
        header: "Kode Order",
        cell: (info) =>
            h("div", {
                class: "table-cell-medium",
                innerText: info.getValue(),
            }),
    }),
    columnHelper.accessor((row) => row.subtotal, {
        id: "subtotal",
        header: "Total Order",
        cell: (info) =>
            h("div", {
                class: "table-cell-medium",
                innerText: parseCurrency(info.getValue()),
            }),
    }),
    columnHelper.accessor((row) => row.jatuh_tempo, {
        id: "jatuh_tempo",
        header: "Tgl Jatuh Tempo",
        cell: (info) =>
            h("div", {
                class: "table-cell-medium",
                innerText: info.getValue(),
            }),
    })
];
