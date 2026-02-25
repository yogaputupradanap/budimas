import { encode, fetchWithAuth } from "../lib/utils";
import { baseService } from "./baseService";

class CabangService extends baseService {
  #baseURL;
  constructor() {
    super();

    const baseColumns = encode(["id", "nama"]);

    this.#baseURL = `/api/base/cabang?columns=${baseColumns}`;

    this.setServiceName("cabang");
  }

  async getAllCabang() {
    try {
      const cabang = await fetchWithAuth("GET", this.#baseURL);
      return cabang;
    } catch (error) {
      this.throwError(error);
    }
  }
}
const cabangService = new CabangService();
export { cabangService };
