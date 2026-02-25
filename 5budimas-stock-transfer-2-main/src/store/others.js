import {defineStore} from "pinia";
import {cabangService} from "../services/cabang";
import {principalService} from "../services/principal";
import {armadaService} from "../services/armada";
import {base} from "./mainStore";
import {perusahaanService} from "@/src/services/perusahaan";

export const useOthers = defineStore("others", {
    state: () => ({
        cabang: {...base},
        principal: {...base},
        armada: {...base},
        perusahaan: {...base},
    }),
    actions: {
        async getCabang() {
            try {
                this.cabang.loading = true;
                this.cabang.list = await cabangService.getAllCabang();
            } catch (error) {
                this.cabang.error = error;
                console.error(`error happen in others store with -> ${error}`)
            } finally {
                this.cabang.loading = false;
            }
        },
        async getPrincipal() {
            try {
                this.principal.loading = true;
                this.principal.list = await principalService.getAllPrincipal();
            } catch (error) {
                this.principal.error = error;
                console.error(`error happen in others store with -> ${error}`)
            } finally {
                this.principal.loading = true;
            }
        },
        async getArmada() {
            try {
                this.armada.loading = true;
                this.armada.list = await armadaService.getAllArmada();
            } catch (error) {
                this.armada.error = error;
                console.error(`error happen in user store with -> ${error}`)
            } finally {
                this.armada.loading = false;
            }
        },
        async getPerusahaan() {
            try {
                this.perusahaan.loading = true;
                this.perusahaan.list = await perusahaanService.getAllPerusahaan();
            } catch (error) {
                this.perusahaan.error = error;
                console.error(`error happen in user store with -> ${error}`)
            } finally {
                this.perusahaan.loading = false;
            }
        }
    },
});
