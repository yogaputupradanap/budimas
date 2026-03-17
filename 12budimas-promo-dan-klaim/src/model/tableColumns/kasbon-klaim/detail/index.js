import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import T from "@/src/components/ui/table/T.vue";
import { parseCurrency } from "@/src/lib/utils";

const columnHelper = createColumnHelper();

export const kasbonKlaimDetailColumn = [
  columnHelper.display({
    id: "select",
    header: ({ table }) => {
      const selectableRows = table
        .getRowModel()
        .rows.filter((row) => row.original.status_klaim !== 'Klaim disetujui');

      const allSelected = selectableRows.length > 0 && 
        selectableRows.every((row) => row.getIsSelected());

      return h("input", {
        type: "checkbox",
        checked: allSelected,
        onChange: (e) => {
          selectableRows.forEach((row) => {
            row.toggleSelected(e.target.checked);
          });
        },
        class: "tw-w-4 tw-h-4 tw-rounded",
      });
    },
    cell: ({ row }) => {
      if (row.original.status_klaim === 'Klaim disetujui') {
        return h("div", { 
          class: "tw-w-4 tw-h-4 tw-flex tw-items-center tw-justify-center tw-text-green-500",
          innerHTML: '<i class="mdi mdi-check-circle"></i>' 
        });
      }
      return h("input", {
        type: "checkbox",
        checked: row.getIsSelected(),
        onChange: row.getToggleSelectedHandler(),
        class: "tw-w-4 tw-h-4 tw-rounded",
      });
    },
    enableSorting: false,
    size: 50
  }),
  columnHelper.display({
    id: "no",
    header: h("div", { class: "tw-pl-3" }, "No"),
    cell: (info) => h(T, null, { default: () => info.row.index + 1 }),
    size: 60
  }),
  columnHelper.accessor((row) => row.nomor_klaim, {
    id: "nomor_klaim",
    header: h("div", null, "Nomor Klaim"),
    cell: (info) =>
      h("div", { class: "table-cell-lg" }, info.getValue() || "-"),
  }),
  columnHelper.accessor((row) => row.kode_promo, {
    id: "kode_promo",
    header: h("div", null, "Kode Promo"),
    cell: (info) =>
      h("div", { class: "table-cell-lg" }, info.getValue() || "-"),
  }),
  columnHelper.accessor((row) => row.nama_promo, {
    id: "nama_promo",
    header: h("div", null, "Nama Promo"),
    cell: (info) =>
      h("div", { class: "table-cell-lg" }, info.getValue() || "-"),
  }),
  columnHelper.accessor((row) => row.principal, {
    id: "principal",
    header: h("div", null, "Principal"),
    cell: (info) =>
      h("div", { class: "table-cell-lg" }, info.getValue() || "-"),
  }),
  columnHelper.accessor((row) => row.nominal_klaim, {
    id: "nominal_klaim",
    header: h("div", null, "Nominal Klaim"),
    cell: (info) =>
      h("div", { class: "table-cell-lg tw-text-right" }, parseCurrency(info.getValue() || 0)),
  }),
  columnHelper.accessor((row) => row.status_klaim, {
    id: "status_klaim",
    header: h("div", null, "Status Klaim"),
    cell: (info) => {
      const status = info.getValue();
      return h("div", { class: `table-cell-lg tw-font-medium` }, status || "-");
    }
  }),
];
