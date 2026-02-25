import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import T from "@/src/components/ui/table/T.vue";
import Button from "@/src/components/ui/Button.vue";
import RouterButton from "@/src/components/ui/RouterButton.vue";

const columnHelper = createColumnHelper();

export const lphColumns = [
  columnHelper.display({
    id: "no",
    header: () => h("div", { class: "tw-pl-3" }, "No"),
    cell: (info) => h(T, { innerText: info.row.original.row_num }),
  }),
  columnHelper.accessor((row) => row.kode_lph, {
    id: "kode_lph",
    header: "Kode LPH",
    cell: (info) =>
      h("div", {
        class: "table-cell-lg",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.accessor((row) => row.nama_pencetak, {
    id: "nama_pencetak",
    header: "Nama Pencetak",
    cell: (info) => {
      return h("div", {
        class: "table-cell-medium",
        innerText: info.getValue(),
      });
    },
  }),
  columnHelper.accessor((row) => row.nama_sales, {
    id: "nama_sales",
    header: "Nama Sales",
    cell: (info) => {
      return h("div", {
        class: "table-cell-medium",
        innerText: info.getValue(),
      });
    },
  }),
  columnHelper.accessor((row) => row.tanggal_lph, {
    id: "tanggal_lph",
    header: "Tanggal LPH",
    cell: (info) => {
      return h("div", {
        class: "table-cell-medium",
        innerText: info.getValue(),
      });
    },
  }),
 columnHelper.display({
  id: "actions",
  header: "Action",
  cell: (info) => {
    // 1. Ambil ID dengan aman (gunakan fallback jika 'id' tidak ada)
    const id = info.row.original?.id;

    // Jika ID belum ada (saat loading atau data corrupt), tampilkan placeholder
    if (!id) return h('span', '...');

    return h(
      RouterButton,
      {
        to: `/lph/detail-lph/${id}`,
        class: "tw-px-4 tw-py-2 tw-bg-blue-500 tw-text-white tw-rounded-md hover:tw-bg-blue-600",
      },
      // 2. PERBAIKAN SLOT: Bungkus teks "Detail" dalam fungsi (object with default key)
      {
        default: () => "Detail"
      }
    );
  },
}),
];
