import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import RouterButton from "@/src/components/ui/RouterButton.vue";
import { useStatusPengiriman } from "@/src/store/mainStore";
const columnHelper = createColumnHelper();
import { status as statuses } from "@/src/lib/utils";

export const listStatusPengirimanColumn = [
  columnHelper.accessor((row) => row.nota_stock_transfer, {
    id: "nota",
    header: h("div", { class: "tw-pl-4", innerText: "Nota" }),
    cell: (info) =>
      h("div", {
        class: "table-cell-lg tw-pl-4",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.accessor((row) => row.created_at, {
    id: "created_at",
    header: "Tanggal",
    cell: (info) =>
      h("div", {
        class: "table-cell-medium",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.accessor((row) => row.nama_cabang_awal, {
    id: "cabang_awal",
    header: "Cabang Awal",
    cell: (info) =>
      h("div", {
        class: "table-cell-medium",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.accessor((row) => row.nama_cabang_tujuan, {
    id: "cabang_tujuan",
    header: "Cabang Tujuan",
    cell: (info) =>
      h("div", {
        class: "table-cell-medium",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.accessor((row) => row.jumlah, {
    id: "jumlah_produk",
    header: "Jumlah Produk",
    cell: (info) => {
      const status = info.row.original.status;

      const jumlah = info.row.original.jumlah;
      const jumlahPicked = info.row.original.jumlah_picked;
      const jumlahDiterima = info.row.original.jumlah_diterima;
      const jumlahDitolak = info.row.original.jumlah_ditolak;

      const value =
        status === statuses["picked"] ||
        status === statuses["konfirmasi"] ||
        status === statuses["pengiriman"]
          ? jumlahPicked
          : status === statuses["diterima"] ||
            status === statuses["eskalasi closed"]
          ? jumlahDiterima
          : status === statuses["tolak diterima"]
          ? jumlahDitolak
          : jumlah;

      return h("div", {
        class: "table-cell-medium",
        innerText: value,
      });
    },
  }),
  columnHelper.accessor((row) => row.status, {
    id: "status",
    header: "Status",
    cell: (info) => {
      const stockTransfer = useStatusPengiriman();
      const value = info.getValue();
      const statusEntries = Object.entries(stockTransfer.status);
      const statusArr = statusEntries.find((val) => val[1] === value);
      return h("div", {
        class: "table-cell-medium",
        innerText: statusArr ? statusArr[0] : "Status tidak diketahui",
      });
    },
  }),
  columnHelper.display({
    id: "actions",
    header: "Action",
    cell: (info) => {
      const id = info.row.original.id_stock_transfer;
      return h(
        RouterButton,
        {
          to: `/status-pengiriman/detail/${id}`,
          class: "tw-text-white tw-w-24",
        },
        () => "Detail"
      );
    },
  }),
];
