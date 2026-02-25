import {defineStore} from "pinia";
import {fetchWithAuth} from "../lib/utils";

export const useListRute = defineStore("sod", {
    state: () => ({
        arraySOD: [],
        listRute: [],
        loading: false,
        error: null,
    }),
    actions: {
        async fetchSOD(cabang_id) { // Menerima cabang_id sebagai parameter
            this.loading = true;
            try {
                // Menggunakan cabang_id langsung dari parameter
                const clause = {
                    id_cabang: `=${cabang_id}`, // Menggunakan parameter cabang_id
                };
                const data = await fetchWithAuth(
                    "GET",
                    `${process.env.VUE_APP_API_URL}/api/base/rute?where=${JSON.stringify(clause)}`
                );
                this.arraySOD = data;
            } catch (error) {
                this.error = error;
            } finally {
                this.loading = false;
            }
        },
    },
});