import { encode, fetchWithAuth } from "../lib/utils";
import { baseService } from "./baseService";

class perusahaan extends baseService {
    #baseURL

    constructor() {
        super();

        const baseColumns = encode([
            "id",
            "nama"
        ])
        this.#baseURL = `/api/base/perusahaan`;
        this.setServiceName("perusahaan");
    }

    async getAllPerusahaan() {
        try {
            const perusahaan = await fetchWithAuth("GET", this.#baseURL);
            return perusahaan
        } catch (error) {
            return this.throwError(error);
        }
    }
}

const perusahaanService = new perusahaan();
export { perusahaanService };
