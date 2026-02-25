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
    ]);
    this.#baseURL = `/api/base/principal/all?columns=${baseColumns}`;
    this.setServiceName("principal");
  }

  // Ambil semua principal
  async getAllprincipal() {
    try {
      const principal = await fetchWithAuth("GET", this.#baseURL);
      return Promise.resolve(principal);
    } catch (error) {
      return this.throwError(error);
    }
  }

  // Ambil principal berdasarkan idPerusahaan
  async getPrincipal(idPerusahaan) {
    try {
      const clause = encode({ id_perusahaan: idPerusahaan });
      const url = `${this.#baseURL}&clause=${clause}`;
      const principal = await fetchWithAuth("GET", url);
      return Promise.resolve(principal);
    } catch (error) {
      return this.throwError(error);
    }
  }
}

const principalService = new principal();
export { principalService };