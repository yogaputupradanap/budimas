import axios from "axios";
import { baseService } from "./baseService";
import { encode, fetchWithAuth, localDisk } from "../lib/utils";

class stockOpname extends baseService {
    baseGetUrl;
    #createUrl;
    #getStockProdukUrl;
    #diterimaUrl;
    #ditolakUrl;
    #eskalasiUrl;
    #eskalasiCloseUrl;
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

        const baseJoinGetStockCabang = encode([
            "produk",
            "principal",
            "produk_uom"
        ]);

        const baseOnGetStockCabang = encode([
            "on produk.id = stok.produk_id ",
            "on produk.id_principal = principal.id",
            "on produk_uom.id_produk = produk.id"
        ])

        const baseColumnsGetStockCabang = encode([
            "stok.*",
            "produk.nama as nama_produk",
            "produk.kode_sku as sku",
            "produk_uom.nama as uom",
            "principal.nama as nama_principal",
        ]);

        this.#getProdukByPrincipalUrl = `/api/stock-opname/get-produks-stock-opname`;
        this.#createUrl = `/api/stock-opname/create-stock-opname`;
        this.#diterimaUrl = `/api/stock-opname/stock-opname-diterima`;
        this.#ditolakUrl = `/api/stock-opname/stock-opname-ditolak`;
        this.#eskalasiUrl = `/api/stock-opname/stock-opname-eskalasi`;
        this.#eskalasiCloseUrl = `/api/stock-opname/stock-opname-eskalasi-closed`;
        this.#baseUrl = `/api/base/stock_opname`;
        this.baseGetUrl = `/api/base/stock_opname/all?join=${baseJoinGetAll}&on=${baseOnGetAll}&columns=${baseColumnsGetAll}`;
        this.#getOneStockOpnameDetailUrl = `/api/base/stock_opname_detail/all?join=${baseJoinGetOne}&on=${baseOnGetOne}&columns=${baseColumnsGetOne}`;
        this.paginateStockOpnameUrl = `/api/stock-opname/stock-opname`;
        this.#getStockProdukUrl = `/api/base/stok/all?join=${baseJoinGetStockCabang}&on=${baseOnGetStockCabang}&columns=${baseColumnsGetStockCabang}`;

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

    // Di dalam class stockOpname

    async getAllStockOpname(filterName = null, filterValue = null) {
        try {
            // PERBAIKAN: Ambil ulang dari LocalStorage jika this.id_cabang masih undefined
            if (!this.id_cabang) {
                const localUser = localDisk.getLocalStorage("user");
                this.id_cabang = localUser?.id_cabang;
            }

            // Proteksi terakhir: Jika masih undefined, jangan jalankan fetch
            if (!this.id_cabang || this.id_cabang === "undefined") {
                console.error("ID Cabang tidak ditemukan. Pastikan user sudah login.");
                return Promise.resolve({ result: [], status: 200 }); 
            }

            const clause = encode({ 
                "stock_opname.id_cabang = ": `${this.id_cabang}  GROUP BY stock_opname.id_stock_opname, principal.nama` 
            });
            
            const url = `${this.baseGetUrl}&clause=${clause}`;
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
            case "eskalasi":
                url = this.#eskalasiUrl;
                break;
            case "eskalasi closed":
                url = this.#eskalasiCloseUrl;
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

    async getStockCabangByPrincipal(id_principal, id_cabang) {
        try {
            const clause = encode({ "stok.cabang_id = ": `${id_cabang}`, "produk.id_principal = ": `${id_principal}`, "produk_uom.level = ": `1` });
            const url = `${this.#getStockProdukUrl}&clause=${clause} `;
            const stockOpname = await fetchWithAuth("GET", url);
            return Promise.resolve(stockOpname);
        } catch (error) {
            return this.throwError(error);
        }
    }
}

export const stockOpnameService = new stockOpname();