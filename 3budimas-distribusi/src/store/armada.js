import { defineStore } from "pinia";
import { apiUrl, fetchWithAuth, sessionDisk } from "../lib/utils";

const base = {
  list: [],
  loading: false,
  error: null,
};

export const useArmada = defineStore("armada", {
  state: () => ({
    armada: { ...base },
    infoArmada: { ...base },
  }),

  actions: {
    async getAllArmada() {
      const idCabang = sessionDisk.getSession("id_cabang_distribusi");

      if (!idCabang) {
        console.warn("idCabang tidak ditemukan di session");
        return;
      }

      try {
        this.armada.loading = true;

        this.armada.list = await fetchWithAuth(
          "GET",
          `${apiUrl}/api/distribusi/get-all-armada?id_cabang=${idCabang}`
        );
      } catch (error) {
        console.log(error);
        this.armada.error = error;
      } finally {
        this.armada.loading = false;
      }
    },

    async getDistribusi(idRute) {
      const idCabang = sessionDisk.getSession("id_cabang_distribusi");

      if (!idCabang || !idRute) return;

      try {
        this.infoArmada.loading = true;

        this.infoArmada.list = await fetchWithAuth(
          "GET",
          `${apiUrl}/api/distribusi/get-info-rute-armada?id_cabang=${idCabang}&id_rute=${idRute}`
        );
      } catch (error) {
        console.log(error);
        this.infoArmada.error = error;
      } finally {
        this.infoArmada.loading = false;
      }
    },
  },
});
