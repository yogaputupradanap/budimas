import { baseService } from "./baseService";
import { fetchWithAuth } from "../lib/utils";

class SetoranService extends baseService {
  constructor() {
    super();
    this.endpoints = {
      nonTunai: `/api/akuntansi/list-setoran-non-tunai`,
      tunai: `/api/akuntansi/list-setoran-tunai`,
      konfirmasiSetoran: "/api/akuntansi/konfirmasi-setoran",
      detailSetoran: "/api/akuntansi/detail-setoran",
      addBiayaLain: "/api/akuntansi/add-biaya-lain"
    };
    this.setServiceName("setoran");
  }

  async detailSetoran({ tanggal, id_sales, tipeSetoran, initField } = {}) {
    const params = `tanggal=${tanggal}&id_sales=${id_sales}&tipe_setoran=${tipeSetoran}`;
    const finalUrl = `${this.endpoints.detailSetoran}?${params}`;

    try {
      const res = await fetchWithAuth("GET", finalUrl);
      return res;
    } catch (error) {
      this.throwError("error while fetching setoran detail : ".error);
    }
  }

  async konfirmasiSetoran(body) {
    try {
      const res = await fetchWithAuth(
        "POST",
        this.endpoints.konfirmasiSetoran,
        body
      );
      return res;
    } catch (error) {
      this.throwError("error while send post konfirmasi setoran : ", error);
    }
  }
  async addBiayaLainnya(body) {
    try {
      const res = await fetchWithAuth(
        "POST",
        this.endpoints.addBiayaLain,
        body
      );
      return res;
    } catch (error) {
      throw error; // Just throw the error instead of using throwError
    }
  }
}

const setoranService = new SetoranService();
export { setoranService };
