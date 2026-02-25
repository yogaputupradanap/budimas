import { defineStore } from "pinia";
import { principalService } from "../services/principal";
import { base } from "./mainStore";
import { stockOpnameService } from "../services/stockOpname";

export const useOthers = defineStore("others", {
  state: () => ({
    principal: { ...base },
    stockOpname: {
      ...base,
      id_stock_opname: "",
      produks: [],
    },
  }),
  actions: {
    async getPrincipal() {
      try {
        this.principal.loading = true;
        this.principal.list = await principalService.getAllPrincipal();
      } catch (error) {
        this.principal.error = error;
        console.error(`error happen in others store with -> ${error}`)
      } finally {
        this.principal.loading = false;
      }
    },
    async getKodeStockOpname() {
      try {
        this.stockOpname.loading = true;
        const res = await stockOpnameService.getIdStockOpname();
        const nextId = res.length + 1;
        this.stockOpname.id_stock_opname = `SO-${String(nextId).padStart(3, '0')}`;
      } catch (error) {
        this.stockOpname.error = error;
        console.error(`error happen in others store with -> ${error}`)
      } finally {
        this.stockOpname.loading = false;
      }
    },
    async getProdukByPrincipal(principal) {
      try {
        this.stockOpname.loading = true;
        this.stockOpname.produks = await stockOpnameService.getProdukByPrincipal(principal);
      } catch (error) {
        this.stockOpname.error = error;
        console.error(`error happen in others store with -> ${error}`)
      } finally {
        this.stockOpname.loading = false;
      }
    },
    async createStockOpname(data) {
      try {
        this.stockOpname.loading = true;
        await stockOpnameService.createStockOpname(data);
      } catch (error) {
        this.stockOpname.error = error;
        console.error(`error happen in others store with -> ${error}`)
      } finally {
        this.stockOpname.loading = false;
      }
    },
    async getAllStockOpname() {
      try {
        this.stockOpname.loading = true;
        this.stockOpname.list = await stockOpnameService.getAllStockOpname();
      } catch (error) {
        this.stockOpname.error = error;
        console.error(`error happen in others store with -> ${error}`)
      } finally {
        this.stockOpname.loading = false;
      }
    },
    async getAllStockOpnameFilter(clause) {
      try {
        this.stockOpname.loading = true;
        this.stockOpname.list = await stockOpnameService.getAllStockOpnameFilter(clause);
      } catch (error) {
        this.stockOpname.error = error;
        console.error(`error happen in others store with -> ${error}`)
      } finally {
        this.stockOpname.loading = false;
      }
    },
    async getOneStockOpnameDetail(id) {
      try {
        this.stockOpname.loading = true;
        this.stockOpname.produks = await stockOpnameService.getOneStockOpnameDetail(id);
      } catch (error) {
        this.stockOpname.error = error;
        console.error(`error happen in others store with -> ${error}`)
      } finally {
        this.stockOpname.loading = false;
      }
    },
  },
});
