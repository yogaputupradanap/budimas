import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import { parseCurrency } from "../../lib/utils";
import FlexBox from "../../components/ui/FlexBox.vue";

const columnHelper = createColumnHelper();
export const listNotaFakturColumns = [
  columnHelper.accessor((row) => row.no_faktur, {
    id: "notaFaktur",
    cell: (info) => {
      const noFaktur =
        info.getValue().length > 20
          ? info.getValue().substring(0, 18) + "..."
          : info.getValue();

      return h(FlexBox, {
        full: true,
        jusCenter: true,
        itCenter: true,
        title: info.getValue(),
        innerText: noFaktur,
      });
    },
    header: () =>
      h(FlexBox, {
        full: true,
        jusCenter: true,
        itCenter: true,
        innerText: "nota faktur",
      }),
  }),
  columnHelper.accessor((row) => row.total_penjualan, {
    id: "totalPenjualan",
    cell: (info) =>
      h(FlexBox, {
        full: true,
        jusCenter: true,
        itCenter: true,
        innerText: `Rp. ${parseCurrency(info.getValue())}`,
      }),
    header: () =>
      h(
        FlexBox,
        { full: true, jusCenter: true, itCenter: true },
        () => "jumlah"
      ),
  }),
  columnHelper.accessor((row) => row.status_faktur, {
    id: "status",
    cell: (info) => {
      const status_faktur = info.getValue();
      const status =
        status_faktur === 12
          ? "Lunas"
          : status_faktur === 11
          ? "Pending"
          : status_faktur === 10
          ? "Belum Bayar"
          : "Belum Bayar";

      return h(FlexBox, {
        full: true,
        jusCenter: true,
        itCenter: true,
        innerText: status,
      });
    },
    header: () =>
      h(
        FlexBox,
        { full: true, jusCenter: true, itCenter: true },
        () => "status"
      ),
  }),
];
