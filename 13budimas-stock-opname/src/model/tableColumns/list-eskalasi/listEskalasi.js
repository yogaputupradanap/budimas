import RouterButton from "@/src/components/ui/RouterButton.vue";
import {formatRupiah} from "@/src/lib/utils";
import {createColumnHelper} from "@tanstack/vue-table";
import { h } from "vue";

const columnHelper = createColumnHelper();
export const listEskalasiColumns = [
    columnHelper.accessor((row) => "no", {
        id: "no",
        header: h("div", {
            class: "tw-w-20 md:tw-w-auto",
            innerText: "No",
        }),
        cell: (info) => h("div", {class: "tw-w-auto", innerText: info.row.index + 1}),
    }),
    columnHelper.accessor((row) => row.kode_so, {
        id: "kode_so",
        header: "Kode SO",
        cell: (info) =>
            h("div", {class: "tw-w-52 md:tw-w-auto", innerText: info.getValue()}),
    }),
    columnHelper.accessor((row) => row.tanggal_so, {
        id: "tanggal_so",
        header: "Tanggal",
        cell: (info) => h("div", {class: "tw-w-20 md:tw-w-auto", innerText: info.getValue()}),
    }),
    columnHelper.accessor((row) => row.nama_principal, {
        id: "nama_principal",
        header: "Principal",
        cell: (info) => h("div", {class: "tw-w-20 md:tw-w-auto", innerText: info.getValue()}),
    }),
    columnHelper.accessor((row) => row.produk_count, {
        id: "not incl1",
        header: "Jml. Produk",
        cell: (info) => h("div", {class: "tw-w-44 md:tw-w-auto", innerText: info.getValue()}),
    }),
    columnHelper.accessor((row) => row.total, {
        id: "total",
        header: "Total Harga",
        cell: (info) => h("div", {class: "tw-w-44 md:tw-w-auto", innerText: formatRupiah(info.getValue())}),
    }),
    columnHelper.accessor((row) => row.ket_so, {
        id: "ket_so",
        header: "Keterangan",
        cell: (info) => h("div", {class: "tw-w-44 md:tw-w-auto", innerText: info.getValue()}),
    }),
    columnHelper.accessor((row) => row.status_so, {
        id: "status_so",
        header: "Status",
        cell: (info) => h("div", {class: "tw-w-44 md:tw-w-auto", innerText: info.getValue()}),
    }),
    columnHelper.accessor((row) => "action", {
        id: "not incl2",
        header: "Action",
        cell: (info) => {
            return h(RouterButton, {
                class: "tw-h-10 tw-mx-1 tw-px-3",
                to: `/list-eskalasi/detail-eskalasi-stock/${info.row.original.id_stock_opname}`,
                innerHTML: 'Detail'
            });
        }
    }),
];