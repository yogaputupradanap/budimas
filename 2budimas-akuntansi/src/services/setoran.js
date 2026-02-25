import { baseService } from "./baseService";
import { fetchWithAuth } from "../lib/utils";

class SetoranService extends baseService {
  constructor() {
    super();
    this.endpoints = {
      nonTunai: `/api/akuntansi/list-setoran-non-tunai`,
      tunai: `/api/akuntansi/list-setoran-tunai`,
      konfirmasiSetoran: "/api/akuntansi/konfirmasi-setoran",
      simpanKasirSetoran: "/api/akuntansi/simpan-kasir-setoran",
      detailSetoran: "/api/akuntansi/detail-setoran",
      addBiayaLain: "/api/akuntansi/add-biaya-lain",
      listPengeluaran: "/api/akuntansi/get-list-pengeluaran-kasir",
      addPengeluaran: "/api/akuntansi/add-pengeluaran-kasir",
      getKonfirmasiPengeluaran: "/api/akuntansi/get-konfirmasi-pengeluaran",
      konfirmasiPengeluaran: "/api/akuntansi/konfirmasi-pengeluaran",
      listLaporanKasir: "/api/akuntansi/list-laporan-kasir",
      getDetailLaporanKasir: "/api/akuntansi/get-detail-laporan-kasir",
      getAddLph: "/api/akuntansi/get-add-lph",
      getAddLphByCustomer: "/api/akuntansi/get-add-lph-customer",
      getAddLphModal: "/api/akuntansi/get-add-lph-modal",
      getAddLphCustomerModal: "/api/akuntansi/get-add-lph-customer-modal",
      addLph: "/api/akuntansi/add-lph",
      getDetailLph: "/api/akuntansi/get-detail-lph",
      cetakUlangLph: "/api/akuntansi/cetak-ulang-lph",
    };
    this.setServiceName("setoran");
  }

  async detailSetoran({
    tanggal,
    id_sales,
    nama_pj,
    pj_setoran,
    tipeSetoran,
    status,
    nama_kasir,
    nama_auditor,
    initField,
  } = {}) {
    const params = `tanggal=${tanggal}&id_sales=${id_sales}&nama_pj=${nama_pj}&pj_setoran=${pj_setoran}&tipe_setoran=${tipeSetoran}&status=${status}&nama_kasir=${nama_kasir}&nama_auditor=${nama_auditor}`;
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

  async simpanKasirSetoran(body) {
    try {
      const res = await fetchWithAuth(
        "POST",
        this.endpoints.simpanKasirSetoran,
        body
      );
      return res;
    } catch (error) {
      this.throwError("error while send post simpan kasir setoran : ", error);
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
