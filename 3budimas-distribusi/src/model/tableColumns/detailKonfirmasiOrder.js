import {calculateProductDiscounts, calculateProductSubtotal, formatCurrencyAuto,} from "@/src/lib/utils";
import {useShipping} from "@/src/store/shipping";
import {createColumnHelper} from "@tanstack/vue-table";
import {h} from "vue";

const columnHelper = createColumnHelper();

// Fungsi untuk mendapatkan status voucher dari produk
const getVoucherStatus = (row) => {
  try {
    const shipping = useShipping();
    return shipping.getVoucherStatusForProduct(row.id_produk);
  } catch (error) {
    console.error("Error getting voucher status:", error);
    return null;
  }
};

const getTotalOrderSubtotal = () => {
  try {
    const shipping = useShipping();
    if (shipping?.listDetailFakturShipping?.detailFaktur) {
      let total = 0;
      shipping.listDetailFakturShipping.detailFaktur.forEach((product) => {
        total += calculateProductSubtotal(product);
      });
      return total;
    }
    return 0;
  } catch (error) {
    console.error("Error getting total order subtotal:", error);
    return 0;
  }
};

const calculateTotalDiscount = (row) => {
  const voucherStatus = getVoucherStatus(row);
  const totalOrderSubtotal = getTotalOrderSubtotal();

  const result = calculateProductDiscounts(
    row,
    voucherStatus,
    totalOrderSubtotal
  );

  return result.totalDiskon;
};

