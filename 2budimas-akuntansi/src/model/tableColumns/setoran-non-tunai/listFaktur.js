import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import Button from "@/src/components/ui/Button.vue";
import { parseCurrency } from "@/src/lib/utils";
import { useUser } from "@/src/store/user";

const columnHelper = createColumnHelper();

const hasAuditRole = () => {
    const userStore = useUser();
    return userStore.hasAccess('audit');
};

export const listFakturNonTunaiColumn = [
    columnHelper.display({
        id: "no",
        header: () => h("div", { class: "tw-pl-3", innerText: "No" }),
        cell: (info) =>
            h("div", { class: "tw-pl-3", innerText: info.row.index + 1 }),
    }),
    columnHelper.accessor((row) => row.tanggal, {
        id: "tanggal",
        header: "Tanggal",
        cell: (info) =>
            h("div", {
                class: "table-cell-lg",
                innerText: info.getValue(),
            }),
    }),
    columnHelper.accessor((row) => row.nama_customer, {
        id: "nama_customer",
        header: "Nama Customer",
        cell: (info) => {
            return h("div", {
                class: "table-cell-lg",
                innerText: info.getValue(),
            });
        },
    }),
    columnHelper.accessor((row) => row.no_faktur, {
        id: "no_faktur",
        header: "No Faktur",
        cell: (info) =>
            h("div", {
                class: "table-cell-lg",
                innerText: info.getValue(),
            }),
    }),
    columnHelper.accessor((row) => row.tagihan, {
        id: "tagihan",
        header: "Tagihan",
        cell: (info) =>
            h("div", {
                class: "table-cell-medium",
                innerText: parseCurrency(info.getValue()),
            }),
    }),
    columnHelper.accessor((row) => row.setoran, {
        id: "setoran",
        header: "Setoran",
        cell: (info) =>
            h("div", {
                class: "table-cell-medium",
                innerText: parseCurrency(info.getValue()),
            }),
    }),
    columnHelper.accessor((row) => row.status_pembayaran, {
        id: "status_pembayaran",
        header: "Status",
        cell: (info) => {
            const value = info.getValue();
            const statusColor = {
                'lunas': "tw-text-green-500",
                'belum lunas': "tw-text-red-500",
            };

            return h("div", {
                class: `table-cell-medium ${statusColor[value]} tw-uppercase`,
                innerText: value,
            });
        },
    }),
    columnHelper.display({
        id: "actions",
        header: () => "actions",
        cell: ({ column, row, table }) => {
            const hasBiayaLainnya = row.original.biaya_lainnya;
            const baseButtonClass = "tw-text-white tw-w-32 tw-py-2 tw-text-xs";
            const isAudit = hasAuditRole();
            const statusSetoran = row.original.status_setoran;

            const buttons = [
                h(Button, {
                    class: baseButtonClass,
                    icon: "mdi mdi-receipt-text-check-outline",
                    trigger: () => table.options.meta.updateRow(
                        row.original,
                        row.index,
                        column.id,
                        "openRowModal",
                        "lihat-bukti-setor"
                    )
                }, () => "Bukti Setor"),
            ];

            // Hanya tampilkan tombol biaya lainnya jika role adalah audit
            if (isAudit) {
                // Jika status_setoran = 3 dan ada biaya_lainnya, tampilkan "Lihat Biaya"
                if (statusSetoran === 3 && hasBiayaLainnya) {
                    buttons.push(
                        h(Button, {
                            class: `${baseButtonClass} tw-bg-green-500`,
                            icon: "mdi mdi-eye-outline",
                            trigger: () => table.options.meta.updateRow(
                                row.original,
                                row.index,
                                column.id,
                                "openRowModal",
                                "tambah-biaya-lainnya"
                            )
                        }, () => "Lihat Biaya")
                    );
                }
                // Jika status_setoran = 2, tampilkan tombol Edit/Tambah Biaya
                else if (statusSetoran === 2) {
                    buttons.push(
                        h(Button, {
                            class: `${baseButtonClass}${hasBiayaLainnya ? " tw-bg-green-500" : ""}`,
                            icon: `mdi mdi-${hasBiayaLainnya ? "pencil" : "plus-circle"}-outline`,
                            trigger: () => table.options.meta.updateRow(
                                row.original,
                                row.index,
                                column.id,
                                "openRowModal",
                                "tambah-biaya-lainnya"
                            )
                        }, () => `${hasBiayaLainnya ? "Edit" : "Tambah"} Biaya`)
                    );
                }
                // Untuk status_setoran lainnya (1 atau status lain), tidak menampilkan tombol biaya
            }

            return h("div", { class: "tw-flex tw-flex-col tw-gap-2" }, buttons);
        }
    })
];
