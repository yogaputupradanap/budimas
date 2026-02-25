import axios from "axios";
import { baseService } from "./baseService";
import { encode, fetchWithAuth, localDisk } from "../lib/utils";

class stockOpname extends baseService {
    baseGetUrl;
    #createUrl;
    #diterimaUrl;
    #ditolakUrl;
    #baseUrl;
    #getProdukByPrincipalUrl;
    #getOneStockOpnameDetailUrl;
    paginateStockOpnameUrl;

    constructor() {
        super();
        const localUser = localDisk.getLocalStorage("user");
        this.id_cabang = localUser?.id_cabang;
        const baseJoinGetAll = encode([
            "principal",
            "left join stock_opname_detail"
        ]);
        const baseOnGetAll = encode([
            "on stock_opname.id_principal = principal.id",
            "on stock_opname.id_stock_opname = stock_opname_detail.id_stock_opname"
        ]);
        const baseColumnsGetAll = encode([
            "stock_opname.*",
            "principal.nama as nama_principal",
            "COUNT(stock_opname_detail) as produk_count"
        ]);

        const baseColumnsGetOne = encode([
            "stock_opname.*",
            "produk.nama as nama_produk",
            "produk.kode_sku as sku",
            "stock_opname_detail.*",
            "principal.nama as nama_principal",
        ]);

        const baseGroupBy = encode([
            "stock_opname.id_stock_opname",
            "principal.nama",
        ]);

        const baseJoinGetOne = encode([
            "stock_opname",
            "produk",
            "principal",
        ]);

        const baseOnGetOne = encode([
            "on stock_opname.id_stock_opname = stock_opname_detail.id_stock_opname",
            "on produk.id = stock_opname_detail.id_produk",
            "on principal.id = stock_opname.id_principal",
        ]);

        this.#getProdukByPrincipalUrl = `/api/stock-opname/get-produks-stock-opname`;
        this.#createUrl = `/api/stock-opname/create-stock-opname`;
        this.#diterimaUrl = `/api/stock-opname/stock-opname-diterima`;
        this.#ditolakUrl = `/api/stock-opname/stock-opname-ditolak`;
        this.#baseUrl = `/api/base/stock_opname`;
        this.baseGetUrl = `/api/base/stock_opname/all?join=${baseJoinGetAll}&on=${baseOnGetAll}&columns=${baseColumnsGetAll}`;
        this.#getOneStockOpnameDetailUrl = `/api/base/stock_opname_detail/all?join=${baseJoinGetOne}&on=${baseOnGetOne}&columns=${baseColumnsGetOne}`;
        this.paginateStockOpnameUrl = `/api/stock-opname/stock-opname`;

        this.setServiceName("stockOpname");
    }

    setIdCabang(id_cabang) {
        this.id_cabang = id_cabang;
        return this;
    }

    async getIdStockOpname() {
        try {
            const id = await fetchWithAuth("GET", this.#baseUrl);
            return Promise.resolve(id);
        } catch (error) {
            return Promise.reject(error);
        }
    }

    async getAllStockOpname() {
        try {
            const clause = encode({ "stock_opname.id_cabang = ": `${this.id_cabang}  GROUP BY stock_opname.id_stock_opname, principal.nama` });
            const url = `${this.baseGetUrl}&clause=${clause} `;
            const stockOpname = await fetchWithAuth("GET", url);
            return Promise.resolve(stockOpname);
        } catch (error) {
            return Promise.reject(error);
        }
    }

    async getAllStockOpnameFilter(clauseFilter) {
        try {

            const clause = encode({
                ...JSON.parse(clauseFilter),
                "stock_opname.id_cabang = ": `${this.id_cabang}  GROUP BY stock_opname.id_stock_opname, principal.nama`
            });
            const url = `${this.baseGetUrl}&clause=${clause} `;
            const stockOpname = await fetchWithAuth("GET", url);
            return Promise.resolve(stockOpname);
        } catch (error) {
            return Promise.reject(error);
        }
    }

    async getProdukByPrincipal(principal) {
        try {
            const url = `${this.#getProdukByPrincipalUrl}?id_principal=${principal} `;
            const produk = await fetchWithAuth("GET", url);
            return Promise.resolve(produk);
        } catch (error) {
            return Promise.reject(error);
        }
    }

    async postStockOpname(commit, data) {
        let url = "";
        switch (commit) {
            case "add":
                url = this.#createUrl;
                break;
            case "diterima":
                url = this.#diterimaUrl;
                break;
            case "ditolak":
                url = this.#ditolakUrl;
                break;
            default:
                this.throwError("Commit not found");
                break;
        }
        try {
            await fetchWithAuth("POST", url, data);
            return Promise.resolve();
        } catch (error) {
            return this.throwError(error);
        }
    }
    async putStockOpname(commit, data) {
        let url = "";
        switch (commit) {
            case "diterima":
                url = this.#diterimaUrl;
                break;
            case "ditolak":
                url = this.#ditolakUrl;
                break;
            default:
                this.throwError("Commit not found");
                break;
        }
        try {
            await fetchWithAuth("PUT", url, data);
            return Promise.resolve();
        } catch (error) {
            return this.throwError(error);
        }
    }

    async getOneStockOpnameDetail(id) {
        try {
            const clause = encode({ "stock_opname_detail.id_stock_opname = ": `${id}` });
            const url = `${this.#getOneStockOpnameDetailUrl}&clause=${clause} `;
            const stockOpnameDetail = await fetchWithAuth("GET", url);
            console.log(stockOpnameDetail);
            return Promise.resolve(stockOpnameDetail);
        } catch (error) {
            return this.throwError(error);
        }
    }
}

export const stockOpnameService = new stockOpname();