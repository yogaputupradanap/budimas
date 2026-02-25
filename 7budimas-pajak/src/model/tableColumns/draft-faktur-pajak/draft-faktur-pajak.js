import { createColumnHelper, useVueTable } from "@tanstack/vue-table";
import { h } from "vue";
import RouterButton from "@/src/components/ui/RouterButton.vue";
import T from "@/src/components/ui/table/T.vue";
import { formatNumberIDR } from "@/src/lib/utils";
import IndeterminateCheckbox from "@/src/components/ui/IndeterminateCheckbox.vue";

const columnHelper = createColumnHelper();


export const DraftFakturPajakColumn = [
  columnHelper.display({
    id: "checkbox_select",
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

  columnHelper.accessor((row) => row.no_faktur, {
    id: "no_faktur",
    header: h("div", {
        class: "tw-pl-2",
        innerText: "No. Faktur",
      }),
    cell: (info) =>
      h("div", {
        class: "table-cell-medium tw-pl-2",
        innerText: info.getValue(),
      }),
  }),

  columnHelper.accessor((row) => row.nama_customer, {
    id: "customer_name",
    header: h("div", {
        class: "tw-pl-2",
        innerText: "Customer",
      }),
    cell: (info) =>
      h("div", {
        class: "table-cell-medium tw-pl-2",
        innerText: info.getValue(),
      }),
  }),

  columnHelper.accessor((row) => row.nama_principal, {
    id: "principal_name",
    header: h("div", {
        class: "tw-pl-2",
        innerText: "Principal",
      }),
    cell: (info) =>
      h("div", {
        class: "table-cell-medium tw-pl-2",
        innerText: info.getValue(),
      }),
  }),

  columnHelper.accessor((row) => row.tanggal_faktur, {
    id: "tanggal_faktur",
    header: h("div", {
        class: "tw-pl-2",
        innerText: "Tanggal Faktur",
      }),
    cell: (info) =>
      h("div", {
        class: "table-cell-medium tw-pl-2",
        innerText: info.getValue(),
      }),
  }),

  // columnHelper.accessor((row) => row.dpp, {
  //   id: "tagihan_dpp",
  //   header: h("div", {
  //       class: "tw-pl-2",
  //       innerText: "DPP (total tagihan)",
  //     }),
  //   cell: (info) =>
  //     h("div", {
  //       class: "table-cell-medium tw-pl-2",
  //       innerText: formatNumberIDR(info.getValue()),
  //     }),
  // }),

  columnHelper.accessor(row => row.subtotal_penjualan,
    {
      id: "subtotal_penjualan",
      header: h("div", {
        class: "tw-pl-2",
        innerText: "HPP",
      }),
      cell: (info) =>
        h("div", {
          class: "table-cell-medium tw-pl-2",
          innerText: formatNumberIDR(info.getValue()),
        }),
    }
  ),

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

  columnHelper.display({
    id: "action",
    header: h("div", {
        class: "tw-pl-2",
        innerText: "Action",
      }),
    cell: (info) => {
      const { id } = info.row.original;
      return h("div", { class: "tw-px-4 tw-text-center " }, [
        h(
          RouterButton,
          {
            to: `/draft-faktur-pajak-detail/${id}`,
            class:
              "tw-px-4 tw-py-2 tw-bg-primary tw-text-white tw-rounded-md hover:tw-bg-blue-900",
          },
          "Detail"
        ),
      ]);
    },
  }),
];
