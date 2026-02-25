import { fetchWithAuth } from "../lib/utils";
import { baseService } from "./baseService";

class voucher extends baseService {
  constructor() {
    super();

    this.allVoucherApi = `/api/voucher/all-voucher`;
    this.voucherApi = "/api/voucher";
    this.baseVoucherApi = "/api/base/voucher";
    this.setServiceName("voucher");
  }

  async getAllVoucher() {
    try {
      const result = await fetchWithAuth("GET", this.allVoucherApi);
      return result;
    } catch (error) {
      this.throwError(error);
    }
  }

  async getVouchers(type) {
    try {
      const url = `${this.voucherApi}_${type}`;
      const result = await fetchWithAuth("GET", url);
      return result;
    } catch (error) {
      this.throwError(error);
    }
  }
  async getVoucher(id, type) {
    try {
      const paramVoucher = new URLSearchParams();
      paramVoucher.append("where", `{"id = ": "${id}"}`);

      const apiVoucher = `${this.baseVoucherApi}_${type}`;
      const url = `${apiVoucher}?${paramVoucher.toString()}`;

      const result = await fetchWithAuth("GET", url);

      if (type != 1) {
        const voucherTable = `voucher_${type}_produk`;
        const apiVoucherproduk = `${this.baseVoucherApi}_${type}_produk`;

        const paramVoucherProduk = new URLSearchParams();
        paramVoucherProduk.append("clause", `{"id_voucher = ": "${id}"}`);
        paramVoucherProduk.append("join", `["produk"]`);
        paramVoucherProduk.append(
          "on",
          `["on produk.id = ${voucherTable}.id_produk"]`
        );
        paramVoucherProduk.append(
          "columns",
          `["${voucherTable}.*", "produk.nama"]`
        );

        const urlVoucherProduk = `${apiVoucherproduk}/all?${paramVoucherProduk.toString()}`;

        const resultProduk = await fetchWithAuth("GET", urlVoucherProduk);
        console.log("resultProduk : ", resultProduk);
        result[0]["id_produk"] = resultProduk;
      }

      return result;
    } catch (error) {
      this.throwError(error);
    }
  }

  async deleteVoucher(id, type) {
    const param = new URLSearchParams();
    param.append("id_voucher", id);

    const url = `${this.voucherApi}/${type}?${param.toString()}`;
    try {
      await fetchWithAuth("DELETE", url);
    } catch (error) {
      this.throwError(error);
    }
  }
  async getVoucherById(id, type) {
    try {
      const url = `/api/voucher/get-voucher-by-id/${type}?id_voucher=${id}`;
      const result = await fetchWithAuth("GET", url);
      return result;
    } catch (error) {
      this.throwError(error);
    }
  }
}

export const voucherService = new voucher();
