import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import { parseCurrency, simpleDateNow } from "@/src/lib/utils";
import T from "@/src/components/ui/table/T.vue";

const currentDate = new Date();
const columnHelper = createColumnHelper();

const getStatusSetoran = (statusArray) => {
  if (!statusArray || statusArray.every((status) => status === null)) {
    return "Pending";
  }
  if (statusArray.some((status) => status === null || status < 3)) {
    return "Pending";
  }
  if (statusArray.every((status) => status === 3)) {
    return "Diterima";
  }
  return "Pending";
};

export const listRiwayatPembayaranColumn = [
  columnHelper.display({
    id: "no",
    header: h("div", { class: "tw-pl-3", innerText: "No" }),
    cell: (info) => h(T, { innerText: info.row.index + 1 }),
  }),
  columnHelper.accessor((row) => row.tanggal_input, {
    id: "tanggal_order",
    header: h("div", { innerText: "Tanggal" }),
    cell: (info) =>
      h("div", {
        class: "table-cell-lg",
        innerText: simpleDateNow(currentDate),
      }),
  }),
  columnHelper.accessor((row) => row.nominal, {
    id: "nominal",
    header: h("div", { innerText: "Nominal" }),
    cell: (info) =>
      h("div", {
        class: "table-cell-lg",
        innerText: parseCurrency(info.getValue()),
      }),
  }),
    columnHelper.accessor((row) => row.status_setoran, {
    id: "status_setoran",
    header: h("div", { innerText: "Status" }),
    cell: (info) => {
      const status = getStatusSetoran(info.getValue());
      return h("div", {
        class: `table-cell-medium ${
          status === "Diterima" ? "text-green-600" : "text-yellow-600"
        }`,
        innerText: status,
      });
    },
  }),
  columnHelper.accessor((row) => row.tanggal_input, {
    id: "tanggal_diterima",
    header: h("div", { innerText: "Tanggal Diterima" }),
    cell: (info) =>
      h("div", {
        class: "table-cell-lg",
        innerText: simpleDateNow(info.getValue()),
      }),
  }),
];
