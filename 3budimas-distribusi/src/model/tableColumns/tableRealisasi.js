import { createColumnHelper } from "@tanstack/vue-table";
const columnHelper = createColumnHelper();
import { h } from "vue";
import { useRouter } from "vue-router";
import RouterButton from "@/src/components/ui/RouterButton.vue";

export const tableRealisasi = [
  columnHelper.accessor((row) => row.id, {
    id: "id",
    cell: (info) => info.getValue(),
    header: "No",
  }),
  columnHelper.accessor((row) => row.faktur, {
    id: "faktur",
    cell: (info) => info.getValue(),
    header: "Faktur",
  }),
  columnHelper.accessor((row) => row.order_date, {
    id: "order_date",
    cell: (info) => info.getValue(),
    header: "Tgl Order",
  }),
  columnHelper.accessor((row) => row.customer, {
    id: "customer",
    cell: (info) => info.getValue(),
    header: "Customer",
  }),
  columnHelper.accessor((row) => row.cubical, {
    id: "cubical",
    cell: (info) => info.getValue(),
    header: "Kubikal",
  }),
  columnHelper.display({
    id: "action",
    header: "Action",
    cell: (info) => {
      const router = useRouter();
      const handleClick = () => {
        router.push("/realisasi/detail");
      };
      return h("button", {
        class: "tw-bg-blue-500 tw-h-8 tw-rounded-md tw-px-3",
        onClick: handleClick,
      });
    },
  }),
];
