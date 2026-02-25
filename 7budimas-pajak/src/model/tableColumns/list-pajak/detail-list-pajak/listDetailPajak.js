import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import T from "@/src/components/ui/table/T.vue";

const columnHelper = createColumnHelper();

export const ListDetailPajakColumn = [
    columnHelper.display({
        id: 'no',
        header: () => h('div', { class: 'tw-pl-3', innerText: 'No' }),
        cell: (info) => h(T, { innerText: info.row.index + 1 })
    }),
    columnHelper.accessor((row) => row.nama_barang, {
        id: "nama_barang",
        header: "Nama Barang",
        cell: (info) => h("div", {
            class: "table-cell-medium",
            innerText: info.getValue(),
        }),
    }),
    columnHelper.accessor((row) => row.SKU, {
        id: "SKU",
        header: "SKU",
        cell: (info) => h("div", {
            class: "table-cell-lg",
            innerText: info.getValue(),
        }),
    }),
    columnHelper.accessor((row) => row.satuan, {
        id: "satuan",
        header: "Satuan",
        cell: (info) => h("div", {
            class: "table-cell-medium",
            innerText: info.getValue(),
        }),
    }),
    columnHelper.accessor((row) => row.jumlah, {
        id: "jumlah",
        header: "Jumlah",
        cell: (info) => h("div", {
            class: "table-cell-medium",
            innerText: info.getValue(),
        }),
    }),
    columnHelper.accessor((row) => row.harga_satuan, {
        id: "harga_satuan",
        header: "Harga Satuan",
        cell: (info) => h("div", {
            class: "table-cell-medium",
            innerText: info.getValue(),
        }),
    }),
    columnHelper.accessor((row) => row.subtotal, {
        id: "subtotal",
        header: "Subtotal",
        cell: (info) => h("div", {
            class: "table-cell-medium",
            innerText: info.getValue(),
        }),
    }),
];
