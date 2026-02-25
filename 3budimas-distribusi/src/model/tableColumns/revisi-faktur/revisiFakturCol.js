import { createColumnHelper } from "@tanstack/vue-table";
const columnHelper = createColumnHelper();
import { h } from "vue";
import RouterButton from "@/src/components/ui/RouterButton.vue";
import { useShipping } from "@/src/store/shipping";
import { useKepalaCabang } from "@/src/store/kepalaCabang";

export const revisiFakturCol = [
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
      h("div", { class: "table-cell-medium", innerText: info.getValue() }),
    header: "delivering date",
  }),
  columnHelper.accessor((row) => row.kode, {
    id: "route_code",
    cell: (info) =>
      h("div", { class: "table-cell-medium", innerText: info.getValue() }),
    header: "Kode Rute",
  }),
  columnHelper.accessor((row) => row.nama_rute, {
    id: "route",
    cell: (info) =>
      h("div", { class: "table-cell-medium", innerText: info.getValue() }),
    header: "Rute",
  }),
  columnHelper.accessor((row) => row.jumlah_toko, {
    id: "total_shop",
    cell: (info) =>
      h("div", { class: "table-cell-small", innerText: info.getValue() }),
    header: "Total Toko",
  }),
  columnHelper.accessor((row) => row.jumlah_nota, {
    id: "total_note",
    cell: (info) =>
      h("div", { class: "table-cell-small", innerText: info.getValue() }),
    header: "Total Nota",
  }),
  columnHelper.accessor((row) => row.kubikal, {
    id: "cubic",
    cell: (info) =>
      h("div", { class: "table-cell-small", innerText: info.getValue() }),
    header: "Kubikal",
  }),
  columnHelper.accessor((row) => row.nama_armada, {
    id: "armada",
    cell: (info) =>
      h("div", { class: "table-cell-medium", innerText: info.getValue() }),
    header: "Armada",
  }),
  columnHelper.accessor((row) => row.nama_driver, {
    id: "driver",
    cell: (info) =>
      h("div", { class: "table-cell-medium", innerText: info.getValue() }),
    header: "Driver",
  }),
  columnHelper.display({
    id: "actions",
    cell: (info) => {
      const shipping = useShipping();
      const kepalaCabang = useKepalaCabang();
      const idCabang = kepalaCabang.kepalaCabangUser.id_cabang;
      const idRute = info.row.original.id_rute;
      const idArmada = info.row.original.id_armada;
      const idDriver = info.row.original.id_driver;
      const deliveringDate = info.row.original.delivering_date;

      // const getListFaktur = async () => {
      //   await shipping.getListFakturShipping(
      //     idCabang,
      //     idRute,
      //     false,
      //     idArmada,
      //     idDriver,
      //     deliveringDate
      //   );
      // };

      return h(
        RouterButton,
        {
          class: "tw-w-24 tw-h-8",
          // trigger: getListFaktur,
          to: `/revisi-faktur/faktur/${idRute}?id_armada=${idArmada}&id_driver=${idDriver}&delivering_date=${deliveringDate}`,
          icon: "mdi mdi-pencil",
        },
        "Detail"
      );
    },
    header: "Action",
  }),
];
