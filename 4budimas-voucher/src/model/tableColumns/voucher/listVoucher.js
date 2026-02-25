import RouterButton from "@/src/components/ui/RouterButton.vue";
import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import Button from "@/src/components/ui/Button.vue";
import { parseCurrency } from "@/src/lib/utils";
import { useRoute } from "vue-router";
import Swal from "sweetalert2";
import { voucherService } from "@/src/services/voucher";
import { useAlert } from "@/src/store/alert";

const columnHelper = createColumnHelper();

export const listVoucher = [
  columnHelper.display({
    id: "action",
    header: () => "Action",
    cell: (info) => {
      const route = useRoute();
      const { nama_voucher, id, kode_voucher } = info.row.original;
      const tipeVoucher = route.name.split(" ").at(-1);
      const alert = useAlert();

      const voucherRoute = `voucher-${tipeVoucher}/edit-voucher-${tipeVoucher}`;
      const param = new URLSearchParams();
      param.append("id", id);

      const url = `${voucherRoute}?${param.toString()}`;

      function copyKodeVoucher() {
        navigator.clipboard.writeText(kode_voucher);

        alert.setMessage(
          `"${kode_voucher}" Disalin`,
          "info",
        );
      }

      function removeRow() {
        info.table.options.meta.removeRow("id", id);
      }

      function deleteRow() {
        Swal.fire({
          title: `Apa kamu yakin ?`,
          html: `Kamu akan menghapus voucher : <br> <strong style="color: red;">${nama_voucher}</strong>`,
          icon: "warning",
          showCancelButton: true,
          confirmButtonColor: "#3085d6",
          cancelButtonColor: "#d33",
          confirmButtonText: "Hapus",
          cancelButtonText: "Batal",
        }).then(async (result) => {
          if (result.isConfirmed) {
            Swal.fire({
              title: "Menghapus Data ....",
              html: `Sistem sedang menghapus voucher : <br> <strong style="color: red;">${nama_voucher}</strong>`,
              didOpen: async () => {
                try {
                  Swal.showLoading();
                  await voucherService.deleteVoucher(id, tipeVoucher);
                  removeRow();

                  alert.setMessage(
                    `Sukses menghapus voucher : ${nama_voucher}`,
                    "success"
                  );
                } catch (error) {
                  console.log(error);
                  alert.setMessage("error", "danger");
                } finally {
                  Swal.close();
                }
              },
            });
          }
        });
      }

      return h("div", { class: "tw-flex tw-gap-2" }, [
        h(RouterButton, {
          title: "Edit",
          icon: "mdi mdi-pencil",
          to: url,
          class: "tw-text-xl",
        }),
        h(Button, {
          trigger: copyKodeVoucher,
          title: "Copy kode voucher",
          icon: "mdi mdi-clipboard",
          class: "tw-bg-gray-400 tw-text-xl",
        }),
        h(Button, {
          trigger: deleteRow,
          title: "Delete",
          icon: "mdi mdi-delete",
          class: "tw-bg-red-600 tw-text-xl",
        }),
      ]);
    },
  }),
  columnHelper.display({
    id: "row_num",
    header: () => h("div", { class: "tw-pl-4", textContent: "No" }),
    cell: (info) => {
      return h("div", {
        textContent: info.row.original.row_num,
        class: "table-cell-small tw-pl-4",
      });
    },
  }),
  columnHelper.accessor((row) => row.nama_voucher, {
    id: "nama_voucher",
    header: () => "Nama Voucher",
    cell: (info) => {
      return h("div", {
        textContent: info.getValue(),
        class: "table-cell-lg",
      });
    },
  }),
  columnHelper.accessor((row) => row.kode_principal, {
    id: "principal.kode",
    header: () => "Kode Principal",
    cell: (info) => {
      return h("div", {
        textContent: info.getValue(),
        class: "table-cell-medium",
      });
    },
  }),
  columnHelper.accessor((row) => row.nama_principal, {
    id: "principal.nama",
    header: () => "Principal",
    cell: (info) => {
      return h("div", {
        textContent: info.getValue(),
        class: "table-cell-lg",
      });
    },
  }),
  columnHelper.accessor((row) => row.kode_voucher, {
    id: "kode_voucher",
    header: () => "Kode Voucher",
    cell: (info) => {
      return h("div", {
        textContent: info.getValue(),
        class: "table-cell-medium",
      });
    },
  }),
  columnHelper.accessor((row) => row.tanggal_mulai, {
    id: "tanggal_mulai",
    header: () => "Tgl Berlaku",
    cell: (info) => {
      return h("div", {
        textContent: info.getValue() || "-",
        class: "table-cell-medium",
      });
    },
  }),
  columnHelper.accessor((row) => row.tanggal_kadaluarsa, {
    id: "tanggal_kadaluarsa",
    header: () => "Tgl Berakhir",
    cell: (info) => {
      return h("div", {
        textContent: info.getValue() || "-",
        class: "table-cell-medium",
      });
    },
  })
];

