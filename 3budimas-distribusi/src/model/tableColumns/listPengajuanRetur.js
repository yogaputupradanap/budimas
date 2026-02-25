import {createColumnHelper} from "@tanstack/vue-table";
import {h} from "vue";

const columnHelper = createColumnHelper();

export const tableListPengajuanRetur = [
    columnHelper.accessor((row) => row.no, {
        id: "no",
        enableSorting: false,
        cell: (info) =>
            h("span", {
                class: "tw-w-10 tw-flex tw-justify-center",
                innerText: info.row.index + 1,
            }),
        header: () =>
            h("span", {
                class: "tw-w-10 tw-flex tw-justify-center",
                innerText: "No",
            }),
    }),

    columnHelper.accessor((row) => row.nama_produk, {
        id: "nama_produk",
        cell: (info) =>
            h("span", {
                class: "table-cell-small",
                innerText: info.getValue(),
            }),
        header: "Nama Barang",
    }),
    columnHelper.accessor((row) => row.kode_sku, {
        id: "kode_sku",
        cell: (info) =>
            h("span", {
                class: "table-cell-small",
                innerText: info.getValue(),
            }),
        header: "Kode SKU",
    }),
    columnHelper.accessor((row) => row.pieces_retur, {
        id: "pieces_retur",
        cell: (info) =>
            h(
                "div",
                {
                    class:
                        "tw-flex tw-flex-col tw-justify-center tw-items-center tw-gap-1"
                },
                [
                    h("span", {innerText: info.getValue() === null ? "0" : info.getValue()}),
                    h("span", {
                        innerText: "pieces",
                        class: "tw-text-blue-400 tw-text-xs"
                    })
                ]
            ),
        header: () =>
            h("span", {
                class: "tw-w-full tw-flex tw-justify-center",
                innerText: "UOM 1 "
            })
    }),
    columnHelper.accessor((row) => row.box_retur, {
        id: "box_retur",
        cell: (info) =>
            h(
                "div",
                {
                    class:
                        "tw-flex tw-flex-col tw-justify-center tw-items-center tw-gap-1"
                },
                [
                    h("span", {innerText: info.getValue() === null ? "0" : info.getValue()}),
                    h("span", {
                        innerText: "box",
                        class: "tw-text-blue-400 tw-text-xs"
                    })
                ]
            ),
        header: () =>
            h("span", {
                class: "tw-w-full tw-flex tw-justify-center",
                innerText: "UOM 2 "
            })
    }),
    columnHelper.accessor((row) => row.karton_retur, {
        id: "karton_retur",
        cell: (info) =>
            h(
                "div",
                {
                    class:
                        "tw-flex tw-flex-col tw-justify-center tw-items-center tw-gap-1"
                },
                [
                    h("span", {innerText: info.getValue() === null ? "0" : info.getValue()}),
                    h("span", {
                        innerText: "karton",
                        class: "tw-text-blue-400 tw-text-xs"
                    })
                ]
            ),
        header: () =>
            h("div", {
                class: "tw-w-full tw-flex tw-justify-center",
                innerText: "UOM 3 "
            }),
    }),
    columnHelper.accessor((row) => row.alasan_retur, {
        id: "alasan_retur",
        cell: (info) =>
            h("span", {
                class: "table-cell-small",
                innerText: info.getValue(),
            }),
        header: "Alasan",
    }),

];
