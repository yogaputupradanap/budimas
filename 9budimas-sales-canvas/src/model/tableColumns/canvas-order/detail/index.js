import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import { parseCurrency } from "@/src/lib/utils";

const columnHelper = createColumnHelper();

export const listCanvasOrderDetailColumn = [
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
        h("span", {}, `${info.getValue() || 0} `),
        h("span", { class: "tw-text-blue-600 tw-ml-1" }, "Pcs"),
      ]),
  }),
  columnHelper.accessor(row => row.qty_uom2, {
    id: "qty_uom2",
    header: h("div", { class: "tw-px-2 tw-py-1", innerText: "UOM 2" }),
    cell: info =>
      h("div", { class: "tw-px-2 tw-py-1 tw-w-auto tw-truncate" }, [
        h("span", {}, `${info.getValue() || 0}`),
        h("span", { class: "tw-text-blue-600 tw-ml-1" }, "Box"),
      ]),
  }),
  columnHelper.accessor(row => row.qty_uom3, {
    id: "qty_uom3",
    header: h("div", { class: "tw-px-2 tw-py-1", innerText: "UOM 3" }),
    cell: info =>
      h("div", { class: "tw-px-2 tw-py-1 tw-w-auto tw-truncate" }, [
        h("span", {}, `${info.getValue() || 0}`),
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
  columnHelper.accessor(row => row.subtotal_harga, {
    id: "jumlah_harga",
    header: h("div", { class: "tw-px-2 tw-py-1", innerText: "Jumlah Harga" }),
    cell: info =>
      h("div", {
        class: "tw-px-2 tw-py-1 tw-w-auto tw-truncate tw-whitespace-nowrap",
        innerText: parseCurrency(info.getValue()),
      }),
  }),
];
