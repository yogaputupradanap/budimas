import { defineStore } from "pinia";
import { base } from "./mainStore";
import { localDisk } from "../lib/utils";
import { customerService } from "../services/customer";

const localProduk = localDisk.getLocalStorage("produk") || [];

export const useProduk = defineStore("produk", {
  state: () => ({
    produk: { ...base, loading: false, list: localProduk },
  }),
  actions: {
    async getProduk() {
      try {
        this.produk.loading = true;
        const res = await customerService.getCustomers();
        this.produk.list = res
      } catch (error) {
        this.produk.error = error;
      } finally {
        this.produk.loading = false;
      }
    },
  },
});
