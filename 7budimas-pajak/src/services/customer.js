import { encode, fetchWithAuth, SuccessResponse, ErrorResponse } from "../lib/utils";
import { baseService } from "./baseService";

class customer extends baseService {
  #baseURL

  constructor() {
    super();

    const baseColumns = encode([
        "id",
        "nama",
        "kode"
    ])
    this.#baseURL = `/api/base/customer/all?columns=${baseColumns}&clause=`;

    this.setServiceName("customer");
  }

  async getCustomer(clause) {
    try {
      const new_clause = { id_cabang : ` = ${clause.id_cabang}`}
      const encoded_clause = encode(new_clause)
      const finalURL = this.#baseURL + encoded_clause;
      // console.log("Clause in getCustomer:", finalURL);
      const customer = await fetchWithAuth("GET", finalURL);
      return SuccessResponse("Data fetched successfully", customer);
    } catch (error) {
      return ErrorResponse(this.throwError(error), null);
    }
  }
}

const customerService = new customer();
export { customerService };
