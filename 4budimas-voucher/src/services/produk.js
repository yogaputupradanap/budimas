import { fetchWithAuth } from "../lib/utils";
import { baseService } from "./baseService";

class produk extends baseService {
  constructor() {
    super();

    this.produkUrl = "/api/base/produk";

    this.setServiceName("produk");
  }

  async getProduks() {
    try {
      const result = await fetchWithAuth("GET", this.produkUrl);
      return result;
    } catch (error) {
      console.error(error);
      this.throwError(error);
    }
  }
}

export const produkService = new produk();
