import { createColumnHelper } from "@tanstack/vue-table";
import { parseCurrency } from "@/src/lib/utils";
import { h } from "vue";
import T from "@/src/components/ui/table/T.vue";
import Button from "@/src/components/ui/Button.vue";

const columnHelper = createColumnHelper();

export const detailCanvasRequestColumns = [
  columnHelper.display({
    id: "no",
    header: h("div", { class: "tw-pl-3", innerText: "No" }),
    cell: (info) => h(T, { innerText: info.row.index + 1 }),
  }),
  columnHelper.accessor((row) => row.nama_produk, {
    id: "nama_produk",
    header: h("div", { innerText: "Produk" }),
    cell: (info) =>
      h("div", {
        class: "table-cell-lg",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.accessor((row) => row.qty_uom1, {
    id: "qty_uom1",
    header: h("div", { innerText: "UOM 1" }),
    cell: (info) =>
      h(
        "div",
        {
          class: "table-cell-lg tw-w-[50px] tw-truncate",
        },
        [
          h("span", {}, `${info.getValue()} `),
          h("span", { class: "tw-text-blue-600 tw-ml-1" }, "Pcs"),
        ]
      ),
  }),
  columnHelper.accessor((row) => row.qty_uom2, {
    id: "qty_uom2",
    header: h("div", { innerText: "UOM 2" }),
    cell: (info) =>
      h(
        "div",
        {
          class: "table-cell-lg tw-w-[50px] tw-truncate",
        },
        [
          h("span", {}, `${info.getValue()}`),
          h("span", { class: "tw-text-blue-600 tw-ml-1" }, "Box"),
        ]
      ),
  }),
  columnHelper.accessor((row) => row.qty_uom3, {
    id: "qty_uom3",
    header: h("div", { innerText: "UOM 3" }),
    cell: (info) =>
      h(
        "div",
        {
          class: "table-cell-lg",
        },
        [
          h("span", {}, `${info.getValue()}`),
          h("span", { class: "tw-text-blue-600 tw-ml-1" }, "Carton"),
        ]
      ),
  }),
  columnHelper.display({
    id: "action",
    header: ({ table }) => {
        const hasStatusThree = table.getRowModel()
        .rows.some(row => row.original.status_canvas === 3);
        
        if (!hasStatusThree) {
            return null;
        }
        return "Actions";
    },
    cell: ({ column, row, table }) => {
      if (row.original.status_canvas !== 3) {
        return null;
      }

      const showModal = () => {
        if (table.options.meta && table.options.meta.updateRow) {
          table.options.meta.updateRow(
            row.original,
            row.index,
            column.id,
            "openRowModal"
          );
        } else {
          console.warn("Table meta.updateRow not found, using direct emit");
          table.options.meta?.onOpenRowModal?.(row.original);
        }
      };
      return h("div", { class: "tw-flex tw-gap-2" }, [
        h(Button, {
          class: "tw-px-2 mdi mdi-pencil",
          trigger: showModal,
        }),
      ]);
    },
  }),
  columnHelper.accessor((row) => row.total_permintaan, {
    id: "total_permintaan",
    header: h("div", { innerText: "Total Produk" }),
    cell: (info) =>
      h("div", {
        class: "table-cell-lg",
        innerText: parseCurrency(info.getValue()),
      }),
  }),
];
