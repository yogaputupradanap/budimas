import { encode, fetchWithAuth } from "../lib/utils";
import { baseService } from "./baseService";

class sales extends baseService {
  #baseURL

  constructor() {
    super();

    const baseJoin = encode([
      "users"
    ])
    const baseOn = encode([
      'on sales.id_user = users.id'
    ])
    const baseClause = encode({
        'users.id_cabang = ': 5
    })
    const baseColumns = encode([
        "users.nama",
        "sales.id",
    ])
    this.#baseURL = `/api/base/sales/all?join=${baseJoin}&on=${baseOn}&clause=${baseClause}&columns=${baseColumns}`;

    this.setServiceName("sales");
  }

  async getAllSales() {
    try {
      const sales = await fetchWithAuth("GET", this.#baseURL);
      return Promise.resolve(sales);
    } catch (error) {
      console.log(error);
      return this.throwError(error);
    }
  }
}

const salesService = new sales();
export { salesService };
