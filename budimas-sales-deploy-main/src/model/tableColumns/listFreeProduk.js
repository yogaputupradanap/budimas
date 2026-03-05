import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";

const columnHelper = createColumnHelper();
export const listFreeProductsColumns = [
  columnHelper.accessor((row) => row.no, {
    id: "No",
    cell: (info) =>
      h("div", {
        class: "tw-w-full tw-flex tw-justify-center",
        innerText: info.getValue(),
      }),
    header: () =>
      h("div", {
        class: "tw-w-full tw-flex tw-justify-center",
        innerText: "No",
      }),
  }),
  columnHelper.accessor((row) => row.kode_voucher, {
    id: "kodeVoucher",
    cell: (info) =>
      h(
        "div",
        { class: "tw-w-28 lg:tw-w-full tw-flex tw-flex-col tw-items-center" },
        [
          h("span", { innerText: info.getValue() })
        ]
      ),
    header: () =>
      h("span", {
        class: "tw-w-28 lg:tw-w-full tw-flex tw-justify-center",
        innerText: "Kode Voucher",
      }),
  }),
  columnHelper.accessor((row) => row.produk.nama, {
    id: "deskripsiProduk",
    cell: (info) =>
      h(
        "div",
        { class: "tw-w-28 lg:tw-w-full tw-flex tw-flex-col tw-items-center" },
        [
          h("span", { innerText: info.getValue() }),
          h("span", {
            class: "tw-text-xs tw-text-blue-500",
            innerText: info.row.original.produk.kode_sku,
          }),
        ]
      ),
    header: () =>
      h("span", {
        class: "tw-w-28 lg:tw-w-full tw-flex tw-justify-center",
        innerText: "deskripsi Produk",
      }),
  }),
  columnHelper.accessor((row) => row.jumlah_produk, {
    id: "jumlahProduk",
    cell: (info) =>
      h("div", {
        class: "tw-w-28 lg:tw-w-full tw-flex tw-justify-center",
        innerText: info.getValue(),
      }),
    header: () =>
      h("span", {
        class: "tw-w-28 lg:tw-w-full tw-flex tw-justify-center",
        innerText: "Jumlah Produk",
      }),
  }),
  columnHelper.accessor((row) => row.satuan, {
    id: "satuan",
    cell: (info) =>
      h("div", {
        class: "tw-w-28 lg:tw-w-full tw-flex tw-justify-center",
        innerText: info.getValue(),
      }),
    header: () =>
      h("div", {
        class: "tw-w-28 lg:tw-w-full tw-flex tw-justify-center",
        innerText: "Uom/Satuan",
      }),
  }),
];
