import {defineStore} from "pinia";
import {apiUrl, fetchWithAuth, localDisk} from "../lib/utils";

const localRuteShipping = localDisk.getLocalStorage("rute_shipping");
const localFakturShipping = localDisk.getLocalStorage("faktur_shipping");
const localDetailShipping = localDisk.getLocalStorage("detail_shipping");
const localVoucherStatus = localDisk.getLocalStorage("voucher_status");
const localRuteRevisiFaktur = localDisk.getLocalStorage("rute_revisi_faktur");

const listRuteShipping = {
  ruteShipping: localRuteShipping || [],
  loading: false,
  error: null,
};

const listFakturShipping = {
 fakturShipping: [],
  fakturShippingInfo: null,
  loading: false,
  error: null
};

const listDetailFakturShipping = {
  // FIX: Ensure this is always initialized as an array if localDisk is empty
  detailFaktur: localDetailShipping || [], 
  detailFakturInfo: null,
  loading: false, // Changed to false by default to prevent early render crashes
  error: null,
};

// Sentralisasi status voucher untuk reguler dan produk
const voucherStatusStore = {
  // Status voucher reguler berlaku global untuk semua produk
  regulerStatus: {
    v1r_active: true,
    v2r_active: true,
    v3r_active: true,
  },
  // Status voucher produk dikelola per produk
  productStatus: localVoucherStatus || {},
  loading: false,
  error: null,
};

