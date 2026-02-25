import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import RouterButton from "@/src/components/ui/RouterButton.vue";

const columnHelper = createColumnHelper();

export const listPenerimaanBarangColumn = [
  columnHelper.accessor((row) => row.nota_stock_transfer, {
    id: "nota",
    header: h("div", { class: "tw-pl-4", innerText: "No" }),
    cell: (info) =>
      h("div", {
        class: "table-cell-lg",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.accessor((row) => row.created_at, {
    id: "created_at",
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
    header: "Cabang Tujuan",
    cell: (info) =>
      h("div", {
        class: "table-cell-medium",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.accessor((row) => row.jumlah_picked, {
    id: "jumlah_produk",
    header: "Jumlah Produk",
    cell: (info) =>
      h("div", {
        class: "table-cell-medium",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.display({
    id: "actions",
    header: "Action",
    cell: (info) => {
      const id = info.row.original.id_stock_transfer;
      return h(
        RouterButton,
        {
          to: `/penerimaan-barang/detail/${id}`,
          class: "tw-text-white tw-w-24",
        },
        () => "Detail"
      );
    },
  }),
];
