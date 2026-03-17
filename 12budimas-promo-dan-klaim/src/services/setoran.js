import { baseService } from "./baseService";
import { fetchWithAuth } from "../lib/utils";

class SetoranService extends baseService {
  constructor() {
    super();
    this.endpoints = {
      nonTunai: `/api/akuntasi/list-setoran-non-tunai`,
      tunai: `/api/akuntasi/list-setoran-tunai`,
      konfirmasiSetoran: "/api/akuntasi/konfirmasi-setoran",
      detailSetoran: "/api/akuntasi/detail-setoran",
      addBiayaLain: "/api/akuntasi/add-biaya-lain"
    };
    this.setServiceName("setoran");
  }

  async detailSetoran({ tanggal, sales, tipeSetoran, initField } = {}) {
    const params = `tanggal=${tanggal}&nama_sales=${sales}&tipe_setoran=${tipeSetoran}`;
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
