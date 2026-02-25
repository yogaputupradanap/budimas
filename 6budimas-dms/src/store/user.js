import { defineStore } from "pinia";
import { userService } from "../services/user";
import { localDisk } from "../lib/utils";

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
    acceptableFeature: [4],
  }),
  getters: {
   userAccess(state) {
  return state.userAccessList.map((val) => {
    const removeOlahPrefix = val?.nama?.split(" ");
    removeOlahPrefix?.shift();

    const namaArray = removeOlahPrefix?.join(" ")?.split("-");
    const namaAccess = namaArray[0]?.split(" ")?.join("-")?.toLowerCase();

    return { name: namaAccess };
  });
},
  },
  actions: {
    async getUserInfo(id) {
  try {
    this.user.loading = true;

    const userInfo = await userService.getUserInfo(id);

    if (userInfo) {
      this.user.value = userInfo;
      localDisk.setLocalStorage("user", userInfo);

      this.userAccessList = hakAkses;
      localDisk.setLocalStorage("hakakses", hakAkses);

      console.log("hak akses loaded:", hakAkses);
    }

  } catch (error) {
    this.user.error = error;
    console.error(`error happen in user store with -> ${error}`);
  } finally {
    this.user.loading = false;
  }
},
  },
});
