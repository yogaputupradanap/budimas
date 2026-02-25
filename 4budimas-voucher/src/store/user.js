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
  }),
  getters: {
    // userAccess(state) {
    //   return [
    //     {
    //       name: 'setoran tunai',
    //       grant: ['kasir']
    //     }
    //   ]
    // },
    userAccess(state) {
      const listAccess = state.userAccessList.map((val) => {
        const removeOlahPrefix = val?.nama?.split(" ");
        removeOlahPrefix?.shift();

        const namaArray = removeOlahPrefix?.join(" ")?.split("-");

        const namaAccess = namaArray[0]?.split(" ")?.join("-")?.toLowerCase();
        const grantAccess = namaArray[1] ? namaArray[1]?.toLowerCase() : null;

        const access = { name: namaAccess };

        if (grantAccess) access["grant"] = grantAccess;

        return access;
      });

      console.log('store hak akses : ', listAccess)
      return listAccess;
    },
  },
  actions: {
    async getUserInfo(id) {
      try {
        this.user.loading = true;
        const user = await userService.getUserInfo(id);
        this.user.value = user
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
