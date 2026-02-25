import { encode, fetchWithAuth } from "../lib/utils";
import { baseService } from "./baseService";

class customer extends baseService {
  #baseURL
  #fullDataURL

  constructor() {
    super();

    const baseClause = encode({
        "id_cabang = ": 5
    })
    const baseColumns = encode([
        "id",
        "nama",
        "kode"
    ])
    this.#baseURL = `/api/base/customer/all?columns=${baseColumns}&clause=${baseClause}&limit=100`;
    this.#fullDataURL = `/api/base/customer/all?columns=${baseColumns}&clause=${baseClause}`;
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

  async getAllCustomersFull() {
    try {
      const customers = await fetchWithAuth("GET", this.#fullDataURL);
      return Promise.resolve(customers || []);
    } catch (error) {
      console.error("Error loading full customers:", error);
      return this.throwError(error);
    }
  }

  async searchCustomerServer(query, limit = 100) {
    if (!query || query.length < 2) {
      return this.getAllCustomer();
    }

    try {
      const baseColumns = encode(["id", "nama", "kode"]);
      const baseClause = encode({
        "id_cabang = ": 5
      });
      const searchClause = encode({
        "AND (nama ILIKE": `'%${query}%'`,
        "OR kode ILIKE": `'%${query}%')`,
        "OR id::text ILIKE": `'%${query}%'`
      });
      
      const url = `/api/base/customer/all?columns=${baseColumns}&clause=${baseClause}${searchClause}&limit=${limit}`;
      const result = await fetchWithAuth("GET", url);
      return Promise.resolve(result || []);
    } catch (error) {
      console.error("Error searching customers:", error);
      return [];
    }
  }
}

const customerService = new customer();
export { customerService };
