import { defineStore } from "pinia";
import { userService } from "../services/user";
import { localDisk } from "../lib/utils";
// import { transferService } from "../services/stockTransfer";

const user = localDisk.getLocalStorage("user");
const hakAkses = localDisk.getLocalStorage("hakakses");

export const useUser = defineStore("user", {
  state: () => ({
    user: {
      value: user || null,
      loading: false,
      error: null,
    },
    userAccessList: hakAkses || [],
    acceptableFeature: [31, 32, 33, 35],
    jabatanAccess: {
      KOOR_FAKTURIS: 20,
    }
  }),
  getters: {
    // Add getter for checking jabatan
    hasAccess: (state) => (role) => {
      return state.user?.value.id_jabatan === state.jabatanAccess[role.toUpperCase()]
    },
    userAccess(state) {
      if (state?.userAccessList?.length) {
        const filterFunc = (val) => {
          if (state.acceptableFeature.some((feat) => feat === val.id)) {
            return val;
          }
        };

        const filterAccessList = state.userAccessList.filter(filterFunc);
        const listAccess = filterAccessList.map((val) => {
          const removeOlahPrefix = val?.nama?.split(" ");
          removeOlahPrefix?.shift();

          const namaArray = removeOlahPrefix?.join(" ")?.split("-");
          const namaAccess = namaArray[0]?.split(" ")?.join("-")?.toLowerCase();
          const grantAccess = namaArray[1]
            ? namaArray.slice(1).map((item) => item.toLowerCase())
            : null;

          const access = { name: namaAccess };

          if (grantAccess) access["grant"] = grantAccess;
          return access;
        });

        return listAccess;
      }

      return [];
    }
  },
  actions: {
    async getUserInfo(id) {
      try {
        this.user.loading = true;
        this.user.value = await userService.getUserInfo(id);
        // transferService.setIdCabang(this.user.value?.id_cabang);
        localDisk.setLocalStorage("user", this.user.value);
      } catch (error) {
        this.user.error = error;
        console.error(`error happen in user store with -> ${error}`);
      } finally {
        this.user.loading = false;
      }
    },
  },
});
