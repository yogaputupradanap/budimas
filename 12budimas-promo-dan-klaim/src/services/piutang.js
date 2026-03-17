import { encode, fetchWithAuth } from "../lib/utils";
import { baseService } from "./baseService";

class piutang extends baseService {
  constructor() {
    super();

    const columnDTN = encode([
      "sales_order.no_tagihan",
      "setoran.jumlah_setoran",
      "principal.kode as kode_principal",
      "customer.nama as nama_customer",
      "customer.kode as kode_customer",
    ]);
    const joinDTN = encode(["left join setoran", "plafon", "customer", "principal"]);
    const onDTN = encode([
      "on sales_order.id = setoran.id_sales_order",
      "on plafon.id = sales_order.id_plafon",
      "on customer.id = plafon.id_customer",
      "on principal.id = plafon.id_principal",
    ]);

    // url that belong to piutang
    this.baseUrl = `/api/akuntasi/get-piutang`;
    this.tagihanSales = `/api/akuntasi/get-tagihan-sales`;
    this.detailTagihanNotaURL = `/api/base/sales_order/all?columns=${columnDTN}&join=${joinDTN}&on=${onDTN}`;
    this.detailTagihanSales = `/api/akuntasi/detail-tagihan-sales`;
    this.createTagihanSales = `/api/akuntasi/create-tagihan-sales`;
    this.setServiceName("piutang");
  }

  async getPiutang() {
    try {
      const result = await fetchWithAuth("GET", this.baseUrl);
      const piutang = this.deduplication(result, [], {
        keyId1: "nota_tagihan",
        keyId2: "nota_tagihan",
        sumKeys: ["total_penjualan", "jumlah_faktur"],
      });
      return piutang;
    } catch (error) {
      this.throwError(error);
    }
  }

  async detailPiutang(nota_tagihan) {
    const param = `no_tagihan=${nota_tagihan}`;
    try {
      const result = await fetchWithAuth(
        "GET",
        `${this.detailTagihanSales}?${param}`
      );

      return result;
    } catch (error) {
      this.throwError(error);
    }
  }

  async detailTagihanNota(nota_tagihan) {
    const clauseEnc = encode({
      "sales_order.no_tagihan = ": `'${nota_tagihan}'`,
    });
    const clause = `clause=${clauseEnc}`;

    try {
      const result = await fetchWithAuth(
        "GET",
        `${this.detailTagihanNotaURL}&${clause}`
      );
      const res = this.deduplication(result, [], {
        keyId1: "nota_tagihan",
        keyId2: "nota_tagihan",
        sumKeys: ["jumlah_setoran"],
      });

      return res;
    } catch (error) {
      this.throwError(error);
    }
  }

  async postTagihan(body) {
    try {
      await fetchWithAuth("POST", this.createTagihanSales, body);
      return "Sukses membuat surat tagihan sales";
    } catch (error) {
      this.throwError(error);
    }
  }
}

const piutangService = new piutang();
export { piutangService };
