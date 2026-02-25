import { createColumnHelper } from "@tanstack/vue-table";
const columnHelper = createColumnHelper();
import { h } from "vue";

export const tableOrderDistribusi = [
  columnHelper.accessor((row) => row.id, {
    id: "id",
    cell: (info) =>
      h("span", {
        class: "tw-w-auto md:tw-w-10 tw-flex tw-justify-center",
        innerText: info.row.index + 1,
      }),
    header: h("span", {
      class: "tw-w-10 tw-flex tw-justify-center",
      innerText: "No",
    }),
  }),
  columnHelper.accessor((row) => row.no_order, {
    id: "nota_order",
    cell: (info) => h("span", {
      class: "table-cell-small",
      innerText: info.getValue(),
    }),
    header: "Nota Order",
  }),
  columnHelper.accessor((row) => row.tanggal_order, {
    id: "tanggal_order",
    cell: (info) => h("span", {
      class: "table-cell-small",
      innerText: info.getValue(),
    }),
    header: "Tgl Order",
  }),
  columnHelper.accessor((row) => row.nama_customer, {
    id: "customer",
    cell: (info) => h("span", {
      class: "table-cell-small",
      innerText: info.getValue(),
    }),
    header: "Customer",
  }),
  columnHelper.accessor((row) => row.nama_principal, {
    id: "kode_principal",
    cell: (info) => h("span", {
      class: "table-cell-medium",
      innerText: info.getValue(),
    }),
    header: "Principal",
  })
];
