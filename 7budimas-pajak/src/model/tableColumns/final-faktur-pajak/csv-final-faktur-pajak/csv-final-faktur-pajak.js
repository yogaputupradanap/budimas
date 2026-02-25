import { createColumnHelper, useVueTable } from "@tanstack/vue-table";
import { h } from "vue";
import RouterButton from "@/src/components/ui/RouterButton.vue";
import T from "@/src/components/ui/table/T.vue";
import { formatNumberIDR } from "@/src/lib/utils";
import IndeterminateCheckbox from "@/src/components/ui/IndeterminateCheckbox.vue";

const columnHelper = createColumnHelper();

export const CsvFinalFakturPajakColumns = [
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

  columnHelper.accessor((row) => row.nsfp, {
    id: "nsfp",
    header: h("div", {
      class: "tw-pl-2",
      innerText: "No. Faktur Pajak",
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

  columnHelper.accessor((row) => row.dpp_csv, {
    id: "tagihan_dpp",
    header: h("div", {
      class: "tw-pl-2",
      innerText: "DPP (total tagihan)",
    }),
    cell: (info) =>
      h("div", {
        class: "table-cell-medium tw-pl-2",
        innerText: formatNumberIDR(info.getValue()),
      }),
  }),

  columnHelper.accessor((row) => row.hpp_csv, {
    id: "tagihan_hpp",
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

  columnHelper.accessor((row) => row.ppn_csv, {
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
];
