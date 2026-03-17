import {encode, fetchWithAuth} from "../lib/utils";
import {baseService} from "./baseService";

class hutang extends baseService {
    constructor() {
        super();

        const columnDTN = encode([
            "DISTINCT ON (purchase_tagihan.id) purchase_tagihan.id AS id_tagihan",
            "principal.nama AS nama_principal",
            "principal.kode as kode_principal",
            "purchase_tagihan.no_tagihan",
            "purchase_tagihan.total as total_tagihan",
            "purchase_tagihan.status_pembayaran as status_bayar",
            "purchase_tagihan.bukti_bayar"
        ]);

        const joinDTN = encode([
            "left join purchase_tagihan_detail",
            "left join purchase_transaksi",
            "left join purchase_order",
            "left join principal"
        ]);

        const onDTN = encode([
            "on purchase_tagihan.id = purchase_tagihan_detail.tagihan_id",
            "on purchase_tagihan_detail.transaksi_id = purchase_transaksi.id",
            "on purchase_transaksi.order_id = purchase_order.id",
            "on purchase_order.principal_id = principal.id"
        ]);

        this.groupDTN = encode([
            "purchase_tagihan.id",
            "principal.nama",
            "principal.kode",
            "purchase_tagihan.total"
        ]);

        this.getHutangUrl = `/api/akuntasi/get-hutang`;
        this.getTagihanPurchaseUrl = `/api/akuntasi/get-tagihan-purchase`;
        this.detailTagihanPurchaseUrl = `/api/akuntasi/detail-tagihan-purchase`;
        this.detailTagihanNotaUrl = `/api/base/purchase_tagihan/all?columns=${columnDTN}&join=${joinDTN}&on=${onDTN}`;

        this.createTagihanPurchaseUrl = `/api/akuntasi/create-tagihan-purchase`;
        this.createPembayaranTagihan = `/api/akuntasi/create-pembayaran-tagihan`;

        this.setServiceName("hutang");
    }

    async getHutang() {
        try {
            const result = await fetchWithAuth("GET", this.getHutangUrl);
            return result;
        } catch (error) {
            this.throwError(error);
        }
    }

    async detailHutang(nota_tagihan) {
        const param = `no_tagihan=${nota_tagihan}`;
        try {
            const result = await fetchWithAuth(
                "GET",
                `${this.detailTagihanPurchaseUrl}?${param}`
            );

            return result;
        } catch (error) {
            this.throwError(error);
        }
    }

    async detailTagihanNota(nota_tagihan) {
        const clauseEnc = encode({
            "purchase_tagihan.no_tagihan = ": `'${nota_tagihan}'`,
        });
        const clause = `clause=${clauseEnc}`;

        try {
            const result = await fetchWithAuth(
                "GET",
                `${this.detailTagihanNotaUrl}&${clause}&group=${this.groupDTN}`
            );
            return result;  // Langsung return result tanpa deduplication
        } catch (error) {
            this.throwError(error);
        }
    }

    async postTagihanPurchase(body) {
        try {
            await fetchWithAuth("POST", this.createTagihanPurchaseUrl, body);
            return "Sukses membuat surat tagihan purchase";
        } catch (error) {
            this.throwError(error);
        }
    }

    async postPembayaranTagihan(body) {
        try {
            await fetchWithAuth("POST", this.createPembayaranTagihan, body);
            return "Pembayaran Sukses";
        } catch (error) {
            this.throwError(error);
        }
    }
}

const hutangService = new hutang();
export {hutangService};
