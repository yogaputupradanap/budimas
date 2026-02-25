import { defineStore } from "pinia";
import { fetchWithAuth, apiUrl } from "../lib/utils";

const initialState = {
  detailRealisasi: [],
  loading: true,
  error: null,
};

export const useRealisasi = defineStore("realisasi", {
  state: () => ({
    listRealisasiDetail: { ...initialState },
  }),
  actions: {
    resetRealisasiState() {
      this.listRealisasiDetail = { ...initialState };
    },
    async getRealisasiDetail(id_sales_order, id_cabang, id_rute, id_armada, id_driver, delivering_date) {
      const idCabang = `id_cabang=${id_cabang}`;
      const idRute = `id_rute=${id_rute}`;
      const idSalesOrder = `id_sales_order=${id_sales_order}`;
      const idArmada = `id_armada=${id_armada}`;
      const idDriver = `id_driver=${id_driver}`;
      const deliveringDate = `delivering_date=${delivering_date}`;

      try {
        this.listRealisasiDetail.loading = true;
        this.listRealisasiDetail.detailRealisasi = await fetchWithAuth("GET", `${apiUrl}/api/distribusi/get-realisasi-detail?${idCabang}&${idRute}&${idSalesOrder}&${idArmada}&${idDriver}&${deliveringDate}`);
      } catch (error) {
        console.log(error);
        this.listRealisasiDetail.error = error;
      } finally {
        this.listRealisasiDetail.loading = false;
      }
    },
  },
});
console.log(listRealisasiDetail);
