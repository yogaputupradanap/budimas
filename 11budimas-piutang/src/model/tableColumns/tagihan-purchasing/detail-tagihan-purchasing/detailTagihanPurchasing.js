import {createColumnHelper} from "@tanstack/vue-table";
import {h} from "vue";
import {basePageTwoTagihanPurchasingColumn} from "../basePageTwoTagihanPurchase";
import Button from "@/src/components/ui/Button.vue";

const columnHelper = createColumnHelper();

export const detailTagihanPurchasingColumn = [
    ...basePageTwoTagihanPurchasingColumn,
    columnHelper.accessor((row) => row.status_bayar, {
        id: "status_bayar",
        header: "Status Bayar",
        cell: (info) =>
            h("div", {
                class: "table-cell-medium",
                innerText: info.getValue(),
            }),
    }),
    // columnHelper.display({
    //     id: "bukti_bayar",
    //     header: "Bukti Bayar",
    //     cell: ({row, column, table}) => {
    //         const openModal = () => {
    //             table.options.meta.updateRow(
    //                 row.original,
    //                 row.index,
    //                 column.id,
    //                 "openRowModal"
    //             );
    //         };
    //         return h(
    //             Button,
    //             {class: "tw-px-7 tw-py-2", trigger: openModal},
    //             "Lihat"
    //         );
    //     },
    // }),
];
