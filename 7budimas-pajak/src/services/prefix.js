import { baseService } from "./baseService";

class PrefixService extends baseService {
    constructor() {
        super();
        this.generateFaktur = `${process.env.VUE_APP_API_PAJAK_URL}/api/pajak/generate-faktur-pajak`;
        this.listNoPajak = `${process.env.VUE_APP_API_PAJAK_URL}/api/pajak/list-no-pajak`;
        this.setServiceName("prefix");
    }

    async postNomorPajak(body) {
        try {
            const response = await fetch(this.generateFaktur, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(body)
            });
            return await response.json();
        } catch (error) {
            this.throwError(error);
        }
    }


}

const prefixService = new PrefixService();
export { prefixService };