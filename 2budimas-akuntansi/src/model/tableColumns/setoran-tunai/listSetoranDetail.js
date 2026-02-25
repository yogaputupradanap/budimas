import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import Button from "@/src/components/ui/Button.vue";
import { parseCurrency } from "@/src/lib/utils";

const columnHelper = createColumnHelper();

export const listSetoranDetailColumn = [
  columnHelper.display({
    id: "no",
    header: () => h("div", { class: "tw-pl-3", innerText: "No" }),
    cell: (info) =>
      h("div", { class: "tw-pl-3", innerText: info.row.original.row_num }),
  }),
  columnHelper.accessor((row) => row.nama_pj, {
    id: "nama_pj",
    header: "Nama PJ",
    cell: (info) =>
      h("div", {
        class: "table-cell-lg",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.accessor((row) => row.draft_tanggal_input, {
    id: "draft_tanggal_input",
    header: "Draft Tanggal Input",
    cell: (info) =>
      h("div", {
        class: "table-cell-medium",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.accessor((row) => row.draft_jumlah_setor, {
    id: "draft_jumlah_setor",
    header: "Draft Jumlah Setor",
    cell: (info) => {
      return h("div", {
        class: "table-cell-medium",
        innerText: parseCurrency(info.getValue()),
      });
    },
  }),
  columnHelper.accessor((row) => row.tanggal_setoran_diterima, {
    id: "tanggal_setoran_diterima",
    header: "Tanggal Setoran Diterima",
    cell: (info) =>
      h("div", {
        class: "table-cell-medium",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.accessor((row) => row.bukti_transfer, {
    id: "bukti_transfer",
    header: "Bukti Transfer",
    cell: (info) =>
      h("div", {
        class: "table-cell-medium",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.display({
    id: "actions",
    header: () => "actions",
    cell: ({ column, row, table }) => {
      const showModal = () =>
        table.options.meta.updateRow(
          row.original,
          row.index,
          column.id,
          "openRowModal"
        );

      return h(
        Button,
        {
          class: "tw-px-7 tw-py-2",
          trigger: showModal,
        },
        "Lihat"
      );
    },
  }),
];