export const detailKonfirmasiOrderColumn = [
  columnHelper.accessor((row) => row.nama_produk, {
    id: "produk",
    cell: (info) =>
      h(
        "span",
        { class: "tw-max-w-72 tw-pl-4 tw-flex tw-flex-col tw-jutify-center" },
        [
          h("span", {}, info.getValue()),
          h(
            "span",
            { class: "tw-text-xs tw-text-blue-400" },
            info.row.original.kode_sku
          ),
        ]
      ),
    header: () => h("span", { class: "tw-pl-4" }, "Produk"),
  }),

  columnHelper.accessor((row) => row.karton_order, {
    id: "uom3",
    cell: (info) =>
      h("span", { class: "tw-w-14 tw-pl-4 tw-flex tw-flex-col" }, [
        h("span", {}, info.getValue()),
        h("span", {
          class: "tw-text-xs tw-text-blue-400",
          innerText: info.row.original.puom3_nama,
        }),
      ]),
    header: () => h("span", { class: "tw-pl-4" }, "UOM 3"),
  }),

  columnHelper.accessor((row) => row.box_order, {
    id: "uom2",
    cell: (info) =>
      h("span", { class: "tw-pl-4 tw-flex tw-flex-col" }, [
        h("span", {}, info.getValue()),
        h("span", {
          class: "tw-text-xs tw-text-blue-400",
          innerText: info.row.original.puom2_nama,
        }),
      ]),
    header: () => h("span", { class: "tw-pl-4" }, "UOM 2"),
  }),

  columnHelper.accessor((row) => row.pieces_order, {
    id: "uom1",
    cell: (info) =>
      h("span", { class: "tw-w-14 tw-pl-4 tw-flex tw-flex-col" }, [
        h("span", {}, info.getValue()),
        h("span", {
          class: "tw-text-xs tw-text-blue-400",
          innerText: info.row.original.puom1_nama,
        }),
      ]),
    header: () => h("span", { class: "tw-pl-4" }, "UOM 1"),
  }),

  columnHelper.accessor((row) => row.harga_jual, {
    id: "harga",
    cell: (info) =>
      h("div", { class: "tw-pl-4" }, formatCurrencyAuto(info.getValue())),
    header: () => h("div", { class: "tw-pl-4" }, "Harga/UOM 1"),
  }),

  columnHelper.accessor((row) => calculateProductSubtotal(row), {
    id: "subtotal_harga",
    cell: (info) =>
      h("div", { class: "tw-pl-4" }, formatCurrencyAuto(info.getValue())),
    header: () => h("div", { class: "tw-pl-4" }, "Subtotal Harga"),
  }),

  // Kolom Disc Reguler 1
  columnHelper.accessor(
    (row) => {
      const voucherStatus = getVoucherStatus(row);
      const totalOrderSubtotal = getTotalOrderSubtotal();
      // Hitung dengan fungsi baru
      const { diskon1r } = calculateProductDiscounts(
        row,
        voucherStatus,
        totalOrderSubtotal
      );
      return diskon1r;
    },
    {
      id: "disc1r",
      cell: (info) => {
        const value = info.getValue();
        return h(
          "span",
          { class: "tw-pl-2 tw-text-center" },
          value ? formatCurrencyAuto(value) : "0"
        );
      },
      header: () => h("div", { class: "tw-pl-2" }, "Disc R1"),
    }
  ),
  // Kolom Disc Reguler 2
  columnHelper.accessor(
    (row) => {
      const voucherStatus = getVoucherStatus(row);
      const totalOrderSubtotal = getTotalOrderSubtotal();
      // Hitung dengan fungsi baru
      const { diskon2r } = calculateProductDiscounts(
        row,
        voucherStatus,
        totalOrderSubtotal
      );
      return diskon2r;
    },
    {
      id: "disc2r",
      cell: (info) => {
        const value = info.getValue();
        return h(
          "span",
          { class: "tw-pl-2 tw-text-center" },
          value ? formatCurrencyAuto(value) : "0"
        );
      },
      header: () => h("div", { class: "tw-pl-2" }, "Disc R2"),
    }
  ),

  // Kolom Disc Reguler 3
  columnHelper.accessor(
    (row) => {
      const voucherStatus = getVoucherStatus(row);
      const totalOrderSubtotal = getTotalOrderSubtotal();
      // Hitung dengan fungsi baru
      const { diskon3r } = calculateProductDiscounts(
        row,
        voucherStatus,
        totalOrderSubtotal
      );
      return diskon3r;
    },
    {
      id: "disc3r",
      cell: (info) => {
        const value = info.getValue();
        return h(
          "span",
          { class: "tw-pl-2 tw-text-center" },
          value ? formatCurrencyAuto(value) : "0"
        );
      },
      header: () => h("div", { class: "tw-pl-2" }, "Disc R3"),
    }
  ),

  // Kolom Disc Produk 2
  columnHelper.accessor(
    (row) => {
      const voucherStatus = getVoucherStatus(row);
      // Hitung dengan fungsi baru
      const { diskon2p } = calculateProductDiscounts(row, voucherStatus);
      return diskon2p;
    },
    {
      id: "disc2p",
      cell: (info) => {
        const value = info.getValue();
        return h(
          "span",
          { class: "tw-pl-2 tw-text-center" },
          value ? formatCurrencyAuto(value) : "0"
        );
      },
      header: () => h("div", { class: "tw-pl-2" }, "Disc P2"),
    }
  ),

  // Kolom Disc Produk 3
  columnHelper.accessor(
    (row) => {
      const voucherStatus = getVoucherStatus(row);
      // Hitung dengan fungsi baru
      const { diskon3p } = calculateProductDiscounts(row, voucherStatus);
      return diskon3p;
    },
    {
      id: "disc3p",
      cell: (info) => {
        const value = info.getValue();
        return h(
          "span",
          { class: "tw-pl-2" },
          value ? formatCurrencyAuto(value) : "0"
        );
      },
      header: () => h("div", { class: "tw-pl-2" }, "Disc P3"),
    }
  ),

  columnHelper.accessor((row) => calculateTotalDiscount(row), {
    id: "total_discount",
    cell: (info) => {
      const totalDiskon = info.getValue();
      return h(
        "div",
        { class: "tw-pl-4 tw-break-words" },
        formatCurrencyAuto(totalDiskon)
      );
    },
    header: () => h("div", { class: "tw-pl-4" }, "Total Diskon"),
  }),

  columnHelper.accessor(
    (row) => {
      const subtotal = calculateProductSubtotal(row);
      const totalDiskon = calculateTotalDiscount(row);
      return subtotal - totalDiskon;
    },
    {
      id: "total_harga",
      cell: (info) =>
        h("div", { class: "tw-pl-4" }, formatCurrencyAuto(info.getValue())),
      header: () => h("div", { class: "tw-pl-4" }, "Total Harga"),
    }
  ),

  columnHelper.accessor(
    (row) => [
      row.v1r_nama,
      row.v2r_nama,
      row.v3r_nama,
      row.v2p_nama,
      row.v3p_nama,
    ],
    {
      id: "vouchers",
      cell: (info) => {
        const row = info.row.original;
        const voucherStatus = getVoucherStatus(row);

        // Tampung semua badge voucher aktif
        let activeBadges = [];

        // Badge untuk voucher reguler
        // Reguler 1
        if (row.v1r_nama && voucherStatus.v1r_active) {
          activeBadges.push(
            h(
              "span",
              {
                class:
                  "tw-bg-blue-100 tw-text-blue-800 tw-text-xs tw-font-medium tw-px-2.5 tw-py-1.5 tw-rounded-lg tw-mr-1 tw-mb-1 tw-flex tw-flex-col tw-items-center",
              },
              [
                h("span", { class: "tw-font-medium" }, row.v1r_nama),
                h(
                  "span",
                  {
                    class:
                      "tw-mt-1 tw-bg-blue-200 tw-text-blue-700 tw-rounded tw-px-1.5 tw-py-0.5 tw-text-xs",
                  },
                  `${row.v1r_persen}%`
                ),
              ]
            )
          );
        }

        // Reguler 2
        if (row.v2r_nama && voucherStatus.v2r_active) {
          activeBadges.push(
            h(
              "span",
              {
                class:
                  "tw-bg-teal-100 tw-text-teal-800 tw-text-xs tw-font-medium tw-px-2.5 tw-py-1.5 tw-rounded-lg tw-mr-1 tw-mb-1 tw-flex tw-flex-col tw-items-center",
              },
              [
                h("span", { class: "tw-font-medium" }, row.v2r_nama),
                h(
                  "span",
                  {
                    class:
                      "tw-mt-1 tw-bg-teal-200 tw-text-teal-700 tw-rounded tw-px-1.5 tw-py-0.5 tw-text-xs",
                  },
                  `${row.v2r_persen}%`
                ),
              ]
            )
          );
        }

        // Reguler 3
        if (row.v3r_nama && voucherStatus.v3r_active) {
          activeBadges.push(
            h(
              "span",
              {
                class:
                  "tw-bg-yellow-100 tw-text-yellow-800 tw-text-xs tw-font-medium tw-px-2.5 tw-py-1.5 tw-rounded-lg tw-mr-1 tw-mb-1 tw-flex tw-flex-col tw-items-center",
              },
              [
                h("span", { class: "tw-font-medium" }, row.v3r_nama),
                h(
                  "span",
                  {
                    class:
                      "tw-mt-1 tw-bg-yellow-200 tw-text-yellow-700 tw-rounded tw-px-1.5 tw-py-0.5 tw-text-xs",
                  },
                  `${row.v3r_persen}%`
                ),
              ]
            )
          );
        }

        // Produk 2
        if (row.v2p_nama && voucherStatus.v2p_active) {
          const v2pDisplay =
            row.v2p_kategori_voucher === 1
              ? `${row.v2p_persen}%`
              : `${formatCurrencyAuto(row.v2p_nominal_diskon)}`;

          activeBadges.push(
            h(
              "span",
              {
                class:
                  "tw-bg-green-100 tw-text-green-800 tw-text-xs tw-font-medium tw-px-2.5 tw-py-1.5 tw-rounded-lg tw-mr-1 tw-mb-1 tw-flex tw-flex-col tw-items-center",
              },
              [
                h("span", { class: "tw-font-medium" }, row.v2p_nama),
                h(
                  "span",
                  {
                    class:
                      "tw-mt-1 tw-bg-green-200 tw-text-green-700 tw-rounded tw-px-1.5 tw-py-0.5 tw-text-xs",
                  },
                  v2pDisplay
                ),
              ]
            )
          );
        }

        // Produk 3
        if (row.v3p_nama && voucherStatus.v3p_active) {
          const v3pDisplay =
            row.v3p_kategori_voucher === 1
              ? `${row.v3p_persen}%`
              : `${formatCurrencyAuto(row.v3p_nominal_diskon)}`;

          activeBadges.push(
            h(
              "span",
              {
                class:
                  "tw-bg-purple-100 tw-text-purple-800 tw-text-xs tw-font-medium tw-px-2.5 tw-py-1.5 tw-rounded-lg tw-mr-1 tw-mb-1 tw-flex tw-flex-col tw-items-center",
              },
              [
                h("span", { class: "tw-font-medium" }, row.v3p_nama),
                h(
                  "span",
                  {
                    class:
                      "tw-mt-1 tw-bg-purple-200 tw-text-purple-700 tw-rounded tw-px-1.5 tw-py-0.5 tw-text-xs",
                  },
                  v3pDisplay
                ),
              ]
            )
          );
        }

        return h(
          "div",
          { class: "tw-pl-4 tw-flex tw-flex-wrap tw-gap-1" },
          activeBadges
        );
      },
      header: () => h("div", { class: "tw-pl-4" }, "Voucher yang dikonfirmasi"),
    }
  ),

  columnHelper.display({
    id: "actions",
    header: () => h("div", { class: "tw-pl-2", innerText: "Actions" }),
    cell: (info) => {
      const row = info.row.original;
      const isProdukVoucherAvailable = Boolean(row.v2p_nama || row.v3p_nama);

      return h(
        "div",
        {
          class: `table-cell-lg tw-pl-2`,
        },
        [
          h(
            "button",
            {
              class: `tw-flex tw-items-center tw-gap-2 tw-px-2 tw-py-1 tw-text-white tw-rounded-md ${
                isProdukVoucherAvailable
                  ? "tw-bg-blue-500 hover:tw-bg-blue-600"
                  : "tw-bg-gray-500"
              }`,
              onClick: () => {
                if (isProdukVoucherAvailable) {
                  // Kirim seluruh data produk untuk perhitungan yang akurat
                  info.table.options.meta.updateRow(
                    row,
                    info.row.index,
                    "voucher",
                    "openRowModal"
                  );
                }
              },
            },
            "Konfirmasi Voucher Produk"
          ),
        ]
      );
    },
  }),
];
