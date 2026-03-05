import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import { BButton } from "bootstrap-vue-next";
import { parseCurrency } from "../../lib/utils";

const columnHelper = createColumnHelper();
export const listReturColumns = [
  columnHelper.accessor((row) => row.no, {
    id: "no",
    cell: (info) => {
      return h("span", {
        class: "tw-w-full tw-flex tw-justify-center",
        innerText: info.row.index + 1
      });
    },
    header: () =>
      h("span", {
        class: "tw-w-full tw-flex tw-justify-center",
        innerText: "No"
      })
  }),
  columnHelper.accessor((row) => row.produk.id, {
    id: "produk",
    cell: (info) => {
      return h(
        "span",
        {
          class:
            "tw-w-full tw-flex tw-flex-col tw-justify-center tw-items-center"
        },
        [
          h("span", { innerText: info.row.original.produk.nama }),
          h("span", {
            class: "tw-text-xs tw-text-blue-500",
            innerText: info.row.original.produk.kode_sku
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
    id: "uom1_retur_bad",
    cell: (info) => {
      return h(
        "div",
        {
          class:
            "tw-flex tw-flex-col tw-justify-center tw-items-center tw-gap-1"
        },
        [
          h("span", { innerText: info.getValue() ? info.getValue() : 0 }),
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
    id: "uom2_retur_bad",
    cell: (info) => {
      return h(
        "div",
        {
          class:
            "tw-flex tw-flex-col tw-justify-center tw-items-center tw-gap-1"
        },
        [
          h("span", { innerText: info.getValue() ? info.getValue() : 0 }),
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
    id: "uom3_retur_bad",
    cell: (info) => {
      return h(
        "div",
        {
          class:
            "tw-flex tw-flex-col tw-justify-center tw-items-center tw-gap-1"
        },
        [
          h("span", { innerText: info.getValue() ? info.getValue() : 0 }),
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
    id: "uom1_retur_good",
    cell: (info) => {
      return h(
        "div",
        {
          class:
            "tw-flex tw-flex-col tw-justify-center tw-items-center tw-gap-1"
        },
        [
          h("span", { innerText: info.getValue() ? info.getValue() : 0 }),
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
    id: "uom2_retur_good",
    cell: (info) => {
      return h(
        "div",
        {
          class:
            "tw-flex tw-flex-col tw-justify-center tw-items-center tw-gap-1"
        },
        [
          h("span", { innerText: info.getValue() ? info.getValue() : 0 }),
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
    id: "uom3_retur_good",
    cell: (info) => {
      return h(
        "div",
        {
          class:
            "tw-flex tw-flex-col tw-justify-center tw-items-center tw-gap-1"
        },
        [
          h("span", { innerText: info.getValue() ? info.getValue() : 0 }),
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
  }),
  columnHelper.accessor((row) => row.produk.harga_jual, {
    id: "harga",
    cell: (info) => {
      return h("div", {
        class: "tw-flex tw-flex-col tw-justify-center tw-items-center tw-gap-2",
        innerText: `Rp. ${parseCurrency(info.getValue())}`
      });
    },
    header: () =>
      h("div", {
        class: "tw-w-full tw-flex tw-justify-center",
        innerText: "harga/UOM"
      })
  }),
  columnHelper.accessor((row) => row.pieces_delivered, {
    id: "uom1",
    cell: (info) => {
      return h(
        "div",
        {
          class:
            "tw-flex tw-flex-col tw-justify-center tw-items-center tw-gap-1"
        },
        [
          h("span", { innerText: info.getValue() ? info.getValue() : 0 }),
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
        innerText: "UOM 1 "
      })
  }),
  columnHelper.accessor((row) => row.box_delivered, {
    id: "uom2",
    cell: (info) => {
      console.log("box delivered : ", "ppp");
      return h(
        "div",
        {
          class:
            "tw-flex tw-flex-col tw-justify-center tw-items-center tw-gap-1"
        },
        [
          h("span", { innerText: info.getValue() ? info.getValue() : 0 }),
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
        innerText: "UOM 2 "
      })
  }),
  columnHelper.accessor((row) => row.karton_delivered, {
    id: "uom3",
    cell: (info) => {
      return h(
        "div",
        {
          class:
            "tw-flex tw-flex-col tw-justify-center tw-items-center tw-gap-1"
        },
        [
          h("span", { innerText: info.getValue() ? info.getValue() : 0 }),
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
        innerText: "UOM 3 "
      })
  }),
  columnHelper.accessor((row) => row.keteranganRetur, {
    id: "keteranganRetur",
    cell: (info) => {
      const value = info.getValue();
      return h("span", {
        title: value,
        class: "tw-w-full tw-flex tw-justify-center",
        innerText: value.length > 20 ? value.substring(0, 20) + "..." : value ? value : "-"
      });
    },
    header: () =>
      h("span", {
        class: "tw-w-full tw-flex tw-justify-center",
        innerText: "Keterangan"
      })
  }),
  columnHelper.display({
    id: "actions",
    header: () =>
      h("span", {
        class: "tw-w-full tw-flex tw-justify-center",
        innerText: "Actions"
      }),
    cell: ({ column, row, table }) => {
      const value = {
        pieces: row.getValue("uom1"),
        box: row.getValue("uom2"),
        karton: row.getValue("uom3"),
        namaProduk: row.original.produk.id
      };

      const openEditModal = () =>
        table.options.meta.updateRow(
          value,
          row.index,
          column.id,
          "openRowModal"
        );
      return h(
        "div",
        { class: "tw-w-full tw-flex tw-gap-2 tw-justify-center" },
        [
          h(
            BButton,
            { onClick: openEditModal, size: "sm", class: "tw-bg-blue-500" },
            () => h("i", { class: "mdi mdi-pencil" })
          )
        ]
      );
    }
  })
];
