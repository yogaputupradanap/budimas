import { fetchWithAuth, buildUrlWithParams, handleError, localDisk } from "../lib/utils";
import { baseService } from "./baseService";

class salesCanvas extends baseService {
    #baseGetUrl
    #baseSalesCanvas
    #baseListProductCanvas
    #baseListOrderCanvas

    constructor() {
        super();
        this.#baseGetUrl = `/api/sales-canvas`;
        this.#baseSalesCanvas = `/all-canvas-request`;
        this.#baseListProductCanvas = `/list-product-canvas`;
        this.#baseListOrderCanvas = `/list-order-canvas`;
        this.serviceName = "salesCanvas";
        this.endpoints = this.#baseGetUrl
    }

    _getCurrentUser() { return localDisk.getLocalStorage("user"); }

    async _fetch(method, url, payload = null, { wrapInArray = false, errorMessage } = {}) {
        try {
            const res = await fetchWithAuth(method, url, payload);
            console.log('Response: ', res);
            return wrapInArray ? (Array.isArray(res) ? res : [res]) : res;
        } catch (error) {
            handleError(error, errorMessage);
        }
    }

    async _fetchWithUserId(path, errorMessage) {
        const user = this._getCurrentUser();
        
        // PERBAIKAN: Gunakan id_user sesuai dengan data dari backend
        const userId = user?.id_user || user?.id; 
        
        // Agar lebih aman bagi backend, kirim kedua varian parameter
        const url = buildUrlWithParams(`${this.#baseGetUrl}${path}`, { 
            id: userId, 
            id_user: userId 
        });
        
        return this._fetch("GET", url, null, { errorMessage });
    }

    async getDetailCanvasRequest(id_canvas, tanggal_request) {
        const user = this._getCurrentUser();
        const userId = user?.id_user || user?.id; // PERBAIKAN SAMA
        
        const params = { id_canvas, tanggal_request, id: userId, id_user: userId };
        const url = buildUrlWithParams(`${this.#baseGetUrl}/detail-canvas-request`, params);
        return this._fetch("GET", url, null, { errorMessage: "Data Detail Canvas Request tidak ditemukan" });
    }

    async getAllCanvasRequest() {
        return this._fetchWithUserId(this.#baseSalesCanvas, "Data Sales Canvas tidak ditemukan");
    }

    async getListProductCanvas() {
        return this._fetchWithUserId(this.#baseListProductCanvas, "Data List Product Canvas tidak ditemukan");
    }

    async getListOrderCanvas() {
        return this._fetchWithUserId(this.#baseListOrderCanvas, "Data List Order Canvas tidak ditemukan");
    }

    async createCanvasRequest(data) {
        const url = `${this.#baseGetUrl}/create-canvas-request`;
        return this._fetch("POST", url, data, { errorMessage: "Gagal membuat Canvas Request" });
    }

    async updateCanvasRequestTemp(data) {
        const url = `${this.#baseGetUrl}/update-canvas-request-temp`;
        return this._fetch("POST", url, data, { errorMessage: "Gagal menghitung Canvas Request" });
    }

    // async getDetailCanvasRequest(id_canvas, tanggal_request) {
    //     const user = this._getCurrentUser();
    //     const userId = user?.id;
    //     const params = { id_canvas, tanggal_request, id: userId };
    //     const url = buildUrlWithParams(`${this.#baseGetUrl}/detail-canvas-request`, params);
    //     return this._fetch("GET", url, null, { errorMessage: "Data Detail Canvas Request tidak ditemukan" });
    // }

    async updateCanvasData(data) {
        const url = `${this.#baseGetUrl}/confirm-edit-canvas-request`;
        return this._fetch("POST", url, data, { errorMessage: "Gagal mengupdate Canvas Request" });
    }

    async getAllCanvasOrder() {
        const url = `${this.#baseGetUrl}/all-canvas-order`;
        return this._fetch("GET", url, null, { errorMessage: "Data Sales Canvas Order tidak ditemukan" });
    }

    async createCanvasOrder(data) {
        const url = `${this.#baseGetUrl}/create-canvas-order`;
        return this._fetch("POST", url, data, { errorMessage: "Gagal membuat Canvas Order" });
    }

    async getDetailCanvasOrder(id_canvas_order) {
        const url = buildUrlWithParams(`${this.#baseGetUrl}/detail-canvas-order`, { id_canvas_order });
        return this._fetch("GET", url, null, { errorMessage: "Data Detail Canvas Order tidak ditemukan" });
    }

    async getListTagihanPembayaran(id_canvas_order) {
        const url = buildUrlWithParams(`${this.#baseGetUrl}/tagihan-pembayaran`, { id_canvas_order });
        return this._fetch("GET", url, null, { errorMessage: "Data Tagihan Pembayaran tidak ditemukan" });
    }

    async postTagihanPembayaran(data) {
        const url = `${this.#baseGetUrl}/submit-tagihan-pembayaran`;
        return this._fetch("POST", url, data, { errorMessage: "Gagal submit Tagihan Pembayaran" });
    }
}
    
const salesCanvasService = new salesCanvas();
export { salesCanvasService };
