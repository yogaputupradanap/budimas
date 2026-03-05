import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import Button from "../../components/ui/Button.vue";

const columnHelper = createColumnHelper();
export const principalColumns = [
  columnHelper.accessor((row) => row.no, {
    id: "No",
    cell: (info) =>
      h("div", {
        class: "tw-w-full tw-flex tw-justify-center",
        innerText: info.getValue(),
      }),
    header: () =>
      h("div", {
        class: "tw-w-full tw-flex tw-justify-center",
        innerText: "No",
      }),
  }),
  columnHelper.accessor("kodePrincipal", {
    cell: (info) => h("div", info.getValue()),
    header: () => h("span", { class: "tw-w-24", innerText: "kode principal" }),
  }),
  columnHelper.accessor((row) => row.namaPrincipal, {
    id: "namaPrincipal",
    cell: (info) => info.getValue(),
    header: () => h("span", { class: "tw-w-28", innerText: "nama principal" }),
  }),
  columnHelper.accessor((row) => row.status, {
    id: "status",
    cell: (info) => info.getValue(),
    header: () => "status",
  }),
  columnHelper.accessor((row) => row.status, {
    id: "status",
    cell: (info) => {
      const comparison = info.getValue() === "Sudah";
      const text = comparison ? "Done" : "Check In";
      const buttColor = comparison
        ? "tw-bg-green-500"
        : "tw-bg-gray-300 tw-text-gray-600";

      return h(
        "div",
        { class: "tw-w-full tw-flex tw-justify-center" },
        h(
          Button,
          {
            class: `tw-w-32 ${buttColor}`,
            fallbackUrl:
              "/kunjungan/daftar-kunjungan-toko/check-in-principal/dashboard-menu-kunjungan-toko",
          },
          () => text
        )
      );
    },
    header: () =>
      h("div", {
        class: "tw-w-full tw-flex tw-justify-center",
        innerText: "Actions",
      }),
  }),
];
