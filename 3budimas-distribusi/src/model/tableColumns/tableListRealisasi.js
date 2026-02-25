import { createColumnHelper } from "@tanstack/vue-table";
const columnHelper = createColumnHelper();
import { h } from "vue";
import RouterButton from "@/src/components/ui/RouterButton.vue";

export const tableListRealisasi = [
  columnHelper.accessor((row) => row.id, {
    id: "id",
    cell: (info) =>
      h("span", {
        class: "tw-w-10 tw-flex tw-justify-center",
        innerText: info.row.index + 1,
      }),
    header: () =>
      h("span", {
        class: "tw-w-10 tw-flex tw-justify-center",
        innerText: "No",
      }),
  }),

  columnHelper.accessor((row) => row.delivering_date, {
    id: "delivering_date",
    cell: (info) =>
      h("span", {
        class: "table-cell-small",
        innerText: info.getValue(),
      }),
    header: "delivering date",
  }),
  columnHelper.accessor((row) => row.kode, {
    id: "route_code",
    cell: (info) =>
      h("span", {
        class: "table-cell-small",
        innerText: info.getValue(),
      }),
    header: "Kode Rute",
  }),
  columnHelper.accessor((row) => row.nama_rute, {
    id: "route",
    cell: (info) =>
      h("span", {
        class: "table-cell-medium",
        innerText: info.getValue(),
      }),
    header: "Rute",
  }),
  columnHelper.accessor((row) => row.jumlah_toko, {
    id: "total_shop",
    cell: (info) =>
      h("span", {
        class: "table-cell-small",
        innerText: info.getValue(),
      }),
    header: "Total Toko",
  }),
  columnHelper.accessor((row) => row.jumlah_nota, {
    id: "total_note",
    cell: (info) =>
      h("span", {
        class: "table-cell-small",
        innerText: info.getValue(),
      }),
    header: "Total Nota",
  }),
  columnHelper.accessor((row) => row.kubikal, {
    id: "cubic",
    cell: (info) =>
      h("span", {
        class: "table-cell-small",
        innerText: info.getValue(),
      }),
    header: "Kubikal",
  }),
  columnHelper.accessor((row) => row.nama_armada, {
    id: "armada",
    cell: (info) =>
      h("span", {
        class: "table-cell-small",
        innerText: info.getValue(),
      }),
    header: "Armada",
  }),
  columnHelper.accessor((row) => row.nama_driver, {
    id: "driver",
    cell: (info) =>
      h("span", {
        class: "table-cell-small",
        innerText: info.getValue(),
      }),
    header: "Driver",
  }),
  columnHelper.display({
    id: "actions",
    cell: (info) => {
      const idRute = info.row.original.id_rute;
      const idArmada = info.row.original.id_armada;
      const idDriver = info.row.original.id_driver;
      const deliveringDate = info.row.original.delivering_date;
      return h(
        RouterButton,
        {
          to: `/realisasi/faktur/${idRute}?id_armada=${idArmada}&id_driver=${idDriver}&delivering_date=${deliveringDate}`,
          class: "tw-w-24",
          icon: "mdi mdi-pencil",
        },
        () => "Detail"
      );
    },
    header: "Action",
  }),
];
