import RouterButton from "@/src/components/ui/RouterButton.vue";
import { formatRupiah } from "@/src/lib/utils";
import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";

const columnHelper = createColumnHelper();
export const listStockColumns = (nama_perusahaan, nama_cabang) => [
  columnHelper.accessor((row) => row.tanggal_update, {
    id: "tanggal",
    header: h("div", {
      class: "tw-pl-4 tw-w-20 md:tw-w-auto",
      innerText: "Tanggal",
    }),
    cell: (info) => h("div", { class: "tw-pl-4", innerText: info.getValue() }),
  }),
  columnHelper.accessor((row) => "row.kode_so", {
    id: "nama_perusahaan",
    header: "Perusahaan",
    cell: (info) =>
      h("div", { class: "tw-w-52 md:tw-w-auto", innerText: nama_perusahaan }),
  }),
  columnHelper.accessor((row) => "row.tanggal_so", {
    id: "nama_cabang",
    header: "Cabang",
    cell: (info) => h("div", { class: "tw-w-20 md:tw-w-auto", innerText: nama_cabang }),
  }),
  columnHelper.accessor((row) => row.nama_principal, {
    id: "nama_principal",
    header: "Principal",
    cell: (info) => h("div", { class: "tw-w-20 md:tw-w-auto", innerText: info.getValue() }),
  }),
  columnHelper.accessor((row) => row.sku, {
    id: "not incl1",
    header: "Kode SKU",
    cell: (info) => h("div", { class: "tw-w-44 md:tw-w-auto", innerText: info.getValue() }),
  }),
  columnHelper.accessor((row) => row.nama_produk, {
    id: "nama_produk",
    header: "Produk",
    cell: (info) => h("div", { class: "tw-w-44 md:tw-w-auto", innerText: info.getValue() }),
  }),
  columnHelper.accessor((row) => row.jumlah_good, {
    id: "summarized_data.ket_so",
    header: "Stock Akhir",
    cell: (info) => h("div", { class: "tw-w-44 md:tw-w-auto", innerText: info.getValue() }),
  }),
  columnHelper.accessor((row) => row.jumlah_incoming, {
    id: "summarized_data.status_so",
    header: "Stock In Transit",
    cell: (info) => h("div", { class: "tw-w-44 md:tw-w-auto", innerText: info.getValue() }),
  }),
  columnHelper.accessor((row) => row.uom, {
    id: "not incl2",
    header: "Satuan",
    cell: (info) => {
      return h("div", { class: "tw-w-44 md:tw-w-auto", innerText: info.getValue() });
    }
  }),
];
