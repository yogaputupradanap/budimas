import {h} from "vue";
import RouterButton from "@/src/components/ui/RouterButton.vue";
import T from "@/src/components/ui/table/T.vue";
import {parseCurrency} from "@/src/lib/utils";
import {createColumnHelper} from "@tanstack/vue-table";

const columnHelper = createColumnHelper();

export const listJurnalColumn = [
    columnHelper.accessor((row) => row.row_num, {
        id: "no",
        header: () => h("div", {class: "tw-pl-3", innerText: "No"}),
        cell: (info) => h(T, {innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium"}),
    }),

    columnHelper.accessor((row) => row.tanggal, {
        id: "tanggal",
        header: () => "Tanggal",
        cell: (info) => h("div", {class: "table-cell-medium", innerText: info.getValue()}),
    }),

    columnHelper.accessor((row) => row.nama_perusahaan, {
        id: "nama_perusahaan",
        header: () => "Perusahaan",
        cell: (info) => h("div", {class: "table-cell-lg", innerText: info.getValue()}),
    }),

    columnHelper.accessor((row) => row.nama_cabang, {
        id: "nama_cabang",
        header: () => "Cabang",
        cell: (info) => h("div", {class: "table-cell-lg", innerText: info.getValue()}),
    }),

    columnHelper.accessor((row) => row.id_jurnal, {
        id: "id_jurnal",
        header: () => "ID Jurnal",
        cell: (info) => h("div", {class: "table-cell-medium", innerText: info.getValue()}),
    }),
    columnHelper.accessor((row) => row.jenis_transaksi, {
        id: "jenis_transaksi",
        header: () => h("div", {class: "tw-pl-2", innerText: "Jenis transaksi"}),
        cell: (info) => h("div", {class: "table-cell-medium", innerText: info.getValue()}),

    }),

    columnHelper.display({
        id: "nama_akun",
        header: () => h("div", {class: "tw-pl-2", innerText: "Nama Akun"}),
        cell: (info) => {
            const detailJurnal = info.row.original.info_jurnal || [];

            return h(
                "div",
                {class: "tw-cell-small tw-flex tw-flex-col"},
                detailJurnal.map((item, index) =>
                    h("div", {
                        class: [
                            "tw-w-full tw-pl-2 tw-py-2",
                            index !== detailJurnal.length - 1 ? "tw-border-b tw-border-gray-300" : "",
                        ].join(" "),
                        innerText: item.nama_akun || "-",
                    })
                )
            );
        },
    }),

    columnHelper.display({
        id: "debit",
        header: () => h("div", {class: "tw-pl-2", innerText: "Debit"}),
        cell: (info) => {
            const detailJurnal = info.row.original.info_jurnal || [];

            return h(
                "div",
                {class: "tw-cell-small tw-flex tw-flex-col tw-text-green-600 tw-font-semibold"},
                detailJurnal.map((item, index) =>
                    h("div", {
                        class: [
                            "tw-w-full tw-pl-2 tw-py-2",
                            index !== detailJurnal.length - 1 ? "tw-border-b tw-border-gray-300" : "",
                        ].join(" "),
                        innerText: item.debit ? parseCurrency(item.debit) : "-",
                    })
                )
            );
        },
    }),

    columnHelper.display({
        id: "kredit",
        header: () => h("div", {class: "tw-pl-2", innerText: "Kredit"}),
        cell: (info) => {
            const detailJurnal = info.row.original.info_jurnal || [];

            return h(
                "div",
                {class: "tw-cell-small tw-flex tw-flex-col tw-text-red-600 tw-font-semibold"},
                detailJurnal.map((item, index) =>
                    h("div", {
                        class: [
                            "tw-w-full tw-pl-2 tw-py-2",
                            index !== detailJurnal.length - 1 ? "tw-border-b tw-border-gray-300" : "",
                        ].join(" "),
                        innerText: item.kredit ? parseCurrency(item.kredit) : "-",
                    })
                )
            );
        },
    }),

    columnHelper.display({
        id: "action",
        header: () => h("div", { class: "tw-pl-2", innerText: "Action" }),
        cell: (info) => {
            const { id_jurnal } = info.row.original;
            return h("div", { class: "tw-px-4 tw-text-center" }, [
                h(
                    RouterButton,
                    {
                        to: `/jurnal/detail-jurnal/${id_jurnal}`,
                        class: "tw-px-4 tw-py-2 tw-bg-blue-500 tw-text-white tw-rounded-md hover:tw-bg-blue-600",
                    },
                    // PERBAIKAN DI SINI: Bungkus teks "Detail" dalam fungsi slot
                    {
                        default: () => "Detail"
                    }
                ),
            ]);
        },
    }),
];
