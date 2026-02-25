import {apiUrl, fetchWithAuth} from "../lib/utils";
import {baseService} from "./baseService";

class customer extends baseService {
    constructor() {
        super();

        this.customerUrl = "/api/base/customer";

        this.setServiceName("customer");
    }

    async getCustomers() {
        try {
            const result = await fetchWithAuth("GET", `${apiUrl}${this.customerUrl}`);
            return result;
        } catch (error) {
            console.error(error);
            this.throwError(error);
        }
    }
}

export const customerService = new customer();
