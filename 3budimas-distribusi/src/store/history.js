import {defineStore} from "pinia";
import {apiUrl, fetchWithAuth} from "../lib/utils";

const listRuteHistory = {
    listRute: [],
    loading: true,
    error: null,
};

const baseNotaList = {
    listNota: [],
    loading: true,
    error: null,
};

const listNotaTerkirim = {...baseNotaList};
const listNotaProses = {...baseNotaList};
const listNotagagal = {...baseNotaList};
const listHistoryDistribusi = {...baseNotaList};

export const useHistory = defineStore("history", {
    state: () => ({
        listRuteHistory,
        listNotaTerkirim,
        listNotaProses,
        listNotagagal,
        listHistoryDistribusi,
    }),
    actions: {
        resetState(stateName) {
            Object.assign(this[stateName], eval(stateName));
        },
        async getAllNota(idCabang, idRute) {
            const listStatus = [4, 10];
            for (const status of listStatus) {
                await this.getListNota(idCabang, idRute, status);
            }
        },
        async getRuteList(id_cabang) {
            try {
                this.listRuteHistory.loading = true;
                this.listRuteHistory.listRute = await fetchWithAuth(
                    "GET",
                    `${apiUrl}/api/distribusi/get-list-rute-history/${id_cabang}`
                );
            } catch (error) {
                this.listRuteHistory.error = error;
                console.log(error);
            } finally {
                this.listRuteHistory.loading = false;
            }
        },

        async getListNota(id_cabang, id_rute, status_faktur) {
            const idRute = `id_rute=${id_rute}`;
            const idCabang = `id_cabang=${id_cabang}`;
            const status = `status_faktur=${status_faktur}`;

            try {
                switch (status_faktur) {
                    case 4:
                        currState = this.listNotaProses;
                        break;
                    case 5:
                        currState = this.listNotaTerkirim;
                        break;
                    case 7:
                        currState = this.listNotagagal;
                        break;
                    case 8:
                        currState = this.listNotaTerkirim;
                        break;
                }

                currState.loading = true;
                const listNota = await fetchWithAuth(
                    "GET",
                    `${apiUrl}/api/distribusi/get-list-nota-history?${idRute}&${idCabang}&${status}`
                );

                currState.listNota = currState.listNota.concat(listNota)
            } catch (error) {
                currState.error = error;
                console.log(error);
            } finally {
                currState.loading = false;
            }
        },
    },
});
