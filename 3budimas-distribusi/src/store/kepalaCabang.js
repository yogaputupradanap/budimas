/* eslint-disable no-unused-vars */
import { defineStore } from "pinia";
import { apiUrl, fetchWithAuth, localDisk } from "../lib/utils";

const localUser = localDisk.getLocalStorage("user_distribusi");
export const useKepalaCabang = defineStore("kepalaCabang", {
  state: () => ({
    kepalaCabangUser: localUser ?? {
      nama: "",
      id_cabang: null,
      kepalaCabang: null,
    },
    loading: !localUser,
    error: null,
  }),
  actions: {
    async getKepalaCabang(id_kepalaCabang) {
      this.loading = true;
      try {
        const kepalaCabang = await fetchWithAuth(
          "GET",
          `${apiUrl}/api/distribusi/get-user-info/${id_kepalaCabang}`
        );

        this.kepalaCabangUser = {
          nama: kepalaCabang.nama,
          id_cabang: kepalaCabang.id_cabang,
          kepalaCabang,
        };
        localDisk.setLocalStorage("user_distribusi", this.kepalaCabangUser);
      } catch (error) {
        this.error = error;
      } finally {
        this.loading = false;
      }
    },
  },
});
