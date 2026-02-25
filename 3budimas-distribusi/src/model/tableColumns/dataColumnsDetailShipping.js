import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import { formatCurrencyAuto, calculateProductDiscounts } from "@/src/lib/utils";
import { useShipping } from "@/src/store/shipping";

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

// Fungsi untuk mendapatkan total subtotal order untuk perhitungan diskon
const getTotalOrderSubtotal = () => {
  try {
    const shipping = useShipping();
    if (shipping?.listDetailFakturShipping?.detailFaktur) {
      let total = 0;
      shipping.listDetailFakturShipping.detailFaktur.forEach((product) => {
        // Konversi semua picked ke level UOM1
        const kartonToUom1 =
          (product.karton_picked || 0) * (product.konversi_level3 || 1);
        const boxToUom1 =
          (product.box_picked || 0) * (product.konversi_level2 || 1);
        const piecesUom1 = product.pieces_picked || 0;

        // Total pieces setelah konversi
        const totalPieces = kartonToUom1 + boxToUom1 + piecesUom1;

        // Hitung subtotal (total pieces x harga jual per piece)
        total += totalPieces * (product.harga_jual || 0);
      });
      return total;
    }
    return 0;
  } catch (error) {
    console.error("Error getting total order subtotal:", error);
    return 0;
  }
};

