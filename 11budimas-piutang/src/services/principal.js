import { encode, fetchWithAuth } from "../lib/utils";
import { baseService } from "./baseService";

class principal extends baseService {
  #baseURL

  constructor() {
    super();

    const baseColumns = encode([
        "id",
        "nama",
        "kode"
    ])
    this.#baseURL = `/api/base/principal/all?columns=${baseColumns}`;
    this.setServiceName("principal");
  }

  async getAllprincipal() {
    try {
      const principal = await fetchWithAuth("GET", this.#baseURL);
      return Promise.resolve(principal);
    } catch (error) {
      return this.throwError(error);
    }
  }
}

const principalService = new principal();
export { principalService };
