import { createColumnHelper } from "@tanstack/vue-table";
import Button from "@/src/components/ui/Button.vue";
import TableInput from "@/src/components/ui/table/TableInput.vue";
import { h } from "vue";
import UnitConversionInput from "@/src/components/ui/table/UnitConversionInput.vue";
const columnHelper = createColumnHelper();

export const tableRealisasiDetail = [
  columnHelper.accessor((row) => row.id_order_detail, {
    id: "id",
    cell: (info) =>
      h("span", {
        class: "tw-w-16 tw-flex tw-justify-center",
        innerText: info.row.index + 1,
      }),
    header: () =>
      h("span", {
        class: "tw-w-16 tw-flex tw-justify-center",
        innerText: "No",
      }),
  }),
  columnHelper.accessor((row) => row.nama_produk, {
    id: "product",
    cell: (info) => {
      return h(
        "div",
        {
          class:
            "tw-w-56 tw-flex tw-flex-col tw-justify-center tw-items-center tw-gap-1",
        },
        [
          h("span", {
            class: "tw-font-medium tw-text-xs",
            innerText: info.row.original.nama_produk,
          }),
          h("span", {
            class: "tw-text-xs tw-text-blue-400",
            innerText: info.row.original.kode_sku,
          }),
        ]
      );
    },
    header: h("span", {
      class: "tw-w-56 tw-flex tw-flex-col tw-justify-center tw-items-center",
      innerText: "Produk",
    }),
  }),
  columnHelper.accessor((row) => row.puom1_nama, {
    id: "satuan",
    cell: (info) =>
      h("span", {
        class: "tw-w-32 tw-flex tw-justify-center",
        innerText: info.getValue() || "pieces",
      }),
    header: () =>
      h("span", { class: "tw-w-32 tw-text-center", innerText: "Satuan" }),
  }),
  columnHelper.accessor((row) => row.jumlah_picked, {
    id: "total_picked",
    cell: (info) => {
      return h("span", {
        class: "tw-w-24 tw-flex tw-justify-center",
        innerText: info.getValue(),
      });
    },
    header: () =>
      h("span", {
        class: "tw-w-24 tw-text-center",
        innerText: "Jumlah Picked",
      }),
  }),
  columnHelper.accessor((row) => row.realisasi, {
    id: "realisasi",
    header: () =>
      h("span", {
        class: "tw-text-center",
        innerText: "Jumlah Realisasi",
      }),
    cell: (info) => {
      return h(UnitConversionInput, {
        table: info.table,
        column: info.column.id,
        row: info.row.index,
        initialValue: info.getValue(),
        konversi1: info.row.original.konversi_level1,
        konversi2: info.row.original.konversi_level2,
        konversi3: info.row.original.konversi_level3,
        totalKarton: info.row.original.total_karton,
        totalBox: info.row.original.total_box,
        totalPieces: info.row.original.total_pieces,
      });
    },
  }),
  columnHelper.accessor(
    (row) => ({
      karton: row.karton_shipped,
      box: row.box_shipped,
      pieces: row.pieces_shipped,
    }),
    {
      id: "keterangan",
      cell: (info) => {
        const { karton, box, pieces } = info.getValue();
        return h("div", {
          innerText: `Dikirim : ${karton} Karton, ${box} Box, ${pieces} Pieces`,
          class: "table-cell-medium",
        });
      },
      header: "Keterangan",
    }
  ),
];
