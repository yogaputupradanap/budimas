import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import Button from "../../components/ui/Button.vue";
import { useKunjungan } from "@/src/store/kunjungan";
import { BButton } from "bootstrap-vue-next";
import { useDashboard } from "@/src/store/dashboard";
import { usePrincipal } from "@/src/store/principal";

const columnHelper = createColumnHelper();

export const kunjunganColumns = [
  columnHelper.accessor((row) => row.no, {
    id: "no",
    cell: (info) =>
      h("div", {
        class: "tw-w-full tw-flex tw-justify-center",
        innerText: info.getValue(),
      }),
    header: () =>
      h("div", {
        class: "tw-w-full tw-flex tw-justify-center",
        innerText: "No",
      }),
  }),
  columnHelper.accessor((row) => row.kode_customer, {
    id: "kode_customer",
    cell: (info) => h("div", info.getValue()),
    header: () =>
      h("span", { class: "tw-w-28 lg:tw-w-auto", innerText: "kode customer" }),
  }),
  columnHelper.accessor((row) => row.nama_customer, {
    id: "nama_customer",
    cell: (info) => info.getValue(),
    header: () =>
      h("span", { class: "tw-w-36 lg:tw-w-auto", innerText: "nama customer" }),
  }),
  columnHelper.accessor((row) => row.status, {
    id: "status",
    cell: (info) => {
      const data = info.getValue();
      const status = data === 0 ? "belum" : data === 1 ? "sedang" : "sudah";
      return status;
    },
    header: () =>
      h("span", { class: "tw-w-28 lg:tw-w-auto", innerText: "status" }),
  }),
  columnHelper.accessor((row) => row.waktu_mulai, {
    id: "waktu_mulai",
    cell: (info) => info.getValue(),
    header: () =>
      h("span", { class: "tw-w-36 lg:tw-w-auto", innerText: "check in" }),
  }),
  columnHelper.accessor((row) => row.waktu_selesai, {
    id: "waktu_selesai",
    cell: (info) => info.getValue(),
    header: () =>
      h("span", { class: "tw-w-36 lg:tw-w-auto", innerText: "check out" }),
  }),
  columnHelper.accessor((row) => row.status, {
    id: "status",
    cell: (info) => {
      const dashboard = useDashboard();
      const data = info.getValue();
      const kunjungan = useKunjungan();
      const text = data === 0 ? "check in" : data === 1 ? "to do" : "done";
      const buttColor =
        data === 0
          ? "tw-bg-gray-300 tw-text-gray-800"
          : data === 1
          ? "tw-bg-blue-500 tw-text-white"
          : "tw-bg-green-500 tw-text-white disabled:tw-bg-green-500";

      const currKunjungan = kunjungan.listKunjungan.find(
        (list) => list.kode_customer === info.row.getValue("kode_customer")
      );

      const ruteData = {
        latitude: currKunjungan?.customer_latitude,
        longitude: currKunjungan?.customer_longitude,
        alamat: `${currKunjungan?.nama_wilayah_4}, ${currKunjungan?.nama_wilayah_3}, ${currKunjungan?.nama_wilayah_2}, ${currKunjungan?.nama_wilayah_1}`,
      };

      const openModal = () => {
        info.table.options.meta.updateRow(ruteData, null, null, "openRowModal");
      };

      const checkInOut = async () => {
        if (data === 0) {
          await kunjungan.checkInOutKunjungan(currKunjungan.id, 1);
        } else {
          await kunjungan.setActiveKunjungan(currKunjungan.id);
        }
        const principal = usePrincipal();
        await principal.getPrincipals(
          kunjungan.activeKunjungan.kunjungan?.user_id,
          kunjungan.activeKunjungan.kunjungan?.customer_id
        );

        dashboard.initActiveButton();
      };

      const disableButton = () => {
        if (kunjungan.listKunjungan.some((list) => list.status === 1)) {
          return data === 0 ? true : data === 2 ? true : false;
        }

        return false;
      };

      return h(
        "div",
        { class: "tw-w-full tw-flex tw-justify-center tw-gap-2" },
        [
          h(
            Button,
            {
              class: `tw-w-24 ${buttColor}`,
              fallbackUrl: `/kunjungan/daftar-kunjungan-toko/dashboard-menu-kunjungan-toko?status=${data}`,
              trigger: checkInOut,
              disabled: disableButton(),
            },
            () => text
          ),
        ]
      );
    },
    header: () =>
      h("div", {
        class: "tw-w-full tw-flex tw-justify-center",
        innerText: "Actions",
      }),
  }),
];
