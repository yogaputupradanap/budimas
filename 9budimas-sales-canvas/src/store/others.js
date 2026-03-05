import { defineStore } from "pinia";
import { base } from "./mainStore";
import { localDisk } from "../lib/utils";
import { principalService } from "../services/principal";
import { salesCanvasService } from "../services/salesCanvas";

const localPrincipal = localDisk.getLocalStorage("principal");
const localSalesCanvas = localDisk.getLocalStorage("salesCanvas") ;

export const useOthers = defineStore("others", {
  state: () => ({
    principal: { ...base, list: localPrincipal },
    salesCanvas: { ...base, list: localSalesCanvas },
    isLoading: false,
  }),
  actions: {
    async getOthers() {
      try {
        this.isLoading = true;
        this.principal.loading = true;
        this.salesCanvas.loading = true;

        const [principal, salesCanvas] = await Promise.all([
          principalService.getAllprincipal(),
          salesCanvasService.getAllCanvasRequest(),
        ]);

        localDisk.setLocalStorage("principal", principal);
        localDisk.setLocalStorage("salesCanvas", salesCanvas);

        this.principal.list = principal;
        this.salesCanvas.list = salesCanvas;
      } catch (error) {
        console.error("error happen in others store: ", error);
      } finally {
        this.isLoading = false;
        this.principal.loading = false;
        this.salesCanvas.loading = false;
      }
    },
  },
});