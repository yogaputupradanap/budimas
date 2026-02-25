import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import RouterButton from "@/src/components/ui/RouterButton.vue";
import { statusToStr } from "@/src/lib/utils";

const columnHelper = createColumnHelper();
export const listPengajuanStockTransferColumn = [
  columnHelper.display({
    id: "no",
    header: h("div", {
      class: "tw-pl-4 md:tw-pl-4 tw-w-12 tw-text-start md:tw-w-auto",
      innerText: "No",
    }),
    cell: (info) =>
      h("div", { class: "tw-pl-4", innerText: info.row.index + 1 }),
  }),
  columnHelper.accessor((row) => row.nota_stock_transfer, {
    id: "nota",
    header: "Nota",
    cell: (info) =>
      h("div", {
        class: "table-cell-lg",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.accessor((row) => row.created_at, {
    id: "tanggal",
    header: "Tanggal",
    cell: (info) =>
      h("div", {
        class: "table-cell-medium",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.accessor((row) => row.nama_cabang_awal, {
    id: "cabang_awal",
    header: "Cabang Awal",
    cell: (info) =>
      h("div", {
        class: "table-cell-medium",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.accessor((row) => row.nama_cabang_tujuan, {
    id: "cabang_tujuan",
    header: "cabang Tujuan",
    cell: (info) =>
      h("div", {
        class: "table-cell-medium",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.accessor((row) => row.status, {
    id: "konfirmasi",
    header: "Konfirmasi",
    cell: (info) =>
      h("div", {
        class: "table-cell-medium",
        innerText: statusToStr[info.getValue()],
      }),
  }),
  columnHelper.accessor((row) => row.jumlah, {
    id: "jumlah",
    header: "Jumlah",
    cell: (info) =>
      h("div", {
        class: "table-cell-medium",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.accessor((row) => row.jumlah_picked, {
    id: "jumlah_picked",
    header: "Jumlah Picked",
    cell: (info) =>
      h("div", {
        class: "table-cell-medium",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.display({
    id: "action",
    header: "Actions",
    cell: (info) => {
      const id = info.row.original.id_stock_transfer;
      return h(
        RouterButton,
        { to: `/konfirmasi/detail/${id}`, class: "tw-w-32" },
        () => "Konfirmasi"
      );
    },
  }),
];
