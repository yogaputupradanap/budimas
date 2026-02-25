import {createColumnHelper} from "@tanstack/vue-table";
import {h} from "vue";
import T from "@/src/components/ui/table/T.vue";
import {formatCurrencyAuto} from "@/src/lib/utils";
import {BButton} from "bootstrap-vue-next";

const columnHelper = createColumnHelper();

export const listSetoranNonTunaiColumn = (openModal) => [
    columnHelper.display({
        id: "no",
        header: () => h("div", {class: "tw-pl-3", innerText: "No"}),
        cell: (info) => h(T, {innerText: info.row.original.row_num}),
    }),
    columnHelper.accessor((row) => row.kode_mutasi, {
        id: "kode_mutasi",
        header: "Kode Mutasi",
        cell: (info) =>
            h("div", {
                class: "table-cell-lg",
                innerText: info.getValue(),
            }),
    }),
    columnHelper.accessor((row) => row.tanggal_mutasi, {
        id: "tanggal_mutasi",
        header: "Tanggal",
        cell: (info) =>
            h("div", {
                class: "table-cell-lg",
                innerText: info.getValue(),
            }),
    }),
    columnHelper.accessor((row) => row.nominal_mutasi, {
        id: "nominal_mutasi",
        header: "Nominal",
        cell: (info) => {
            return h("div", {
                class: "tw-text-start ",
                innerText: formatCurrencyAuto(info.getValue()),
            });
        },
    }),
    columnHelper.accessor((row) => row.keterangan, {
        id: "keterangan",
        header: "Keterangan",
        cell: (info) => {
            return h("div", {
                class: "table-cell-medium",
                innerText: info.getValue() || "-",
            });
        },
    }),

    columnHelper.display({
        id: "actions",
        header: "Action",
        cell: (info) => {
            return h(BButton, {
                onClick: () => openModal(info.row.original),
                class: "tw-text-white tw-py-2 tw-bg-blue-500 tw-rounded",
                innerText: "Detail",
            });
        },
    }),
];
