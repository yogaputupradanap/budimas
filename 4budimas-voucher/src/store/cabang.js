import { defineStore } from "pinia";
import { base } from "./mainStore";
import { localDisk } from "../lib/utils";
import { cabangService } from "../services/cabang";

const localCabang = localDisk.getLocalStorage("cabang") || [];

export const useCabang = defineStore("cabang", {
  // Ubah "others" menjadi "cabang"
  state: () => ({
    cabang: { ...base, loading: false, list: localCabang },
  }),
  actions: {
    async fetchCabang() {
      // Rename method untuk konsistensi
      try {
        this.cabang.loading = true;
        const result = await cabangService.getCabangs();
        this.cabang.list = result;
        // Simpan ke localStorage
        localDisk.setLocalStorage("cabang", result);
        return result;
      } catch (error) {
        this.cabang.error = error;
        throw error;
      } finally {
        this.cabang.loading = false;
      }
    },
  },
});
