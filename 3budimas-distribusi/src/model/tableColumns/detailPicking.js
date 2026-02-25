import { createColumnHelper } from "@tanstack/vue-table";
const columnHelper = createColumnHelper();
import { h } from "vue";
import UnitConversionInput from "@/src/components/ui/table/UnitConversionInput.vue";

export const tableDetailPicking = [
  columnHelper.display({
    id: "no",
    cell: (info) =>
      h("span", {
        class: "tw-w-16 tw-flex tw-justify-center",
        innerText: info.row.index + 1,
      }),
    header: () =>
      h("span", { class: "tw-w-16 tw-text-center", innerText: "No" }),
  }),
  columnHelper.accessor((row) => row.no_order, {
    id: "no_order",
    cell: (info) =>
      h("div", {
        class: "table-cell-lg",
        innerText: info.getValue(),
      }),
    header: "no order",
  }),
  columnHelper.accessor((row) => row.nama_customer, {
    id: "nama_customer",
    cell: (info) =>
      h("div", {
        class: "table-cell-lg",
        innerText: info.getValue(),
      }),
    header: "Nama Toko",
  }),
  columnHelper.accessor((row) => row.total_in_pieces, {
    id: "total_in_pieces",
    cell: (info) => {
      return h("div", {
        class: "table-cell-small",
        innerText: info.getValue(),
      });
    },
    header: () =>
      h("span", {
        class: "table-cell-small",
        innerText: "Jumlah Order",
      }),
  }),
  columnHelper.display({
    id: "picking",
    header: "Jumlah Picked",
    cell: (info) => {
      const rowData = info.row.original;
      const produkInfo = rowData.produkInfo;
      const jumlahPicked = rowData.jumlah_picked || 0;

      // Konversi dari produkInfo
      const konversi1 = produkInfo?.konversi_1 || 1; // pieces
      const konversi2 = produkInfo?.konversi_2 || 1; // box
      const konversi3 = produkInfo?.konversi_3 || 1; // karton

      // Hitung nilai default dari jumlah_picked
      let remainingPieces = jumlahPicked;

      // Hitung karton terlebih dahulu
      const defaultKarton = Math.floor(remainingPieces / konversi3);
      remainingPieces = remainingPieces % konversi3;

      // Hitung box
      const defaultBox = Math.floor(remainingPieces / konversi2);
      remainingPieces = remainingPieces % konversi2;

      // Sisanya adalah pieces
      const defaultPieces = remainingPieces;

      return h(UnitConversionInput, {
        table: info.table,
        column: info.column.id,
        row: info.row.index,
        // Data konversi dari produkInfo
        konversi1: konversi1,
        konversi2: konversi2,
        konversi3: konversi3,
        // Nilai default dari jumlah_picked yang sudah dikonversi
        totalKarton: defaultKarton,
        totalBox: defaultBox,
        totalPieces: defaultPieces,
      });
    },
  }),
];
