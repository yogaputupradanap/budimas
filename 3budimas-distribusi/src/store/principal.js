import { defineStore } from "pinia";
import { apiUrl, fetchWithAuth } from "../lib/utils";

export const usePrincipal = defineStore("principal", {
  state: () => ({
    principals: null,
    loading: true,
    error: null,
    principalProduct: {
      products: [],
      tableKey: 0,
      loading: true,
      error: null,
    },
  }),
  getters: {
    stockOpnameProducts(state) {
      return state.principalProduct.products.map((product, idx) => ({
        no: idx + 1,
        ...product,
        pieces: 0,
        box: 0,
        karton: 0,
      }));
    },
  },
  actions: {
    async getPrincipals(user_id, customer_id) {
      this.loading = true;
      try {
        this.principals = await fetchWithAuth(
          "POST",
          `${apiUrl}/api/principal/get-principals`,
          {
            user_id,
            customer_id,
          }
        );

      } catch (error) {
        this.error = error;
      }
      this.loading = false;
    },
    async getPrincipalProducts(principal_id, user_id, customer_id) {
      this.principalProduct.loading = true;
      try {
        this.principalProduct.products = await fetchWithAuth(
          "POST",
          `${apiUrl}/api/produk/get-plafon-produks`,
          {
            principal_id,
            user_id,
            customer_id,
          }
        );
        this.principalProduct.tableKey++;
      } catch (error) {
        this.principalProduct.error = error;
      }
      this.principalProduct.loading = false;
    },
  },
});
