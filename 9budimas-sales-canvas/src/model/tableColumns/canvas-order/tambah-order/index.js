import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import { parseCurrency } from "@/src/lib/utils";
import Button from "@/src/components/ui/Button.vue";

const columnHelper = createColumnHelper();

export const listAddCanvasOrderColumn = [
  columnHelper.display({
    id: "action",
    header: "Actions",
    cell: ({ column, row, table }) => {
      const showModal = () => {
        if (table.options.meta && table.options.meta.updateRow) {
          table.options.meta.updateRow(row.original, row.index, column.id, "openRowModal");
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
  columnHelper.accessor(row => row.nama_produk, {
    id: "nama_produk",
    header: h("div", { class: "tw-px-2 tw-py-1", innerText: "Produk" }),
    cell: info =>
      h("div", {
        class: "tw-px-2 tw-py-1 tw-w-auto tw-whitespace-nowrap",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.accessor(row => row.qty_uom1, {
    id: "qty_uom1",
    header: h("div", { class: "tw-px-2 tw-py-1", innerText: "UOM 1" }),
    cell: info =>
      h("div", { class: "tw-px-2 tw-py-1 tw-w-auto tw-truncate" }, [
        h("span", {}, `${info.getValue()} `),
        h("span", { class: "tw-text-blue-600 tw-ml-1" }, "Pcs"),
      ]),
  }),
  columnHelper.accessor(row => row.qty_uom2, {
    id: "qty_uom2",
    header: h("div", { class: "tw-px-2 tw-py-1", innerText: "UOM 2" }),
    cell: info =>
      h("div", { class: "tw-px-2 tw-py-1 tw-w-auto tw-truncate" }, [
        h("span", {}, `${info.getValue()}`),
        h("span", { class: "tw-text-blue-600 tw-ml-1" }, "Box"),
      ]),
  }),
  columnHelper.accessor(row => row.qty_uom3, {
    id: "qty_uom3",
    header: h("div", { class: "tw-px-2 tw-py-1", innerText: "UOM 3" }),
    cell: info =>
      h("div", { class: "tw-px-2 tw-py-1 tw-w-auto tw-truncate" }, [
        h("span", {}, `${info.getValue()}`),
        h("span", { class: "tw-text-blue-600 tw-ml-1" }, "Carton"),
      ]),
  }),
  columnHelper.accessor(row => row.harga_per_uom1, {
    id: "harga_uom1",
    header: h("div", { class: "tw-px-2 tw-py-1", innerText: "Harga / UOM 1" }),
    cell: info =>
      h("div", {
        class: "tw-px-2 tw-py-1 tw-w-auto tw-truncate tw-whitespace-nowrap",
        innerText: parseCurrency(info.getValue()),
      }),
  }),
  columnHelper.accessor(row => row.v1r, {
    id: "v1r",
    header: h("div", { class: "tw-px-2 tw-py-1", innerText: "V1R" }),
    cell: (info) =>
      h("div", { class: "tw-px-2 tw-py-1 tw-w-auto tw-truncate tw-text-start" }, [
        h("span", {}, parseCurrency(info.getValue())),
      ]),
  }),
  columnHelper.accessor(row => row.v2r, {
    id: "v2r",
    header: h("div", { class: "tw-px-2 tw-py-1", innerText: "V2R" }),
    cell: (info) =>
      h("div", { class: "tw-px-2 tw-py-1 tw-w-auto tw-truncate tw-text-start" }, [
        h("span", {}, parseCurrency(info.getValue())),
      ]),
  }),
  columnHelper.accessor(row => row.v3r, {
    id: "v3r",
    header: h("div", { class: "tw-px-2 tw-py-1", innerText: "V3R" }),
    cell: (info) =>
      h("div", { class: "tw-px-2 tw-py-1 tw-w-auto tw-truncate tw-text-start" }, [
        h("span", {}, parseCurrency(info.getValue())),
      ]),
  }),
  columnHelper.accessor(row => row.v2p, {
    id: "v2p",
    header: h("div", { class: "tw-px-2 tw-py-1", innerText: "V2P" }),
    cell: (info) =>
      h("div", { class: "tw-px-2 tw-py-1 tw-w-auto tw-truncate tw-text-start" }, [
        h("span", {}, parseCurrency(info.getValue())),
      ]),
  }),
  columnHelper.accessor(row => row.v3p, {
    id: "v3p",
    header: h("div", { class: "tw-px-2 tw-py-1", innerText: "V3P" }),
    cell: (info) =>
      h("div", { class: "tw-px-2 tw-py-1 tw-w-auto tw-truncate tw-text-start" }, [
        h("span", {}, parseCurrency(info.getValue())),
      ]),
  }),
  columnHelper.accessor(row => row.total_diskon, {
    id: "total_diskon",
    header: h("div", { class: "tw-px-2 tw-py-1", innerText: "Total Disc." }),
    cell: (info) =>
      h("div", { class: "tw-px-2 tw-py-1 tw-w-auto tw-truncate tw-text-start" }, [
        h("span", {}, parseCurrency(info.getValue())),
      ]),
  }),
  columnHelper.accessor(row => row.jumlah_harga, {
    id: "jumlah_harga",
    header: h("div", { class: "tw-px-2 tw-py-1", innerText: "Jumlah Harga" }),
    cell: info =>
      h("div", {
        class: "tw-px-2 tw-py-1 tw-w-auto tw-truncate tw-whitespace-nowrap",
        innerText: parseCurrency(info.getValue()),
      }),
  }),
];
