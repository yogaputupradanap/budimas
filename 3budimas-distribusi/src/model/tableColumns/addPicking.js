import { createColumnHelper } from "@tanstack/vue-table";
const columnHelper = createColumnHelper();
import { h } from "vue";
import RouterButton from "@/src/components/ui/RouterButton.vue";
import { apiUrl, fetchWithAuth, localDisk } from "../../lib/utils";


export const tableAddPicking = [
  columnHelper.accessor((row) => row.id, {
    id: "id",
    cell: (info) =>
      h("span", {
        class: "tw-w-16 tw-flex tw-justify-center",
        innerText: info.row.index + 1,
      }),
    header: () =>
      h("span", {
        class: "tw-w-16 tw-flex tw-justify-center",
        innerText: "No",
      }),
  }),
  columnHelper.accessor((row) => row.nama_produk, {
    id: "product",
    cell: (info) => {
      return h(
        "div",
        {
          class:
            "tw-w-56 tw-flex tw-flex-col tw-justify-center tw-items-center tw-gap-1",
        },
        [
          h("span", {
            class: "tw-font-medium tw-text-xs",
            innerText: info.row.original.nama_produk,
          }),
          h("span", {
            class: "tw-text-xs tw-text-blue-400",
            innerText: info.row.original.kode_sku,
          }),
        ]
      );
    },
    header: h("span", {
      class: "tw-w-56 tw-flex tw-flex-col tw-justify-center tw-items-center",
      innerText: "Produk",
    }),
  }),
  columnHelper.accessor((row) => row.pieces, {
    id: "satuan",
    cell: (info) =>
      h("span", {
        class: "tw-w-32 tw-flex tw-justify-center",
        innerText: info.getValue(),
      }),
    header: () =>
      h("span", { class: "tw-w-32 tw-text-center", innerText: "Satuan" }),
  }),
  columnHelper.accessor((row) => row.total_in_pieces, {
    id: "total_order",
    cell: (info) =>
      h("span", {
        class: "tw-w-24 tw-flex tw-justify-center",
        innerText: info.getValue(),
      }),
    header: () =>
      h("span", { class: "tw-w-24 tw-text-center", innerText: "Total Order" }),
  }),
  columnHelper.accessor((row) => row.jumlah_picked, {
    id: "total_picked",
    cell: (info) =>
      h("span", {
        class: "tw-w-24 tw-flex tw-justify-center",
        innerText: info.getValue(),
      }),
    header: () =>
      h("span", { class: "tw-w-24 tw-text-center", innerText: "Total Picked" }),
  }),
  columnHelper.accessor((row) => row.stok, {
    id: "stok",
    cell: (info) =>
      h("span", {
        class: "tw-w-24 tw-flex tw-justify-start",
        innerText: info.getValue(),
      }),
    header: () =>
      h("span", { class: "tw-w-24 tw-text-start", innerText: "stok" }),
  }),
  columnHelper.accessor((row) => row.keterangan, {
    id: "keterangan",
    cell: (info) =>
      h("span", {
        class: "tw-w-40 tw-flex tw-justify-start",
        innerText: info.getValue(),
      }),
    header: () =>
      h("span", { class: "tw-w-40 tw-text-start", innerText: "Keterangan" }),
  }),
  columnHelper.display({
  id: "actions",
  cell: (info) => {
    const row = info.row.original;

    const idRute = row.id_rute;
    const produkId = info.row.original.produk_id;
    const orderDetailId = row.id_order_detail;
    localDisk.setLocalStorage("produkid", produkId);
    // console.log(info.row.original.produk_id);
    return h(
      RouterButton,
      {
        to: `/picking/add-picking/${idRute}/detail/${produkId}?id_order_detail=${orderDetailId}`,
        class: "tw-w-24 tw-mr-2",
        icon: "mdi mdi-pencil",
      },
      { default: () => "Edit" }
    );
  },
  header: "Actions",
}),
];
