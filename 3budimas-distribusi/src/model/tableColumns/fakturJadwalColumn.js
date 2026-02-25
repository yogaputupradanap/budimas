import { formatCurrency } from "@/src/lib/utils";
import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";

const columnHelper = createColumnHelper();

export const fakturJadwalColumn = () => {
  return [
    columnHelper.display({
      id: "select",
      header: ({ table }) =>
        h("div", { class: "tw-flex tw-justify-center tw-w-full" }, [
          h("input", {
            type: "checkbox",
            checked: table.getIsAllRowsSelected(),
            onChange: (e) => table.toggleAllRowsSelected(!!e.target.checked),
            class: "tw-w-5 tw-h-5 tw-rounded",
          }),
        ]),
      cell: ({ row }) =>
        h("div", { class: "tw-flex tw-justify-center" }, [
          h("input", {
            type: "checkbox",
            checked: row.getIsSelected(),
            onChange: (e) => row.toggleSelected(!!e.target.checked),
            class: "tw-w-5 tw-h-5 tw-rounded",
          }),
        ]),
      enableSorting: false,
    }),
    columnHelper.accessor((row) => row.id, {
      id: "id",
      cell: (info) =>
        h("div", {
          class: "tw-w-10 tw-text-center",
          innerText: info.row.index + 1,
        }),
      header: h("span", { class: "tw-w-10", innerText: "No" }),
    }),
    columnHelper.accessor((row) => row.no_order, {
      id: "no_order",
      cell: (info) =>
        h("span", {
          class: "table-cell-small",
          innerText: info.getValue(),
        }),
      header: "no order",
    }),
    columnHelper.accessor((row) => row.nama_principal, {
      id: "nama_principal",
      cell: (info) =>
        h("span", {
          class: "table-cell-small",
          innerText: info.getValue(),
        }),
      header: "Nama Principal",
    }),
    columnHelper.accessor((row) => row.nama_customer, {
      id: "nama_customer",
      cell: (info) =>
        h("span", {
          class: "table-cell-small",
          innerText: info.getValue(),
        }),
      header: "nama customer",
    }),
    columnHelper.accessor((row) => row.estimasi_kubikasi, {
      id: "estimasi_kubikasi",
      cell: (info) =>
        h("span", {
          class: "table-cell-small",
          innerText: info.getValue(),
        }),
      header: "estimasi kubikasi (m)",
    }),
    columnHelper.accessor((row) => row.total_bayar, {
      id: "total_bayar",
      cell: (info) =>
        h("span", {
          class: "table-cell-small",
          innerText: formatCurrency(info.getValue(), 2),
        }),
      header: "total bayar",
    }),
  ];
};