export const useShipping = defineStore("shipping", {
  state: () => ({
    listRuteShipping,
    isFromShipping: false,
    listFakturShipping,
    voucherStatusStore,
    isFromFakturShipping: false,
    listDetailFakturShipping,
  }),
  actions: {
    resetShippingState(stateName) {
      Object.assign(this[stateName], eval(stateName));
    },

    // Simpan status voucher reguler (global untuk semua produk)
    saveRegulerVoucherStatus(status) {
      this.voucherStatusStore.regulerStatus = {
        ...this.voucherStatusStore.regulerStatus,
        ...status,
      };
      this.persistVoucherStatus();
    },

    // Simpan status voucher produk untuk produk tertentu
    saveProductVoucherStatus(productId, status) {
      if (!this.voucherStatusStore.productStatus) {
        this.voucherStatusStore.productStatus = {};
      }

      this.voucherStatusStore.productStatus[productId] = {
        ...(this.voucherStatusStore.productStatus[productId] || {}),
        ...status,
      };

      this.persistVoucherStatus();
    },

    // Simpan status voucher ke localStorage
    persistVoucherStatus() {
      localDisk.setLocalStorage(
        "voucher_status",
        this.voucherStatusStore.productStatus
      );
    },

    // Reset semua status voucher
    resetVoucherStatus() {
      this.voucherStatusStore.regulerStatus = {
        v1r_active: true,
        v2r_active: true,
        v3r_active: true,
      };

      this.voucherStatusStore.productStatus = {};
      this.persistVoucherStatus();
    },

    // Dapatkan status voucher gabungan untuk produk tertentu (menggabungkan reguler dan produk)
    getVoucherStatusForProduct(productId) {
      const regulerStatus = this.voucherStatusStore.regulerStatus;
      const productSpecificStatus =
        this.voucherStatusStore.productStatus[productId] || {};

      return {
        // Status voucher reguler (global)
        v1r_active: regulerStatus.v1r_active,
        v2r_active: regulerStatus.v2r_active,
        v3r_active: regulerStatus.v3r_active,

        // Status voucher produk (spesifik produk)
        v2p_active:
          productSpecificStatus.v2p_active !== undefined
            ? productSpecificStatus.v2p_active
            : true,
        v3p_active:
          productSpecificStatus.v3p_active !== undefined
            ? productSpecificStatus.v3p_active
            : true,
      };
    },

    async getListRuteShipping(id_cabang, isRealisasi = false) {
      const url = isRealisasi
        ? `${apiUrl}/api/distribusi/get-list-rute-realisasi/${id_cabang}`
        : `${apiUrl}/api/distribusi/get-list-rute-shipping/${id_cabang}`;

      try {
        this.listRuteShipping.loading = true;
        this.listRuteShipping.ruteShipping = await fetchWithAuth("GET", url);
        this.isFromShipping = true;
        localDisk.setLocalStorage(
          "rute_shipping",
          this.listRuteShipping.ruteShipping
        );
      } catch (error) {
        this.listRuteShipping.error = error;
        console.log(error);
      } finally {
        this.listRuteShipping.loading = false;
      }
    },

    async getListFakturShipping(
      id_cabang,
      id_rute,
      isRealisasi,
      id_armada,
      id_driver,
      delivering_date
    ) {
      try {
        this.listFakturShipping.loading = true;

        const url = isRealisasi
          ? `${apiUrl}/api/distribusi/get-list-faktur-realisasi?id_cabang=${id_cabang}&id_rute=${id_rute}&id_armada=${id_armada}&id_driver=${id_driver}&delivering_date=${delivering_date}`
          : `${apiUrl}/api/distribusi/get-list-faktur-shipping?id_cabang=${id_cabang}&id_rute=${id_rute}&id_armada=${id_armada}&id_driver=${id_driver}&delivering_date=${delivering_date}`;

        const fakturShipping = await fetchWithAuth("GET", url);

        this.listFakturShipping.fakturShipping =
          fakturShipping.list_faktur_shipping;

        this.listFakturShipping.fakturShippingInfo =
          fakturShipping.list_faktur_shipping_info;

        // console.log(
        //   "DATA TABLE FINAL",
        //   this.listFakturShipping.fakturShipping
        // );

        // console.log(
        //   "CHECK ARRAY",
        //   this.listFakturShipping.fakturShipping,
        //   Array.isArray(this.listFakturShipping.fakturShipping)
        // );

      } catch (error) {
        this.listFakturShipping.error = error;
        console.log(error);
      } finally {
        this.listFakturShipping.loading = false;
      }
    },


    async getListDetailFakturShipping(id_sales_order, id_order_batch, id_sales_orders) {
      try {
        this.resetVoucherStatus();
        this.listDetailFakturShipping.loading = true;

        let url = `${apiUrl}/api/distribusi/get-detail-faktur/${id_sales_order}`;
        if (id_order_batch) {
            url += `?id_order_batch=${id_order_batch}&id_sales_orders=${id_sales_orders}`;
        }

        const detailFakturShipping = await fetchWithAuth("GET", url);

        // FIX: Verify it is an array using Array.isArray
        const rawData = detailFakturShipping?.list_detail_order?.result; 
        const orders = Array.isArray(rawData) ? rawData : [];

        this.listDetailFakturShipping.detailFaktur = orders.map((val) => ({
          ...val,
        }));

        this.listDetailFakturShipping.detailFakturInfo = detailFakturShipping?.detail_faktur || null;

        localDisk.setLocalStorage(
          "detail_shipping",
          this.listDetailFakturShipping.detailFaktur
        );
      } catch (error) {
        this.listDetailFakturShipping.error = error;
        this.listDetailFakturShipping.detailFaktur = []; // Ensure state is reset on error
        console.error("Store Error:", error);
      } finally {
        this.listDetailFakturShipping.loading = false;
      }
    },


    async getListRuteRevisiFaktur(id_cabang) {
      try {
        const res = await fetchWithAuth(
          "GET",
          `${apiUrl}/api/distribusi/get-list-rute-revisi-faktur?id_cabang=${id_cabang}`
        );
        return res;
      } catch (error) {
        this.listRuteShipping.error = error;
        console.error("Error fetching data:", error);
      } finally {
        this.listRuteShipping.loading = false;
      }
    },
    async getListFakturRevisiFaktur(
      id_cabang,
      id_rute,
      id_armada,
      id_driver,
      delivering_date
    ) {
      try {
        this.listFakturShipping.loading = true;
        const res = await fetchWithAuth(
          "GET",
          `${apiUrl}/api/distribusi/get-list-faktur-revisi-faktur?id_cabang=${id_cabang}&id_rute=${id_rute}&id_armada=${id_armada}&id_driver=${id_driver}&delivering_date=${delivering_date}`
        );
        return res;
      } catch (error) {
        this.listFakturShipping.error = error;
        console.error("Error fetching data:", error);
      } finally {
        this.listFakturShipping.loading = false;
      }
    },
  },
});
