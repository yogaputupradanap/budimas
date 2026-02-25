import { defineStore } from "pinia";
import { base } from "./mainStore";
import { localDisk } from "../lib/utils";
import { customerService } from "../services/customer";

const localCustomer = localDisk.getLocalStorage("customer") || [];

export const useCustomer = defineStore("customer", {
  state: () => ({
    customer: { ...base, loading: false, list: localCustomer },
  }),
  actions: {
    async getCustomer() {
      try {
        this.customer.loading = true;
        this.customer.list = await customerService.getCustomers();
      } catch (error) {
        this.customer.error = error;
      } finally {
        this.customer.loading = false;
      }
    },
  },
});
