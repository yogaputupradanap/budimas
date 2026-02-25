import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import Button from "@/src/components/ui/Button.vue";
import { parseCurrency } from "@/src/lib/utils";

const columnHelper = createColumnHelper();

export const listFakturColumn = [
  columnHelper.display({
    id: "no",
    header: () => h("div", { class: "tw-pl-3", innerText: "No" }),
    cell: (info) =>
      h("div", { class: "tw-pl-3", innerText: info.row.index + 1 }),
  }),
  columnHelper.accessor((row) => row.tanggal, {
    id: "tanggal",
    header: "Tanggal",
    cell: (info) =>
      h("div", {
        class: "table-cell-lg",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.accessor((row) => row.nama_customer, {
    id: "nama_customer",
    header: "Nama Customer",
    cell: (info) => {
      return h("div", {
        class: "table-cell-lg",
        innerText: info.getValue(),
      });
    },
  }),
  columnHelper.accessor((row) => row.no_faktur, {
    id: "no_faktur",
    header: "No Faktur",
    cell: (info) =>
      h("div", {
        class: "table-cell-lg",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.accessor((row) => row.tagihan, {
    id: "tagihan",
    header: "Tagihan",
    cell: (info) =>
      h("div", {
        class: "table-cell-medium",
        innerText: parseCurrency(info.getValue()),
      }),
  }),
  columnHelper.accessor((row) => row.setoran, {
    id: "setoran",
    header: "Setoran",
    cell: (info) =>
      h("div", {
        class: "table-cell-medium",
        innerText: parseCurrency(info.getValue()),
      }),
  }),
  // Kolom Diterima Kasir - VIEW untuk semua akses
  columnHelper.accessor((row) => row.setor_diterima_kasir, {
    id: "setor_diterima_kasir",
    header: "Diterima Kasir",
    cell: (info) =>
      h("div", {
        class: "table-cell-medium",
        innerText: parseCurrency(info.getValue() || 0),
      }),
  }),
  columnHelper.display({
    id: "selisih",
    header: "Selisih",
    cell: (info) => {
      const item = info.row.original;
      const diterimaKasir = item.setor_diterima_kasir || 0;
      const setoran = item.setoran || 0;
      const isLunas = diterimaKasir === setoran;

      return h("div", {
        class: `table-cell-medium tw-text-center ${
          !isLunas ? "tw-text-red-500" : "tw-text-green-500"
        }`,
        innerText: !isLunas ? "Ya" : "Tidak",
      });
    },
  }),
  // Kolom Input - hanya untuk kasir
  columnHelper.display({
    id: "input_terima",
    header: () => {
      // Header hanya tampil untuk kasir
      if (window.userStore?.hasAccess("kasir")) {
        return "Input Terima";
      }
      return null;
    },
    cell: (info) => {
      // Cek apakah user adalah kasir
      if (!window.userStore?.hasAccess("kasir")) {
        return null; // Tidak tampil untuk non-kasir
      }

      const item = info.row.original;
      const selisih = item.setoran - (item.setor_diterima_kasir || 0);

      return h("input", {
        type: "number",
        class: `form-control tw-w-32 tw-text-center ${
          selisih === 0 ? "tw-bg-gray-200" : ""
        }`,
        value: window.inputDiterimaKasir?.[item.id_setoran] || 0,
        max: selisih,
        min: 0,
        step: "0.01",
        disabled: selisih === 0, // Disabled jika selisih = 0
        onInput: (e) => {
          if (selisih === 0) return;

          let value = parseFloat(e.target.value) || 0;

          if (window.inputDiterimaKasir) {
            window.inputDiterimaKasir[item.id_setoran] = value;
          }
        },
      });
    },
  }),
  columnHelper.accessor((row) => row.status_pembayaran, {
    id: "status_pembayaran",
    header: "Status",
    cell: (info) => {
      const value = info.getValue();
      const statusColor = {
        lunas: "tw-text-green-500",
        "belum lunas": "tw-text-red-500",
      };

      return h("div", {
        class: `table-cell-medium ${statusColor[value]} tw-uppercase`,
        innerText: value,
      });
    },
  }),
  columnHelper.display({
    id: "actions",
    header: () => "actions",
    cell: ({ column, row, table }) => {
      const showModal = () =>
        table.options.meta.updateRow(
          row.original,
          row.index,
          column.id,
          "openRowModal"
        );

      return h(
        Button,
        {
          class: "tw-text-white tw-w-32 tw-py-2 tw-text-xs",
          icon: "mdi mdi-receipt-text-check-outline",
          trigger: showModal,
        },
        "Bukti Bayar"
      );
    },
  }),
];
