import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import T from "@/src/components/ui/table/T.vue";
import { formatCurrencyAuto } from "@/src/lib/utils";
import { useRoute } from "vue-router";

const columnHelper = createColumnHelper();

export const detailLaporanKasirColumn = [
  columnHelper.display({
    id: "no",
    header: () => h("div", { class: "tw-pl-3" }, "No"),
    cell: (info) => h(T, { innerText: info.row.index + 1 }),
  }),
  columnHelper.accessor((row) => row.tanggal, {
    id: "tanggal",
    header: "Tanggal",
    cell: (info) => {
      const route = useRoute();
      return h("div", {
        class: "table-cell-medium",
        innerText: route.query.tanggal,
      });
    },
  }),
  columnHelper.accessor((row) => row.jenis, {
    id: "jenis",
    header: "Jenis",
    cell: (info) => {
      const value = info.getValue();
      return h("div", {
        class: `table-cell-medium ${
          value === "pengeluaran" ? "tw-text-red-600" : "tw-text-green-600"
        }`,
        innerText: value.charAt(0).toUpperCase() + value.slice(1),
      });
    },
  }),
  columnHelper.accessor((row) => row.nominal, {
    id: "nominal",
    header: "Nominal",
    cell: (info) => {
      return h("div", {
        class: "table-cell-medium",
        innerText: formatCurrencyAuto(info.getValue()),
      });
    },
  }),
  columnHelper.accessor((row) => row.pic, {
    id: "pic",
    header: "PIC",
    cell: (info) =>
      h("div", {
        class: "table-cell-medium",
        innerText: info.getValue(),
      }),
  }),
];
