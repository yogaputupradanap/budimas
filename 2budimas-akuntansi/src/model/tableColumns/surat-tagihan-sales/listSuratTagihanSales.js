import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import RouterButton from "@/src/components/ui/RouterButton.vue";
import T from "@/src/components/ui/table/T.vue";
import { parseCurrency } from "@/src/lib/utils";
import { format } from "date-fns";
import { id } from "date-fns/locale";

const columnHelper = createColumnHelper();

export const listSuratTagihanColumn = [
  columnHelper.accessor((row) => row.row_num, {
    id: "no",
    header: () => h("div", { class: "tw-pl-3", innerText: "No" }),
    cell: (info) => h(T, { innerText: info.getValue() }),
  }),
  columnHelper.accessor((row) => row.nota_tagihan, {
    id: "nota_tagihan",
    header: "Surat Tagihan",
    cell: (info) =>
      h("div", {
        class: "table-cell-medium",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.accessor((row) => row.nama_customer, {
    id: "nama_customer",
    header: "Customer",
    cell: (info) =>
      h("div", {
        class: "table-cell-lg",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.accessor((row) => row.nama_principal, {
    id: "nama_principal",
    header: "Nama Principal",
    cell: (info) => {
      return h("div", {
        class: "table-cell-lg",
        innerText: info.getValue(),
      });
    },
  }),
  columnHelper.accessor((row) => row.nama_pj, {
    id: "nama_pj",
    header: "Nama PJ",
    cell: (info) => {
      return h("div", {
        class: "table-cell-medium",
        innerText: info.getValue(),
      });
    },
  }),
  columnHelper.accessor((row) => row.total_penjualan, {
    id: "total_penjualan",
    header: "Total Tagihan",
    cell: (info) => {
      return h("div", {
        class: "table-cell-medium",
        innerText: parseCurrency(info.getValue()),
      });
    },
  }),
  columnHelper.accessor((row) => row.jumlah_faktur, {
    id: "jumlah_faktur",
    header: "Jumlah Faktur",
    cell: (info) =>
      h("div", {
        class: "table-cell-small",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.accessor((row) => row.status_kirim, {
    id: "status_kirim",
    header: "Status Kirim",
    cell: (info) =>
      h("div", {
        class: "table-cell-small",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.accessor((row) => row.status_bayar, {
    id: "status_bayar",
    header: "Status Bayar",
    cell: (info) =>
      h("div", {
        class: "table-cell-small",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.display({
    header: "Action",
    cell: (info) => {
      const { nota_tagihan } = info.row.original;
      return h("div", { class: "tw-pr-2" }, [
        h(
          RouterButton,
          {
            to: `/surat-tagihan-sales/detail-surat-tagihan-sales/${nota_tagihan}`,
            class: "tw-px-4 tw-py-2",
          },
          "Detail"
        ),
      ]);
    },
  }),
];
