import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import { useRouter } from "vue-router";
import RouterButton from "@/src/components/ui/RouterButton.vue";

const columnHelper = createColumnHelper();

export const tableRuteDanArmada = () => {
  return [
    columnHelper.accessor((row) => row.id, {
      id: "id",
      cell: (info) =>
        h("div", {
          class: "tw-w-10 tw-text-center",
          innerText: info.row.index + 1,
        }),
      header: h("span", { class: "tw-w-10", innerText: "No" }),
    }),
    columnHelper.accessor((row) => row.kode, {
      id: "kode",
      cell: (info) =>
        h("span", {
          class: "table-cell-small",
          innerText: info.getValue(),
        }),
      header: "Kode Rute",
    }),
    columnHelper.accessor((row) => row.nama_rute, {
      id: "nama",
      cell: (info) =>
        h("span", {
          class: "table-cell-medium",
          innerText: info.getValue(),
        }),
      header: "Rute",
    }),
    columnHelper.accessor((row) => row.jumlah_toko, {
      id: "jumlah_toko",
      cell: (info) =>
        h("span", {
          class: "table-cell-small",
          innerText: info.getValue(),
        }),
      header: "Total Toko",
    }),
    columnHelper.accessor((row) => row.jumlah_nota, {
      id: "jumlah_nota",
      cell: (info) =>
        h("span", {
          class: "table-cell-small",
          innerText: info.getValue(),
        }),
      header: "Total Nota",
    }),
    columnHelper.accessor((row) => row.kubikal, {
      id: "kubikal",
      cell: (info) =>
        h("span", {
          class: "table-cell-small",
          innerText: info.getValue(),
        }),
      header: "Kubikal",
    }),
    columnHelper.display({
      id: "action",
      header: "Action",
      cell: (info) => {
        return h(
          RouterButton,
          {
            to: `/jadwal/jadwal-dan-rute/armada/${info.row.original.id_rute}`,
            class: "tw-w-32",
            icon: "mdi mdi-truck",
          },
          "Pilih Armada"
        );
      },
    }),
  ];
};
