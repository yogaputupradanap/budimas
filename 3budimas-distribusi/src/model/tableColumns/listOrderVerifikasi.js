import {createColumnHelper} from "@tanstack/vue-table";
import {h} from "vue";
import RouterButton from "@/src/components/ui/RouterButton.vue";
import {apiUrl, fetchWithAuth, parseCurrency} from "@/src/lib/utils";
import {$swal} from "@/src/components/ui/SweetAlert.vue";

const columnHelper = createColumnHelper();

export const listOrderVerifikasi = [
  columnHelper.accessor((row) => row.no_order, {
    id: "nota_order",
    cell: (info) =>
      h("span", {
        class: "table-cell-lg tw-pl-2",
        innerText: info.row.original.no_order,
      }),
    header: h("span", {
      class: "tw-pl-2",
      innerText: "No Order",
    }),
  }),
  columnHelper.accessor((row) => row.kode_customer, {
    id: "kode_customer",
    cell: (info) =>
      h("span", {
        class: "table-cell-medium",
        innerText: info.getValue(),
      }),
    header: "Kode Customer",
  }),
  columnHelper.accessor((row) => row.nama_customer, {
    id: "nama_customer",
    cell: (info) =>
      h("span", {
        class: "table-cell-lg",
        innerText: info.getValue(),
      }),
    header: "Nama Customer",
  }),
  columnHelper.accessor((row) => row.kode_principal, {
    id: "kode_principal",
    cell: (info) =>
      h("span", {
        class: "table-cell-small",
        innerText: info.getValue(),
      }),
    header: "Kode Principal",
  }),
  columnHelper.accessor((row) => row.nama_sales, {
    id: "nama_sales",
    cell: (info) =>
      h("span", {
        class: "table-cell-lg tw-pl-2",
        innerText: info.getValue(),
      }),
    header: h("span", {
      class: "tw-pl-2",
      innerText: "Nama Sales",
    }),
  }),
  columnHelper.accessor((row) => row.total_bayar, {
    id: "total_bayar",
    cell: (info) =>
      h("span", {
        class: "table-cell-medium",
        innerText: `Rp. ${parseCurrency(info.getValue())}`,
      }),
    header: "Total Bayar",
  }),
  columnHelper.accessor((row) => row.tanggal_order, {
    id: "tanggal_order",
    cell: (info) =>
      h("span", {
        class: "table-cell-medium",
        innerText: Array.isArray(info.getValue()) ? info.getValue()[0]: info.getValue(),
      }),
    header: "Tanggal Order",
  }),
  columnHelper.display({
    id: "action",
    cell: (info) => {
      const { id_sales_order, no_order,id_order_batch } = info.row.original;
      const tableState = info.table.getState();
      const currentPagination = tableState.pagination.pageIndex;
      let to = `/konfirmasi/detail/${Array.isArray(id_sales_order)? id_order_batch:id_sales_order}`
        if (id_order_batch) {
            to += `?id_order_batch=${id_order_batch}&id_sales_orders=${id_sales_order}`;
        }
      return h(
        "div",
        {
          class: "tw-flex tw-gap-2",
        },
        [
          h("button", {
            innerText: "Tolak",
            class:
              "tw-w-20 tw-px-3 tw-rounded-lg tw-py-1 tw-bg-red-500 hover:tw-bg-red-600 tw-text-white tw-rounded tw-text-sm tw-font-medium tw-transition-colors",
            onclick: async () => {
              try {
                const isConfirmed = await $swal.confirmTolak(
                  `Apakah Anda yakin ingin menolak order [${no_order}]?`
                );
                if (!isConfirmed) return;

                await fetchWithAuth(
                  "PATCH",
                  `${apiUrl}/api/distribusi/tolak-order`,
                  {
                    id_sales_order: String(id_sales_order),
                      id_order_batch: id_order_batch ? id_order_batch : undefined,
                  }
                );

                if (info.table.options.meta?.updateRow) {
                  info.table.options.meta.updateRow(
                    null,
                    null,
                    null,
                    "refreshData"
                  );
                }
                await $swal.success(`Order [${no_order}] berhasil ditolak!`);
              } catch (error) {
                await $swal.error(
                  error.message || "Terjadi kesalahan saat menolak order"
                );
              }
            },
          }),
          h(RouterButton, {
            innerText: "Detail",
            class: "tw-w-20 tw-bg-blue-500 hover:tw-bg-blue-600",
            to: to,
          }),
        ]
      );
    },
    header: "Actions",
  }),
];
