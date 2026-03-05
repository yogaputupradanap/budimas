import { fetchWithAuth, buildUrlWithParams, handleError, localDisk } from "../lib/utils";
import { baseService } from "./baseService";

class VoucherService extends baseService {
  #baseGetUrl;

  constructor() {
    super();
    this.#baseGetUrl = `/api/voucher`;
    this.serviceName = "voucher";
    this.endpoints = this.#baseGetUrl;
  }

  _getCurrentUser() {
    return localDisk.getLocalStorage("user");
  }

  async _fetch(method, url, payload = null, { wrapInArray = false, errorMessage } = {}) {
    try {
      const res = await fetchWithAuth(method, url, payload);
      return wrapInArray ? (Array.isArray(res) ? res : [res]) : res;
    } catch (error) {
      handleError(error, errorMessage);
    }
  }

  async getVouchers() {
    return this._fetch("GET", this.#baseGetUrl, null, { errorMessage: "Gagal mengambil data voucher" });
  }

  async insertVoucher(tipe, data) {
    return this._fetch("POST", `${this.#baseGetUrl}/${tipe}`, data, { errorMessage: "Gagal menambahkan voucher" });
  }

  async updateVoucher(tipe, data) {
    return this._fetch("PUT", `${this.#baseGetUrl}/${tipe}`, data, { errorMessage: "Gagal mengupdate voucher" });
  }

  async deleteVoucher(tipe) {
    return this._fetch("DELETE", `${this.#baseGetUrl}/${tipe}`, null, { errorMessage: "Gagal menghapus voucher" });
  }

  async declineProductVoucher(data) {
    return this._fetch("POST", `${this.#baseGetUrl}/tolak-voucher`, data, { errorMessage: "Gagal menolak voucher produk" });
  }

  async declineRegularVoucher(data) {
    return this._fetch("POST", `${this.#baseGetUrl}/tolak-voucher-regular`, data, { errorMessage: "Gagal menolak voucher regular" });
  }

  async useVoucher(data) {
    return this._fetch("POST", `${this.#baseGetUrl}/use-voucher`, data, { errorMessage: "Gagal menggunakan voucher" });
  }

  async getVoucherV1Regular() {
    return this._fetch("GET", `${this.#baseGetUrl}/get-v1-regular`, null, { errorMessage: "Gagal mengambil voucher reguler V1" });
  }

  async getVoucherV2Product(id_produk, params = {}) {
    const url = buildUrlWithParams(`${this.#baseGetUrl}/get-v2-product/${id_produk}`, params);
    return this._fetch("GET", url, null, { errorMessage: "Gagal mengambil voucher produk V2" });
  }

  async getVoucherV2Regular() {
    return this._fetch("GET", `${this.#baseGetUrl}/get-v2-regular`, null, { errorMessage: "Gagal mengambil voucher reguler V2" });
  }

  async getVoucherV3Product(id_produk, params = {}) {
    const url = buildUrlWithParams(`${this.#baseGetUrl}/get-v3-product/${id_produk}`, params);
    return this._fetch("GET", url, null, { errorMessage: "Gagal mengambil voucher produk V3" });
  }

  async getVoucherV3Regular() {
    return this._fetch("GET", `${this.#baseGetUrl}/get-v3-regular`, null, { errorMessage: "Gagal mengambil voucher reguler V3" });
  }

  async getVoucherById(tipe) {
    return this._fetch("GET", `${this.#baseGetUrl}/get-voucher-by-id/${tipe}`, null, { errorMessage: "Gagal mengambil voucher by ID" });
  }

  async getVoucherV2ProductAll() {
    return this._fetch("GET", `${this.#baseGetUrl}/get-v2-product-all`, null, { errorMessage: "Gagal mengambil semua voucher produk V2" });
  }

  async getVoucherV3ProductAll() {
    return this._fetch("GET", `${this.#baseGetUrl}/get-v3-product-all`, null, { errorMessage: "Gagal mengambil semua voucher produk V3" });
  }
}

const voucherService = new VoucherService();
export { voucherService };
