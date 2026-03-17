import { encode, fetchWithAuth } from "../lib/utils";
import { baseService } from "./baseService";

class customer extends baseService {
  #baseURL

  constructor() {
    super();

    const baseClause = encode({
        "id_cabang = ": 5
    })
    const baseColumns = encode([
        "id",
        "nama"
    ])
    this.#baseURL = `/api/base/customer/all?clause=${baseClause}&columns=${baseColumns}`;

    this.setServiceName("customer");
  }

  async getAllCustomer() {
    try {
      const customer = await fetchWithAuth("GET", this.#baseURL);
      return Promise.resolve(customer);
    } catch (error) {
      return this.throwError(error);
    }
  }
}

const customerService = new customer();
export { customerService };
