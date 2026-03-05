import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import { parseCurrency } from "@/src/lib/utils";
import T from "@/src/components/ui/table/T.vue";
import Button from "@/src/components/ui/Button.vue";
import RouterButton from "@/src/components/ui/RouterButton.vue";

const columnHelper = createColumnHelper();

export const listCanvasOrderColumn = [
  columnHelper.display({
    id: "no",
    header: h("div", { class: "tw-pl-3", innerText: "No" }),
    cell: (info) => h(T, { innerText: info.row.index + 1 }),
  }),
  columnHelper.accessor((row) => row.tanggal_order, {
    id: "tanggal_order",
    header: h("div", { innerText: "Tanggal Order" }),
    cell: (info) =>
      h("div", {
        class: "table-cell-lg",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.accessor((row) => row.nama_customer, {
    id: "nama_customer",
    header: h("div", { innerText: "Customer" }),
    cell: (info) =>
      h("div", {
        class: "table-cell-lg",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.accessor((row) => row.total_order, {
    id: "total_order",
    header: h("div", { innerText: "Total Order" }),
    cell: (info) =>
      h("div", {
        class: "table-cell-lg",
        innerText: parseCurrency(info.getValue()),
      }),
  }),
  columnHelper.accessor((row) => row.total_dibayarkan, {
    id: "total_dibayarkan",
    header: h("div", { innerText: "Total Dibayarkan" }),
    cell: (info) =>
      h("div", {
        class: "table-cell-lg",
        innerText: parseCurrency(info.getValue() || 0),
      }),
  }),
  columnHelper.display({
    id: "action",
    header: "Actions",
    cell: ({ row }) => {
      const totalOrder = Number(row.original.total_order) || 0;
      const totalDibayarkan = Number(row.original.total_dibayarkan) || 0;
      const isLunas = totalDibayarkan === totalOrder;

      const goToBayar = () => {
        window.location.href = `/canvas-order/tagihan-pembayaran/${row.original.id}`;
      };

      return h("div", { class: "tw-flex tw-gap-2" }, [
        h(
          RouterButton,
          {
            class: "tw-px-5 tw-py-2 tw-text-white mdi mdi-information-outline tw-bg-blue-500 hover:tw-bg-blue-700 tw-rounded-lg tw-flex tw-items-center tw-gap-2",
            innerText: "Detail",
            to: `/canvas-order/detail-canvas/${row.original.id}`,
          },
          ""
        ),
        h(
          Button,
          {
            class: `tw-px-5 tw-py-2 tw-bg-green-500 hover:tw-bg-green-700 mdi mdi-cash-check tw-gap-2 tw-text-white tw-rounded-lg 
            ${ isLunas ? "tw-disabled tw-opacity-50 pointer-events-none" : "" }`,
            trigger: goToBayar,
            disabled: isLunas,
          }, () => "Bayar"
        ),
      ]);
    },
  }),
];
