import {encode, fetchWithAuth} from "../lib/utils";
import {baseService} from "./baseService";

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
            'users.id_cabang = ': this.id
        })
        const baseColumns = encode([
            "users.nama",
            "sales.id",
        ])
        this.#baseURL = `/api/base/sales/all?join=${baseJoin}&on=${baseOn}&columns=${baseColumns}`;

        this.setServiceName("sales");
    }

    async getAllSales(id_cabang) {
        try {
            const clause = encode({"users.id_cabang = ": id_cabang});
            const url = `${this.#baseURL}&clause=${clause}`;
            const sales = await fetchWithAuth("GET", url);
            // console.log("sales in service : ", sales)
            return Promise.resolve(sales);
        } catch (error) {
            console.log(error);
            return this.throwError(error);
        }
    }
}

const salesService = new sales();
export {salesService};
