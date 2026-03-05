import { defineStore } from "pinia";
import { apiUrl, fetchWithAuth, localDisk } from "../lib/utils";
import { useKunjungan } from "./kunjungan";

export const usePrincipal = defineStore("principal", {
  state: () => ({
    principals: localDisk.getLocalStorage("principal"),
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
      return state.principalProduct.products.map((product) => ({
        ...product,
        pieces: 0,
        box: 0,
        karton: 0,
      }));
    },
    idPlafons(state) {
      return state.principals.map((val) => val.plafon_id);
    },
  },
  actions: {
    /**
     * Asynchronously fetches the principals for a given user and customer ID.
     * Sets loading to true while fetching data, then sets loading to false when done.
     * If successful, stores the fetched principals in local storage under the key 'principal'.
     * If an error occurs during the fetch, sets the error property to the error object.
     * @param {string} user_id - The ID of the user.
     * @param {string} customer_id - The ID of the customer.
     * @returns None
     */
    async getPrincipals(user_id, customer_id) {
      this.loading = true;
      try {
        const idUser = `user_id=${user_id}`;
        const idCustomer = `customer_id=${customer_id}`;

        // Dapatkan kunjungan aktif untuk mengakses id_plafon
        const kunjungan = useKunjungan();
        const activeKunjungan = kunjungan.activeKunjungan.kunjungan;

        // Tambahkan id_plafon ke query jika tersedia
        let plafonParams = "";
        if (activeKunjungan && activeKunjungan.id_plafon) {
          // Flatten id_plafon jika berbentuk array
          const plafonIds = Array.isArray(activeKunjungan.id_plafon)
            ? activeKunjungan.id_plafon.flat()
            : [activeKunjungan.id_plafon];

          if (plafonIds.length > 0) {
            plafonParams = `&plafon_ids=${plafonIds.join(",")}`;
          }
        }

        console.log(
          "Fetching principals with params:",
          idUser,
          idCustomer,
          plafonParams
        );

        const principals = await fetchWithAuth(
          "GET",
          `${apiUrl}/api/principal/get-principals?${idUser}&${idCustomer}${plafonParams}`
        );

        this.principals = principals.reduce((acc, val) => {
          const checkDuplicate = acc.some((i) => i.id == val.id);
          if (!checkDuplicate) acc.push(val);

          return acc;
        }, []);

        console.log("Fetched principals:", this.principals);
        localDisk.setLocalStorage("principal", this.principals);
      } catch (error) {
        console.error("Error fetching principals:", error);
        this.error = error;
      }
      this.loading = false;
    },
    /**
     * Asynchronously fetches the principal products data and updates the state accordingly.
     * @returns None
     */
    async getPrincipalProducts() {
      const kunjungan = useKunjungan();
      let products = [];
      this.principalProduct.loading = true;

      try {
        for (const principal of this.principals) {
          const idPrincipal = `principal_id=${principal.id}`;
          const idUser = `user_id=${kunjungan.activeKunjungan.kunjungan.user_id}`;
          const idCustomer = `customer_id=${kunjungan.activeKunjungan.kunjungan.customer_id}`;

          const product = await fetchWithAuth(
            "GET",
            `${apiUrl}/api/produk/get-plafon-produks?${idPrincipal}&${idUser}&${idCustomer}`
          );
          products = [...products, ...product];
        }

        this.principalProduct.products = products;
        this.principalProduct.tableKey++;
      } catch (error) {
        this.principalProduct.error = error;
      }
      this.principalProduct.loading = false;
    },
  },
});
