import { createColumnHelper } from "@tanstack/vue-table";
import { useRouter } from "vue-router";
import { h } from "vue";

const columnHelper = createColumnHelper();

export const tableDistribusiHistoryDetail = [
  columnHelper.accessor((row) => row.id_rute, {
    id: "id",
    cell: (info) =>
      h("span", {
        class: "tw-w-10 tw-flex tw-justify-center",
        innerText: info.row.index + 1,
      }),
    header: () =>
      h("span", {
        class: "tw-w-10 tw-flex tw-justify-center",
        innerText: "No",
      }),
  }),
  columnHelper.accessor((row) => row.no_faktur, {
    id: "faktur",
    cell: (info) => h("span", {
      class: "table-cell-lg",
      innerText: info.getValue(),
    }),
    header: "Faktur",
  }),
  columnHelper.accessor((row) => row.nama_customer, {
    id: "nama_toko",
    cell: (info) => h("span", {
      class: "table-cell-medium",
      innerText: info.getValue(),
    }),
    header: "Nama Toko",
  }),
  columnHelper.accessor((row) => row.kubikal, {
    id: "kubikasi",
    cell: (info) => h("span", {
      class: "table-cell-small",
      innerText: info.getValue(),
    }),
    header: "Kubikasi",
  }),
  columnHelper.accessor((row) => row.jenis_faktur, {
    id: "keterangan",
    cell: (info) => h("span", {
      class: "table-cell-small",
      innerText: info.getValue(),
    }),
    header: "Keterangan",
  }),
];
