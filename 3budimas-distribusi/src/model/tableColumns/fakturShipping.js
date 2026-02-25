import RouterButton from "@/src/components/ui/RouterButton.vue";
import {statusOrderText, trimText} from "@/src/lib/utils";
import {useShipping} from "@/src/store/shipping";
import {createColumnHelper} from "@tanstack/vue-table";
import {h} from "vue";
import {useRoute} from "vue-router";

const columnHelper = createColumnHelper();

export const fakturShipping = [
  columnHelper.display({
    id: "select",
    header: ({ table }) => {
      // Hitung total baris yang bisa diseleksi (bukan status_order = 10)
      const selectableRows = table
        .getRowModel()
        .rows.filter((row) => row.original.status_order !== 10);

      // Cek apakah semua baris yang bisa diseleksi sudah dipilih
      const allSelectableSelected =
        selectableRows.length > 0 &&
        selectableRows.every((row) => row.getIsSelected());

      return h("input", {
        type: "checkbox",
        checked: allSelectableSelected,
        onChange: (e) => {
          // Toggle hanya untuk baris yang bisa diseleksi
          selectableRows.forEach((row) => {
            row.toggleSelected(e.target.checked);
          });
        },
        class: "tw-w-4 tw-h-4 tw-rounded",
      });
    },
    cell: ({ row }) => {
      // Jika status_order = 10, jangan tampilkan checkbox
      if (row.original.status_order === 10) {
        return h("div", { class: "tw-w-4 tw-h-4" });
      }

      return h("input", {
        type: "checkbox",
        checked: row.getIsSelected(),
        onChange: row.getToggleSelectedHandler(),
        class: "tw-w-4 tw-h-4 tw-rounded",
      });
    },
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
  columnHelper.accessor((row) => row.status_order, {
    id: "status_order",
    cell: (info) =>
      h("div", {
        class: "tw-pl-2 table-cell-lg",
        innerText: statusOrderText(info.getValue()),
        title: info.getValue(),
      }),
    header: () => h("div", { class: "tw-pl-2", innerText: "status order" }),
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
  columnHelper.display({
    id: "actions",
    cell: (info) => {
      const shipping = useShipping();
      const router = useRoute();
      const idArmada = router.query.id_armada;
      const idDriver = router.query.id_driver;
      const deliveringDate = router.query.delivering_date;

      // const getDetailShipping = async () => {
      //   await shipping.getListDetailFakturShipping(
      //     info.row.original.id_sales_order
      //   );
      // };
        let to = `/shipping/faktur/${router.params.id_rute}/detail`;
        if (typeof info.row.original.id_sales_order === 'string') {

        const ids_sales_order = info.row.original.id_sales_order?.split(',');
        if (ids_sales_order.length > 1) {
          to += `/${ids_sales_order[0]}?id_order_batch=${info.row.original.id_order_batch}&id_armada=${idArmada}&id_driver=${idDriver}&delivering_date=${deliveringDate}&id_sales_orders=${info.row.original.id_sales_order}`;
        } else {
          to += `/${info.row.original.id_sales_order}?id_armada=${idArmada}&id_driver=${idDriver}&delivering_date=${deliveringDate}`;
        }
        } else {
            to += `/${info.row.original.id_sales_order}?id_armada=${idArmada}&id_driver=${idDriver}&delivering_date=${deliveringDate}`;
        }

      return h(
        RouterButton,
        {
          class: "tw-w-24 tw-h-8",
          // trigger: getDetailShipping,
          to:to,
          icon: "mdi mdi-pencil",
        },
        "Detail"
      );
    },
    header: "Actions",
  }),
];
