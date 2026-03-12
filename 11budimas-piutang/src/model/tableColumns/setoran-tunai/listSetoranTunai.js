import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import RouterButton from "@/src/components/ui/RouterButton.vue";
import T from "@/src/components/ui/table/T.vue";
import { parseCurrency } from "@/src/lib/utils";

const columnHelper = createColumnHelper();

export const listSetoranTunaiColumn = [
  columnHelper.display({
    id: "no",
    header: () => h("div", { class: "tw-pl-3", innerText: "No" }),
    cell: (info) => h(T, { innerText: info.row.original.row_num }),
  }),
  columnHelper.accessor((row) => row.draft_tanggal_input, {
    id: "draft_tanggal_input",
    header: "Tanggal",
    cell: (info) =>
      h("div", {
        class: "table-cell-lg",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.accessor((row) => row.nama_sales, {
    id: "nama_sales",
    header: "Sales",
    cell: (info) => {
      return h("div", {
        class: "table-cell-medium",
        innerText: info.getValue(),
      });
    },
  }),
  columnHelper.accessor((row) => row.setoran_piutang, {
    id: "setoran_piutang",
    header: "Setoran Piutang",
    cell: (info) => {
      return h("div", {
        class: "table-cell-medium",
        innerText: parseCurrency(info.getValue()),
      });
    },
  }),
  columnHelper.accessor((row) => row.status_setoran, {
    id: "status_setoran",
    header: "Status Setoran",
    cell: (info) => {
      const value = info.getValue();
      const statusColor = {
        sales: "tw-bg-red-500",
        kasir: "tw-bg-yellow-600",
        audit: "tw-bg-green-600",
      };
      const classColor = statusColor[value];

      return h(
        "div",
        {
          class: "table-cell-medium",
        },
        [
          h("span", {
            class: `tw-px-7 tw-py-1 tw-text-white tw-font-medium tw-rounded-md ${classColor}`,
            innerText: value,
          }),
        ]
      );
    },
  }),
  columnHelper.display({
    id: "actions",
    header: "Action",
    cell: (info) => {
      const { id_sales, draft_tanggal_input: tanggal, status_setoran } =
        info.row.original;
      // Menentukan text button berdasarkan status_setoran
      const buttonText = status_setoran === "audit"
        ? "Detail Setoran"
        : "Konf. Setoran";
      return h(RouterButton, {
        to: `/setoran-tunai/list-faktur?id_sales=${id_sales}&tanggal=${tanggal}`,
        class: "tw-text-white tw-w-32 tw-py-2",
        innerText: buttonText,
      });
    },
  }),
];
