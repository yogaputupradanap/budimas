import { defineStore } from "pinia";
import { apiUrl, fetchWithAuth } from "../lib/utils";
import { useAlert } from "./alert";
import { useSales } from "./sales";
import { useKunjungan } from "./kunjungan";
import { useSalesRequest } from "./salesRequest";

export const useVoucher = defineStore("voucher", {
  state: () => ({
    // Voucher Reguler
    voucher1RegularList: [],
    voucher2RegularList: [],
    voucher3RegularList: [],
    // Voucher Produk
    voucher2ProductList: [],
    voucher3ProductList: [],
    loading: false,
    // Status untuk menyimpan voucher reguler yang terpilih di level aplikasi
    selectedRegularVouchers: {
      voucher1Regular: null,
      voucher2Regular: null,
      voucher3Regular: null,
    },
  }),
  actions: {
    // Reset store
    $reset() {
      this.voucher1RegularList = [];
      this.voucher2RegularList = [];
      this.voucher3RegularList = [];
      this.voucher2ProductList = [];
      this.voucher3ProductList = [];
      this.selectedRegularVouchers = {
        voucher1Regular: null,
        voucher2Regular: null,
        voucher3Regular: null,
      };
    },

    /**
     * Mendapatkan semua voucher untuk satu produk
     * @param {number} productId - ID produk
     * @returns {Object} - Object berisi voucher2Product dan voucher3Product
     */
    /**
     * Mendapatkan semua voucher untuk satu produk
     * @param {number} productId - ID produk
     * @returns {Object} - Object berisi voucher2Product dan voucher3Product
     */
    async getAllVouchersForProduct(productId) {
      const alert = useAlert();
      this.loading = true;

      try {
        // Reset daftar voucher produk
        this.voucher2ProductList = [];
        this.voucher3ProductList = [];

        // Dapatkan ID cabang dan ID customer yang diperlukan
        const sales = useSales();
        const kunjungan = useKunjungan();
        const branchId = sales.salesUser.id_cabang;
        const customerId = kunjungan.activeKunjungan.kunjungan.customer_id;

        if (!branchId || !customerId) {
          throw new Error(
            "ID Cabang dan ID Customer diperlukan untuk memuat voucher produk"
          );
        }

        const [v2p, v3p] = await Promise.all([
          this.getVoucher2Product(productId, branchId),
          this.getVoucher3Product(productId, branchId, customerId),
        ]);

        return {
          voucher2Product: this.voucher2ProductList,
          voucher3Product: this.voucher3ProductList,
        };
      } catch (error) {
        console.error("Error getting vouchers for product:", error);
        alert.setMessage(`Error: ${error}`, "danger");
        return { voucher2Product: [], voucher3Product: [] };
      } finally {
        this.loading = false;
      }
    },

    /**
     * Mendapatkan Voucher 1 Reguler
     */
    async getVoucher1Regular() {
      const alert = useAlert();
      this.loading = true;

      try {
        const response = await fetchWithAuth(
          "GET",
          `${apiUrl}/api/voucher/get-v1-regular`
        );
        this.voucher1RegularList = response;
        return response;
      } catch (error) {
        console.error("Error getting Voucher 1 Regular:", error);
        alert.setMessage(`Error: ${error}`, "danger");
        return [];
      } finally {
        this.loading = false;
      }
    },

    /**
     * Mendapatkan Voucher 2 Reguler
     */
    async getVoucher2Regular() {
      const alert = useAlert();
      this.loading = true;

      try {
        const response = await fetchWithAuth(
          "GET",
          `${apiUrl}/api/voucher/get-v2-regular`
        );
        this.voucher2RegularList = response;
        return response;
      } catch (error) {
        console.error("Error getting Voucher 2 Regular:", error);
        alert.setMessage(`Error: ${error}`, "danger");
        return [];
      } finally {
        this.loading = false;
      }
    },

    /**
     * Mendapatkan Voucher 3 Reguler
     */
    async getVoucher3Regular() {
      const alert = useAlert();
      this.loading = true;

      try {
        const response = await fetchWithAuth(
          "GET",
          `${apiUrl}/api/voucher/get-v3-regular`
        );
        this.voucher3RegularList = response;
        return response;
      } catch (error) {
        console.error("Error getting Voucher 3 Regular:", error);
        alert.setMessage(`Error: ${error}`, "danger");
        return [];
      } finally {
        this.loading = false;
      }
    },

    /**
     * Mendapatkan Voucher 2 untuk produk tertentu
     * @param {number} productId - ID produk
     * @param {number} branchId - ID cabang
     */
    async getVoucher2Product(productId, branchId) {
      const alert = useAlert();

      try {
        const response = await fetchWithAuth(
          "GET",
          `${apiUrl}/api/voucher/get-v2-product/${productId}?id_cabang=${branchId}`
        );
        this.voucher2ProductList = response;
        return response;
      } catch (error) {
        console.error("Error getting Voucher 2 Product:", error);
        alert.setMessage(`Error: ${error}`, "danger");
        return [];
      }
    },

    /**
     * Mendapatkan Voucher 3 untuk produk tertentu
     * @param {number} productId - ID produk
     * @param {number} branchId - ID cabang
     * @param {number} customerId - ID customer
     */
    async getVoucher3Product(productId, branchId, customerId) {
      const alert = useAlert();

      try {
        const url = `${apiUrl}/api/voucher/get-v3-product/${productId}?id_cabang=${branchId}&id_customer=${customerId}`;
        const response = await fetchWithAuth("GET", url);
        this.voucher3ProductList = response;
        return response;
      } catch (error) {
        console.error("Error getting Voucher 3 Product:", error);
        alert.setMessage(`Error: ${error}`, "danger");
        return [];
      }
    },
    async getVoucher2ProductAll() {
      const alert = useAlert();

      try {
        const response = await fetchWithAuth(
          "GET",
          `${apiUrl}/api/voucher/get-v2-product-all`
        );
        return response;
      } catch (error) {
        console.error("Error getting Voucher 3 Product:", error);
        alert.setMessage(`Error: ${error}`, "danger");
        return [];
      }
    },
    async getVoucher3ProductAll() {
      const alert = useAlert();

      try {
        const response = await fetchWithAuth(
          "GET",
          `${apiUrl}/api/voucher/get-v3-product-all`
        );
        return response;
      } catch (error) {
        console.error("Error getting Voucher 3 Product:", error);
        alert.setMessage(`Error: ${error}`, "danger");
        return [];
      }
    },

    /**
     * Set voucher reguler terpilih
     * @param {Object} vouchers - Objek berisi voucher1Regular, voucher2Regular, voucher3Regular
     */
    setSelectedRegularVouchers(vouchers) {
      this.selectedRegularVouchers = {
        voucher1Regular: vouchers.voucher1Regular || null,
        voucher2Regular: vouchers.voucher2Regular || null,
        voucher3Regular: vouchers.voucher3Regular || null,
      };
    },

    /**
     * Mengaplikasikan semua voucher (reguler dan produk) ke semua produk
     * @param {Object} allVouchers - Semua voucher yang akan diaplikasikan
     */
    applyAllVouchersToProducts(allVouchers) {
      const salesRequestStore = useSalesRequest();

      // Iterasi semua produk
      salesRequestStore.initialProducts.forEach((product) => {
        product.voucherSelections = {
          ...product.voucherSelections,
          ...allVouchers,
        };

        // Recalculate discount
        salesRequestStore.recalculateProductDiscount(product);
      });

      // Update tableKey untuk memaksa render ulang
      salesRequestStore.tableKey++;
    },
    /**
     * Mengaplikasikan voucher ke produk tertentu
     * @param {Object} product - Produk yang akan diaplikasikan voucher
     * @param {Object} voucherSelections - Objek berisi pilihan voucher
     * @returns {Object} - Produk yang sudah diupdate dengan voucher
     */
    async applyVouchersToSingleProduct(product, voucherSelections) {
      // Dapatkan store yang dibutuhkan
      const salesRequestStore = useSalesRequest();

      // Update voucherSelections untuk produk
      product.voucherSelections = {
        ...product.voucherSelections,
        ...voucherSelections,
      };

      // Recalculate product discount
      salesRequestStore.recalculateProductDiscount(product);

      return product;
    },

    /**
     * Mendapatkan voucher reguler terpilih
     * @returns {Object} - Objek berisi voucher reguler yang terpilih
     */
    getSelectedRegularVouchers() {
      return this.selectedRegularVouchers;
    },
  },
});