export const dataColumnsDetailShipping = [
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

  columnHelper.accessor((row) => row.karton_picked, {
    id: "uom3",
    cell: (info) =>
      h("span", { class: "tw-w-14 tw-pl-4 tw-flex tw-flex-col" }, [
        h("span", {}, info.getValue()),
        h("span", {
          class: "tw-text-xs tw-text-blue-400",
          innerText: info.row.original.puom3_nama || "karton",
        }),
      ]),
    header: () => h("span", { class: "tw-pl-4" }, "UOM 3"),
  }),

  columnHelper.accessor((row) => row.box_picked, {
    id: "uom2",
    cell: (info) =>
      h("span", { class: "tw-pl-4 tw-flex tw-flex-col" }, [
        h("span", {}, info.getValue()),
        h("span", {
          class: "tw-text-xs tw-text-blue-400",
          innerText: info.row.original.puom2_nama || "box",
        }),
      ]),
    header: () => h("span", { class: "tw-pl-4" }, "UOM 2"),
  }),

  columnHelper.accessor((row) => row.pieces_picked, {
    id: "uom1",
    cell: (info) =>
      h("span", { class: "tw-w-14 tw-pl-4 tw-flex tw-flex-col" }, [
        h("span", {}, info.getValue()),
        h("span", {
          class: "tw-text-xs tw-text-blue-400",
          innerText: info.row.original.puom1_nama || "pieces",
        }),
      ]),
    header: () => h("span", { class: "tw-pl-4" }, "UOM 1"),
  }),

  columnHelper.accessor((row) => row.harga_jual, {
    id: "harga",
    cell: (info) =>
      h(
        "div",
        { class: "tw-pl-4" },
         formatCurrencyAuto(info.getValue())
      ),
    header: () => h("div", { class: "tw-pl-4" }, "Harga/UOM 1"),
  }),

  // Mengubah accessor subtotal_harga untuk menghitung berdasarkan picked
  columnHelper.accessor(
    (row) => {
      // Konversi semua picked ke level UOM1
      const kartonToUom1 =
        (row.karton_picked || 0) * (row.konversi_level3 || 1);
      const boxToUom1 = (row.box_picked || 0) * (row.konversi_level2 || 1);
      const piecesUom1 = row.pieces_picked || 0;

      // Total pieces setelah konversi
      const totalPieces = kartonToUom1 + boxToUom1 + piecesUom1;

      // Hitung subtotal (total pieces x harga jual per piece)
      return totalPieces * (row.harga_jual || 0);
    },
    {
      id: "subtotal_harga",
      cell: (info) =>
        h(
          "div",
          { class: "tw-pl-4" },
           formatCurrencyAuto(info.getValue())
        ),
      header: () => h("div", { class: "tw-pl-4" }, "Subtotal Harga"),
    }
  ),

  // Untuk accessor disc1 - Voucher Reguler 1 (v1r)
  columnHelper.accessor(
    (row) => {
      const voucherStatus = getVoucherStatus(row);
      const totalOrderSubtotal = getTotalOrderSubtotal();
      // Hitung dengan fungsi baru
      const { diskon1r } = calculateProductDiscounts(
        row,
        voucherStatus,
        totalOrderSubtotal,
        "picked"
      );
      return diskon1r;
    },
    {
      id: "disc1",
      cell: (info) => {
        const value = info.getValue();
        return h(
          "span",
          { class: "tw-pl-2 tw-text-center" },
          value ?  formatCurrencyAuto(value) : "0"
        );
      },
      header: () => h("div", { class: "tw-pl-2" }, "Disc R1"),
    }
  ),

  // Untuk accessor disc2 - Voucher Reguler 2 (v2r)
  columnHelper.accessor(
    (row) => {
      const voucherStatus = getVoucherStatus(row);
      const totalOrderSubtotal = getTotalOrderSubtotal();
      // Hitung dengan fungsi baru
      const { diskon2r } = calculateProductDiscounts(
        row,
        voucherStatus,
        totalOrderSubtotal,
        "picked"
      );
      return diskon2r;
    },
    {
      id: "disc2",
      cell: (info) => {
        const value = info.getValue();
        return h(
          "span",
          { class: "tw-pl-2 tw-text-center" },
          value ?  formatCurrencyAuto(value) : "0"
        );
      },
      header: () => h("div", { class: "tw-pl-2" }, "Disc R2"),
    }
  ),

  // Untuk accessor disc3 - Voucher Reguler 3 (v3r)
  columnHelper.accessor(
    (row) => {
      const voucherStatus = getVoucherStatus(row);
      const totalOrderSubtotal = getTotalOrderSubtotal();
      // Hitung dengan fungsi baru
      const { diskon3r } = calculateProductDiscounts(
        row,
        voucherStatus,
        totalOrderSubtotal,
        "picked"
      );
      return diskon3r;
    },
    {
      id: "disc3",
      cell: (info) => {
        const value = info.getValue();
        return h(
          "span",
          { class: "tw-pl-2" },
          value ?  formatCurrencyAuto(value) : "0"
        );
      },
      header: () => h("div", { class: "tw-pl-2" }, "Disc R3"),
    }
  ),

  // Kolom baru untuk Disc P2 (v2p)
  columnHelper.accessor(
    (row) => {
      const voucherStatus = getVoucherStatus(row);
      const totalOrderSubtotal = getTotalOrderSubtotal();
      // Hitung dengan fungsi baru
      const { diskon2p } = calculateProductDiscounts(
        row,
        voucherStatus,
        totalOrderSubtotal,
        "picked"
      );
      return diskon2p;
    },
    {
      id: "disc2p",
      cell: (info) => {
        const value = info.getValue();
        return h(
          "span",
          { class: "tw-pl-2 tw-text-center" },
          value ?  formatCurrencyAuto(value) : "0"
        );
      },
      header: () => h("div", { class: "tw-pl-2" }, "Disc P2"),
    }
  ),

  // Kolom baru untuk Disc P3 (v3p)
  columnHelper.accessor(
    (row) => {
      const voucherStatus = getVoucherStatus(row);
      const totalOrderSubtotal = getTotalOrderSubtotal();
      // Hitung dengan fungsi baru
      const { diskon3p } = calculateProductDiscounts(
        row,
        voucherStatus,
        totalOrderSubtotal,
        "picked"
      );
      return diskon3p;
    },
    {
      id: "disc3p",
      cell: (info) => {
        const value = info.getValue();
        return h(
          "span",
          { class: "tw-pl-2" },
          value ?  formatCurrencyAuto(value) : "0"
        );
      },
      header: () => h("div", { class: "tw-pl-2" }, "Disc P3"),
    }
  ),

  columnHelper.accessor(
    (row) => {
      const voucherStatus = getVoucherStatus(row);
      const totalOrderSubtotal = getTotalOrderSubtotal();
      // Hitung total diskon dengan fungsi baru
      const { totalDiskon } = calculateProductDiscounts(
        row,
        voucherStatus,
        totalOrderSubtotal,
        "picked"
      );
      return totalDiskon;
    },
    {
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
    }
  ),

  columnHelper.accessor(
    (row) => {
      const voucherStatus = getVoucherStatus(row);
      const totalOrderSubtotal = getTotalOrderSubtotal();

      // Konversi semua picked ke level UOM1
      const kartonToUom1 =
        (row.karton_picked || 0) * (row.konversi_level3 || 1);
      const boxToUom1 = (row.box_picked || 0) * (row.konversi_level2 || 1);
      const piecesUom1 = row.pieces_picked || 0;

      // Total pieces setelah konversi
      const totalPieces = kartonToUom1 + boxToUom1 + piecesUom1;

      // Hitung subtotal (total pieces x harga jual per piece)
      const subtotal = totalPieces * (row.harga_jual || 0);

      const { totalDiskon } = calculateProductDiscounts(
        row,
        voucherStatus,
        totalOrderSubtotal,
        "picked"
      );

      return subtotal - totalDiskon;
    },
    {
      id: "total_harga",
      cell: (info) =>
        h(
          "div",
          { class: "tw-pl-4" },
           formatCurrencyAuto(info.getValue())
        ),
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
        const totalOrderSubtotal = getTotalOrderSubtotal();
        const voucherBadges = [];

        // Hitung semua diskon dengan fungsi yang sudah ada
        const { diskon1r, diskon2r, diskon3r, diskon2p, diskon3p } =
          calculateProductDiscounts(
            row,
            voucherStatus,
            totalOrderSubtotal,
            "picked"
          );

        // Voucher Reguler 1 (v1r) - Tampilkan hanya jika diskon > 0
        if (row.v1r_nama && diskon1r > 0) {
          voucherBadges.push(
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

        // Voucher Reguler 2 (v2r) - Tampilkan hanya jika diskon > 0
        if (row.v2r_nama && diskon2r > 0) {
          voucherBadges.push(
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

        // Voucher Reguler 3 (v3r) - Tampilkan hanya jika diskon > 0
        if (row.v3r_nama && diskon3r > 0) {
          voucherBadges.push(
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

        // Voucher Produk 2 (v2p) - Tampilkan hanya jika diskon > 0
        if (row.v2p_nama && diskon2p > 0) {
          const v2pDisplay =
            row.v2p_kategori_voucher === 1
              ? `${row.v2p_persen}%`
              : `${formatCurrencyAuto(row.v2p_nominal_diskon)}/${
                  row.puom1_nama || "pieces"
                }`;

          voucherBadges.push(
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

        // Voucher Produk 3 (v3p) - Tampilkan hanya jika diskon > 0
        if (row.v3p_nama && diskon3p > 0) {
          const v3pDisplay =
            row.v3p_kategori_voucher === 1
              ? `${row.v3p_persen}%`
              : `${formatCurrencyAuto(row.v3p_nominal_diskon)}/${
                  row.puom1_nama || "pieces"
                }`;

          voucherBadges.push(
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
          voucherBadges
        );
      },
      header: () => h("div", { class: "tw-pl-4" }, "Voucher"),
    }
  ),
];
