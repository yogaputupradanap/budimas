import {createColumnHelper} from "@tanstack/vue-table";
import {h} from "vue";
import T from "@/src/components/ui/table/T.vue";
import {formatCurrencyAuto} from "@/src/lib/utils";
import {BButton} from "bootstrap-vue-next";

const columnHelper = createColumnHelper();

export const listFakturNonTunaiCustomer = (openModalCN) => [
    columnHelper.display({
        id: "select",
        header: ({table}) => {
            // Hitung total baris yang bisa diseleksi (bukan status_order = 10)
            const selectableRows = table
                .getRowModel()
                .rows.filter((row) => row.original.status_order !== 10);

            // Cek apakah semua baris yang bisa diseleksi sudah dipilih
            const allSelectableSelected =
                selectableRows.length > 0 &&
                selectableRows.every((row) => row.getIsSelected());

            return h("input", {
                type: "checkbox",
                checked: allSelectableSelected,
                onChange: (e) => {
                    // Toggle hanya untuk baris yang bisa diseleksi
                    selectableRows.forEach((row) => {
                        row.toggleSelected(e.target.checked);
                    });
                },
                class: "tw-w-4 tw-h-4 tw-rounded",
            });
        },
        cell: ({row}) => {
            return h("input", {
                type: "checkbox",
                checked: row.getIsSelected(),
                onChange: row.getToggleSelectedHandler(),
                class: "tw-w-4 tw-h-4 tw-rounded",
            });
        },
        enableSorting: false,
    }),
    columnHelper.display({
        id: "no",
        header: () => h("div", {class: "tw-pl-3", innerText: "No"}),
        cell: (info) => h(T, {innerText: info.row.index + 1}),
    }),
    columnHelper.accessor((row) => row.tanggal_faktur, {
        id: "tanggal",
        header: "Tanggal",
        cell: (info) =>
            h("div", {
                class: "table-cell-lg",
                innerText: info.getValue(),
            }),
    }),
    columnHelper.accessor((row) => row.nama, {
        id: "nama",
        header: "Principal",
        cell: (info) =>
            h("div", {
                class: "table-cell-lg",
                innerText: info.getValue(),
            }),
    }),
    columnHelper.accessor((row) => row.no_faktur, {
        id: "no_faktur",
        header: "No Faktur",
        cell: (info) => {
            return h("div", {
                class: "table-cell-medium",
                innerText: info.getValue(),
            });
        },
    }),
    columnHelper.accessor((row) => row.tanggal_jatuh_tempo, {
        id: "tanggal_jatuh_tempo",
        header: "Jatuh Tempo",
        cell: (info) => {
            return h("div", {
                class: "table-cell-medium",
                innerText: info.getValue(),
            });
        },
    }),
    columnHelper.accessor((row) => row.total_penjualan - row.setoran - (row.total_retur || 0), {
        id: "total_penjualan",
        header: "Tagihan",
        cell: (info) => {
            return h("div", {
                class: "tw-text-end ",
                innerText: formatCurrencyAuto(info.getValue()),
            });
        },
    }),
    columnHelper.accessor((row) => row.setoran, {
        id: "setoran",
        header: "Setoran",
        cell: (info) => {
            return h("div", {
                class: "tw-text-end ",
                innerText: formatCurrencyAuto(info.getValue()),
            });
        },
    }),
    columnHelper.accessor((row) => row.total_retur, {
        id: "total_retur",
        header: "Nominal Retur",
        cell: (info) => {
            return h("div", {
                class: "tw-text-end ",
                innerText: formatCurrencyAuto(info.getValue()),
            });
        },
    }),
    columnHelper.accessor((row) => null, {
        id: "action",
        header: "Action",
        cell: (info) => {
            return h(BButton,
                {
                    class: "tw-w-32 tw-text-center tw-block tw-mx-auto tw-bg-blue-500 tw-text-white tw-border-blue-500 tw-border tw-rounded hover:tw-bg-blue-600",
                    onClick: () => openModalCN(info.row.original),
                    innerText: "Gunakan CN",
                },
            );
        },
    }),


];

