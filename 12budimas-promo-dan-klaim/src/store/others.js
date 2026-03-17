import { defineStore } from "pinia";
import { base } from "./mainStore";
import { localDisk } from "../lib/utils";
import { salesService } from "../services/sales";
import { customerService } from "../services/customer";
import { principalService } from "../services/principal";
// import { jurnalService } from "../services/jurnal";
import { perusahaanService } from "../services/perusahaan";
import { cabangService } from "../services/cabang";

const localSales = localDisk.getLocalStorage("sales") || [];
const localCustomer = localDisk.getLocalStorage("customer") || [];
const localPrincipal = localDisk.getLocalStorage("principal") || [];

export const useOthers = defineStore("others", {
  state: () => ({
    sales: { ...base, loading: false, list: localSales },
    customer: { ...base, loading: false, list: localCustomer },
    principal: { ...base, loading: false, list: localPrincipal },
    // jurnal: { ...base, loading: false, list: [] },
    perusahaan: { ...base, loading: false, list: [] },
    cabang: { ...base, loading: false, list: [] },
  }),
  actions: {
    async getOthers() {
      try {
        this.sales.loading = true;
        this.customer.loading = true;
        this.principal.loading = true;
        // this.jurnal.loading = true;
        this.cabang.loading = true;
        this.perusahaan.loading = true;

        const [sales, customer, principal, cabang, perusahaan] = await Promise.all([
          salesService.getAllSales(),
          customerService.getAllCustomer(),
          principalService.getAllprincipal(),
          // jurnalService.getJurnal(),
          cabangService.getAllCabang(),
          perusahaanService.getAllPerusahaan(),


        ]);

        localDisk.setLocalStorage("sales", sales);
        localDisk.setLocalStorage("customer", customer);
        localDisk.setLocalStorage("principal", principal);

        this.sales.list = sales;
        this.customer.list = customer;
        this.principal.list = principal;
        // this.jurnal.list = jurnal;
        this.cabang.list = cabang;
        this.perusahaan.list = perusahaan;
        console.log(this.perusahaan.list);
      } catch (error) {
        console.error("error happen in others store: ", error);
      } finally {
        this.sales.loading = false;
        this.customer.loading = false;
        this.principal.loading = false;
        // this.jurnal.loading = false;
        this.cabang.loading = false;
        this.perusahaan.loading = false;
      }
    },
  },
});
