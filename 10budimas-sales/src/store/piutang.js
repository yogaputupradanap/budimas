import { defineStore } from "pinia";
import { apiUrl, fetchWithAuth } from "../lib/utils";

export const usePiutang = defineStore("piutang", {
  state: () => ({
    listPiutang: [],
    tableKey: 0,
    loading: true,
    error: null,
  }),
  actions: {
    /**
     * Asynchronously fetches the piutang data for a given user and customer ID.
     * @param {number} id_user - The ID of the user.
     * @param {number} id_customer - The ID of the customer.
     * @returns None
     */
    async getPiutang(id_user, id_customer) {
      try {
        this.loading = true;
        const idUser = `id_user=${id_user}`
        const idCustomer = `id_customer=${id_customer}`

        this.listPiutang = await fetchWithAuth(
          "GET",
          `${apiUrl}/api/customer/sisa-plafon?${idUser}&${idCustomer}`
        );
        this.tableKey++
      } catch (error) {
        this.error = error;
      }

      this.loading = false;
    },
  },
});
