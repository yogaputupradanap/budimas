import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import T from "@/src/components/ui/table/T.vue";
import { status } from "@/src/lib/utils";
import RouterButton from "@/src/components/ui/RouterButton.vue";

const columnHelper = createColumnHelper();

export const listEskalasiColumn = [
  columnHelper.display({
    id: "no",
    header: h(T, () => "No"),
    cell: (info) => h(T, () => info.row.index + 1),
  }),
  columnHelper.accessor((row) => row.nota_stock_transfer, {
    id: "nota",
    header: "Nota",
    cell: (info) => h("div", {
      class: "table-cell-lg",
      innerText: info.getValue(),
    }),
  }),
  columnHelper.accessor((row) => row.created_at, {
    id: "tanggal",
    header: "Tanggal",
    cell: (info) => h("div", {
      class: "table-cell-medium",
      innerText: info.getValue(),
    }),
  }),
  columnHelper.accessor((row) => row.tanggal_diterima, {
    id: "tanggal_penerimaan",
    header: "Tanggal Penerimaan",
    cell: (info) => h("div", {
      class: "table-cell-medium",
      innerText: info.getValue(),
    }),
  }),
  columnHelper.accessor((row) => row.nama_cabang_awal, {
    id: "cabang_awal",
    header: "Cabang Awal",
    cell: (info) => h("div", {
      class: "table-cell-medium",
      innerText: info.getValue(),
    }),
  }),
  columnHelper.accessor((row) => row.nama_cabang_tujuan, {
    id: "cabang_tujuan",
    header: "Cabang Tujuan",
    cell: (info) => h("div", {
      class: "table-cell-medium",
      innerText: info.getValue(),
    }),
  }),
  columnHelper.accessor((row) => row.status, {
    id: "status",
    header: "Status",
    cell: (info) => {
      const id_status = info.getValue();
      const statusString = Object.entries(status).find(
        (val) => val[1] === id_status
      );

      return h("div", {
        class: "table-cell-small",
        innerText: statusString[0],
      })
    },
  }),
  columnHelper.display({
    id: "actions",
    header: "Action",
    cell: (info) => {
      const id = info.row.original.id_stock_transfer

      return h(
        RouterButton,
        {
          class: "tw-w-24",
          to: `/list-eskalasi/detail/${id}`
        },
        "check"
      );
    },
  }),
];
