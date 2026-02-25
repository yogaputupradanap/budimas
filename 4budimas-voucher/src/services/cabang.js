import { fetchWithAuth } from "../lib/utils";
import { baseService } from "./baseService";

class cabang extends baseService {
  constructor() {
    super();

    this.cabangUrl = "/api/base/cabang";

    this.setServiceName("cabang");
  }

  async getCabangs() {
    try {
      const result = await fetchWithAuth("GET", this.cabangUrl);
      return result;
    } catch (error) {
      console.error(error);
      this.throwError(error);
    }
  }
}

export const cabangService = new cabang();
