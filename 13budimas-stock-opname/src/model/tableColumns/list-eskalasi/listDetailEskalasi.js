import { formatRupiah } from "@/src/lib/utils";
import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";

const columnHelper = createColumnHelper();
export const listDetailEskalasiColumns = (data) => [
    columnHelper.accessor((row) => "no", {
        id: "no",
        header: h("div", {
            class: "tw-pl-4 tw-w-20 md:tw-w-auto",
            innerText: "No",
        }),
        cell: (info) => h("div", { class: "tw-text-base", innerText: info.row.index + 1 }),
    }),
    columnHelper.accessor((row) => row.sku, {
        id: "sku",
        header: "SKU",
        cell: (info) =>
            h("div", { class: "tw-w-52 tw-text-base md:tw-w-auto", innerText: info.getValue() }),
    }),
    columnHelper.accessor((row) => row.nama_produk, {
        id: "nama produk",
        header: "Nama Produk",
        cell: (info) =>
            h("div", { class: "tw-w-52 tw-text-base md:tw-w-auto", innerText: info.getValue() }),
    }),
    columnHelper.accessor((row) => row.uom_3, {
        id: "uom3",
        header: "UOM 3",
        cell: (info) => {
            return h("input", {
                type: "number",
                class: "tw-border tw-border-gray-300 tw-rounded tw-px-2 tw-py-1 tw-text-center tw-w-10",
                value: info.getValue(),
                onBlur: (e) => {
                    info.row.original.uom_3 = Number(e.target.value) || 0;
                    data(info.row.original, 3);
                }
            });
        },
    }),
    columnHelper.accessor((row) => row.uom_2, {
        id: "uom2",
        header: "UOM 2",
        cell: (info) => {
            return h("input", {
                type: "number",
                class: "tw-border tw-border-gray-300 tw-rounded tw-px-2 tw-py-1 tw-text-center tw-w-10",
                value: info.getValue(),
                onBlur: (e) => {
                    info.row.original.uom_2 = Number(e.target.value) || 0;
                    data(info.row.original, 2);
                }
            });
        },
    }),
    columnHelper.accessor((row) => row.uom_1, {
        id: "uom1",
        header: "UOM 1",
        cell: (info) => {
            return h("input", {
                type: "number",
                class: "tw-border tw-border-gray-300 tw-rounded tw-px-2 tw-py-1 tw-text-center tw-w-10",
                value: info.getValue(),
                onBlur: (e) => {
                    info.row.original.uom_1 = Number(e.target.value) || 0;
                    data(info.row.original, 1);
                }
            });
        },
    }),
    columnHelper.accessor((row) => row.stok, {
        id: "stok",
        header: "Stock",
        cell: (info) =>
            h("div", { class: "tw-w-52 tw-text-base md:tw-w-auto", innerText: info.getValue() }),
    }),
    columnHelper.accessor((row) => row.bad_stock, {
        id: "bad qty",
        header: "Bad Stock",
        cell: (info) =>
            h("div", { class: "tw-w-52 tw-text-base md:tw-w-auto", innerText: info.getValue() }),
    }),
    columnHelper.accessor((row) => "row.bad_stock", {
        id: "Selisih",
        header: "Selisih",
        cell: (info) =>
            h("div", { class: "tw-w-52 tw-text-base md:tw-w-auto", innerText: info.row.original.stok - info.row.original.stok_sistem }),
    }),
    columnHelper.accessor((row) => row.stok_sistem, {
        id: "stok system",
        header: "Stock System",
        cell: (info) =>
            h("div", { class: "tw-w-52 tw-text-base md:tw-w-auto", innerText: info.getValue() }),
    }),
    columnHelper.accessor((row) => row.harga, {
        id: "harga",
        header: "Harga",
        cell: (info) =>
            h("div", { class: "tw-w-52 tw-text-base md:tw-w-auto", innerText: formatRupiah(info.getValue()) }),
    }),
    columnHelper.accessor((row) => row.subtotal, {
        id: "subtotal",
        header: "Subtotal",
        cell: (info) =>
            h("div", { class: "tw-w-28 tw-text-base md:tw-w-auto", innerText: formatRupiah(info.getValue()) }),
    }),
    columnHelper.accessor((row) => row.subtotal_selisih, {
        id: "subtotal selisih",
        header: "Subtotal Selisih",
        cell: (info) =>
            h("div", { class: "tw-w-32 tw-text-base md:tw-w-auto", innerText: formatRupiah(info.getValue()) }),
    }),
    columnHelper.accessor((row) => row.ket_produk, {
        id: "keterangan",
        header: "Keterangan",
        cell: (info) =>
            h("div", { class: "tw-w-52 tw-text-base md:tw-w-auto", innerText: info.getValue() }),
    }),
];
