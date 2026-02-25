import { formatRupiah } from "@/src/lib/utils";
import { createColumnHelper } from "@tanstack/vue-table";
import { BFormInput } from "bootstrap-vue-next";
import { h, ref, watch } from "vue";

const columnHelper = createColumnHelper();
export const listPreviewFile = [
    columnHelper.accessor((row) => row.invoice_no, {
        id: "nota order",
        header: "Nota Order",
        cell: (info) => h("div", { class: "tw-text-base", innerText: info.getValue() }),
    }),
    columnHelper.accessor((row) => row.customer_code, {
        id: "Kode Customer",
        header: "Kode Customer",
        cell: (info) =>
            h("div", { class: "tw-w-52 tw-text-base md:tw-w-auto", innerText: info.row.original.customer_code }),
    }),
    columnHelper.accessor((row) => row.customer_name, {
        id: "Nama Customer",
        header: "Nama Customer",
        cell: (info) =>
            h("div", { class: "tw-w-52 tw-text-base md:tw-w-auto", innerText: info.getValue() }),
    }),
    columnHelper.accessor((row) => row.route_name, {
        id: "Nama Sales",
        header: "Nama Sales",
        cell: (info) =>
            h("div", { class: "tw-w-52 tw-text-base md:tw-w-auto", innerText: info.getValue().split("-")[1] }),
    }),
    columnHelper.accessor((row) => row.total_net_amount, {
        id: "Total Bayar",
        header: "Total Bayar",
        cell: (info) =>
            h("div", { class: "tw-w-52 tw-text-base md:tw-w-auto", innerText: formatRupiah(Number(info.getValue())) }),
    }),
    columnHelper.accessor((row) => row.order_date, {
        id: "Kode Customer",
        header: "Tanggal Order",
        cell: (info) =>
            h("div", { class: "tw-w-52 tw-text-base md:tw-w-auto", innerText: info.getValue().replace(/\//g, "-") }),
    }),
];
