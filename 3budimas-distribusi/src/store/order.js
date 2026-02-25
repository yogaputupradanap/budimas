import { defineStore } from "pinia";
import { apiUrl, fetchWithAuth } from "../lib/utils";

export const useOrder = defineStore("order", {
  state: () => ({
    lastUpdate: null,
    listOrder: [],
    loading: true,
    error: null,
  }),
  actions: {
    async getListOrder(id_cabang, isDraft = false) {
      this.loading = true
      const orderEndPoints = {
        nonDraft: `/api/distribusi/get-list-order/${id_cabang}`,
        draft: `/api/distribusi/get-list-verifikasi?id_cabang=${id_cabang}`,
      };
      const orderEndpoint = isDraft
        ? orderEndPoints["draft"]
        : orderEndPoints["nonDraft"];

      try {
        const order = await fetchWithAuth("GET", `${apiUrl}${orderEndpoint}`);
        // console.log("Fetched Order Data:", `${apiUrl}${orderEndpoint}`);

        this.lastUpdate = order.last_update;
        this.listOrder = order?.listOrder || order;
      } catch (error) {
        console.log(error);
        this.error = error;
      } finally {
        this.loading = false;
      }
    },
  },
});
