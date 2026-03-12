import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import Button from "@/src/components/ui/Button.vue";
import { parseCurrency } from "@/src/lib/utils";

const columnHelper = createColumnHelper();

export const listFakturColumn = [
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
      const showModal = () => table.options.meta.updateRow(
        row.original,
        row.index,
        column.id,
        "openRowModal"
      );

      return h(Button, {
        class: "tw-text-white tw-w-32 tw-py-2 tw-text-xs",
        icon: "mdi mdi-receipt-text-check-outline",
        trigger: showModal,
      },
        "Bukti Bayar")
    }
  })
];
