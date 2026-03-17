import { defineStore } from "pinia";
import { userService } from "../services/user";
import { localDisk } from "../lib/utils";
import { stockOpnameService } from "../services/stockOpname";

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
    acceptableFeature: [3, 5],
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

        const result = stockOpnameService.deduplication(listAccess, [], {
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
        const data = await userService.getUserInfo(id);
        if (this.user.value?.id_cabang) {
            // BERITAHU SERVICE LAIN TENTANG ID CABANG BARU
            stockOpnameService.setIdCabang(this.user.value.id_cabang);
            
            localDisk.setLocalStorage("user", this.user.value);
        }
        
        if (data) {
          this.user.value = data;
          localDisk.setLocalStorage("user", data);
          console.log('User Data Loaded:', this.user.value);
        } else {
          console.warn('User not found in database');
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
