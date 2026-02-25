import { h } from "vue";
import T from "@/src/components/ui/table/T.vue";
import { parseCurrency } from "@/src/lib/utils";

export const listBukuBesarColumn = [
    {
        id: "no",
        header: "No",
        accessorKey: "row_num",
        meta: { text: "No" }, // Ini yang dicari ServerTable.vue line 32
        cell: (info) => h(T, { 
            innerText: info.row.original.row_num, 
            class: "tw-py-3 tw-px-4 tw-font-medium" 
        }),
    },
    {
        id: "tanggal",
        header: "Tanggal",
        accessorKey: "tanggal",
        meta: { text: "Tanggal" },
        cell: (info) => h("div", { class: "table-cell-medium", innerText: info.getValue() || "-" }),
    },
    {
  id: "nama_akun",
  header: "Akun",
  accessorKey: "nama_akun",
  meta: { text: "Akun" },
  cell: (info) => {
    const row = info.row.original;

    if (row.isParent) {
      return h("div", {
        class: "tw-bg-gray-100 tw-py-3 tw-px-4 tw-font-bold tw-text-gray-800 tw-rounded"
      }, [
        h("div", { class: "tw-text-xs tw-text-gray-500" }, row.nomor_akun || ""),
        h("div", { class: "tw-text-base" }, row.nama_akun || "-")
      ]);
    }

    return h("div", {
      class: "tw-flex tw-gap-3 tw-items-center tw-pl-8"
    }, [
      h("span", {
        class: "tw-text-gray-400 tw-w-24 tw-text-sm"
      }, row.nomor_akun || ""),
      h("span", {
        class: "tw-text-gray-700"
      }, row.nama_akun || "")
    ]);
  }
},
    {
        id: "keterangan",
        header: "Keterangan",
        accessorKey: "keterangan",
        meta: { text: "Keterangan" },
        cell: (info) => h("div", { 
            class: "table-cell-lg tw-min-w-[250px]", 
            innerText: info.getValue() || "-" 
        }),
    },
    {
        id: "debit",
        header: "Debit",
        accessorKey: "debit",
        meta: { text: "Debit" },
        cell: (info) => h("div", { 
            class: "table-cell-medium tw-text-green-600 tw-font-semibold tw-text-right", 
            innerText: parseCurrency(info.getValue() || 0) 
        }),
    },
    {
        id: "kredit",
        header: "Kredit",
        accessorKey: "kredit",
        meta: { text: "Kredit" },
        cell: (info) => h("div", { 
            class: "table-cell-medium tw-text-red-600 tw-font-semibold tw-text-right", 
            innerText: parseCurrency(info.getValue() || 0) 
        }),
    },
    {
        id: "saldo_kumulatif",
        header: "Saldo",
        accessorKey: "saldo_kumulatif",
        meta: { text: "Saldo" },
        cell: (info) => h("div", { 
            class: "table-cell-medium tw-font-bold tw-text-blue-700 tw-text-right", 
            innerText: parseCurrency(info.getValue() || 0) 
        }),
    },
    {
        id: "nama_perusahaan",
        header: "Perusahaan",
        accessorKey: "nama_perusahaan",
        meta: { text: "Perusahaan" },
        cell: (info) => h("div", { class: "table-cell-lg", innerText: info.getValue() || "-" }),
    }
];