import { fetchWithAuth } from "../lib/utils";
import { baseService } from "./baseService";

class cabang extends baseService {
  #baseURL

  constructor() {
    super();

    this.#baseURL = "/api/base/cabang";

    this.setServiceName("cabang");
  }

  async getAllCabang() {
    try {
      const data = await fetchWithAuth("GET", this.#baseURL);
      return Promise.resolve(data);
    } catch (error) {
      console.log(error);
      return this.throwError(error);
    }
  }
}

const cabangService = new cabang();
export { cabangService };
