import { h } from "vue";
import RouterButton from "@/src/components/ui/RouterButton.vue";
import T from "@/src/components/ui/table/T.vue";
import { parseCurrency } from "@/src/lib/utils";
import { createColumnHelper } from "@tanstack/vue-table";

const columnHelper = createColumnHelper();

export const listJurnalColumn = [
  columnHelper.accessor((row) => row.row_num, {
    id: "no",
    header: () => h("div", { class: "tw-pl-3", innerText: "No" }),
    cell: (info) => h(T, { innerText: info.getValue(), class: "tw-py-3 tw-px-4 tw-font-medium" }),
  }),

  columnHelper.accessor((row) => row.tgl_transaksi, {
    id: "tgl_transaksi",
    header: () => "Tanggal",
    cell: (info) => h("div", { class: "table-cell-medium", innerText: info.getValue() }),
  }),

  columnHelper.accessor((row) => row.nama_perusahaan, {
    id: "nama_perusahaan",
    header: () => "Perusahaan",
    cell: (info) => h("div", { class: "table-cell-lg", innerText: info.getValue() }),
  }),

  columnHelper.accessor((row) => row.nama_cabang, {
    id: "nama_cabang",
    header: () => "Cabang",
    cell: (info) => h("div", { class: "table-cell-lg", innerText: info.getValue() }),
  }),

  columnHelper.accessor((row) => row.id_jurnal, {
    id: "id_jurnal",
    header: () => "ID Jurnal",
    cell: (info) => h("div", { class: "table-cell-medium", innerText: info.getValue() }),
  }),

  columnHelper.display({
    id: "nama_akun",
    header: () => h("div", { class: "tw-pl-2", innerText: "Nama Akun" }),
    cell: (info) => {
      const detailJurnal = info.row.original.info_jurnal || [];
      const namaAkun1 = detailJurnal[0]?.nama_akun || "-";
      const namaAkun2 = detailJurnal[1]?.nama_akun || "-";

      return h("div", { class: "tw-cell-small tw-flex-col" }, [
        h("div", {
          class: "tw-w-full tw-border-b tw-border-gray-300 tw-pb-4 tw-pl-2",
          innerText: namaAkun1,
        }),
        h("div", {
          class: "tw-w-full tw-pt-4 tw-pl-2",
          innerText: namaAkun2,
        }),
      ]);
    },
  }),

  columnHelper.display({
    id: "jenis_transaksi",
    header: () => h("div", { class: "tw-pl-2", innerText: "Jenis transaksi" }),
    cell: (info) => {
      const detailJurnal = info.row.original.info_jurnal || [];
      const jenisTransaksi1 = detailJurnal[0]?.jenis_transaksi || "-";
      const jenisTransaksi2 = detailJurnal[1]?.jenis_transaksi || "-";

      return h("div", { class: "tw-cell-small tw-flex-col" }, [
        h("div", {
          class: "tw-w-full tw-border-b tw-border-gray-300 tw-pb-4 tw-pl-2",
          innerText: jenisTransaksi1,
        }),
        h("div", {
          class: "tw-w-full tw-pt-4 tw-pl-2",
          innerText: jenisTransaksi2,
        }),
      ]);
    },
  }),

  columnHelper.display({
    id: "debit",
    header: () => h("div", { class: "tw-pl-2", innerText: "Debit" }),
    cell: (info) => {
      const detailJurnal = info.row.original.info_jurnal || [];
      const debit1 = detailJurnal[0]?.debit;
      const debit2 = detailJurnal[1]?.debit;

      return h("div", { class: "tw-cell-small tw-flex-col tw-text-green-600 tw-font-semibold" }, [
        h("div", {
          class: "tw-w-full tw-border-b tw-border-gray-300 tw-pb-4 tw-pl-2 ",
          innerText: debit1 ? parseCurrency(debit1) : "-",
        }),
        h("div", {
          class: "tw-w-full tw-pt-4 tw-pl-2",
          innerText: debit2 ? parseCurrency(debit2) : "-",
        }),
      ]);
    },
  }),

  columnHelper.display({
    id: "kredit",
    header: () => h("div", { class: "tw-pl-2", innerText: "Kredit" }),
    cell: (info) => {
      const detailJurnal = info.row.original.info_jurnal || [];
      const kredit1 = detailJurnal[0]?.kredit;
      const kredit2 = detailJurnal[1]?.kredit;

      return h("div", { class: "tw-cell-small tw-flex-col tw-text-red-600 tw-font-semibold" }, [
        h("div", {
          class: "tw-w-full tw-border-b tw-border-gray-300 tw-pb-4 tw-pl-2",
          innerText: kredit1 ? parseCurrency(kredit1) : "-",
        }),
        h("div", {
          class: "tw-w-full tw-pt-4 tw-pl-2",
          innerText: kredit2 ? parseCurrency(kredit2) : "-",
        }),
      ]);
    },
  }),

  columnHelper.display({
    id: "action",
    header: () => h("div", { class: "tw-pl-2", innerText: "Action" }),
    cell: (info) => {
      const { id_jurnal } = info.row.original;
      return h("div", { class: "tw-px-4 tw-text-center " }, [
        h(
          RouterButton,
          {
            to: `/jurnal/detail-jurnal/${id_jurnal}`,
            class: "tw-px-4 tw-py-2 tw-bg-blue-500 tw-text-white tw-rounded-md hover:tw-bg-blue-600",
          },
          "Detail"
        ),
      ]);
    },
  }),
];
