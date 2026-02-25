import { fetchWithAuth } from "../lib/utils";
import { baseService } from "./baseService";

class armada extends baseService {
  #baseURL

  constructor() {
    super();

    this.#baseURL = "/api/base/armada";

    this.setServiceName("armada");
  }

  async getAllArmada() {
    try {
      const armada = await fetchWithAuth("GET", this.#baseURL);
      return Promise.resolve(armada);
    } catch (error) {
      console.log(error);
      return this.throwError(error);
    }
  }
}

const armadaService = new armada();
export { armadaService };
