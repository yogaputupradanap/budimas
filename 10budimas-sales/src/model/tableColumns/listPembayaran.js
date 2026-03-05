import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import { parseCurrency, statusFakturText } from "../../lib/utils";
import RouterButton from "@/src/components/ui/RouterButton.vue";

const columnHelper = createColumnHelper();
export const ListPembayaranColumn = (openModal) => [
  columnHelper.accessor((row) => row.id_sales_order, {
    id: "id_sales_order",
    header: () => h("div", { class: "tw-pl-2", innerText: "No" }),
    cell: (info) =>
      h("div", { class: "tw-pl-2", innerText: info.row.index + 1 })
  }),
  columnHelper.accessor((row) => row.no_faktur, {
    id: "no_faktur",
    header: () =>
      h("div", { class: "table-cell-medium", innerText: "No. Faktur" }),
    cell: (info) =>
      h("div", { class: "table-cell-medium", innerText: info.getValue() })
  }),
  columnHelper.accessor((row) => row.total_penjualan - row.nominal_retur, {
    id: "total_penjualan",
    header: () =>
      h("div", { class: "table-cell-medium", innerText: "Total Tagihan" }),
    cell: (info) =>
      h("div", {
        class: "table-cell-medium",
        innerText: "Rp. " + parseCurrency(info.getValue())
      })
  }),
  columnHelper.accessor((row) => row.status_faktur, {
    id: "status_faktur",
    header: () => h("div", { class: "table-cell-medium", innerText: "Status" }),
    cell: (info) => {
      const status = info.getValue();

      return h("div", {
        class: "table-cell-medium",
        innerText: statusFakturText(status) || "Status Tidak Di Ketahui"
      });
    }
  }),
  columnHelper.accessor((row) => row.nominal_retur, {
    id: "nominal_retur",
    header: () => h("div", { class: "table-cell-medium", innerText: "Nominal Retur" }),
    cell: (info) => {
      const status = info.getValue();

      return h("div", {
        class: "table-cell-medium",
        innerText: "Rp. " + parseCurrency(info.getValue()) || "Rp. 0"
      });
    }
  }),
  columnHelper.accessor((row) => row.tanggal_jatuh_tempo, {
    id: "tanggal_jatuh_tempo",
    header: () =>
      h("div", { class: "table-cell-medium", innerText: "Jatuh Tempo" }),
    cell: (info) =>
      h("div", { class: "table-cell-small", innerText: info.getValue() })
  }),
  columnHelper.accessor((row) => row.jumlah_bayar, {
    id: "jumlah_bayar",
    header: () =>
      h("div", { class: "table-cell-medium", innerText: "Total Bayar" }),
    cell: (info) =>
      h("div", {
        class: "table-cell-medium",
        innerText: "Rp. " + parseCurrency(info.getValue())
      })
  }),
  columnHelper.display({
    id: "actions",
    cell: (info) => {
      const { id_sales_order, total_penjualan, jumlah_bayar, status_faktur, nominal_retur } =
        info.row.original;

      const url = `/kunjungan/daftar-kunjungan-toko/dashboard-menu-kunjungan-toko/pembayaran/detail-pembayaran/${id_sales_order}`;

      const isLunas =
        Number(jumlah_bayar.toFixed(3)) >= Number(total_penjualan.toFixed(3) - Number(nominal_retur.toFixed(3)));
      const checkStatus = status_faktur !== 2;


      console.log("jumlah bayar : ", Number(jumlah_bayar.toFixed(3)));
      console.log("total penjualan : ", Number(total_penjualan.toFixed(3)));

      const statusColor = {
        10: "tw-bg-gray-300 tw-text-black",
        12: "tw-bg-blue-500 tw-text-white"
      };

      // Tambahkan styling untuk disabled
      const getButtonClass = () => {
        if (checkStatus) {
          return "tw-bg-gray-200 tw-text-gray-600 tw-opacity-50";
        }
        return statusColor[status_faktur] || statusColor[10];
      };

      return h("div", { class: "tw-mx-4 tw-flex tw-items-center tw-gap-5" }, [
        h(RouterButton, {
          to: checkStatus ? undefined : url,
          innerText: isLunas ? "Lunas" : "Bayar",
          disabled: checkStatus,
          class: getButtonClass()
        }),
        h("button", {
          onClick: () => openModal(info.row.original),
          innerText: "Gunakan Retur",
          disabled: checkStatus,
          class: `${getButtonClass()} tw-px-2 tw-py-1 tw-rounded-lg hover:tw-bg-gray-500 hover:tw-text-white tw-transition-all tw-duration-200`
        })
      ]);
    },
    header: () =>
      h("div", {
        class: "tw-w-full tw-flex tw-justify-center",
        innerText: "Actions"
      })
  })
];
