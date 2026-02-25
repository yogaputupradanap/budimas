import {createColumnHelper} from "@tanstack/vue-table";
import {h} from "vue";
import T from "@/src/components/ui/table/T.vue";
import {formatCurrencyAuto, parseCurrency} from "@/src/lib/utils";

const columnHelper = createColumnHelper();

export const listDetailJurnalColumn = [
    columnHelper.accessor((row) => row.nama_akun, {
        id: "nama_akun",
        header: () => h("div", {class: "tw-pl-3", innerText: "Akun"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),

    columnHelper.accessor((row) => row.debit, {
        id: "debit",
        header: () => h("div", {class: "tw-pl-3", innerText: "Debit"}),
        cell: (info) => h("div", {
            class: "tw-w-44 md:tw-w-auto tw-text-center",
            innerText: info.getValue() ? parseCurrency(info.getValue()) : "-",
        }),
    }),

    columnHelper.accessor((row) => row.kredit, {
        id: "kredit",
        header: () => h("div", {class: "tw-pl-16", innerText: "Kredit"}),
        cell: (info) => h("div", {
            class: "tw-w-44 md:tw-w-auto tw-text-center",
            innerText: info.getValue() ? parseCurrency(info.getValue()) : '-'
        }),
    }),
];

export const listDetailJurnalKeteranganIdFiturMal1 = [
    columnHelper.accessor((row) => row.nama, {
        id: "nama",
        header: () => h("div", {class: "tw-pl-3", innerText: "Nama Produk"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
    columnHelper.accessor((row) => row.qtys.uom_3 || 0, {
        id: "uom_3",
        header: () => h("div", {class: "tw-pl-3", innerText: "UOM 3"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
    columnHelper.accessor((row) => row.qtys.uom_2 || 0, {
        id: "uom_2",
        header: () => h("div", {class: "tw-pl-3", innerText: "UOM 2"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
    columnHelper.accessor((row) => row.qtys.uom_1 || 0, {
        id: "uom_1",
        header: () => h("div", {class: "tw-pl-3", innerText: "UOM 1"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
];

export const listDetailJurnalKeteranganIdFiturMal2 = [
    columnHelper.accessor((row) => row.no_transaksi, {
        id: "no_transaksi",
        header: () => h("div", {class: "tw-pl-3", innerText: "No Faktur"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),

    columnHelper.accessor((row) => row.subtotal, {
        id: "subtotal",
        header: () => h("div", {class: "tw-pl-3", innerText: "Total Order"}),
        cell: (info) => h(T, {innerText: formatCurrencyAuto(info.getValue()), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
];

export const listDetailJurnalKeteranganIdFiturMal3 = [
    columnHelper.accessor((row) => row.nama, {
        id: "nama",
        header: () => h("div", {class: "tw-pl-3", innerText: "Nama Produk"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
    columnHelper.accessor((row) => row.jumlah_picked || 0, {
        id: "qty",
        header: () => h("div", {class: "tw-pl-3", innerText: "Jumlah Picked"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
]

export const listDetailJurnalKeteranganIdFiturMal4 = [
    columnHelper.accessor((row) => row.nama, {
        id: "nama",
        header: () => h("div", {class: "tw-pl-3", innerText: "Nama Produk"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
    columnHelper.accessor((row) => row.jumlah_picked || 0, {
        id: "qty",
        header: () => h("div", {class: "tw-pl-3", innerText: "Jumlah Shipping"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
]

export const listDetailJurnalKeteranganIdFiturMal5 = [
    columnHelper.accessor((row) => row.nama, {
        id: "nama",
        header: () => h("div", {class: "tw-pl-3", innerText: "Nama Produk"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
    columnHelper.accessor((row) => row.karton_delivered || 0, {
        id: "uom_3",
        header: () => h("div", {class: "tw-pl-3", innerText: "UOM 3"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
    columnHelper.accessor((row) => row.box_delivered || 0, {
        id: "uom_2",
        header: () => h("div", {class: "tw-pl-3", innerText: "UOM 2"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
    columnHelper.accessor((row) => row.pieces_delivered || 0, {
        id: "uom_1",
        header: () => h("div", {class: "tw-pl-3", innerText: "UOM 1"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
];

export const listDetailJurnalKeteranganIdFiturMal6 = [
    columnHelper.accessor((row) => row.no_faktur, {
        id: "no_faktur",
        header: () => h("div", {class: "tw-pl-3", innerText: "No Faktur"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
];

export const listDetailJurnalKeteranganIdFiturMal7 = [
    columnHelper.accessor((row) => row.nama, {
        id: "nama",
        header: () => h("div", {class: "tw-pl-3", innerText: "Nama Produk"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
    columnHelper.accessor((row) => row.uom_3 || 0, {
        id: "uom_3",
        header: () => h("div", {class: "tw-pl-3", innerText: "UOM 3"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
    columnHelper.accessor((row) => row.uom_2 || 0, {
        id: "uom_2",
        header: () => h("div", {class: "tw-pl-3", innerText: "UOM 2"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
    columnHelper.accessor((row) => row.uom_1 || 0, {
        id: "uom_1",
        header: () => h("div", {class: "tw-pl-3", innerText: "UOM 1"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
    columnHelper.accessor((row) => row.stok || 0, {
        id: "stok",
        header: () => h("div", {class: "tw-pl-3", innerText: "Stok"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
    columnHelper.accessor((row) => row.stok_sistem || 0, {
        id: "stok_sistem",
        header: () => h("div", {class: "tw-pl-3", innerText: "Stok Sistem"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
    columnHelper.accessor((row) => row.selisih || 0, {
        id: "selisih",
        header: () => h("div", {class: "tw-pl-3", innerText: "Selisih"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
];

export const listDetailJurnalKeteranganIdFiturMal8 = [
    columnHelper.accessor((row) => row.nama, {
        id: "nama",
        header: () => h("div", {class: "tw-pl-3", innerText: "Nama Produk"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
    columnHelper.accessor((row) => row.uom_3 || 0, {
        id: "uom_3",
        header: () => h("div", {class: "tw-pl-3", innerText: "UOM 3"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
    columnHelper.accessor((row) => row.uom_2 || 0, {
        id: "uom_2",
        header: () => h("div", {class: "tw-pl-3", innerText: "UOM 2"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
    columnHelper.accessor((row) => row.uom_1 || 0, {
        id: "uom_1",
        header: () => h("div", {class: "tw-pl-3", innerText: "UOM 1"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
    columnHelper.accessor((row) => row.stok || 0, {
        id: "stok",
        header: () => h("div", {class: "tw-pl-3", innerText: "Stok"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
    columnHelper.accessor((row) => row.stok_sistem || 0, {
        id: "stok_sistem",
        header: () => h("div", {class: "tw-pl-3", innerText: "Stok Sistem"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
    columnHelper.accessor((row) => row.selisih || 0, {
        id: "selisih",
        header: () => h("div", {class: "tw-pl-3", innerText: "Selisih"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
];

export const listDetailJurnalKeteranganIdFiturMal9 = [
    columnHelper.accessor((row) => row.nama, {
        id: "nama",
        header: () => h("div", {class: "tw-pl-3", innerText: "Nama Produk"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
    columnHelper.accessor((row) => row.jumlah_diterima || 0, {
        id: "qty",
        header: () => h("div", {class: "tw-pl-3", innerText: "Jumlah Diterima"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
]

export const listDetailJurnalKeteranganIdFiturMal10 = [
    columnHelper.accessor((row) => row.nama, {
        id: "nama",
        header: () => h("div", {class: "tw-pl-3", innerText: "Nama Produk"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
    columnHelper.accessor((row) => row.jumlah_diterima || 0, {
        id: "qty",
        header: () => h("div", {class: "tw-pl-3", innerText: "Jumlah Diterima"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
]

export const listDetailJurnalKeteranganIdFiturMal12 = [
    columnHelper.accessor((row) => row.no_faktur, {
        id: "no_faktur",
        header: () => h("div", {class: "tw-pl-3", innerText: "No Faktur"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
];

export const listDetailJurnalKeteranganIdFiturMal13 = [
    columnHelper.accessor((row) => row.no_faktur, {
        id: "no_faktur",
        header: () => h("div", {class: "tw-pl-3", innerText: "No Faktur"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
];

export const listDetailJurnalKeteranganIdFiturMal14 = [
    columnHelper.accessor((row) => row.no_faktur, {
        id: "no_faktur",
        header: () => h("div", {class: "tw-pl-3", innerText: "No Faktur"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
];

export const listDetailJurnalKeteranganIdFiturMal16 = [
    columnHelper.accessor((row) => row.nama, {
        id: "nama",
        header: () => h("div", {class: "tw-pl-3", innerText: "Nama Produk"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
    columnHelper.accessor((row) => row.karton_delivered || 0, {
        id: "uom_3",
        header: () => h("div", {class: "tw-pl-3", innerText: "UOM 3"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
    columnHelper.accessor((row) => row.box_delivered || 0, {
        id: "uom_2",
        header: () => h("div", {class: "tw-pl-3", innerText: "UOM 2"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
    columnHelper.accessor((row) => row.pieces_delivered || 0, {
        id: "uom_1",
        header: () => h("div", {class: "tw-pl-3", innerText: "UOM 1"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
];

export const listDetailJurnalKeteranganIdFiturMal17 = [
    columnHelper.accessor((row) => row.nama, {
        id: "nama",
        header: () => h("div", {class: "tw-pl-3", innerText: "Nama Produk"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
    columnHelper.accessor((row) => row.qtys.uom_3 || 0, {
        id: "uom_3",
        header: () => h("div", {class: "tw-pl-3", innerText: "UOM 3"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
    columnHelper.accessor((row) => row.qtys.uom_2 || 0, {
        id: "uom_2",
        header: () => h("div", {class: "tw-pl-3", innerText: "UOM 2"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
    columnHelper.accessor((row) => row.qtys.uom_1 || 0, {
        id: "uom_1",
        header: () => h("div", {class: "tw-pl-3", innerText: "UOM 1"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
];

export const listDetailJurnalKeteranganIdFiturMal18 = [
    columnHelper.accessor((row) => row.nama, {
        id: "nama",
        header: () => h("div", {class: "tw-pl-3", innerText: "Nama Produk"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
    columnHelper.accessor((row) => row.qtys.uom_3 || 0, {
        id: "uom_3",
        header: () => h("div", {class: "tw-pl-3", innerText: "UOM 3"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
    columnHelper.accessor((row) => row.qtys.uom_2 || 0, {
        id: "uom_2",
        header: () => h("div", {class: "tw-pl-3", innerText: "UOM 2"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
    columnHelper.accessor((row) => row.qtys.uom_1 || 0, {
        id: "uom_1",
        header: () => h("div", {class: "tw-pl-3", innerText: "UOM 1"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
];

export const listDetailJurnalKeteranganIdFiturMal19 = [
    columnHelper.accessor((row) => row.nama, {
        id: "nama",
        header: () => h("div", {class: "tw-pl-3", innerText: "Nama Produk"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
    columnHelper.accessor((row) => row.qtys.uom_3 || 0, {
        id: "uom_3",
        header: () => h("div", {class: "tw-pl-3", innerText: "UOM 3"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
    columnHelper.accessor((row) => row.qtys.uom_2 || 0, {
        id: "uom_2",
        header: () => h("div", {class: "tw-pl-3", innerText: "UOM 2"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
    columnHelper.accessor((row) => row.qtys.uom_1 || 0, {
        id: "uom_1",
        header: () => h("div", {class: "tw-pl-3", innerText: "UOM 1"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
];

export const listDetailJurnalKeteranganIdFiturMal20 = [
    columnHelper.accessor((row) => row.nama, {
        id: "nama",
        header: () => h("div", {class: "tw-pl-3", innerText: "Nama Produk"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
    columnHelper.accessor((row) => row.qtys.uom_3 || 0, {
        id: "uom_3",
        header: () => h("div", {class: "tw-pl-3", innerText: "UOM 3"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
    columnHelper.accessor((row) => row.qtys.uom_2 || 0, {
        id: "uom_2",
        header: () => h("div", {class: "tw-pl-3", innerText: "UOM 2"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
    columnHelper.accessor((row) => row.qtys.uom_1 || 0, {
        id: "uom_1",
        header: () => h("div", {class: "tw-pl-3", innerText: "UOM 1"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
];

export const listDetailJurnalKeteranganIdFiturMal21 = [
    columnHelper.accessor((row) => row.no_transaksi, {
        id: "no_transaksi",
        header: () => h("div", {class: "tw-pl-3", innerText: "No Faktur"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),

    columnHelper.accessor((row) => row.subtotal, {
        id: "subtotal",
        header: () => h("div", {class: "tw-pl-3", innerText: "Total Order"}),
        cell: (info) => h(T, {innerText: formatCurrencyAuto(info.getValue()), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
];

export const listDetailJurnalKeteranganIdFiturMal22 = [
    columnHelper.accessor((row) => row.no_transaksi, {
        id: "no_transaksi",
        header: () => h("div", {class: "tw-pl-3", innerText: "No Faktur"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),

    columnHelper.accessor((row) => row.subtotal, {
        id: "subtotal",
        header: () => h("div", {class: "tw-pl-3", innerText: "Total Order"}),
        cell: (info) => h(T, {innerText: formatCurrencyAuto(info.getValue()), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),

    columnHelper.accessor((row) => row.potongan, {
        id: "potongan",
        header: () => h("div", {class: "tw-pl-3", innerText: "Potongan"}),
        cell: (info) => h(T, {innerText: formatCurrencyAuto(info.getValue()), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
];

export const listDetailJurnalKeteranganIdFiturMal23 = [
    columnHelper.accessor((row) => row.no_transaksi, {
        id: "no_transaksi",
        header: () => h("div", {class: "tw-pl-3", innerText: "No Faktur"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),

    columnHelper.accessor((row) => row.subtotal, {
        id: "subtotal",
        header: () => h("div", {class: "tw-pl-3", innerText: "Total Order"}),
        cell: (info) => h(T, {innerText: formatCurrencyAuto(info.getValue()), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),

    columnHelper.accessor((row) => row.potongan, {
        id: "potongan",
        header: () => h("div", {class: "tw-pl-3", innerText: "Potongan"}),
        cell: (info) => h(T, {innerText: formatCurrencyAuto(info.getValue()), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),
];
