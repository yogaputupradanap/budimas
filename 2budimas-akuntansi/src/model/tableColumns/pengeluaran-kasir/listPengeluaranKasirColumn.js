import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import RouterButton from "@/src/components/ui/RouterButton.vue";
import T from "@/src/components/ui/table/T.vue";
import { formatCurrencyAuto, statusPengeluaranList } from "@/src/lib/utils";
import Button from "@/src/components/ui/Button.vue";

const columnHelper = createColumnHelper();

export const listPengeluaranKasirColumn = [
  columnHelper.display({
    id: "no",
    header: () => h("div", { class: "tw-pl-3" }, "No"),
    cell: (info) => h(T, { innerText: info.row.original.row_num }),
  }),
  columnHelper.accessor((row) => row.no_pengeluaran, {
    id: "no_pengeluaran",
    header: "No Pengeluaran",
    cell: (info) =>
      h("div", {
        class: "table-cell-lg",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.accessor((row) => row.pic, {
    id: "pic",
    header: "PIC",
    cell: (info) => {
      return h("div", {
        class: "table-cell-medium",
        innerText: info.getValue(),
      });
    },
  }),
  columnHelper.accessor((row) => row.tanggal_pengajuan, {
    id: "tanggal_pengajuan",
    header: "Tanggal Pengajuan",
    cell: (info) => {
      return h("div", {
        class: "table-cell-medium",
        innerText: info.getValue(),
      });
    },
  }),
  columnHelper.accessor((row) => row.tanggal_diberikan, {
    id: "tanggal_diberikan",
    header: "Tanggal Diberikan",
    cell: (info) => {
      return h("div", {
        class: "table-cell-medium",
        innerText: info.getValue(),
      });
    },
  }),
  columnHelper.accessor((row) => row.keterangan_pengeluaran, {
    id: "keterangan_pengeluaran",
    header: "Keterangan",
    cell: (info) => {
      return h("div", {
        class: "table-cell-lg",
        innerText: info.getValue(),
      });
    },
  }),
  columnHelper.accessor((row) => row.jumlah_pengeluaran, {
    id: "jumlah_pengeluaran",
    header: "Nominal Pengajuan",
    cell: (info) => {
      return h("div", {
        class: "table-cell-medium",
        innerText: formatCurrencyAuto(info.getValue()),
      });
    },
  }),
  columnHelper.accessor((row) => row.jumlah_acc, {
    id: "jumlah_acc",
    header: "Nominal disetujui",
    cell: (info) => {
      return h("div", {
        class: "table-cell-medium",
        innerText: formatCurrencyAuto(info.getValue()),
      });
    },
  }),
  columnHelper.accessor((row) => row.status_pengeluaran, {
    id: "status_pengeluaran",
    header: "Status",
    cell: (info) => {
      const value = info.getValue();
      const statusItem = statusPengeluaranList.find(
        (item) => item.value === value
      );
      const statusColors = {
        0: "tw-bg-yellow-600",
        1: "tw-bg-green-600",
        2: "tw-bg-red-500",
        3: "tw-bg-blue-600",
      };

      const statusText = statusItem?.name || "Unknown";
      const statusColor = statusColors[value] || "tw-bg-gray-500";

      return h(
        "div",
        {
          class: "table-cell-medium",
        },
        [
          h("span", {
            class: `tw-px-4 tw-py-1 tw-text-white tw-font-medium tw-rounded-md ${statusColor}`,
            innerText: statusText,
          }),
        ]
      );
    },
  }),
  columnHelper.display({
    id: "actions",
    header: "Action",
    cell: (info) => {
      const { id, status_pengeluaran } = info.row.original;
      const isDisabled = status_pengeluaran !== 1;

      return h(
        Button,
        {
          class: isDisabled
            ? "tw-px-4 tw-py-1 tw-bg-gray-400 tw-cursor-not-allowed"
            : "tw-px-4 tw-py-1 tw-bg-blue-500 hover:tw-bg-blue-700",
          disabled: isDisabled,
          trigger: isDisabled
            ? () => {}
            : () => {
                info.table.options.meta?.updateRow(
                  id,
                  info.row.index,
                  "konfirmasi",
                  "customAction"
                );
              },
        },
        {
          default: () => "Konfirmasi",
        }
      );
    },
  }),
];