export const listFakturNonTunaiSales = [
    columnHelper.display({
        id: "select",
        header: ({table}) => {
            // Hitung total baris yang bisa diseleksi (bukan status_order = 10)
            const selectableRows = table
                .getRowModel()
                .rows.filter((row) => row.original.status_order !== 10);

            // Cek apakah semua baris yang bisa diseleksi sudah dipilih
            const allSelectableSelected =
                selectableRows.length > 0 &&
                selectableRows.every((row) => row.getIsSelected());

            return h("input", {
                type: "checkbox",
                checked: allSelectableSelected,
                onChange: (e) => {
                    // Toggle hanya untuk baris yang bisa diseleksi
                    selectableRows.forEach((row) => {
                        row.toggleSelected(e.target.checked);
                    });
                },
                class: "tw-w-4 tw-h-4 tw-rounded",
            });
        },
        cell: ({row}) => {
            return h("input", {
                type: "checkbox",
                checked: row.getIsSelected(),
                onChange: row.getToggleSelectedHandler(),
                class: "tw-w-4 tw-h-4 tw-rounded",
            });
        },
        enableSorting: false,
    }),
    columnHelper.display({
        id: "no",
        header: () => h("div", {class: "tw-pl-3", innerText: "No"}),
        cell: (info) => h(T, {innerText: info.row.index + 1}),
    }),
    columnHelper.accessor((row) => row.tanggal_faktur, {
        id: "tanggal",
        header: "Tanggal",
        cell: (info) =>
            h("div", {
                class: "table-cell-lg",
                innerText: info.getValue(),
            }),
    }),
    columnHelper.accessor((row) => row.nama, {
        id: "nama",
        header: "Principal",
        cell: (info) =>
            h("div", {
                class: "table-cell-lg",
                innerText: info.getValue(),
            }),
    }),
    columnHelper.accessor((row) => row.nama_customer, {
        id: "nama_customer",
        header: "Nama Customer",
        cell: (info) =>
            h("div", {
                class: "table-cell-lg",
                innerText: info.getValue(),
            }),
    }),
    columnHelper.accessor((row) => row.no_faktur, {
        id: "no_faktur",
        header: "No Faktur",
        cell: (info) => {
            return h("div", {
                class: "table-cell-medium",
                innerText: info.getValue(),
            });
        },
    }),
    columnHelper.accessor((row) => row.tanggal_jatuh_tempo, {
        id: "tanggal_jatuh_tempo",
        header: "Jatuh Tempo",
        cell: (info) => {
            return h("div", {
                class: "table-cell-medium",
                innerText: info.getValue(),
            });
        },
    }),
    columnHelper.accessor((row) => row.total_penjualan - row.setoran - (row.total_retur || 0), {
        id: "total_penjualan",
        header: "Tagihan",
        cell: (info) => {
            return h("div", {
                class: "tw-text-end ",
                innerText: formatCurrencyAuto(info.getValue()),
            });
        },
    }),
    columnHelper.accessor((row) => row.jumlah_setoran, {
        id: "jumlah_setoran",
        header: "Nominal Dibayar",
        cell: (info) => {
            return h("div", {
                class: "tw-text-end ",
                innerText: formatCurrencyAuto(info.getValue()),
            });
        },
    }),
    columnHelper.accessor((row) => row.setoran, {
        id: "setoran",
        header: "Setoran",
        cell: (info) => {
            return h("div", {
                class: "tw-text-end ",
                innerText: formatCurrencyAuto(info.getValue()),
            });
        },
    }),
    columnHelper.accessor((row) => row.total_retur, {
        id: "total_retur",
        header: "Nominal Retur",
        cell: (info) => {
            return h("div", {
                class: "tw-text-end ",
                innerText: formatCurrencyAuto(info.getValue()),
            });
        },
    }),


];
