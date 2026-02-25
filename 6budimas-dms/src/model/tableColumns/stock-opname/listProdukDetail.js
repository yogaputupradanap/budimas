import { formatRupiah } from "@/src/lib/utils";
import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";

const columnHelper = createColumnHelper();
export const listProdukDetailColumns = (data) => [
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
        header: "Id Produk",
        cell: (info) =>
            h("div", { class: "tw-w-52 tw-text-base md:tw-w-auto", innerText: info.getValue() }),
    }),
    columnHelper.accessor((row) => row.uom_3, {
        id: "uom3",
        header: "UOM 3",
        cell: (info) =>
            h("div", { class: "tw-w-52 tw-text-base md:tw-w-auto", innerText: info.getValue() }),
    }),
    columnHelper.accessor((row) => row.uom_2, {
        id: "uom2",
        header: "UOM 2",
        cell: (info) =>
            h("div", { class: "tw-w-52 tw-text-base md:tw-w-auto", innerText: info.getValue() }),
    }),
    columnHelper.accessor((row) => row.uom_1, {
        id: "uom1",
        header: "UOM 1",
        cell: (info) =>
            h("div", { class: "tw-w-52 tw-text-base md:tw-w-auto", innerText: info.getValue() }),
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
            h("div", { class: "tw-w-52 tw-text-base md:tw-w-auto", innerText: formatRupiah(info.getValue()) }),
    }),
    columnHelper.accessor((row) => row.ket_produk, {
        id: "keterangan",
        header: "Keterangan",
        cell: (info) =>
            h("div", { class: "tw-w-52 tw-text-base md:tw-w-auto", innerText: info.getValue() }),
    }),
];
