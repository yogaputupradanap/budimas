import { fetchWithAuth } from "../lib/utils";
import { baseService } from "./baseService";

class PromoService extends baseService {
    constructor() {
        super();
        this.endpoints = {
            promo: `/api/promo`,
            promoListFaktur: `/api/promo/list-faktur`,
            generateKlaimCode: `/api/promo/generate-code`,
            klaimKategori: `/api/promo/klaim-kategori`,
            logPenggunaanPromo: `/api/promo/log-penggunaan`,
            klaimPromo: `/api/promo/klaim-promo`,
            kasbonKlaim: `/api/promo/kasbon-klaim`,
        };
        this.setServiceName("promo");
    }

    _buildUrlWithParams(baseUrl, params = {}) {
        const queryParams = new URLSearchParams();
        Object.keys(params).forEach(key => {
            if (params[key] !== undefined && params[key] !== null) {
                queryParams.append(key, params[key]);
            }
        });
        return queryParams.toString() ? `${baseUrl}?${queryParams.toString()}` : baseUrl;
    }

    _handleError(error, errorMessage) {
        console.log("error in service : ", error);
        this.throwError(`${errorMessage}: ${error.message}`);
        throw error;
    }

    async _fetch(method, url, payload = null, { wrapInArray = false, errorMessage } = {}) {
        try {
            const res = await fetchWithAuth(method, url, payload);
            return wrapInArray ? (Array.isArray(res) ? res : [res]) : res;
        } catch (error) {
            this._handleError(error, errorMessage);
        }
    }

    async getDropdownData() {
        const url = `${this.endpoints.promo}/dropdown-data`;
        return this._fetch("GET", url, null, {
            wrapInArray: true,
            errorMessage: "error while fetching promo dropdown data"
        });
    }

    async getDropdownDataLog() {
        const url = `${this.endpoints.promo}/dropdown-data-log`;
        return this._fetch("GET", url, null, {
            errorMessage: "error while fetching log dropdown data"
        });
    }

    async getDropdownDataKlaim(status_klaim = null) {
        let conditions = status_klaim ? `?status_klaim=${status_klaim}` : "";
        const url = `${this.endpoints.promo}/dropdown-data-klaim${conditions}`;
        return this._fetch("GET", url, null, {
            errorMessage: "error while fetching klaim dropdown data"
        });
    }

    async generateKlaimCode(payload) {
        const url = this.endpoints.generateKlaimCode;
        return this._fetch("POST", url, payload, {
            errorMessage: "error while generating klaim code"
        });
    }

    async updateKlaimStatus(payload) {
        const url = `${this.endpoints.klaimPromo}/update-status/${payload.id}`;
        return this._fetch("PUT", url, payload, {
            errorMessage: "error while updating klaim status"
        });
    }

    async getListFaktur(params = {}) {
        const baseUrl = this.endpoints.promoListFaktur;
        const url = this._buildUrlWithParams(baseUrl, params);
        return this._fetch("GET", url, null, {
            errorMessage: "error while fetching faktur list"
        });
    }

    async getKlaimKategori() {
        const url = this.endpoints.klaimKategori;
        return this._fetch("GET", url, null, {
            wrapInArray: true,
            errorMessage: "error while fetching klaim kategori"
        });
    }

    async getLogPenggunaanPromo(params = {}) {
        const baseUrl = this.endpoints.logPenggunaanPromo;
        const url = this._buildUrlWithParams(baseUrl, params);
        return this._fetch("GET", url, null, {
            errorMessage: "error while fetching log penggunaan promo"
        });
    }

    async getListKlaimPromo(params = {}) {
        const baseUrl = this.endpoints.klaimPromo;
        const url = this._buildUrlWithParams(baseUrl, params);
        return this._fetch("GET", url, null, {
            errorMessage: "error while fetching klaim promo list"
        });
    }

    async getListKasbonKlaim(params = {}) {
        const baseUrl = this.endpoints.kasbonKlaim;
        const url = this._buildUrlWithParams(baseUrl, params);
        return this._fetch("GET", url, null, {
            errorMessage: "error while fetching kasbon klaim list"
        });
    }

    async getKasbonKlaimDetail(id) {
        const url = `${this.endpoints.kasbonKlaim}/${id}`;
        return this._fetch("GET", url, null, {
            errorMessage: "error while fetching kasbon klaim detail"
        });
    }

    async getListKlaimForKasbonKlaim(id, params = {}) {
        const baseUrl = `${this.endpoints.kasbonKlaim}/${id}/klaim`;
        const url = this._buildUrlWithParams(baseUrl, params);
        return this._fetch("GET", url, null, {
            errorMessage: "error while fetching klaim for kasbon klaim"
        });
    }

    async getDetailPromo({ kode_promo } = {}) {
        const url = `${this.endpoints.promo}/${kode_promo}`;
        return this._fetch("GET", url, null, {
            wrapInArray: true,
            errorMessage: "error while fetching detail promo"
        });
    }

    async getKlaimDetail(id) {
        const url = `${this.endpoints.klaimPromo}/detail/${id}`;
        return this._fetch("GET", url, null, {
            errorMessage: "error while fetching klaim detail by kode"
        });
    }

    async postAjukanKlaim(payload) {
        const url = `${this.endpoints.promo}/ajukan-klaim`;
        return this._fetch("POST", url, payload, {
            errorMessage: "error while submitting klaim"
        });
    }

    async ajukanUlangKlaimData(payload) {
        const url = `${this.endpoints.promo}/ajukan-ulang-klaim`;
        return this._fetch("PUT", url, payload, {
            errorMessage: "error while submitting ulang klaim"
        });
    }

    async postAjukanKasbonKlaim(payload) {
        const url = `${this.endpoints.kasbonKlaim}/ajukan`;
        return this._fetch("POST", url, payload, {
            errorMessage: "error while submitting kasbon klaim"
        });
    }

    async konfirmasiDetailKasbonKlaim(id_kasbon_klaim, payload) {
        const url = `${this.endpoints.kasbonKlaim}/${id_kasbon_klaim}/konfirmasi`;
        return this._fetch("POST", url, payload, {
            errorMessage: "error while confirming kasbon klaim detail"
        });
    }
}

const promoService = new PromoService();
export { promoService };