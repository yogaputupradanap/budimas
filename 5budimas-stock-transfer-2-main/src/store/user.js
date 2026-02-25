import { defineStore } from "pinia";
import { userService } from "../services/user";
import { localDisk } from "../lib/utils";
import { transferService } from "../services/stockTransfer";

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
    acceptableFeature: [12, 13, 14, 15, 16, 17, 18],
  }),
  getters: {
    userAccess(state) {
      if (state?.userAccessList?.length) {
        const filterFunc = (val) => {
          if (state.acceptableFeature.some((i) => i === val.id)) {
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
            ? namaArray.slice(1).map((val) => val.toLowerCase())
            : null;

          const access = { name: namaAccess };

          if (grantAccess) access["grant"] = grantAccess;

          return access;
        });

        const result = transferService.deduplication(listAccess, [], {
          keyId1: "name",
          keyId2: "name",
          appendKeys: ["grant"],
          sumKeys: []
        });
        return result;
      }

      return [];
    },
  },
  actions: {
    async getUserInfo(id) {
  try {
    this.user.loading = true;

    const user = await userService.getUserInfo(id);

    this.user.value = user;

    console.log("USER INFO:", user);

    transferService.setIdCabang(this.user.value?.id_cabang);
    transferService.setIdPerusahaan(this.user.value?.id_perusahaan);

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
