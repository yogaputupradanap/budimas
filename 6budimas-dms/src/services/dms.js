import axios from "axios";
import { baseService } from "./baseService";
import { encode, fetchWithAuth, localDisk } from "../lib/utils";

class dms extends baseService {
    #insertUrl;
    constructor() {
        super();
        const localUser = localDisk.getLocalStorage("user");
        this.id_cabang = localUser?.id_cabang;
        this.#insertUrl = `/api/dms/insert-dms`;
        this.setServiceName("stockOpname");
    }

    setIdCabang(id_cabang) {
        this.id_cabang = id_cabang;
        return this;
    }

    async insertDms(data) {
        try {
            const response = await fetchWithAuth(
                "POST",
                this.#insertUrl,
                data
            );
            return Promise.resolve(response);
        } catch (error) {
            return this.throwError(error);
        }
    }
}

export const dmsService = new dms();