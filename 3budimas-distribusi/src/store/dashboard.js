import { defineStore } from "pinia";
import { apiUrl, fetchWithAuth, sessionDisk } from "../lib/utils";

export const useDashboard = defineStore("dashboard", {
  state: () => ({
    dashboardInfo: {
      belumKunjungan: 0,
      sudahBerkunjung: 0,
      totalCustomerOrder: 0,
      totalOrder: 0,
      updateTerakhir: 0,
    },
    loading: true,
    error: null,
  }),
  actions: {
    async getDashboardInfo(id_user) {
  if (!id_user) {
    console.warn("id_user undefined — skip dashboard fetch");
    return;
  }

  this.loading = true;
  try {
    const dashboard = await fetchWithAuth(
      "GET",
      `${apiUrl}/api/kepala-cabang/get-user-info/${id_user}`
    );
    this.dashboardInfo = dashboard;
  } catch (err) {
    this.error = err;
  }
  this.loading = false;
},
  },
});
