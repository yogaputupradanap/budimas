import RouterButton from "@/src/components/ui/RouterButton.vue";
import {trimText} from "@/src/lib/utils";
import {useShipping} from "@/src/store/shipping";
import {createColumnHelper} from "@tanstack/vue-table";
import {h} from "vue";
import {useRoute} from "vue-router";

const columnHelper = createColumnHelper();

export const listFakturCol = [
  columnHelper.display({
    id: "select",
    header: ({ table }) =>
      h("input", {
        type: "checkbox",
        checked: table.getIsAllRowsSelected(),
        onChange: table.getToggleAllRowsSelectedHandler(),
        class: "tw-w-4 tw-h-4 tw-rounded",
      }),
    cell: ({ row }) =>
      h("input", {
        type: "checkbox",
        checked: row.getIsSelected(),
        onChange: row.getToggleSelectedHandler(),
        class: "tw-w-4 tw-h-4 tw-rounded",
      }),
    enableSorting: false,
  }),
  columnHelper.accessor((row) => row.no_faktur, {
    id: "faktur",
    cell: (info) =>
      h("div", {
        class: "tw-pl-2 table-cell-lg",
        innerText: trimText(info.getValue(), 30),
        title: info.getValue(),
      }),
    header: () => h("div", { class: "tw-pl-2", innerText: "Faktur" }),
  }),
  columnHelper.accessor((row) => row.tanggal_order, {
    id: "rute",
    cell: (info) =>
      h("span", {
        class: "table-cell-small",
        innerText: info.getValue(),
      }),
    header: "Tanggal order",
  }),
  columnHelper.accessor((row) => row.nama_customer, {
    id: "customer",
    cell: (info) =>
      h("span", {
        class: "table-cell-medium",
        innerText: info.getValue(),
      }),
    header: "Customer",
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
  // columnHelper.display({
  //   id: "pembayaran_dropper",
  //   cell: (info) => {
  //     return h(
  //       "div",
  //       {
  //         class: "tw-flex tw-justify-start tw-items-center",
  //       },
  //       [
  //         h(BFormCheckbox, {
  //           modelValue: info.row.original.pembayaran_via_dropper || false,
  //           switch: true,
  //           size: "lg",
  //           class: "tw-scale-110",
  //           "onUpdate:modelValue": (value) => {
  //             // Update data di row
  //             info.row.original.pembayaran_via_dropper = value;
  //           },
  //         }),
  //       ]
  //     );
  //   },
  //   header: () =>
  //     h("div", {
  //       class: "tw-text-center",
  //       innerText: "Pembayaran COD",
  //     }),
  //   enableSorting: false,
  // }),
  columnHelper.display({
    id: "actions",
    cell: (info) => {
      const shipping = useShipping();
      const router = useRoute();
      const idArmada = router.query.id_armada;
      const idDriver = router.query.id_driver;
      const deliveringDate = router.query.delivering_date;
      let to = `/revisi-faktur/faktur/${router.params.id_rute}/detail`;
        if (info.row.original.id_order_batch) {
            to += `/${info.row.original.id_order_batch}?id_order_batch=${info.row.original.id_order_batch}&id_sales_order=${info.row.original.id_sales_order}&id_armada=${idArmada}&id_driver=${idDriver}&delivering_date=${deliveringDate}`;
        } else {
            to += `/${info.row.original.id_sales_order}?id_armada=${idArmada}&id_driver=${idDriver}&delivering_date=${deliveringDate}`;
        }

      return h(
        RouterButton,
        {
          class: "tw-w-24 tw-h-8",
          to: to,
          icon: "mdi mdi-pencil",
        },
        "Detail"
      );
    },
    header: "Actions",
  }),
];
