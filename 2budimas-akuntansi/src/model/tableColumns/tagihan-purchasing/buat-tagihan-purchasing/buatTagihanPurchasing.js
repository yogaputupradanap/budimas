import {createColumnHelper} from "@tanstack/vue-table";
import {h} from "vue";
import {basePageTwoTagihanPurchasingColumn} from "../basePageTwoTagihanPurchase";
import IndeterminateCheckbox from "@/src/components/ui/IndeterminateCheckbox.vue";

const columnHelper = createColumnHelper();

export const buatTagihanPurchasingColumn = [
    ...basePageTwoTagihanPurchasingColumn,
    // columnHelper.accessor((row) => row.status_bayar, {
    //   id: "status_bayar",
    //   header: "Status Bayar",
    //   cell: (info) =>
    //     h("div", {
    //       class: "table-cell-medium",
    //       innerText: info.getValue(),
    //     }),
    // }),
    columnHelper.display({
        id: "action",
        header: ({table}) =>
            h("div", {class: "tw-px-2 tw-pt-1"}, [
                h(IndeterminateCheckbox, {
                    checked: table.getIsAllRowsSelected(),
                    indeterminate: table.getIsSomeRowsSelected(),
                    onChange: table.getToggleAllRowsSelectedHandler(),
                }),
            ]),
        cell: ({row}) => {
            return h("div", {class: "tw-px-2 tw-pt-1"}, [
                h(IndeterminateCheckbox, {
                    checked: row.getIsSelected(),
                    disabled: !row.getCanSelect(),
                    onChange: row.getToggleSelectedHandler(),
                }),
            ]);
        },
    }),
];
