import { defineStore } from "pinia";
import { usePrincipal } from "./principal";
import { useVoucher } from "./voucher";
import { calculateTotalDiscount } from "../lib/calculateVoucher";
import { useAlert } from "./alert";

export const useSalesRequest = defineStore("salesRequest", {
  state: () => ({
    initialProducts: [],
    tableKey: 0,
    loading: true,
    error: null,
    // Tambahkan properti untuk melacak validasi voucher
    voucherValidationResults: {}
  }),
  actions: {
    /**
     * Asynchronously fetches sales request data and updates the component state with the retrieved data.
     * @returns None
     */
    async getSalesRequest() {
      const principalStore = usePrincipal();
      const voucherStore = useVoucher();
      this.loading = true;

      try {
        // Pastikan produk principal sudah dimuat jika belum
        if (
          !principalStore.principalProduct.products ||
          principalStore.principalProduct.products.length === 0
        ) {
          await principalStore.getPrincipalProducts();
        }

        this.initialProducts = principalStore.principalProduct.products.map(
          (product) => {
            return {
              ...product,
              uom3: 0,
              uom2: 0,
              uom1: 0,
              totalHarga: 0,
              jumlahHarga: 0,
              totalDiskon: 0,
              ppnValue: 0,
              voucherSelections: {
                voucher1Regular: null,
                voucher2Regular: null,
                voucher3Regular: null,
                voucher2Product: null,
                voucher3Product: null
              },
              discountDetails: {
                diskon1Regular: 0,
                diskon2Regular: 0,
                diskon3Regular: 0,
                diskon2Product: 0,
                diskon3Product: 0
              },
              // Tambahkan properti untuk menyimpan hasil validasi voucher
              voucherValidations: {
                voucher1Regular: { isValid: true, reason: null },
                voucher2Regular: { isValid: true, reason: null },
                voucher3Regular: { isValid: true, reason: null },
                voucher2Product: { isValid: true, reason: null },
                voucher3Product: { isValid: true, reason: null }
              }
            };
          }
        );
      } catch (error) {
        console.error("Error in getSalesRequest:", error);
        this.error = error.message || "Terjadi kesalahan saat memuat data";
      } finally {
        this.loading = false;
        this.tableKey++;
      }
    },

    /**
     * Menerapkan voucher reguler ke semua produk
     * @param {Object} regularVouchers - Objek berisi voucher1Regular, voucher2Regular, voucher3Regular
     * @returns {Object} Hasil validasi voucher
     */
    applyRegularVouchersToAllProducts(regularVouchers) {
      const alert = useAlert();

      // Objek untuk melacak hasil validasi voucher
      const validationResults = {
        hasInvalidVouchers: false,
        invalidProducts: []
      };

      // Hitung subtotal semua produk untuk validasi voucher reguler
      const currentSubtotal = this.getCurrentSubtotal();

      // Validasi minimal subtotal untuk voucher reguler
      let hasInvalidRegularVoucher = false;

      // Validasi voucher 1 regular
      if (
        regularVouchers.voucher1Regular &&
        regularVouchers.voucher1Regular.minimal_subtotal_pembelian &&
        currentSubtotal <
        regularVouchers.voucher1Regular.minimal_subtotal_pembelian
      ) {


        validationResults.hasInvalidVouchers = true;
        validationResults.invalidProducts.push({
          productName: "Semua Produk",
          productId: "all",
          invalidVouchers: [
            {
              type: "voucher1Regular",
              reason: `Total pembelian (${currentSubtotal}) kurang dari minimal subtotal (${regularVouchers.voucher1Regular.minimal_subtotal_pembelian})`
            }
          ]
        });

        // Reset voucher yang tidak valid
        regularVouchers.voucher1Regular = null;
        hasInvalidRegularVoucher = true;
      }

      // Validasi voucher 2 regular
      if (
        regularVouchers.voucher2Regular &&
        regularVouchers.voucher2Regular.minimal_subtotal_pembelian &&
        currentSubtotal <
        regularVouchers.voucher2Regular.minimal_subtotal_pembelian
      ) {


        validationResults.hasInvalidVouchers = true;
        validationResults.invalidProducts.push({
          productName: "Semua Produk",
          productId: "all",
          invalidVouchers: [
            {
              type: "voucher2Regular",
              reason: `Total pembelian (${currentSubtotal}) kurang dari minimal subtotal (${regularVouchers.voucher2Regular.minimal_subtotal_pembelian})`
            }
          ]
        });

        // Reset voucher yang tidak valid
        regularVouchers.voucher2Regular = null;
        hasInvalidRegularVoucher = true;
      }

      // Validasi voucher 3 regular
      if (
        regularVouchers.voucher3Regular &&
        regularVouchers.voucher3Regular.minimal_subtotal_pembelian &&
        currentSubtotal <
        regularVouchers.voucher3Regular.minimal_subtotal_pembelian
      ) {


        validationResults.hasInvalidVouchers = true;
        validationResults.invalidProducts.push({
          productName: "Semua Produk",
          productId: "all",
          invalidVouchers: [
            {
              type: "voucher3Regular",
              reason: `Total pembelian (${currentSubtotal}) kurang dari minimal subtotal (${regularVouchers.voucher3Regular.minimal_subtotal_pembelian})`
            }
          ]
        });

        // Reset voucher yang tidak valid
        regularVouchers.voucher3Regular = null;
        hasInvalidRegularVoucher = true;
      }

      console.log("this.initialProducts", this.initialProducts);
      console.log("regularVouchers", regularVouchers);
      // Iterasi semua produk dan terapkan voucher reguler
      this.initialProducts.forEach((product, index) => {

        const isValidPrincipal = () => {
          if (!regularVouchers.voucher1Regular && !regularVouchers.voucher2Regular && !regularVouchers.voucher3Regular) {
            return true; // Tidak ada voucher reguler yang diterapkan, jadi valid
          } else {
            return regularVouchers.voucher1Regular?.id_principal === product.id_principal ||
              regularVouchers.voucher2Regular?.id_principal === product.id_principal ||
              regularVouchers.voucher3Regular?.id_principal === product.id_principal;
          }
        };
        if (!isValidPrincipal()) return;

        // Hanya terapkan voucher jika produk memiliki kuantitas
        if (product.uom1 > 0 || product.uom2 > 0 || product.uom3 > 0) {
          // Deep clone seluruh product.voucherSelections
          const existingVoucherSelections = product.voucherSelections
            ? JSON.parse(JSON.stringify(product.voucherSelections))
            : {
              voucher1Regular: null,
              voucher2Regular: null,
              voucher3Regular: null,
              voucher2Product: null,
              voucher3Product: null
            };

          // Deep clone regularVouchers untuk menghindari referensi ke objek yang sama
          const clonedRegularVouchers = {
            voucher1Regular: regularVouchers.voucher1Regular
              ? JSON.parse(JSON.stringify(regularVouchers.voucher1Regular))
              : null,
            voucher2Regular: regularVouchers.voucher2Regular
              ? JSON.parse(JSON.stringify(regularVouchers.voucher2Regular))
              : null,
            voucher3Regular: regularVouchers.voucher3Regular
              ? JSON.parse(JSON.stringify(regularVouchers.voucher3Regular))
              : null
          };

          // Update voucherSelections dengan voucher reguler baru
          product.voucherSelections = {
            // Pertahankan voucher produk yang sudah ada
            voucher2Product: existingVoucherSelections.voucher2Product || null,
            voucher3Product: existingVoucherSelections.voucher3Product || null,
            // Update voucher reguler dengan deep clone
            voucher1Regular: clonedRegularVouchers.voucher1Regular || null,
            voucher2Regular: clonedRegularVouchers.voucher2Regular || null,
            voucher3Regular: clonedRegularVouchers.voucher3Regular || null
          };

          // Recalculate discount untuk produk ini
          const result = this.recalculateProductDiscount(product);

          // Periksa hasil validasi
          if (result && result.hasInvalidVoucher) {
            validationResults.hasInvalidVouchers = true;

            // Kumpulkan voucher yang tidak valid
            const invalidVouchers = [];
            for (const [voucherType, validation] of Object.entries(
              result.voucherValidations
            )) {
              if (!validation.isValid) {
                invalidVouchers.push({
                  type: voucherType,
                  reason: validation.reason
                });

                // Reset voucher yang tidak valid
                product.voucherSelections[voucherType] = null;
              }
            }

            // Jika ada voucher yang tidak valid, tambahkan ke daftar produk dengan voucher tidak valid
            if (invalidVouchers.length > 0) {
              validationResults.invalidProducts.push({
                productName: product.nama,
                productId: product.id,
                invalidVouchers
              });

              // Hitung ulang diskon setelah reset voucher tidak valid
              this.recalculateProductDiscount(product);
            }
          }
        }
      });

      this.tableKey++;
      return validationResults;
    },

    /**
     * Menghitung ulang diskon untuk satu produk
     * @param {Object} product - Produk yang akan dihitung ulang diskonnya
     * @returns {Object} Hasil perhitungan diskon termasuk validasi
     */
    recalculateProductDiscount(product) {


      // Hitung total harga dasar
      const totalHarga = this.calculateBasePrice(product);
      product.totalHarga = totalHarga;


      if (totalHarga <= 0) {
        product.totalDiskon = 0;
        product.jumlahHarga = 0;
        product.discountDetails = {
          diskon1Regular: 0,
          diskon2Regular: 0,
          diskon3Regular: 0,
          diskon2Product: 0,
          diskon3Product: 0
        };
        product.voucherValidations = {
          voucher1Regular: { isValid: true, reason: null },
          voucher2Regular: { isValid: true, reason: null },
          voucher3Regular: { isValid: true, reason: null },
          voucher2Product: { isValid: true, reason: null },
          voucher3Product: { isValid: true, reason: null }
        };
        return { hasInvalidVoucher: false };
      }

      // Deep clone seluruh voucherSelections untuk mencegah efek samping
      const voucherSelectionsTemp = product.voucherSelections
        ? JSON.parse(JSON.stringify(product.voucherSelections))
        : {
          voucher1Regular: null,
          voucher2Regular: null,
          voucher3Regular: null,
          voucher2Product: null,
          voucher3Product: null
        };

      // Hitung diskon
      const discountResult = calculateTotalDiscount(
        voucherSelectionsTemp,
        totalHarga,
        product
      );


      // Update voucherSelections dengan hasil validasi
      product.voucherSelections = JSON.parse(
        JSON.stringify(voucherSelectionsTemp)
      );

      // Simpan hasil validasi voucher
      product.voucherValidations = discountResult.voucherValidations || {
        voucher1Regular: { isValid: true, reason: null },
        voucher2Regular: { isValid: true, reason: null },
        voucher3Regular: { isValid: true, reason: null },
        voucher2Product: { isValid: true, reason: null },
        voucher3Product: { isValid: true, reason: null }
      };

      // Update discount details dengan hasil perhitungan
      product.discountDetails = discountResult.discountDetails || {
        diskon1Regular: 0,
        diskon2Regular: 0,
        diskon3Regular: 0,
        diskon2Product: 0,
        diskon3Product: 0
      };

      product.totalDiskon = discountResult.totalDiskon || 0;
      product.jumlahHarga = discountResult.hargaSetelahDiskon || totalHarga;

      // Hitung PPn jika ada
      if (product.ppn) {
        product.ppnValue = (product.jumlahHarga * product.ppn) / 100;
      } else {
        product.ppnValue = 0;
      }


      return {
        hasInvalidVoucher: discountResult.hasInvalidVoucher || false,
        voucherValidations: product.voucherValidations
      };
    },

    /**
     * Menghitung harga dasar produk (sebelum diskon)
     * @param {Object} product - Produk
     * @returns {number} Harga dasar
     */
    calculateBasePrice(product) {
      const piecesPrice = (product.uom1 || 0) * product.harga_jual;
      const boxPrice =
        (product.uom2 || 0) * product.harga_jual * (product.konversi_2 || 1);
      const kartonPrice =
        (product.uom3 || 0) * product.harga_jual * (product.konversi_3 || 1);

      return piecesPrice + boxPrice + kartonPrice;
    },

    /**
     * Menerapkan voucher produk ke produk tertentu
     * @param {number} productId - ID produk yang akan diterapkan voucher
     * @param {Object} productVouchers - Objek berisi voucher2Product, voucher3Product
     * @returns {Object} Hasil penerapan voucher termasuk validasi
     */
    applyProductVouchersToProduct(productId, productVouchers) {


      const productIndex = this.initialProducts.findIndex(
        (p) => p.id === productId
      );
      if (productIndex === -1) {
        return {
          success: false,
          error: "Produk tidak ditemukan",
          validationResults: null
        };
      }

      // Dapatkan produk
      const product = this.initialProducts[productIndex];

      // Deep clone untuk menghindari referensi objek yang sama
      const existingVoucherSelections = product.voucherSelections
        ? JSON.parse(JSON.stringify(product.voucherSelections))
        : {
          voucher1Regular: null,
          voucher2Regular: null,
          voucher3Regular: null,
          voucher2Product: null,
          voucher3Product: null
        };


      // Deep clone productVouchers yang diberikan
      const clonedProductVouchers = {
        voucher2Product: productVouchers.voucher2Product
          ? JSON.parse(JSON.stringify(productVouchers.voucher2Product))
          : null,
        voucher3Product: productVouchers.voucher3Product
          ? JSON.parse(JSON.stringify(productVouchers.voucher3Product))
          : null
      };

      // Update voucherSelections untuk produk dengan deep clone
      product.voucherSelections = {
        // Pertahankan voucher reguler yang ada
        voucher1Regular: existingVoucherSelections.voucher1Regular || null,
        voucher2Regular: existingVoucherSelections.voucher2Regular || null,
        voucher3Regular: existingVoucherSelections.voucher3Regular || null,
        // Update voucher produk
        voucher2Product: clonedProductVouchers.voucher2Product || null,
        voucher3Product: clonedProductVouchers.voucher3Product || null
      };


      let validationResults = null;

      // Recalculate diskon jika produk memiliki kuantitas
      if (product.uom1 > 0 || product.uom2 > 0 || product.uom3 > 0) {

        // Recalculate discount
        validationResults = this.recalculateProductDiscount(product);

        // Jika ada voucher yang tidak valid, reset voucher tersebut
        if (validationResults.hasInvalidVoucher) {
          const invalidVouchers = [];

          // Cek voucher mana yang tidak valid
          for (const [voucherType, validation] of Object.entries(
            validationResults.voucherValidations
          )) {
            if (!validation.isValid) {
              invalidVouchers.push({
                type: voucherType,
                reason: validation.reason
              });

              // Reset voucher yang tidak valid
              product.voucherSelections[voucherType] = null;
            }
          }

          // Hitung ulang setelah reset voucher yang tidak valid
          if (invalidVouchers.length > 0) {
            this.recalculateProductDiscount(product);
          }
        }
      }

      this.tableKey++;

      return {
        success: true,
        validationResults
      };
    },

    /**
     * Mendapatkan subtotal pembelian saat ini untuk validasi voucher
     * @returns {number} - Total subtotal pembelian
     */
    getCurrentSubtotal() {
      return this.initialProducts.reduce((total, product) => {
        const productTotal = this.calculateBasePrice(product);
        return total + productTotal;
      }, 0);
    },

    /**
     * Mendapatkan produk dengan voucher tidak valid
     * @returns {Array} Array produk dengan voucher tidak valid
     */
    getProductsWithInvalidVouchers() {
      const invalidProducts = [];

      this.initialProducts.forEach((product) => {
        if (!product.voucherValidations) return;

        const invalidVouchers = [];
        for (const [voucherType, validation] of Object.entries(
          product.voucherValidations
        )) {
          if (!validation.isValid && product.voucherSelections[voucherType]) {
            invalidVouchers.push({
              type: voucherType,
              reason: validation.reason
            });
          }
        }

        if (invalidVouchers.length > 0) {
          invalidProducts.push({
            productId: product.id,
            productName: product.nama,
            invalidVouchers
          });
        }
      });

      return invalidProducts;
    },

    /**
     * Clear product list
     */
    clearInitialProducts() {
      this.initialProducts = [];
    }
  }
});
