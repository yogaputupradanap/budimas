import {createColumnHelper} from "@tanstack/vue-table";
import {h} from "vue";
import RouterButton from "@/src/components/ui/RouterButton.vue";
import T from "@/src/components/ui/table/T.vue";
import {parseCurrency} from "@/src/lib/utils";

const columnHelper = createColumnHelper();

export const listSetoranTunaiPiutangColumn = [
    columnHelper.display({
        id: "no",
        header: () => h("div", {class: "tw-pl-3", innerText: "No"}),
        cell: (info) => h(T, {innerText: info.row.index + 1}),
    }),
    columnHelper.accessor((row) => row.draft_tanggal_input, {
        id: "draft_tanggal_input",
        header: "Tanggal",
        cell: (info) =>
            h("div", {
                class: "table-cell-lg",
                innerText: info.getValue(),
            }),
    }),
    columnHelper.accessor((row) => row.nama_pj, {
        id: "nama_pj",
        header: "Nama PJ",
        cell: (info) => {
            return h("div", {
                class: "table-cell-medium",
                innerText: info.getValue(),
            });
        },
    }),
    columnHelper.accessor((row) => row.total_setor_diterima_kasir, {
        id: "total_setor_diterima_kasir",
        header: "Setoran Piutang",
        cell: (info) => {
            return h("div", {
                class: "tw-text-start",
                innerText: parseCurrency(info.getValue()),
            });
        },
    }),
    columnHelper.accessor((row) => row.status_setoran, {
        id: "status_setoran",
        header: "Status Setoran",
        cell: (info) => {
            const value = info.getValue();
            const statusColor = {
                sales: "tw-bg-red-500",
                kasir: "tw-bg-yellow-600",
                audit: "tw-bg-green-600",
                "admin gudang": "tw-bg-blue-600",
            };
            const classColor = statusColor['kasir'];

            return h(
                "div",
                {
                    class: "table-cell-medium",
                },
                [
                    h("span", {
                        class: `tw-px-7 tw-py-1 tw-text-white tw-font-medium tw-rounded-md ${classColor}`,
                        innerText: "Kasir",
                    }),
                ]
            );
        },
    }),
    columnHelper.display({
        id: "actions",
        header: "Action",
        cell: (info) => {
            return h(RouterButton, {
                to: `/setoran-tunai/${info.row.original.nama_pj}/${info.row.original.draft_tanggal_input}`,
                class: "tw-text-white  tw-py-2",
                innerText: "Konfirmasi Piutang",
            });
        },
    }),
];

export const listSetoranTunaiColumn = [
    columnHelper.display({
        id: "no",
        header: () => h("div", {class: "tw-pl-3", innerText: "No"}),
        cell: (info) => h(T, {innerText: info.row.original.row_num}),
    }),
    columnHelper.accessor((row) => row.draft_tanggal_input, {
        id: "draft_tanggal_input",
        header: "Tanggal",
        cell: (info) =>
            h("div", {
                class: "table-cell-lg",
                innerText: info.getValue(),
            }),
    }),
    columnHelper.accessor((row) => row.nama_pj, {
        id: "nama_pj",
        header: "Nama PJ",
        cell: (info) => {
            return h("div", {
                class: "table-cell-medium",
                innerText: info.getValue(),
            });
        },
    }),
    columnHelper.accessor((row) => row.setoran_piutang, {
        id: "setoran_piutang",
        header: "Setoran Piutang",
        cell: (info) => {
            return h("div", {
                class: "tw-text-start ",
                innerText: parseCurrency(info.getValue()),
            });
        },
    }),
    columnHelper.accessor((row) => row.status_setoran, {
        id: "status_setoran",
        header: "Status Setoran",
        cell: (info) => {
            const value = info.getValue();
            const statusColor = {
                sales: "tw-bg-red-500",
                kasir: "tw-bg-yellow-600",
                audit: "tw-bg-green-600",
                "admin gudang": "tw-bg-blue-600",
            };
            const classColor = statusColor[value];

            return h(
                "div",
                {
                    class: "table-cell-medium",
                },
                [
                    h("span", {
                        class: `tw-px-7 tw-py-1 tw-text-white tw-font-medium tw-rounded-md ${classColor}`,
                        innerText: value,
                    }),
                ]
            );
        },
    }),
    columnHelper.display({
    id: "actions",
    header: "Action",
    cell: (info) => {
        const {
            id_sales,
            draft_tanggal_input: tanggal,
            status_setoran,
            status, // Berpotensi undefined/null
            nama_pj,
            pj_setoran,
        } = info.row.original;

        const nama_kasir = info.row.original.nama_kasir ?? "";
        const nama_auditor = info.row.original.nama_auditor ?? "";

        // FIX: Pastikan status adalah array sebelum akses index [0]
        // Jika status undefined, gunakan string kosong agar URL tidak rusak
        const safeStatus = (Array.isArray(status) && status.length > 0) ? status[0] : (status ?? "");

        const buttonText = status_setoran === "audit" ? "Detail Setoran" : "Konf. Setoran";

        return h(RouterButton, {
            // Gunakan safeStatus di sini
            to: `/setoran-tunai/list-faktur?id_sales=${id_sales}&nama_pj=${nama_pj}&pj_setoran=${pj_setoran}&tanggal=${tanggal}&status=${safeStatus}&nama_kasir=${nama_kasir}&nama_auditor=${nama_auditor}`,
            class: "tw-text-white tw-w-32 tw-py-2",
            innerText: buttonText,
        });
    },
}),
];


