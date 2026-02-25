import { defineStore } from "pinia";
import { base } from "./mainStore";
import { perusahaanService } from "../services/perusahaan";
import { cabangService } from "../services/cabang";

export const useOthers = defineStore("others", {
  state: () => ({
    perusahaan: { ...base, loading: false, list: [] },
    cabang: { ...base, loading: false, list: [] },
  }),

  actions: {
    async getOthers() {
      try {
        this.perusahaan.loading = true;
        const perusahaan = await perusahaanService.getAllPerusahaan();
        const cabang = await cabangService.getAllCabang();
        // console.log("Fetched perusahaan:", perusahaan);
        // console.log("Fetched Cabang:", cabang);
        this.perusahaan.list = perusahaan;
        this.cabang.list = cabang;
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        this.perusahaan.loading = false;
      }
    },
  },
});

// export const useGetPerusahaan = defineStore("getPerusahaan", {
//   state: () => ({
//     perusahaan: { ...base, loading: false, list: [] },
//   }),
//   actions: {
//     async fetchPerusahaan() {
//       try {
//         this.perusahaan.loading = true;
//         const perusahaan = await perusahaanService.getAllPerusahaan();
//         console.log("Fetched perusahaan:", perusahaan);
//         this.perusahaan.list = perusahaan;
//       } catch (error) {
//         console.error("Error fetching data:", error);
//       } finally {
//         this.perusahaan.loading = false;
//       }
//     },
//   },
// });