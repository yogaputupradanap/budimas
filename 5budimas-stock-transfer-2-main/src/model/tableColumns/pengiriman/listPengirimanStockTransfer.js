import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import RouterButton from "@/src/components/ui/RouterButton.vue";
import IndeterminateCheckbox from "@/src/components/ui/IndeterminateCheckbox.vue";

const columnHelper = createColumnHelper();

export const listPengirimanStockTransferColumn = [
  columnHelper.display({
    id: "select",
    header: ({ table }) =>
      h("div", { class: "tw-px-2 tw-pt-1" }, [
        h(IndeterminateCheckbox, {
          checked: table.getIsAllRowsSelected(),
          indeterminate: table.getIsSomeRowsSelected(),
          onChange: table.getToggleAllRowsSelectedHandler(),
        }),
      ]),
    cell: ({ row }) => {
      return h("div", { class: "tw-px-2 tw-pt-1" }, [
        h(IndeterminateCheckbox, {
          checked: row.getIsSelected(),
          disabled: !row.getCanSelect(),
          onChange: row.getToggleSelectedHandler(),
        }),
      ]);
    },
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
    id: "nama_produk",
    header: "Tanggal",
    cell: (info) =>
      h("div", {
        class: "table-cell-lg",
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
    id: "jumlah_picked",
    header: "Jumlah Picked",
    cell: (info) =>
      h("div", {
        class: "table-cell-medium",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.accessor((row) => row.status, {
    id: "status",
    header: "Status",
    cell: (info) => {
      const value = info.getValue();
      const status = value === 5 ? "Picked" : value === 2 && "Pengiriman";

      return h("div", {
        class: "table-cell-medium",
        innerText: status,
      });
    },
  }),
  columnHelper.display({
    id: "actions",
    header: h("div", { class: "tw-px-2 tw-text-xs", innerText: "Action" }),
    cell: (info) => {
      const id = info.row.original.id_stock_transfer;
      return h("div", { class: "tw-px-2" }, [
        h(
          RouterButton,
          {
            to: `/pengiriman/detail/${id}`,
            class: "tw-text-white tw-w-24 tw-h-8 tw-text-xs tw-rounded-md",
          },
          () => "Detail"
        ),
      ]);
    },
  }),
];
