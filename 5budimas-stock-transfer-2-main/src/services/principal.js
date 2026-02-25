import { fetchWithAuth } from "../lib/utils";
import { baseService } from "./baseService";

class principal extends baseService {
  #baseURL

  constructor() {
    super();

    this.#baseURL = "/api/base/principal";

    this.setServiceName("principal");
  }

  async getAllPrincipal() {
    try {
      const data = await fetchWithAuth("GET", this.#baseURL);
      return Promise.resolve(data);
    } catch (error) {
      console.log(error);
      return this.throwError(error);
    }
  }
}

const principalService = new principal();
export { principalService };
