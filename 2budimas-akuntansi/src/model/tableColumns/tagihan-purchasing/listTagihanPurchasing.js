import {createColumnHelper} from "@tanstack/vue-table";
import {h} from "vue";
import RouterButton from "@/src/components/ui/RouterButton.vue";
import T from "@/src/components/ui/table/T.vue";
import {parseCurrency} from "@/src/lib/utils";
import Button from "@/src/components/ui/Button.vue";

const columnHelper = createColumnHelper();

export const listTagihanPurchasing = [
    columnHelper.display({
        id: "no",
        header: h("div", {class: "tw-pl-3", innerText: "No"}),
        cell: (info) => h(T, {innerText: info.row.original.row_num}),
    }),
    columnHelper.accessor((row) => row.surat_tagihan, {
        id: "surat_tagihan",
        header: "Surat Tagihan",
        cell: (info) =>
            h("div", {
                class: "table-cell-lg",
                innerText: info.getValue(),
            }),
    }),
    columnHelper.accessor((row) => row.nama_principal, {
        id: "nama_principal",
        header: "Principal",
        cell: (info) =>
            h("div", {
                class: "table-cell-medium",
                innerText: info.getValue(),
            }),
    }),
    columnHelper.accessor((row) => row.total_tagihan, {
        id: "total_tagihan",
        header: "Total Tagihan",
        cell: (info) =>
            h("div", {
                class: "table-cell-medium",
                innerText: parseCurrency(info.getValue().toFixed(2)),
            }),
    }),
    columnHelper.accessor((row) => row.jumlah_faktur, {
        id: "jumlah_faktur",
        header: "Jumlah Faktur",
        cell: (info) =>
            h("div", {
                class: "table-cell-medium",
                innerText: info.getValue(),
            }),
    }),
    columnHelper.accessor((row) => row.tanggal_bayar, {
        id: "tanggal_bayar",
        header: "Tanggal Bayar",
        cell: (info) =>
            h("div", {
                class: "table-cell-medium",
                innerText: info.getValue(),
            }),
    }),
    // columnHelper.accessor((row) => row.status_kirim, {
    //     id: "status_kirim",
    //     header: "Status Kirim",
    //     cell: (info) =>
    //         h("div", {
    //             class: "table-cell-medium",
    //             innerText: info.getValue(),
    //         }),
    // }),
    columnHelper.accessor((row) => row.status_bayar, {
        id: "status_bayar",
        header: "Status Bayar",
        cell: (info) =>
            h("div", {
                class: "table-cell-medium",
                innerText: info.getValue(),
            }),
    }),
    // columnHelper.display({
    //     id: "action",
    //     header: "Action",
    //     cell: (info) => {
    //         const {surat_tagihan} = info.row.original;
    //         return h("div", {class: "tw-pr-2"}, [
    //             h(
    //                 RouterButton,
    //                 {
    //                     to: `/tagihan-purchasing/detail-tagihan-purchasing/${surat_tagihan}`,
    //                     class: "tw-px-4 tw-py-2",
    //                 },
    //                 "Detail"
    //             ),
    //         ]);
    //     },
    // }),
    columnHelper.display({
        id: "actions",
        header: () => "actions",
        cell: ({row}) => {
            const {surat_tagihan, status_bayar} = row.original;
            // console.log(status_bayar);
            return h('div', {class: "tw-flex tw-flex-col tw-gap-2"}, [
                h(RouterButton, {
                    to: `/tagihan-purchasing/detail-tagihan-purchasing/${surat_tagihan}`,
                    class: "tw-py-2",
                }, "Detail"),
                status_bayar !== 'lunas' && h(RouterButton, {
                    to: `/tagihan-purchasing/bayar-tagihan-purchasing/${surat_tagihan}`,
                    class: "tw-py-2",
                }, "bayar"),
                status_bayar === 'lunas' && h(Button, {
                    class: "tw-py-2 tw-text-xs tw-font-normal",
                    disabled: true,
                }, "bayar")
            ])
        }
    })
];