export const listVoucher1 = [
  columnHelper.display({
    id: "action",
    header: () => "Action",
    cell: (info) => {
      const route = useRoute();
      const { nama_voucher, id, kode_voucher } = info.row.original;
      const tipeVoucher = route.name.split(" ").at(-1);
      const alert = useAlert();

      const voucherRoute = `voucher-${tipeVoucher}/edit-voucher-${tipeVoucher}`;
      const param = new URLSearchParams();
      param.append("id", id);

      const url = `${voucherRoute}?${param.toString()}`;

      function copyKodeVoucher() {
        navigator.clipboard.writeText(kode_voucher);

        alert.setMessage(
          `"${kode_voucher}" Disalin`,
          "info",
        );
      }

      function removeRow() {
        info.table.options.meta.removeRow("id", id);
      }

      function deleteRow() {
        Swal.fire({
          title: `Apa kamu yakin ?`,
          html: `Kamu akan menghapus voucher : <br> <strong style="color: red;">${nama_voucher}</strong>`,
          icon: "warning",
          showCancelButton: true,
          confirmButtonColor: "#3085d6",
          cancelButtonColor: "#d33",
          confirmButtonText: "Hapus",
          cancelButtonText: "Batal",
        }).then(async (result) => {
          if (result.isConfirmed) {
            Swal.fire({
              title: "Menghapus Data ....",
              html: `Sistem sedang menghapus voucher : <br> <strong style="color: red;">${nama_voucher}</strong>`,
              didOpen: async () => {
                try {
                  Swal.showLoading();
                  await voucherService.deleteVoucher(id, tipeVoucher);
                  removeRow();

                  alert.setMessage(
                    `Sukses menghapus voucher : ${nama_voucher}`,
                    "success"
                  );
                } catch (error) {
                  console.log(error);
                  alert.setMessage("error", "danger");
                } finally {
                  Swal.close();
                }
              },
            });
          }
        });
      }

      return h("div", { class: "tw-flex tw-gap-2" }, [
        h(RouterButton, {
          title: "Edit",
          icon: "mdi mdi-pencil",
          to: url,
          class: "tw-text-xl",
        }),
        h(Button, {
          trigger: copyKodeVoucher,
          title: "Copy kode voucher",
          icon: "mdi mdi-clipboard",
          class: "tw-bg-gray-400 tw-text-xl",
        }),
        h(Button, {
          trigger: deleteRow,
          title: "Delete",
          icon: "mdi mdi-delete",
          class: "tw-bg-red-600 tw-text-xl",
        }),
      ]);
    },
  }),
  columnHelper.display({
    id: "row_num",
    header: () => h("div", { class: "tw-pl-4", textContent: "No" }),
    cell: (info) => {
      return h("div", {
        textContent: info.row.original.row_num,
        class: "table-cell-small tw-pl-4",
      });
    },
  }),
  columnHelper.accessor((row) => row.nama_voucher, {
    id: "nama_voucher",
    header: () => "Nama Voucher",
    cell: (info) => {
      return h("div", {
        textContent: info.getValue(),
        class: "table-cell-lg",
      });
    },
  }),
  columnHelper.accessor((row) => row.kode_principal, {
    id: "principal.kode",
    header: () => "Kode Principal",
    cell: (info) => {
      return h("div", {
        textContent: info.getValue(),
        class: "table-cell-medium",
      });
    },
  }),
  columnHelper.accessor((row) => row.nama_principal, {
    id: "principal.nama",
    header: () => "Principal",
    cell: (info) => {
      return h("div", {
        textContent: info.getValue(),
        class: "table-cell-lg",
      });
    },
  }),
  columnHelper.accessor((row) => row.kode_voucher, {
    id: "kode_voucher",
    header: () => "Kode Voucher",
    cell: (info) => {
      return h("div", {
        textContent: info.getValue(),
        class: "table-cell-medium",
      });
    },
  }),
  columnHelper.accessor((row) => row.status_voucher === 1, {
    id: "status_voucher",
    header: () => "Status",
    cell: (info) => {
      return h("div", {
        textContent: info.getValue() ? "Aktif" : "Tidak Aktif",
        class: "table-cell-medium",
      });
    },
  })
];
