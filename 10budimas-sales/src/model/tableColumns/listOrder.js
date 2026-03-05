import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import Button from "@/src/components/ui/Button.vue";
import { checkNaN, parseCurrency } from "../../lib/utils";
import { useSalesRequest } from "@/src/store/salesRequest";
import { useVoucher } from "@/src/store/voucher";
import { useKunjungan } from "@/src/store/kunjungan";
import { useSales } from "@/src/store/sales";

const getProdukById = (info) => {
  const salesRequest = useSalesRequest();
  const produkId = info.row.getValue("id");
  return salesRequest.initialProducts.find((req) => req.id === produkId);
};
const getVoucherValidationStatus = (produk, voucherType) => {
  if (!produk.voucherValidations || !produk.voucherValidations[voucherType]) {
    return { isValid: true, reason: null };
  }
  return produk.voucherValidations[voucherType];
};
const columnHelper = createColumnHelper();
export const listOrderColumns = [
  columnHelper.display({
    id: "actions",
    header: () =>
      h("span", {
        class: "tw-w-full tw-flex tw-justify-center",
        innerText: "Actions"
      }),
    cell: ({ column, row, table }) => {
      const salesRequest = useSalesRequest();
      const voucher = useVoucher();
      const currOBJ = salesRequest.initialProducts.find(
        (product) => product.id === row.getValue("id")
      );

      const value = {
        pieces: row.getValue("uom1"),
        box: row.getValue("uom2"),
        karton: row.getValue("uom3"),
        namaProduk: currOBJ.id,
        principalId: currOBJ.id_principal
      };

      const openEditModal = () =>
        table.options.meta.updateRow(
          value,
          row.index,
          column.id,
          "openRowModal"
        );

      const resettingVoucher = async () => {
        const sales = useSales();
        const kunjungan = useKunjungan();
        const idProduk = currOBJ.id; // dari value namaProduk
        const idCabang = sales.salesUser.id_cabang;
        const idCustomer = kunjungan.activeKunjungan.kunjungan.customer_id;

        // Reset voucher produk
        // Gunakan cara lama seperti di listOrderColumns.js
        await voucher.getVoucher2Product(idProduk, idCabang);
        await voucher.getVoucher3Product(idProduk, idCabang, idCustomer);

        openEditModal();
      };
      const removeRow = () =>
        table.options.meta.updateRow(value, row.index, column.id, "removeRow");

      return h(
        "div",
        { class: "tw-w-full tw-flex tw-gap-2 tw-justify-center tw-px-2" },
        [
          h(
            Button,
            {
              trigger: resettingVoucher,
              class: "tw-bg-blue-500 tw-w-8 tw-h-8",
              loadingMode: "icon"
            },
            () => h("i", { class: "mdi mdi-pencil" })
          )
          // h(
          //   BButton,
          //   { onClick: removeRow, size: "sm", class: "tw-bg-red-500" },
          //   () => h("i", { class: "mdi mdi-delete" })
          // ),
        ]
      );
    }
  }),
  columnHelper.accessor((row) => row.id, {
    id: "id",
    cell: (info) => {
      const salesRequest = useSalesRequest();
      const produk = salesRequest.initialProducts.find(
        (req) => req.id === info.getValue()
      );

      const original = info.row.original;

      // Cek apakah setiap voucher digunakan
      const hasValidQuantity =
        original.uom1 > 0 || original.uom2 > 0 || original.uom3 > 0;

      // Cek apakah setiap voucher digunakan - HANYA jika jumlah produk > 0
      console.log(original.voucherSelections);
      const hasVoucher1Regular =
        hasValidQuantity &&
        original.voucherSelections?.voucher1Regular !== null &&
        original.voucherSelections?.voucher1Regular !== undefined;
      const hasVoucher2Regular =
        hasValidQuantity &&
        original.voucherSelections?.voucher2Regular !== null &&
        original.voucherSelections?.voucher2Regular !== undefined;
      const hasVoucher3Regular =
        hasValidQuantity &&
        original.voucherSelections?.voucher3Regular !== null &&
        original.voucherSelections?.voucher3Regular !== undefined;
      const hasVoucher2Product =
        hasValidQuantity &&
        original.voucherSelections?.voucher2Product !== null &&
        original.voucherSelections?.voucher2Product !== undefined;
      const hasVoucher3Product =
        hasValidQuantity &&
        original.voucherSelections?.voucher3Product !== null &&
        original.voucherSelections?.voucher3Product !== undefined;

      const voucher1RegularIcon = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="28" height="28">
  <rect width="22" height="16" x="1" y="4" rx="2" fill="#E6F7FF" stroke="#1890FF" stroke-width="1.5"/>
  <text x="12" y="14.5" text-anchor="middle" font-family="Arial, sans-serif" font-weight="bold" font-size="10" fill="#1890FF">R1</text>
  <path d="M4 4 L4 20" stroke="#1890FF" stroke-width="1" stroke-dasharray="2 1"/>
  <path d="M20 4 L20 20" stroke="#1890FF" stroke-width="1" stroke-dasharray="2 1"/>
</svg>`;

      const voucher2RegularIcon = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="28" height="28">
  <rect width="22" height="16" x="1" y="4" rx="2" fill="#FFF7E6" stroke="#FA8C16" stroke-width="1.5"/>
  <text x="12" y="14.5" text-anchor="middle" font-family="Arial, sans-serif" font-weight="bold" font-size="10" fill="#FA8C16">R2</text>
  <path d="M4 4 L4 20" stroke="#FA8C16" stroke-width="1" stroke-dasharray="2 1"/>
  <path d="M20 4 L20 20" stroke="#FA8C16" stroke-width="1" stroke-dasharray="2 1"/>
</svg>`;

      const voucher3RegularIcon = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="28" height="28">
  <rect width="22" height="16" x="1" y="4" rx="2" fill="#F9F0FF" stroke="#722ED1" stroke-width="1.5"/>
  <text x="12" y="14.5" text-anchor="middle" font-family="Arial, sans-serif" font-weight="bold" font-size="10" fill="#722ED1">R3</text>
  <path d="M4 4 L4 20" stroke="#722ED1" stroke-width="1" stroke-dasharray="2 1"/>
  <path d="M20 4 L20 20" stroke="#722ED1" stroke-width="1" stroke-dasharray="2 1"/>
</svg>`;

      const voucher2ProductIcon = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="28" height="28">
  <rect width="22" height="16" x="1" y="4" rx="2" fill="#E6FFFB" stroke="#13C2C2" stroke-width="1.5"/>
  <text x="12" y="14.5" text-anchor="middle" font-family="Arial, sans-serif" font-weight="bold" font-size="10" fill="#13C2C2">P2</text>
  <path d="M4 4 L4 20" stroke="#13C2C2" stroke-width="1" stroke-dasharray="2 1"/>
  <path d="M20 4 L20 20" stroke="#13C2C2" stroke-width="1" stroke-dasharray="2 1"/>
</svg>`;

      const voucher3ProductIcon = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="28" height="28">
  <rect width="22" height="16" x="1" y="4" rx="2" fill="#FFF1F0" stroke="#F5222D" stroke-width="1.5"/>
  <text x="12" y="14.5" text-anchor="middle" font-family="Arial, sans-serif" font-weight="bold" font-size="10" fill="#F5222D">P3</text>
  <path d="M4 4 L4 20" stroke="#F5222D" stroke-width="1" stroke-dasharray="2 1"/>
  <path d="M20 4 L20 20" stroke="#F5222D" stroke-width="1" stroke-dasharray="2 1"/>
</svg>`;

      return h("div", { class: "tw-w-full tw-flex tw-justify-center" }, [
        h(
          "div",
          {
            class:
              "tw-w-56 tw-flex tw-flex-col tw-justify-center tw-items-center tw-gap-1"
          },
          [
            // Nama produk
            h("span", {
              class: "tw-text-center tw-font-medium",
              innerText: produk.nama
            }),

            // Kode produk
            h("span", {
              class: "tw-text-sm tw-text-blue-400",
              innerText: produk.kode_sku
            }),

            // Ikon voucher
            h(
              "div",
              {
                class:
                  "tw-flex tw-gap-1 tw-justify-center tw-items-center tw-mt-1"
              },
              [
                // Icons sesuai voucher yang digunakan
                hasVoucher1Regular
                  ? h("span", {
                    class: "tw-inline-block",
                    innerHTML: voucher1RegularIcon,
                    title: "Voucher 1 Reguler digunakan"
                  })
                  : null,
                hasVoucher2Regular
                  ? h("span", {
                    class: "tw-inline-block",
                    innerHTML: voucher2RegularIcon,
                    title: "Voucher 2 Reguler digunakan"
                  })
                  : null,
                hasVoucher3Regular
                  ? h("span", {
                    class: "tw-inline-block",
                    innerHTML: voucher3RegularIcon,
                    title: "Voucher 3 Reguler digunakan"
                  })
                  : null,
                hasVoucher2Product
                  ? h("span", {
                    class: "tw-inline-block",
                    innerHTML: voucher2ProductIcon,
                    title: "Voucher 2 Produk digunakan"
                  })
                  : null,
                hasVoucher3Product
                  ? h("span", {
                    class: "tw-inline-block",
                    innerHTML: voucher3ProductIcon,
                    title: "Voucher 3 Produk digunakan"
                  })
                  : null
              ]
            )
          ]
        )
      ]);
    },
    header: () =>
      h("span", {
        class: "tw-w-full tw-flex tw-justify-center",
        innerText: "Produk"
      })
  }),
  columnHelper.accessor((row) => row.uom3, {
    id: "uom3",
    cell: (info) => {
      const produk = getProdukById(info);
      return h(
        "div",
        {
          class:
            "tw-flex tw-flex-col tw-justify-center tw-items-center tw-gap-1 tw-px-2"
        },
        [
          h("span", { innerText: info.getValue() }),
          h("span", {
            innerText: produk?.konversi_3_nama,
            class: "tw-text-blue-400 tw-text-xs"
          })
        ]
      );
    },
    header: () =>
      h("div", {
        class: "tw-w-full tw-flex tw-justify-center",
        innerText: "UOM 3"
      })
  }),

  columnHelper.accessor((row) => row.uom2, {
    id: "uom2",
    cell: (info) => {
      const produk = getProdukById(info);
      return h(
        "div",
        {
          class:
            "tw-flex tw-flex-col tw-justify-center tw-items-center tw-gap-1 tw-px-2"
        },
        [
          h("span", { innerText: info.getValue() }),
          h("span", {
            innerText: produk?.konversi_2_nama,
            class: "tw-text-blue-400 tw-text-xs"
          })
        ]
      );
    },
    header: () =>
      h("span", {
        class: "tw-w-full tw-flex tw-justify-center",
        innerText: "UOM 2"
      })
  }),
  columnHelper.accessor((row) => row.uom1, {
    id: "uom1",
    cell: (info) => {
      const produk = getProdukById(info);
      return h(
        "div",
        {
          class:
            "tw-flex tw-flex-col tw-justify-center tw-items-center tw-gap-1 tw-px-2"
        },
        [
          h("span", { innerText: info.getValue() }),
          h("span", {
            innerText: produk?.konversi_1_nama,
            class: "tw-text-blue-400 tw-text-xs"
          })
        ]
      );
    },
    header: () =>
      h("span", {
        class: "tw-w-full tw-flex tw-justify-center",
        innerText: "UOM 1"
      })
  }),

  columnHelper.accessor((row) => row.harga_jual, {
    id: "harga_jual",
    cell: (info) => {
      const parse = parseCurrency(checkNaN(info.getValue()));
      const harga_jual = `Rp. ${parse}`;
      return h(
        "div",
        {
          class: "tw-w-full tw-flex tw-justify-center"
        },
        [
          h("span", {
            class: "tw-w-20 tw-text-xs tw-text-center",
            innerText: harga_jual
          })
        ]
      );
    },
    header: () =>
      h("div", {
        class: "tw-w-full tw-flex tw-justify-center",
        innerText: "harga/UOM 1"
      })
  }),
  // Kolom Voucher 1 Reguler
  columnHelper.accessor("v1r", {
    id: "v1r",
    cell: (info) => {
      const produk = info.row.original;
      const hasValidQuantity =
        produk.uom1 > 0 || produk.uom2 > 0 || produk.uom3 > 0;
      const diskonValue = hasValidQuantity
        ? produk.discountDetails?.diskon1Regular || 0
        : 0;
      const diskonPersen = hasValidQuantity
        ? produk.voucherSelections?.voucher1Regular?.persentase_diskon_1 || 0
        : 0;

      // Dapatkan status validasi voucher
      const validationStatus = getVoucherValidationStatus(
        produk,
        "voucher1Regular"
      );

      // Hanya tambahkan border merah jika voucher ada dan tidak valid
      const hasVoucher =
        produk.voucherSelections?.voucher1Regular !== null &&
        produk.voucherSelections?.voucher1Regular !== undefined;

      const errorClass =
        hasVoucher && !validationStatus.isValid
          ? "tw-border-red-500 tw-border tw-rounded-md"
          : "";

      return h(
        "div",
        {
          class: `tw-w-full tw-flex tw-justify-center tw-items-center ${errorClass}`,
          title: !validationStatus.isValid ? validationStatus.reason || "" : ""
        },
        [
          h(
            "div",
            {
              class:
                "tw-flex tw-flex-col tw-items-center tw-justify-center tw-text-center tw-py-1"
            },
            [
              // Baris persentase
              h(
                "div",
                {
                  class:
                    "tw-flex tw-items-center tw-justify-center tw-text-center tw-w-full"
                },
                [
                  h("span", {
                    class: "tw-text-xs tw-text-center",
                    innerText: checkNaN(diskonPersen)
                  }),
                  h("span", {
                    class: "tw-text-xs",
                    innerText: "%"
                  })
                ]
              ),
              // Baris nilai rupiah dengan warna merah jika tidak valid
              h("span", {
                class: `tw-text-xs tw-text-center ${
                  hasVoucher && !validationStatus.isValid
                    ? "tw-text-red-500 tw-font-medium"
                    : "tw-text-blue-400"
                }`,
                innerText: "Rp." + parseCurrency(checkNaN(diskonValue))
              })
            ]
          )
        ]
      );
    },
    header: () =>
      h("span", {
        class: "tw-w-full tw-flex tw-justify-center",
        innerText: "V1R"
      })
  }),

  // Kolom Voucher 2 Reguler
  columnHelper.accessor("v2r", {
    id: "v2r",
    cell: (info) => {
      const produk = info.row.original;
      const hasValidQuantity =
        produk.uom1 > 0 || produk.uom2 > 0 || produk.uom3 > 0;
      const diskonValue = hasValidQuantity
        ? produk.discountDetails?.diskon2Regular || 0
        : 0;
      const voucher = produk.voucherSelections?.voucher2Regular;
      const diskonPersen = hasValidQuantity
        ? voucher?.persentase_diskon_2 || 0
        : 0;

      // Dapatkan status validasi voucher
      const validationStatus = getVoucherValidationStatus(
        produk,
        "voucher2Regular"
      );

      // Hanya tambahkan border merah jika voucher ada dan tidak valid
      const hasVoucher =
        produk.voucherSelections?.voucher2Regular !== null &&
        produk.voucherSelections?.voucher2Regular !== undefined;

      const errorClass =
        hasVoucher && !validationStatus.isValid
          ? "tw-border-red-500 tw-border tw-rounded-md"
          : "";

      return h(
        "div",
        {
          class: `tw-w-full tw-flex tw-justify-center tw-items-center ${errorClass}`,
          title: !validationStatus.isValid ? validationStatus.reason || "" : ""
        },
        [
          h(
            "div",
            {
              class:
                "tw-flex tw-flex-col tw-items-center tw-justify-center tw-text-center tw-py-1"
            },
            [
              // Baris persentase
              h(
                "div",
                {
                  class:
                    "tw-flex tw-items-center tw-justify-center tw-text-center tw-w-full"
                },
                [
                  h("span", {
                    class: "tw-text-xs tw-text-center",
                    innerText: checkNaN(diskonPersen)
                  }),
                  h("span", {
                    class: "tw-text-xs",
                    innerText: "%"
                  })
                ]
              ),
              // Baris nilai rupiah dengan warna merah jika tidak valid
              h("span", {
                class: `tw-text-xs tw-text-center ${
                  hasVoucher && !validationStatus.isValid
                    ? "tw-text-red-500 tw-font-medium"
                    : "tw-text-blue-400"
                }`,
                innerText: "Rp." + parseCurrency(checkNaN(diskonValue))
              })
            ]
          )
        ]
      );
    },
    header: () =>
      h("span", {
        class: "tw-w-full tw-flex tw-justify-center",
        innerText: "V2R"
      })
  }),

  // Kolom Voucher 3 Reguler
  columnHelper.accessor("v3r", {
    id: "v3r",
    cell: (info) => {
      const produk = info.row.original;
      const hasValidQuantity =
        produk.uom1 > 0 || produk.uom2 > 0 || produk.uom3 > 0;
      const diskonValue = hasValidQuantity
        ? produk.discountDetails?.diskon3Regular || 0
        : 0;
      const voucher = produk.voucherSelections?.voucher3Regular;
      const diskonPersen = hasValidQuantity
        ? voucher?.persentase_diskon_3 || 0
        : 0;

      // Dapatkan status validasi voucher
      const validationStatus = getVoucherValidationStatus(
        produk,
        "voucher3Regular"
      );

      // Hanya tambahkan border merah jika voucher ada dan tidak valid
      const hasVoucher =
        produk.voucherSelections?.voucher3Regular !== null &&
        produk.voucherSelections?.voucher3Regular !== undefined;

      const errorClass =
        hasVoucher && !validationStatus.isValid
          ? "tw-border-red-500 tw-border tw-rounded-md"
          : "";

      return h(
        "div",
        {
          class: `tw-w-full tw-flex tw-justify-center tw-items-center ${errorClass}`,
          title: !validationStatus.isValid ? validationStatus.reason || "" : ""
        },
        [
          h(
            "div",
            {
              class:
                "tw-flex tw-flex-col tw-items-center tw-justify-center tw-text-center tw-py-1"
            },
            [
              // Baris persentase
              h(
                "div",
                {
                  class:
                    "tw-flex tw-items-center tw-justify-center tw-text-center tw-w-full"
                },
                [
                  h("span", {
                    class: "tw-text-xs tw-text-center",
                    innerText: checkNaN(diskonPersen)
                  }),
                  h("span", {
                    class: "tw-text-xs",
                    innerText: "%"
                  })
                ]
              ),
              // Baris nilai rupiah dengan warna merah jika tidak valid
              h("span", {
                class: `tw-text-xs tw-text-center ${
                  hasVoucher && !validationStatus.isValid
                    ? "tw-text-red-500 tw-font-medium"
                    : "tw-text-blue-400"
                }`,
                innerText: "Rp." + parseCurrency(checkNaN(diskonValue))
              })
            ]
          )
        ]
      );
    },
    header: () =>
      h("span", {
        class: "tw-w-full tw-flex tw-justify-center",
        innerText: "V3R"
      })
  }),

  // Kolom Voucher 2 Produk
  columnHelper.accessor("v2p", {
    id: "v2p",
    cell: (info) => {
      const produk = info.row.original;
      const diskonValue = produk.discountDetails?.diskon2Product || 0;
      const voucher = produk.voucherSelections?.voucher2Product;

      // Menyiapkan nilai yang akan ditampilkan
      let diskonDisplay;
      let labelText;

      if (voucher) {
        if (voucher.kategori_voucher === 1) {
          // Kategori 1: Tampilkan persentase
          diskonDisplay = voucher.persentase_diskon_2 || 0;
          labelText = "%";
        } else if (voucher.kategori_voucher === 2) {
          // Kategori 2: Tampilkan nominal diskon per satuan
          diskonDisplay = parseCurrency(voucher.nominal_diskon || 0);
          labelText = ``;
        } else {
          diskonDisplay = 0;
          labelText = "";
        }
      } else {
        diskonDisplay = 0;
        labelText = "";
      }

      // Dapatkan status validasi voucher
      const validationStatus = getVoucherValidationStatus(
        produk,
        "voucher2Product"
      );

      // Hanya tambahkan border merah jika voucher ada dan tidak valid
      const hasVoucher =
        produk.voucherSelections?.voucher2Product !== null &&
        produk.voucherSelections?.voucher2Product !== undefined;

      const errorClass =
        hasVoucher && !validationStatus.isValid
          ? "tw-border-red-500 tw-border tw-rounded-md"
          : "";

      return h(
        "div",
        {
          class: `tw-w-full tw-flex tw-justify-center tw-items-center ${errorClass}`,
          title: !validationStatus.isValid ? validationStatus.reason || "" : ""
        },
        [
          h(
            "div",
            {
              class:
                "tw-flex tw-flex-col tw-items-center tw-justify-center tw-text-center tw-py-1"
            },
            [
              // Baris nilai dan label
              h(
                "div",
                {
                  class:
                    "tw-flex tw-items-center tw-justify-center tw-text-center tw-w-full"
                },
                [
                  h("span", {
                    class: "tw-text-xs tw-text-center",
                    innerText: checkNaN(diskonDisplay)
                  }),
                  h("span", {
                    class: "tw-text-xs",
                    innerText: labelText
                  })
                ]
              ),
              // Baris nilai rupiah dengan warna merah jika tidak valid
              h("span", {
                class: `tw-text-xs tw-text-center ${
                  hasVoucher && !validationStatus.isValid
                    ? "tw-text-red-500 tw-font-medium"
                    : "tw-text-blue-400"
                }`,
                innerText: "Rp." + parseCurrency(checkNaN(diskonValue))
              })
            ]
          )
        ]
      );
    },
    header: () =>
      h("span", {
        class: "tw-w-full tw-flex tw-justify-center",
        innerText: "V2P"
      })
  }),

  // Kolom Voucher 3 Produk
  columnHelper.accessor("v3p", {
    id: "v3p",
    cell: (info) => {
      const produk = info.row.original;
      const diskonValue = produk.discountDetails?.diskon3Product || 0;
      const voucher = produk.voucherSelections?.voucher3Product;

      // Menyiapkan nilai yang akan ditampilkan
      let diskonDisplay;
      let labelText;

      if (voucher) {
        if (voucher.kategori_voucher === 1) {
          // Kategori 1: Tampilkan persentase
          diskonDisplay = voucher.persentase_diskon_3 || 0;
          labelText = "%";
        } else if (voucher.kategori_voucher === 2) {
          // Kategori 2: Tampilkan nominal diskon per satuan
          diskonDisplay = parseCurrency(voucher.nominal_diskon || 0);
          labelText = ``;
        } else {
          diskonDisplay = 0;
          labelText = "";
        }
      } else {
        diskonDisplay = 0;
        labelText = "";
      }

      // Dapatkan status validasi voucher
      const validationStatus = getVoucherValidationStatus(
        produk,
        "voucher3Product"
      );

      // Hanya tambahkan border merah jika voucher ada dan tidak valid
      const hasVoucher =
        produk.voucherSelections?.voucher3Product !== null &&
        produk.voucherSelections?.voucher3Product !== undefined;

      const errorClass =
        hasVoucher && !validationStatus.isValid
          ? "tw-border-red-500 tw-border tw-rounded-md"
          : "";

      return h(
        "div",
        {
          class: `tw-w-full tw-flex tw-justify-center tw-items-center ${errorClass}`,
          title: !validationStatus.isValid ? validationStatus.reason || "" : ""
        },
        [
          h(
            "div",
            {
              class:
                "tw-flex tw-flex-col tw-items-center tw-justify-center tw-text-center tw-py-1"
            },
            [
              // Baris nilai dan label
              h(
                "div",
                {
                  class:
                    "tw-flex tw-items-center tw-justify-center tw-text-center tw-w-full"
                },
                [
                  h("span", {
                    class: "tw-text-xs tw-text-center",
                    innerText: checkNaN(diskonDisplay)
                  }),
                  h("span", {
                    class: "tw-text-xs",
                    innerText: labelText
                  })
                ]
              ),
              // Baris nilai rupiah dengan warna merah jika tidak valid
              h("span", {
                class: `tw-text-xs tw-text-center ${
                  hasVoucher && !validationStatus.isValid
                    ? "tw-text-red-500 tw-font-medium"
                    : "tw-text-blue-400"
                }`,
                innerText: "Rp." + parseCurrency(checkNaN(diskonValue))
              })
            ]
          )
        ]
      );
    },
    header: () =>
      h("span", {
        class: "tw-w-full tw-flex tw-justify-center",
        innerText: "V3P"
      })
  }),
  columnHelper.accessor("totalDisc", {
    id: "totalDisc",
    cell: (info) => {
      const produk = info.row.original;
      const totalDiskon = produk.totalDiskon || 0;

      return h(
        "div",
        {
          class: "tw-w-full tw-flex tw-justify-center tw-items-center"
        },
        [
          h(
            "div",
            {
              class:
                "tw-flex tw-flex-col tw-items-center tw-justify-center tw-text-center"
            },
            [
              h("span", {
                class: "tw-text-xs tw-text-center",
                innerText: "Rp. " + parseCurrency(totalDiskon)
              })
            ]
          )
        ]
      );
    },
    header: () =>
      h("span", {
        class: "tw-w-full tw-flex tw-justify-center",
        innerText: "Total Disc"
      })
  }),
  columnHelper.accessor("jumlahHarga", {
    id: "jumlahHarga",
    cell: (info) => {
      const produk = info.row.original;
      const jumlahHarga = produk.jumlahHarga || 0;
      const parse = parseCurrency(checkNaN(jumlahHarga));

      return h(
        "div",
        {
          class: "tw-w-full tw-flex tw-justify-center"
        },
        [
          h("span", {
            class: "tw-w-24 tw-text-xs tw-text-center",
            innerText: `Rp. ${parse}`
          })
        ]
      );
    },
    header: () =>
      h("span", {
        class: "tw-w-full tw-flex tw-justify-center",
        innerText: "Jml Harga"
      })
  })
];
