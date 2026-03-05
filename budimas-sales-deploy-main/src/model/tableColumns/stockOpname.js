import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import TableInput from "@/src/components/ui/table/TableInput.vue";
import { usePrincipal } from "@/src/store/principal";

const columnHelper = createColumnHelper();
export const StockOpnameColumns = [
  columnHelper.accessor((row) => row.no, {
    id: "no",
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
  columnHelper.accessor((row) => row.nama, {
    id: "nama",
    cell: (info) => {
      const principal = usePrincipal();
      const { id } = info.row.original;

      const product = principal.principalProduct.products.find(
        (product) => product?.id === id
      );

      return h("div", { id, class: "tw-flex tw-flex-col tw-items-center" }, [
        h("span", { class: "tw-text-sm", innerText: info.getValue() }),
        h("span", {
          class: "tw-text-sm tw-text-blue-500",
          innerText: product?.kode_sku,
        }),
      ]);
    },
    header: () =>
      h("span", {
        class: "lg:tw-w-full tw-w-32 tw-text-center",
        innerText: "produk",
      }),
  }),
  columnHelper.display({
    id: "karton",
    cell: (info) => {
      const { id } = info.row.original;
      // Ambil nilai karton dari data asli row
      const kartonValue =
        info.row.original.karton !== undefined ? info.row.original.karton : "";

      return h("div", { class: "tw-flex tw-flex-col tw-items-center" }, [
        h("span", {
          class: "tw-text-blue-500 tw-text-sm",
          innerText: "karton",
        }),
        h(TableInput, {
          id: `${id}-karton`,
          table: info.table,
          column: info.column.id,
          row: info.row.index,
          initialValue: kartonValue,
          type: "number",
        }),
      ]);
    },
    header: () =>
      h("span", {
        class: "lg:tw-w-full tw-w-16 tw-text-center",
        innerText: "Jml. UOM 1",
      }),
  }),
  columnHelper.display({
    id: "box",
    cell: (info) => {
      const { id } = info.row.original;
      // Ambil nilai box dari data asli row
      const boxValue =
        info.row.original.box !== undefined ? info.row.original.box : "";

      return h("div", { class: "tw-flex tw-flex-col tw-items-center" }, [
        h("span", {
          class: "tw-text-blue-500 tw-text-sm",
          innerText: "box",
        }),
        h(TableInput, {
          id: `${id}-box`,
          table: info.table,
          column: info.column.id,
          row: info.row.index,
          initialValue: boxValue,
          type: "number",
        }),
      ]);
    },
    header: () =>
      h("span", {
        class: "lg:tw-w-full tw-w-32 tw-text-center",
        innerText: "Jml. UOM 2",
      }),
  }),
  columnHelper.display({
    id: "pieces",
    cell: (info) => {
      const { id } = info.row.original;
      // Ambil nilai pieces dari data asli row
      const piecesValue =
        info.row.original.pieces !== undefined ? info.row.original.pieces : "";

      return h("div", { class: "tw-flex tw-flex-col tw-items-center" }, [
        h("span", {
          class: "tw-text-blue-500 tw-text-sm",
          innerText: "pieces",
        }),
        h(TableInput, {
          id: `${id}-pieces`,
          table: info.table,
          column: info.column.id,
          row: info.row.index,
          initialValue: piecesValue,
          type: "number",
        }),
      ]);
    },
    header: () =>
      h("span", {
        class: "lg:tw-w-full tw-w-32 tw-text-center",
        innerText: "Jml. UOM 3",
      }),
  }),
];
