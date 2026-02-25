import { createColumnHelper } from "@tanstack/vue-table";
import { h, ref } from "vue";
import { apiUrl, fetchWithAuth, parseCurrency } from "@/src/lib/utils";
import { getVoucherDiscount } from "@/src/lib/utils";
import Button from "@/src/components/ui/Button.vue";
import { useAlert } from "@/src/store/alert";

const columnHelper = createColumnHelper();

export const detailKonfirmasiVoucherRegularColumn = [
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
      columnHelper.accessor((row) => row.id, {
        id: "disc1",
        cell: (info) => {
          const { draft_voucher_detail } = info.row.original;

          return h("span", { class: "tw-pl-2 tw-text-center" }, draft_voucher_detail[0]?.discount);
        },
        header: h("div", { class: "tw-pl-2" }, "Disc 1"),
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
            `${apiUrl}/api/voucher/tolak-voucher-regular`,
            body
          );

          disabled.value = true;
          table.options.meta.updateRow(
            info.row.original.id,
            row.index,
            column.id,
            "removeRow"
          );
          
          alert.setMessage(
            `Berhasil melakukan penolakan pada voucher : ${body.kode}`,
            "success"
          );
        } catch (error) {
          alert.setMessage(error, "danger");
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
