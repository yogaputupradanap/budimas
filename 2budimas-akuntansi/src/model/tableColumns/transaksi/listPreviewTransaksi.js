import {createColumnHelper} from "@tanstack/vue-table";
import {h} from "vue";
import {formatCurrencyAuto} from "@/src/lib/utils";
import Button from "@/src/components/ui/Button.vue";

const columnHelper = createColumnHelper();

export const listPreviewTransaksi = (shomModal, handledelete) => [
    // Gunakan string langsung sebagai accessor untuk keandalan
    columnHelper.accessor("tanggal_transaksi", {
        header: "Tanggal Transaksi",
        cell: (info) => h("div", { class: "table-cell-lg" }, info.getValue()),
    }),
    columnHelper.accessor("kode_transaksi", {
        header: "Kode Transaksi",
        cell: (info) => h("div", { class: "table-cell-medium" }, info.getValue()),
    }),
    columnHelper.accessor("nomor_rekening", {
        header: "Rekening Perusahaan",
        cell: (info) => h("div", { class: "table-cell-medium" }, info.getValue()),
    }),
    columnHelper.accessor("tipe_transaksi", {
        header: "Tipe Transaksi",
        cell: (info) => h("div", { class: "table-cell-medium" }, info.getValue() === 1 ? "Debit" : "Kredit"),
    }),
    columnHelper.accessor("nominal", {
        header: "Nominal",
        cell: (info) => h("div", { class: "tw-text-start" }, formatCurrencyAuto(info.getValue())),
    }),
    columnHelper.accessor((row) => row.keterangan, {
        id: "keterangan",
        header: "Keterangan",
        cell: (info) => {
            return h("div", {
                class: "table-cell-medium",
                innerText: info.getValue(),
            });
        },
    }),
    columnHelper.accessor((row) => row.status, {
        id: "status",
        header: "Status",
        cell: (info) => {
            return h("div", {
                class: "table-cell-medium",
                innerText: info.getValue() === 0 ? "Pending" : (info.getValue() === 1 ? "Confirmed" : "Posted"),
            });
        },
    }),
columnHelper.display({
        id: "action",
        header: "Action",
        cell: (info) => {
            const rowData = info.row.original;
            return h("div", { class: "tw-flex tw-gap-2" }, [
                h(Button, {
                    class: "tw-bg-blue-500 tw-text-white",
                    icon: "mdi mdi-pencil",
                    disabled: rowData.status > 0,
                    // Kirim sebagai prop 'trigger' karena Button.vue mencarinya
                    trigger: () => shomModal(rowData), 
                }),
                h(Button, {
                    class: "tw-bg-red-500 tw-text-white",
                    icon: "mdi mdi-trash-can-outline",
                    disabled: rowData.status > 0,
                    // Gunakan nama handleDelete sesuai parameter fungsi di atas
                    trigger: () => handledelete(rowData),
                }),
            ]);
        },
    }),

];
