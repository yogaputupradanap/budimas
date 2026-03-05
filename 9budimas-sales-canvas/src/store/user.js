import { defineStore } from "pinia";
import { userService } from "../services/user";
import { localDisk } from "../lib/utils";
import { listFeatures } from "./mainStore";

const user = localDisk.getLocalStorage("user");
const ROLE_CANVAS = 22

export const useUser = defineStore("user", {
  state: () => ({
    user: {
      value: user || null,
      loading: false,
      error: null,
    },
    jabatanAccess: Object.fromEntries(
      listFeatures.map((route) => [route, ROLE_CANVAS])
    )
  }),
  getters: {
    hasAccess: (state) => (routeName) => {
      if (!routeName || !state.user?.value?.id_jabatan) return false;
      const requiredRole = state.jabatanAccess[routeName];
      return state.user.value.id_jabatan === requiredRole;
    },
  },
  actions: {
    async getUserInfo(id) {
      try {
        this.user.loading = true;
        const response = await userService.getUserInfo(id);

        console.log("Data diterima di Store:", response);

        // Karena di userService sudah kita return userInfo.result[0],
        // maka 'response' di sini sudah langsung berisi objek {id: 216, email: ...}
        if (response && response.id) {
            this.user.value = response;
            localDisk.setLocalStorage("user", response);
            console.log("Sukses simpan user ke LocalStorage!");
        } else {
            console.error("Data user tidak valid atau kosong");
        }

      } catch (error) {
        console.error(`Error: ${error}`);
      } finally {
        this.user.loading = false;
      }
    },
  },
});
