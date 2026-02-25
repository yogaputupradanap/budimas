import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import T from "@/src/components/ui/table/T.vue";
import { formatCurrencyAuto } from "@/src/lib/utils";
import RouterButton from "@/src/components/ui/RouterButton.vue";

const columnHelper = createColumnHelper();

export const listLaporanKasirColumn = [
  columnHelper.display({
    id: "no",
    header: () => h("div", { class: "tw-pl-3" }, "No"),
    cell: (info) => h(T, { innerText: info.row.original.row_num }),
  }),
  columnHelper.accessor((row) => row.tanggal, {
    id: "tanggal",
    header: "Tanggal",
    cell: (info) =>
      h("div", {
        class: "table-cell-medium",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.accessor((row) => row.total_pemasukan, {
    id: "total_pemasukan",
    header: "Total Pemasukan",
    cell: (info) => {
      return h("div", {
        class: "table-cell-medium",
        innerText: formatCurrencyAuto(info.getValue()),
      });
    },
  }),
  columnHelper.accessor((row) => row.total_pengeluaran, {
    id: "total_pengeluaran",
    header: "Total Pengeluaran",
    cell: (info) => {
      return h("div", {
        class: "table-cell-medium",
        innerText: formatCurrencyAuto(info.getValue()),
      });
    },
  }),
  columnHelper.accessor((row) => row.saldo_akhir, {
    id: "saldo_akhir",
    header: "Saldo Akhir",
    cell: (info) => {
      const value = info.getValue();
      const isNegative = value < 0;
      return h("div", {
        class: `table-cell-medium ${
          isNegative ? "tw-text-red-600" : "tw-text-green-600"
        }`,
        innerText: formatCurrencyAuto(value),
      });
    },
  }),
  columnHelper.display({
    id: "actions",
    header: "Action",
    cell: (info) => {
      const { id, tanggal } = info.row.original;

      return h(
        RouterButton,
        {
          to: `/laporan-kasir/detail?tanggal=${tanggal}`,
          icon: "mdi mdi-eye",
          class: "tw-w-24 tw-py-1",
        },
        {
          default: () => "Detail",
        }
      );
    },
  }),
];
