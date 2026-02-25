import { createColumnHelper } from "@tanstack/vue-table";
import { h, ref } from "vue";
import { apiUrl, fetchWithAuth, parseCurrency } from "@/src/lib/utils";
import Button from "@/src/components/ui/Button.vue";
import { useAlert } from "@/src/store/alert";
import { $swal } from "@/src/components/ui/SweetAlert.vue";

const columnHelper = createColumnHelper();

function getPercentDiskon(row, diskonType) {
  const diskon = row[`percent_diskon_${diskonType}`];
  return diskon;
}

export const detailKonfirmasiVoucherColumn = [
  columnHelper.accessor((row) => row.kode, {
    id: "Kode Voucher",
    cell: (info) => {
      return h("div", { class: "tw-pl-4 tw-max-w-40" }, info.getValue());
    },
    header: h("div", { class: "tw-pl-4" }, "Voucher"),
  }),
  columnHelper.group({
    id: "disc",
    header: () =>
      h("div", {
        class: "tw-w-full tw-flex tw-justify-center",
        innerText: "Disc (%)",
      }),
    columns: [
      columnHelper.accessor((row) => row.harga_jual, {
        id: "disc2",
        cell: (info) => {
          const diskon = getPercentDiskon(info.row.original, 2);

          return h(
            "span",
            { class: "tw-pl-2 tw-text-center" },
            Math.round(diskon)
          );
        },
        header: h("div", { class: "tw-pl-2" }, "Disc 2"),
      }),
      columnHelper.accessor((row) => row.harga_jual, {
        id: "disc3",
        cell: (info) => {
          const diskon = getPercentDiskon(info.row.original, 3);
          return h("span", { class: "tw-pl-2" }, Math.round(diskon));
        },
        header: h("div", { class: "tw-pl-2" }, "Disc 3"),
      }),
    ],
  }),
  columnHelper.accessor((row) => row.nilai_diskon, {
    id: "total_discount",
    cell: (info) => {
      return h(
        "div",
        { class: "tw-pl-4" },
        "Rp. " + parseCurrency(info.getValue())
      );
    },
    header: h("div", { class: "tw-pl-4" }, "Jumlah Disc"),
  }),
  columnHelper.display({
    id: "actions",
    header: h("div", { class: "tw-pl-2", innerText: "Actions" }),
    cell: (info) => {
      const { row, column, table } = info;
      const disabled = ref(false);

      const declineVoucher = async () => {
        const alert = useAlert();
        const body = { ...info.row.original };

        try {
          await fetchWithAuth(
            "POST",
            `${apiUrl}/api/voucher/tolak-voucher`,
            body
          );

          disabled.value = true;
          table.options.meta.updateRow(
            info.row.original.id_draft_voucher_2,
            row.index,
            column.id,
            "removeRow"
          );
          $swal.success(
            `Berhasil melakukan decline pada voucher : ${body.kode}`
          );
        } catch (error) {
          $swal.error(error);
          console.log(error);
        }
      };

      return h(
        "div",
        {
          class: "tw-px-2",
        },
        [
          h(
            Button,
            {
              disabled: false,
              trigger: declineVoucher,
              class: "tw-bg-red-500 tw-text-white tw-w-32",
              icon: "mdi mdi-close",
            },
            "Tolak"
          ),
        ]
      );
    },
  }),
];
