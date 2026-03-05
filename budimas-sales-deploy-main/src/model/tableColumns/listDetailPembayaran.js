import { formatCurrencyAuto } from "@/src/lib/utils";
import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";

const columnHelper = createColumnHelper();
// Helper function untuk menentukan status
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

// Helper function untuk mendapatkan tanggal setoran terbaru
const getTanggalSetoranDiterima = (tanggalArray, idSetoranArray) => {
  if (!tanggalArray || !idSetoranArray) return "-";

  // Filter tanggal yang tidak null
  const validTanggal = tanggalArray.filter((tanggal) => tanggal !== null);

  // Jika jumlah tanggal valid tidak sama dengan jumlah id_setoran, return kosong
  if (
    validTanggal.length !== idSetoranArray.filter((id) => id !== null).length
  ) {
    return "-";
  }

  // Jika semua tanggal sudah terisi, ambil yang terbaru
  if (validTanggal.length > 0) {
    return validTanggal.sort((a, b) => new Date(b) - new Date(a))[0];
  }

  return "-";
};

export const ListDetailPembayaranColumn = [
  columnHelper.accessor((row) => row.id, {
    id: "id",
    header: () => h("div", { class: "tw-pl-2", innerText: "No" }),
    cell: (info) =>
      h("div", { class: "tw-pl-2", innerText: info.row.index + 1 }),
  }),
  columnHelper.accessor((row) => row.tanggal_input, {
    id: "tanggal_input",
    header: () =>
      h("div", { class: "table-cell-medium", innerText: "Tanggal" }),
    cell: (info) =>
      h("div", { class: "table-cell-medium", innerText: info.getValue() }),
  }),
  columnHelper.accessor((row) => row.jumlah_setoran, {
    id: "jumlah_setoran",
    header: () =>
      h("div", { class: "table-cell-medium", innerText: "Nominal" }),
    cell: (info) =>
      h("div", {
        class: "table-cell-medium",
        innerText: formatCurrencyAuto(info.getValue()),
      }),
  }),
  columnHelper.accessor((row) => row.status_setoran, {
    id: "status_setoran",
    header: () => h("div", { class: "table-cell-medium", innerText: "Status" }),
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
  columnHelper.accessor((row) => row.tanggal_setoran_diterima, {
    id: "tanggal_setoran_diterima",
    header: () =>
      h("div", {
        class: "table-cell-medium",
        innerText: "Tanggal Diterima",
      }),
    cell: (info) => {
      const tanggal = getTanggalSetoranDiterima(
        info.getValue(),
        info.row.original.id_setoran
      );
      return h("div", { class: "table-cell-medium", innerText: tanggal });
    },
  }),
];
