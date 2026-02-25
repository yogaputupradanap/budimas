import { usePicking } from "@/src/store/picking";
import { createColumnHelper } from "@tanstack/vue-table";
const columnHelper = createColumnHelper();
import { h } from "vue";
import Button from "@/src/components/ui/Button.vue";
import { useKepalaCabang } from "@/src/store/kepalaCabang";

export const tableListPicking = [
  columnHelper.accessor((row) => row.id, {
    id: "id",
    cell: (info) =>
      h("span", {
        class: "tw-w-12 tw-flex tw-justify-center",
        innerText: info.row.index + 1,
      }),
    header: h("span", {
      class: "tw-w-12 tw-flex tw-justify-center",
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
    header: "Tanggal Kirim",
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
    id: "total_toko",
    cell: (info) =>
      h("span", {
        class: "table-cell-small",
        innerText: info.getValue(),
      }),
    header: "Total Toko",
  }),
  columnHelper.accessor((row) => row.jumlah_nota, {
    id: "total_nota",
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
    const picking = usePicking();
    const user = useKepalaCabang();
    const idCabang = user.kepalaCabangUser.id_cabang;

    const changeRoute = async () => {
      await picking.getListAddPicking(
        info.row.original.id_rute,
        idCabang,
        info.row.original.id_armada,
        info.row.original.id_driver,
        info.row.original.delivering_date
      );
    };
    

    return h(
      Button,
      {
        class: "tw-w-28 tw-h-8",
        trigger: changeRoute,
        fallbackUrl: `/picking/add-picking/${info.row.original.id_rute}?delivering_date=${info.row.original.delivering_date}&id_armada=${info.row.original.id_armada}&id_driver=${info.row.original.id_driver}`,
        icon: "mdi mdi-pencil",
      },
      {
        default: () => "Picking",
      }
    );
  },
  header: "Actions",
}),
];
