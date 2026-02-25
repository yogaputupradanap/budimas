import {trimText} from "@/src/lib/utils";
import {createColumnHelper} from "@tanstack/vue-table";
import {h} from "vue";
import {useRoute} from "vue-router";
import RouterButton from "@/src/components/ui/RouterButton.vue";

const columnHelper = createColumnHelper();

export const fakturRealisasi = [
  columnHelper.accessor((row) => row.no_faktur, {
    id: "faktur",
    cell: (info) =>
      h("div", {
        class: "tw-pl-2 table-cell-large tw-pr-4",
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
        class: "table-cell-small",
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
  columnHelper.display({
  id: "actions",
  cell: (info) => {
    const route = useRoute();

    const idRute = route.params.id_rute;
    const idSalesOrder = info.row.original?.id_sales_order;
    const idOrderBatch = info.row.original?.id_order_batch;

    const idArmada = route.query.id_armada;
    const idDriver = route.query.id_driver;
    const deliveringDate = route.query.delivering_date;
    

    if (!idSalesOrder && !idOrderBatch) {
      return h("span", "—");
    }

    let to = `/realisasi/faktur/${idRute}`;

    if (idOrderBatch) {
      to += `/${idOrderBatch}?id_order_batch=${idOrderBatch}&id_sales_order=${idSalesOrder}&id_armada=${idArmada}&id_driver=${idDriver}&delivering_date=${deliveringDate}`;
    } else {
      to += `/${idSalesOrder}?id_armada=${idArmada}&id_driver=${idDriver}&delivering_date=${deliveringDate}`;
    }

    return h(
      RouterButton,
      {
        to,
        class: "tw-w-24",
        icon: "mdi mdi-pencil",
      },
      () => "Detail"
    );
  },
}),
];
