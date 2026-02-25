import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import Button from "@/src/components/ui/Button.vue";

const columnHelper = createColumnHelper();
export const listProdukColumns = [
  columnHelper.display({
    id: "no",
    header: h("div", { class: "tw-pl-4", innerText: "No" }),
    cell: (info) =>
      h("div", { class: "tw-pl-4", innerText: info.row.index + 1 }),
  }),
  columnHelper.accessor((row) => row.nama_produk, {
    id: "nama_produk",
    header: "Produk",
    cell: (info) => info.getValue(),
  }),

  columnHelper.accessor((row) => row.uom_1, {
    id: "uom1",
    header: "UOM 3 (karton)",
    cell: (info) => info.getValue(),
  }),
  columnHelper.accessor((row) => row.uom_2, {
    id: "uom2",
    header: "UOM 2 (box)",
    cell: (info) => info.getValue(),
  }),
  columnHelper.accessor((row) => row.uom_3, {
    id: "uom3",
    header: "UOM 1 (pieces)",
    cell: (info) => info.getValue(),
  }),
  columnHelper.display({
    id: "actions",
    header: "Action",
    cell: ({ column, row, table }) => {
      const { id } = column;
      const { index } = row;

      const remove = () =>
        table.options.meta.updateRow(null, index, id, "removeRow");

      return h(Button, {
        trigger: () => remove(),
        icon: "mdi mdi-delete tw-text-lg",
        class: "tw-bg-red-500 tw-text-white tw-w-14",
      });
    },
  }),
];
