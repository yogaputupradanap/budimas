import {defineStore} from "pinia";
import {apiUrl, fetchWithAuth, localDisk} from "../lib/utils";

const localListPengajuan = localDisk.getLocalStorage("list_pengajuan");
const listPengajuan = {
    listPengajuan: [],
    loading: false,
    error: null,
};
const detailRetur = {
    detail: {},
    items: [],
    loading: false,
    error: null,
}


export const useRetur = defineStore("retur", {
    state: () => ({
        listPengajuan,
        detailRetur
    }),
    actions: {
        resetReturState(stateName) {
            Object.assign(this[stateName], eval(stateName));
        },
        async getListPengajuan(id_rute) {
            try {
                this.listPengajuan.loading = true;
                this.listPengajuan.listPengajuan = await fetchWithAuth(
                    "GET",
                    `${apiUrl}/api/retur/get-list-pengajuan?id_rute=${id_rute}`
                );
                localDisk.setLocalStorage("list_pengajuan", this.listPengajuan.listPengajuan);
            } catch (error) {
                this.listPengajuan.error = error;
                console.error("Error fetching data:", error);
            } finally {
                this.listPengajuan.loading = false;
            }
        },
        async getDetailRetur(id_request) {
            try {
                this.detailRetur.loading = true;
                const data = await fetchWithAuth(
                    "GET",
                    `${apiUrl}/api/retur/get-detail-retur/${id_request}`
                );
                this.detailRetur.detail = data.header;
                this.detailRetur.items = data.detail;
            } catch (error) {
                this.detailRetur.error = error;
                console.error("Error fetching detail retur:", error);
            } finally {
                this.detailRetur.loading = false;
            }
        },
    },
});
