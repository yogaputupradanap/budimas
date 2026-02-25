import { encode, fetchWithAuth } from "../lib/utils";
import { baseService } from "./baseService";

class hutang extends baseService {
  constructor() {
    super();

    const columnDTN = encode([
      "principal.kode as kode_principal",
      "principal.nama as nama_principal",
      "principal.id as id_principal",
      "purchase_transaksi.total",
    ]);
    const joinDTN = encode(["purchase_order", "principal", "purchase_tagihan"]);
    const onDTN = encode([
      "on purchase_transaksi.order_id = purchase_order.id",
      "on principal.id = purchase_order.principal_id",
      "on purchase_transaksi.id = purchase_tagihan.transaksi_id",
    ]);

    this.getHutangUrl = `/api/akuntasi/get-hutang`;
    this.getTagihanPurchaseUrl = `/api/akuntasi/get-tagihan-purchase`;
    this.detailTagihanPurchaseUrl = `/api/akuntasi/detail-tagihan-purchase`;
    this.detailTagihanNotaUrl = `/api/base/purchase_transaksi/all?columns=${columnDTN}&join=${joinDTN}&on=${onDTN}`;

    this.createTagihanPurchaseUrl = `/api/akuntasi/create-tagihan-purchase`;

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
      "purchase_tagihan.keterangan = ": `'${nota_tagihan}'`,
    });
    const clause = `clause=${clauseEnc}`;

    try {
      const result = await fetchWithAuth(
        "GET",
        `${this.detailTagihanNotaUrl}&${clause}`
      );

      const res = this.deduplication(result, [], {
        keyId1: "id_principal",
        keyId2: "id_principal",
        sumKeys: ['total']
      });

      return res;
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
}

const hutangService = new hutang();
export { hutangService };
