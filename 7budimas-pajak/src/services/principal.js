import { encode, ErrorResponse, fetchWithAuth, status, SuccessResponse } from "../lib/utils";
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
    this.#baseURL = `/api/base/principal/all?columns=${baseColumns}&clause=`;
    this.setServiceName("principal");
  }

  async getPrincipal(clause) {
    try {
      // Ubah format clause sesuai kebutuhan API
      const new_clause = {id_perusahaan: ` = ${clause.id_perusahaan}`}
      
      const encoded_clause = encode(new_clause);
      const finalURL = this.#baseURL + encoded_clause;
      const principal = await fetchWithAuth("GET", finalURL);
      // Fetch not use pinia
      return SuccessResponse("Data fetched successfully", principal);
    } catch (error) {
      // Fetch not use pinia
      return ErrorResponse(this.throwError(error), null);
    }
  }
  
}

const principalService = new principal();
export { principalService };
