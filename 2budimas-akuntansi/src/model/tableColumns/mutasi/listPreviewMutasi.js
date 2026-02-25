import {createColumnHelper} from "@tanstack/vue-table";
import {h} from "vue";
import {formatCurrencyAuto} from "@/src/lib/utils";

const columnHelper = createColumnHelper();

export const listPreviewMutasi = [
    columnHelper.accessor((row) => row.tanggal, {
        id: "tanggal",
        header: "Tanggal",
        cell: (info) =>
            h("div", {
                class: "table-cell-lg",
                innerText: info.getValue(),
            }),
    }),
    columnHelper.accessor((row) => row.keterangan, {
        id: "keterangan",
        header: "Keterangan",
        cell: (info) => {
            return h("div", {
                class: "table-cell-medium",
                innerText: info.getValue(),
            });
        },
    }),
    columnHelper.accessor((row) => row.kredit, {
        id: "kredit",
        header: "Kredit",
        cell: (info) => {
            return h("div", {
                class: "tw-text-start",
                innerText: formatCurrencyAuto(info.getValue()),
            });
        },
    }),
    columnHelper.accessor((row) => row.debit, {
        id: "debit",
        header: "Debit",
        cell: (info) => {
            return h("div", {
                class: "tw-text-start ",
                innerText: formatCurrencyAuto(info.getValue()),
            });
        },
    }),
    columnHelper.accessor((row) => row.saldo, {
        id: "saldo",
        header: "Saldo",
        cell: (info) => {
            return h("div", {
                class: "tw-text-start",
                innerText: formatCurrencyAuto(info.getValue()),
            });
        },
    }),
];

export const summaryPreviewMutasi = [
    columnHelper.accessor(row => row.saldo_awal, {
        id: "saldo_awal",
        header: "Saldo Awal",
        cell: (info) => {
            return h("div", {
                class: "table-cell-medium",
                innerText: formatCurrencyAuto(info.getValue()),
            });
        }
    }),
    columnHelper.accessor(row => row.mutasi_debet, {
        id: "mutasi_debet",
        header: "Mutasi Debit",
        cell: (info) => {
            return h("div", {
                class: "table-cell-medium",
                innerText: formatCurrencyAuto(info.getValue()),
            });
        }
    }),
    columnHelper.accessor(row => row.mutasi_kredit, {
        id: "mutasi_kredit",
        header: "Mutasi Kredit",
        cell: (info) => {
            return h("div", {
                class: "table-cell-medium",
                innerText: formatCurrencyAuto(info.getValue()),
            });
        }
    }),
    columnHelper.accessor(row => row.saldo_akhir, {
        id: "saldo_akhir",
        header: "Saldo Akhir",
        cell: (info) => {
            return h("div", {
                class: "table-cell-medium",
                innerText: formatCurrencyAuto(info.getValue()),
            });
        }
    }),
]