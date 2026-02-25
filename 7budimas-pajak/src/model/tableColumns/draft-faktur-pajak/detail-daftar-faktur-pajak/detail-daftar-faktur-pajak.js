import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import RouterButton from "@/src/components/ui/RouterButton.vue";
import { formatNumberIDR } from "@/src/lib/utils";
import IndeterminateCheckbox from "@/src/components/ui/IndeterminateCheckbox.vue";

const columnHelper = createColumnHelper();

export const DraftDetailFakturPajakColumns = [
  columnHelper.display({
    id: "no",
    header: "No",
    cell: (info) => info.row.index + 1,
  }),

  columnHelper.accessor((row) => row.nama_produk, {
    id: "nama_produk",
    header: h("div", {
      class: "tw-pl-2",
      innerText: "Nama Produk",
    }),
    cell: (info) =>
      h("div", {
        class: "table-cell-medium tw-pl-2",
        innerText: info.getValue(),
      }),
  }),

  columnHelper.accessor((row) => row.jumlah_uom_1, {
    id: "jumlah_uom_1",
    header: h("div", {
      class: "tw-pl-2",
      innerText: "Jumlah UOM 1",
    }),
    cell: (info) =>
      h("div", {
        class: "table-cell-medium tw-pl-2",
        innerText: info.getValue(),
      }),
  }),

  columnHelper.accessor((row) => row.harga, {
    id: "harga",
    header: h("div", {
      class: "tw-pl-2",
      innerText: "Harga",
    }),
    cell: (info) =>
      h("div", {
        class: "table-cell-medium tw-pl-2",
        innerText: formatNumberIDR(info.getValue()),
      }),
  }),

  columnHelper.accessor((row) => row.hpp, {
    id: "hpp",
    header: h("div", {
      class: "tw-pl-2",
      innerText: "HPP",
    }),
    cell: (info) =>
      h("div", {
        class: "table-cell-medium tw-pl-2",
        innerText: formatNumberIDR(info.getValue()),
      }),
  }),

  columnHelper.accessor((row) => row.dpp, {
    id: "dpp",
    header: h("div", {
      class: "tw-pl-2",
      innerText: "DPP",
    }),
    cell: (info) =>
      h("div", {
        class: "table-cell-medium tw-pl-2",
        innerText: formatNumberIDR(info.getValue()),
      }),
  }),

  columnHelper.accessor((row) => row.pajak, {
    id: "ppn",
    header: h("div", {
      class: "tw-pl-2",
      innerText: "PPN",
    }),
    cell: (info) =>
      h("div", {
        class: "table-cell-medium tw-pl-2",
        innerText: formatNumberIDR(info.getValue()),
      }),
  }),


  columnHelper.accessor((row) => row.status_faktur_pajak, {
    id: "status_faktur_pajak",
    header: h("div", {
      class: "tw-pl-2",
      innerText: "Status",
    }),
    cell: (info) =>
      h("div", {
        class: "table-cell-medium tw-pl-2",
        innerText: info.getValue(),
      }),
  }),
];
