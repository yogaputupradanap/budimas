import { encode, fetchWithAuth } from "../lib/utils";
import { baseService } from "./baseService";

class cabang extends baseService {
    #baseURL

    constructor() {
        super();

        const baseColumns = encode([
            "id",
            "nama"
        ]);
        this.#baseURL = `/api/base/cabang`;
        this.setServiceName("cabang");
    }

    async getAllCabang() {
        try {
            const cabang = await fetchWithAuth("GET", this.#baseURL);
            return cabang;
        } catch (error) {
            return this.throwError(error);
        }
    }
}

const cabangService = new cabang();
export { cabangService };
