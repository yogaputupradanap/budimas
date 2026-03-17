import { fetchWithAuth } from "../lib/utils";
import { baseService } from "./baseService";

class brand extends baseService {
    #baseURL

    constructor() {
        super();

        this.#baseURL = "/api/base/produk_brand";

        this.setServiceName("brand");
    }

    async getAllBrand() {
        try {
            const data = await fetchWithAuth("GET", this.#baseURL);
            return Promise.resolve(data);
        } catch (error) {
            console.log(error);
            return this.throwError(error);
        }
    }
}

const brandService = new brand();
export { brandService };