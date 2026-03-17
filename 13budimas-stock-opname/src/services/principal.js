import { encode, fetchWithAuth } from "../lib/utils";
import { baseService } from "./baseService";

class principal extends baseService {
  #baseURL

  constructor() {
    super();

    this.#baseURL = "/api/base/principal/all";

    this.setServiceName("principal");
  }

  async getAllPrincipal(id_perusahaan) {
    try {
      // const clause = encode({ "id_perusahaan = ": id_perusahaan });
      const url = `${this.#baseURL}`;
      const data = await fetchWithAuth("GET", url);
      return Promise.resolve(data);
    } catch (error) {
      console.log(error);
      return this.throwError(error);
    }
  }
}

const principalService = new principal();
export { principalService };
