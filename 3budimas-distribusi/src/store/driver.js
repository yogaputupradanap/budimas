import { defineStore } from "pinia";
import { apiUrl, fetchWithAuth, sessionDisk } from "../lib/utils";

const baseDriver = {
  list: [],
  loading: true,
  error: null,
};

export const driver = { ...baseDriver };
export const listPengeluaran = { ...baseDriver };
export const listInfoFaktur = { ...baseDriver, loading: false };
export const infoPengeluaran = { ...baseDriver, info: {} };

export const useDriver = defineStore("driver", {
  state: () => ({
    driver,
    listPengeluaran,
    listInfoFaktur,
    infoPengeluaran,
  }),
  actions: {
    addPengeluaranDriver(driverData) {
      this.listPengeluaran.list = [...this.listPengeluaran.list, driverData];
    },
    updatePengeluaranDriver(driverData) {
      this.listPengeluaran.list = this.listPengeluaran.list.filter((val) => {
        return val.id_info_driver !== driverData.id_info_driver;
      });

      this.addPengeluaranDriver(driverData);
    },
    async getListDriver(state, url) {
      try {
        this.listPengeluaran.loading = true;
        this.listPengeluaran.list = await fetchWithAuth(
          "GET",
          `${apiUrl}/api/distribusi/get-pengeluaran-driver-list`
        );
      } catch (error) {
        this.listPengeluaran.error = error;
        console.log(error);
      } finally {
        this.listPengeluaran.loading = false;
      }
    },
    async getAllDriver() {
    const idCabang = sessionDisk.getSession("id_cabang_distribusi");

      if (!idCabang) {
        console.warn("idCabang tidak ditemukan di session");
        return;
      }      
      try {
        this.driver.loading = true;
        this.driver.list = await fetchWithAuth(
          "GET",
          `${apiUrl}/api/distribusi/get-all-driver?id_cabang=${idCabang}`
        );
      } catch (error) {
        this.driver.error = error;
        console.log(error);
      } finally {
        this.driver.loading = false;
      }
    },
    async getInfoPengeluaran(id) {
      try {
        this.infoPengeluaran.loading = true;
        this.infoPengeluaran.info = await fetchWithAuth(
          "GET",
          `${apiUrl}/api/distribusi/get-pengeluaran-driver-info-update/${id}`
        );
      } catch (error) {
        console.log(error);
        this.infoPengeluaran.error = error;
      } finally {
        this.infoPengeluaran.loading = false;
      }
    },
    async getDriverFaktur(id, type) {
      try {
        let endPoint = `get-pengeluaran-driver-info-fakturs-`;

        if (type === "add") endPoint += "add";
        else if (type === "update") endPoint += "update";

        this.listInfoFaktur.loading = true;
        this.listInfoFaktur.list = await fetchWithAuth(
          "GET",
          `${apiUrl}/api/distribusi/${endPoint}/${id}`
        );
      } catch (error) {
        this.listInfoFaktur.error = error;
        console.log(error);
      } finally {
        this.listInfoFaktur.loading = false;
      }
    },
  },
});
