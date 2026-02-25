import { defineStore } from "pinia";
import { base } from "./mainStore";
import { localDisk } from "../lib/utils";
import { principalService } from "../services/principal";

const localPrincipal = localDisk.getLocalStorage("principal") || [];

export const usePrincipal = defineStore("others", {
  state: () => ({
    principal: { ...base, loading: false, list: localPrincipal },
  }),
  actions: {
    async getPrincipal() {
      try {
        this.principal.loading = true;
        this.principal.list = await principalService.getPrincipals();
      } catch (error) {
        this.principal.error = error;
      } finally {
        this.principal.loading = false;
      }
    },
  },
});
