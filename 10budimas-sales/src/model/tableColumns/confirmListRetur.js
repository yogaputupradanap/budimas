import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";

const columnHelper = createColumnHelper();
export const confirmListReturColumns = [
  columnHelper.accessor((row) => row.produk.nama, {
    id: "produk",
    cell: (info) => {
      return h(
        "span",
        {
          class: "tw-w-full tw-flex tw-justify-center"
        },
        [
          h("span", {
            class: "tw-w-40 text-center",
            innerText: info.getValue()
          })
        ]
      );
    },
    header: () =>
      h("span", {
        class: "tw-w-full tw-flex tw-justify-center",
        innerText: "Produk"
      })
  }),
  columnHelper.accessor((row) => row.pieces_retur_bad || 0, {
    id: "uom1_bad",
    cell: (info) => {
      const value = info.getValue();

      return h(
        "div",
        {
          class:
            "tw-flex tw-flex-col tw-justify-center tw-items-center tw-gap-1"
        },
        [
          h("span", { innerText: value }),
          h("span", {
            innerText: "pieces",
            class: "tw-text-blue-400 tw-text-xs"
          })
        ]
      );
    },
    header: () =>
      h("span", {
        class: "tw-w-full tw-flex tw-justify-center",
        innerText: "UOM 1 Retur Bad"
      })
  }),
  columnHelper.accessor((row) => row.box_retur_bad || 0, {
    id: "uom2_bad",
    cell: (info) => {
      const value = info.getValue();
      return h(
        "div",
        {
          class:
            "tw-flex tw-flex-col tw-justify-center tw-items-center tw-gap-1"
        },
        [
          h("span", { innerText: value }),
          h("span", {
            innerText: "box",
            class: "tw-text-blue-400 tw-text-xs"
          })
        ]
      );
    },
    header: () =>
      h("span", {
        class: "tw-w-full tw-flex tw-justify-center",
        innerText: "UOM 2 Retur Bad"
      })
  }),
  columnHelper.accessor((row) => row.karton_retur_bad || 0, {
    id: "uom3_bad",
    cell: (info) => {
      const value = info.getValue();

      return h(
        "div",
        {
          class:
            "tw-flex tw-flex-col tw-justify-center tw-items-center tw-gap-1"
        },
        [
          h("span", { innerText: value }),
          h("span", {
            innerText: "karton",
            class: "tw-text-blue-400 tw-text-xs"
          })
        ]
      );
    },
    header: () =>
      h("div", {
        class: "tw-w-full tw-flex tw-justify-center",
        innerText: "UOM 3 Retur Bad"
      })
  }),
  columnHelper.accessor((row) => row.pieces_retur_good || 0, {
    id: "uom1_good",
    cell: (info) => {
      const value = info.getValue();

      return h(
        "div",
        {
          class:
            "tw-flex tw-flex-col tw-justify-center tw-items-center tw-gap-1"
        },
        [
          h("span", { innerText: value }),
          h("span", {
            innerText: "pieces",
            class: "tw-text-blue-400 tw-text-xs"
          })
        ]
      );
    },
    header: () =>
      h("span", {
        class: "tw-w-full tw-flex tw-justify-center",
        innerText: "UOM 1 Retur Good"
      })
  }),
  columnHelper.accessor((row) => row.box_retur_good || 0, {
    id: "uom2_good",
    cell: (info) => {
      const value = info.getValue();
      return h(
        "div",
        {
          class:
            "tw-flex tw-flex-col tw-justify-center tw-items-center tw-gap-1"
        },
        [
          h("span", { innerText: value }),
          h("span", {
            innerText: "box",
            class: "tw-text-blue-400 tw-text-xs"
          })
        ]
      );
    },
    header: () =>
      h("span", {
        class: "tw-w-full tw-flex tw-justify-center",
        innerText: "UOM 2 Retur Good"
      })
  }),
  columnHelper.accessor((row) => row.karton_retur_good || 0, {
    id: "uom3_good",
    cell: (info) => {
      const value = info.getValue();

      return h(
        "div",
        {
          class:
            "tw-flex tw-flex-col tw-justify-center tw-items-center tw-gap-1"
        },
        [
          h("span", { innerText: value }),
          h("span", {
            innerText: "karton",
            class: "tw-text-blue-400 tw-text-xs"
          })
        ]
      );
    },
    header: () =>
      h("div", {
        class: "tw-w-full tw-flex tw-justify-center",
        innerText: "UOM 3 Retur Good"
      })
  })
];
