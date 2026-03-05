import { parseCurrency } from "@/src/lib/utils";
import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import { useAlert } from "@/src/store/alert";

const columnHelper = createColumnHelper();

export const listRekapPembayaran = [
  columnHelper.accessor((row) => row.id, {
    id: "id",
    header: () =>
      h("div", {
        class: "tw-pl-2 tw-w-[60px] tw-text-center tw-font-semibold",
        innerText: "No",
      }),
    cell: (info) =>
      h("div", {
        class: "tw-pl-2 tw-w-[60px] tw-text-center",
        innerText: info.row.index + 1,
      }),
  }),
  columnHelper.accessor((row) => row.no_faktur, {
    id: "no_faktur",
    header: () =>
      h("div", {
        class: "tw-w-auto tw-font-semibold",
        innerText: "No. Faktur",
      }),
    cell: (info) =>
      h("div", {
        class: "tw-w-auto truncate",
        innerText: `TW-12834732894`,
      }),
  }),
  columnHelper.accessor((row) => row.nama_customer, {
    id: "nama_customer",
    header: () =>
      h("div", {
        class: "tw-w-auto tw-font-semibold",
        innerText: "Nama Customer",
      }),
    cell: (info) =>
      h("div", {
        class: "tw-w-auto truncate",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.accessor((row) => row.tunai || 0, {
    id: "tunai",
    header: () =>
      h("div", {
        class: "tw-w-auto tw-font-semibold tw-text-center",
        innerText: "Setoran Tunai",
      }),
    cell: (info) => {
      const rowData = info.row.original;
      const totalSetoran = rowData.jumlah_setoran || 0;
      const alert = useAlert();

      if (rowData.tunai === undefined) rowData.tunai = 0;
      if (rowData.non_tunai === undefined) rowData.non_tunai = totalSetoran;
      if (rowData.hasError === undefined) rowData.hasError = false;

      return h("div", { class: "tw-flex tw-flex-col tw-w-[180px]" }, [
        h("input", {
          type: "number",
          value: rowData.tunai,
          class: `tw-w-full tw-px-2 tw-py-1 tw-border tw-rounded ${
            rowData.hasError
              ? "tw-border-red-500 tw-bg-red-50"
              : "tw-border-gray-300"
          }`,
          placeholder: "0",
          min: 0,
          max: totalSetoran,
          onInput: (e) => {
            const tunai = Number(e.target.value) || 0;
            if (tunai > totalSetoran) {
              alert.setMessage(
                `Tunai tidak boleh melebihi total setoran (Rp ${parseCurrency(
                  totalSetoran
                )})`,
                "warning"
              );
              e.target.value = totalSetoran;
              rowData.tunai = totalSetoran;
              rowData.non_tunai = 0;
              rowData.hasError = true;
              return;
            }
            rowData.tunai = tunai;
            rowData.non_tunai = Math.max(0, totalSetoran - tunai);
            rowData.hasError = false;
          },
        }),
        rowData.hasError
          ? h("span", {
              class: "tw-text-red-500 tw-text-xs tw-mt-1",
              innerText: `Maksimal: ${parseCurrency(totalSetoran)}`,
            })
          : null,
      ]);
    },
  }),
  columnHelper.accessor((row) => row.non_tunai || row.jumlah_setoran, {
    id: "non_tunai",
    header: () =>
      h("div", {
        class: "tw-w-auto tw-font-semibold tw-text-start",
        innerText: "Setoran Non Tunai",
      }),
    cell: (info) => {
      const rowData = info.row.original;
      return h("div", {
        class: "tw-w-auto tw-font-medium tw-text-start",
        innerText: parseCurrency(rowData.non_tunai || 0),
      });
    },
  }),
  columnHelper.accessor((row) => row.jumlah_setoran, {
    id: "jumlah_setoran",
    header: () =>
      h("div", {
        class: "tw-w-auto tw-font-semibold tw-text-start",
        innerText: "Total Nominal",
      }),
    cell: (info) =>
      h("div", {
        class: "tw-w-auto tw-font-bold tw-text-start",
        innerText: parseCurrency(info.getValue()),
      }),
  }),
];
