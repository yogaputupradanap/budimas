import {encode, fetchWithAuth, localDisk} from "../lib/utils";
import {baseService} from "./baseService";

class stockTransfer extends baseService {
    #baseGetURL;
    #addURL;
    #konfirmasiURL;
    #konfirmasiAdminURL;
    #penerimaanURL;
    #closeEskalasiPenerimaanURL;
    #tolakPenerimaanURL;
    #base;
    #cabangAwalbase;
    #cabangTujuanBase;
    #paginateBaseJoin;
    #paginateBaseOn;
    #paginateBaseColumns;

    constructor() {
        super();
        const localUser = localDisk.getLocalStorage("user");
        // ***specific page condition**** //
        this.id_cabang = localUser?.id_cabang;
        this.id_perusahaan = localUser?.id_perusahaan;

        const baseJoin = encode([
            "stock_transfer_detail",
            "principal",
            "produk",
            "left join armada",
        ]);
        const baseOn = encode([
            "on stock_transfer.id = stock_transfer_detail.id_stock_transfer",
            "on principal.id = stock_transfer_detail.id_principal",
            "on produk.id = stock_transfer_detail.id_produk",
            "on stock_transfer.id_armada = armada.id",
        ]);
        const baseColumns = encode([
            "stock_transfer.*",
            "stock_transfer_detail.*",
            "produk.nama as nama_produk",
            "principal.nama as nama_principal",
            "armada.nama as nama_armada",
        ]);

        const stockBaseColumns = encode([
            "produk.kode_sku as sku",
            "produk.nama as nama_produk",
            "stok.id as id",
            "produk.satuan",
            "principal.nama as nama_principal",
            "stok.jumlah_good",
            "cabang.nama as nama_cabang",
        ]);
        const stockBaseJoin = encode(["produk", "cabang", "principal"]);
        const stockBaseOn = encode([
            "on stok.produk_id = produk.id",
            "on stok.cabang_id = cabang.id",
            "on produk.id_principal = principal.id",
        ]);

        this.#paginateBaseJoin = encode([
            "produk",
            "cabang",
            "principal",
            "produk_uom",
        ]);
        this.#paginateBaseOn = encode([
            "on stok.produk_id = produk.id",
            "on stok.cabang_id = cabang.id",
            "on produk.id_principal = principal.id",
            "on produk.id = produk_uom.id_produk",
        ]);
        this.#paginateBaseColumns = encode([
            "produk.kode_sku as sku",
            "produk.nama as nama_produk",
            "stok.id as id",
            "produk_uom.nama as satuan",
            "cabang.nama as nama_cabang",
            "principal.nama as nama_principal",
            "stok.jumlah_good",
        ]);

        // GET methods
        this.#baseGetURL = `/api/base/stock_transfer/all?join=${baseJoin}&on=${baseOn}&columns=${baseColumns}`;

        // POST, PUT, DELETE methods
        this.#addURL = "/api/stock-transfer/add-stock-transfer";
        this.#konfirmasiURL = "/api/stock-transfer/konfirmasi-stock-transfer";
        this.#konfirmasiAdminURL =
            "/api/stock-transfer/konfirmasi-admin-stock-transfer";
        this.#penerimaanURL = "/api/stock-transfer/penerimaan-stock-transfer";
        this.#closeEskalasiPenerimaanURL = "/api/stock-transfer/close-eskalasi-penerimaan-stock-transfer"
        this.#tolakPenerimaanURL = "/api/stock-transfer/tolak-stock-transfer";

        // basic url
        this.#base = "/api/base/stock_transfer";

        // base url to get stock
        this.stockBase = `/api/base/stok/all?columns=${stockBaseColumns}&field=stok.id&join=${stockBaseJoin}&on=${stockBaseOn}`;

        this.updatePaginateStockBase();
        this.setCabangBase();
        this.setServiceName("stock transfer");
    }

    updatePaginateStockBase() {
        const paginateBaseClause = encode({
            "produk_uom.level= ": 1,
            "cabang.id_perusahaan=": this.id_perusahaan,
        });

        this.paginateStockBase = `/api/base/stok/paginate?join=${
            this.#paginateBaseJoin
        }&on=${this.#paginateBaseOn}&columns=${
            this.#paginateBaseColumns
        }&clause=${paginateBaseClause}`;
    }

    setIdCabang(id_cabang) {
        this.id_cabang = id_cabang;
        this.updatePaginateStockBase();
        return this;
    }

    setIdPerusahaan(id_perusahaan) {
        this.id_perusahaan = id_perusahaan;
        this.updatePaginateStockBase();
        return this;
    }

    setCabangBase(clause = null) {
        if (clause) {
            const clause_awal = {...clause};
            const clause_tujuan = {...clause};

            clause_awal["stock_transfer.id_cabang_awal = "] = `${this.id_cabang}`;
            clause_tujuan["stock_transfer.id_cabang_tujuan = "] = `${this.id_cabang}`;

            const encode_string_clause_awal = encodeURIComponent(
                JSON.stringify(clause_awal)
            );
            const encode_string_clause_tujuan = encodeURIComponent(
                JSON.stringify(clause_tujuan)
            );

            const string_clause_awal = `&clause=${encode_string_clause_awal}`;
            const string_clause_tujuan = `&clause=${encode_string_clause_tujuan}`;

            this.#cabangAwalbase = `${this.#baseGetURL}${string_clause_awal}`;
            this.#cabangTujuanBase = `${this.#baseGetURL}${string_clause_tujuan}`;

            return this;
        }

        const encode_clause_awal = encode({
            "stock_transfer.id_cabang_awal = ": `${this.id_cabang}`,
        });
        const encode_clause_tujuan = encode({
            "stock_transfer.id_cabang_tujuan = ": `${this.id_cabang}`,
        });

        this.#cabangAwalbase = `${this.#baseGetURL}&clause=${encode_clause_awal}`;

        this.#cabangTujuanBase = `${
            this.#baseGetURL
        }&clause=${encode_clause_tujuan}`;

        return this;
    }

    async baseGetStockTransfer(
        status,
        columns = [],
        filtered_branch = "id_cabang_awal"
    ) {
        const isArray = Array.isArray(status);

        const statusSets = isArray ? `(${status.join(", ")})` : status;
        const operator = isArray ? " in " : " = ";

        const key = `stock_transfer.status ${operator}`;
        const clause = {[key]: `${statusSets}`};

        this.setCabangBase(clause);

        try {
            const url =
                filtered_branch === "id_cabang_awal"
                    ? this.#cabangAwalbase
                    : filtered_branch === "id_cabang_tujuan"
                        ? this.#cabangTujuanBase
                        : this.#baseGetURL;

            const stockTransfer = await fetchWithAuth("GET", url);
            const result = this.deduplication(stockTransfer, columns);
            return Promise.resolve(result);
        } catch (error) {
            return Promise.reject(error);
        }
    }

    async geAllStockTransfer(columns = [], filtered_branch = "id_cabang_awal") {
        this.setCabangBase();
        try {
            const url =
                filtered_branch === "id_cabang_awal"
                    ? this.#cabangAwalbase
                    : filtered_branch === "id_cabang_tujuan"
                        ? this.#cabangTujuanBase
                        : this.#baseGetURL;

            const allStockTransfer = await fetchWithAuth("GET", url);
            const result = this.deduplication(allStockTransfer, columns);
            return Promise.resolve(result);
        } catch (error) {
            return this.throwError(error);
        }
    }

    async getStockTransferById(id) {
        try {
            const encodeClause = encode({"stock_transfer.id = ": `"${id}"`});
            const url = `${this.#baseGetURL}?clause=${encodeClause}`;

            const stockTransferById = await fetchWithAuth("GET", url);
            return Promise.resolve(stockTransferById);
        } catch (error) {
            return this.throwError(error);
        }
    }

    async putStockTransfer(id, body) {
        try {
            const form = new FormData();
            Object.entries(body).forEach(([key, value]) => {
                form.append(key, value);
            });

            const encodeQueryWhere = encode({"id = ": `${id}`});
            const query = `?where=${encodeQueryWhere}`;
            await fetchWithAuth("PUT", `${this.#base}${query}`, form);
            return Promise.resolve();
        } catch (error) {
            return this.throwError(error);
        }
    }

    async postStockTransfer(commit, body) {
        let url = "";

        if (commit) {
            switch (commit) {
                case "add":
                    url = this.#addURL;
                    break;
                case "konfirmasi":
                    url = this.#konfirmasiURL;
                    break;
                case "konfirmasi-admin":
                    url = this.#konfirmasiAdminURL;
                    break;
                case "penerimaan":
                    url = this.#penerimaanURL;
                    break;
                case "close-eskalasi":
                    url = this.#closeEskalasiPenerimaanURL;
                    break;
                case "tolak":
                    url = this.#tolakPenerimaanURL;
                default:
                    break;
            }
        } else {
            url = this.base;
        }

        try {
            await fetchWithAuth("POST", url, body);
            return Promise.resolve();
        } catch (error) {
            return this.throwError(error);
        }
    }
}

const transferService = new stockTransfer();
export {transferService};
