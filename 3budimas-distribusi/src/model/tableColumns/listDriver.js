import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import { parseCurrency } from "@/src/lib/utils";
import Button from "@/src/components/ui/Button.vue";
import { useDriver } from "@/src/store/driver";
const columnHelper = createColumnHelper();

export const listDriver = [
  columnHelper.display({
    id: "no",
    header: () => h("div", { class: "tw-w-10" }, "No"),
    cell: (info) => h("div", { class: "tw-w-10 tw-text-center" }, info.row.index + 1),
  }),
  columnHelper.accessor((row) => row.tanggal_berangkat, {
    id: "tanggal",
    header: () => h("div", { class: "tw-w-20" }, "Tanggal"),
    cell: (info) => h("div", { class: "tw-w-20 tw-text-center" }, info.getValue()),
  }),
  columnHelper.accessor((row) => row.nama_driver, {
    id: "nama driver",
    header: () => h("div", { class: "tw-w-20" }, "Nama Driver"),
    cell: (info) => h("div", { class: "tw-w-20 tw-text-center" }, info.getValue()),
  }),
  columnHelper.accessor((row) => row.uang_saku, {
    id: "uang saku",
    header: () => h("div", { class: "tw-w-20" }, "Uang Saku"),
    cell: (info) => h("div", { class: "tw-w-20 tw-text-center" }, 'Rp. ' + parseCurrency(info.getValue())),
  }),
  columnHelper.accessor((row) => row.total_pengeluran, {
    id: "total pengeluaran",
    header: () => h("div", { class: "tw-w-20" }, "Pengeluaran"),
    cell: (info) => h("div", { class: "tw-w-20 tw-text-center" },'Rp. ' + parseCurrency(info.getValue())),
  }),
  columnHelper.accessor((row) => row.sisa_uang, {
    id: "sisa uang",
    header: () => h("div", { class: "tw-w-20" }, "Sisa Uang"),
    cell: (info) => h("div", { class: "tw-w-20 tw-text-center" }, 'Rp. ' + parseCurrency(info.getValue())),
  }),
  columnHelper.accessor((row) => row.helper, {
    id: "helper",
    header: () => h("div", { class: "tw-w-20" }, "Helper"),
    cell: (info) => h("div", { class: "tw-w-20 tw-text-center" }, info.getValue()),
  }),
  columnHelper.display({
    id: "actions",
    header: () => h("div", { class: "tw-w-20" }, "Actions"),
    cell: (info) => {
      const driver = useDriver()
      const getinfoPengeluaran = async () => {
        await driver.getInfoPengeluaran(info.row.original?.id_info_driver)
      }
      return h(
        Button,
        {
          class: "tw-w-24",
          trigger: getinfoPengeluaran,
          fallbackUrl: `/driver/update-driver/${info.row.original.id_info_driver}`,
          icon: 'mdi mdi-pencil'
        },
        "Detail"
      );
    },
  }),
];
