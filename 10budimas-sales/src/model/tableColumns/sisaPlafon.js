import { parseCurrency } from "@/src/lib/utils";
import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";

const columnHelper = createColumnHelper();
export const sisaPlafonColumns = [
  columnHelper.accessor((row) => row.nama_principal, {
    id: "nama_principal",
    cell: (info) =>
      h("div", {
        class: "tw-w-28 lg:tw-w-full tw-flex tw-justify-center",
        innerText: info.getValue(),
      }),
    header: () =>
      h("div", {
        class: "tw-w-28 lg:tw-w-full tw-flex tw-justify-center",
        innerText: "Nama Principal",
      }),
  }),
  columnHelper.accessor((row) => row.limit_bon, {
    id: "limit_bon",
    cell: (info) => {
      const value = info.getValue();
      const sisaPlafon = value < 0 ? 0 : value;

      return h("div", {
        class: "tw-w-28 lg:tw-w-full tw-flex tw-justify-center",
        innerText: `Rp. ${parseCurrency(sisaPlafon)}`,
      });
    },
    header: () =>
      h("span", {
        class: "tw-w-28 lg:tw-w-full tw-flex tw-justify-center",
        innerText: "Sisa Plafon",
      }),
  }),
  columnHelper.accessor((row) => row.piutang, {
    id: "piutang",
    cell: (info) =>
      h("div", {
        class: "tw-w-28 lg:tw-w-full tw-flex tw-justify-center",
        innerText: `Rp. ${parseCurrency(info.getValue())}`,
      }),
    header: () =>
      h("span", {
        class: "tw-w-28 lg:tw-w-full tw-flex tw-justify-center",
        innerText: "Piutang",
      }),
  }),
];
