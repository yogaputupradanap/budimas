import { defineStore } from "pinia";
import { userService } from "../services/user";
import { userAksesService } from "../services/userAkses";
import { localDisk } from "../lib/utils";

const user = localDisk.getLocalStorage("user");
let hakAkses = localDisk.getLocalStorage("hakakses");

if (!Array.isArray(hakAkses)) {
  hakAkses = [];
}

export const useUser = defineStore("user", {
  state: () => ({
    user: {
      value: user || null,
      loading: false,
      error: null,
    },
    userAccessList: Array.isArray(hakAkses) ? hakAkses : [],
    acceptableFeature: [20, 21, 22, 23],
    jabatanAccess: {
      KASIR: 16,
      AUDIT: 15,
      ADMIN: 2,
    },
  }),

  getters: {
    hasAccess: (state) => (role) => {
      return (
        state.user?.value?.id_jabatan ===
        state.jabatanAccess[role.toUpperCase()]
      );
    },

    userAccess(state) {
      if (!Array.isArray(state.userAccessList)) return [];

      const filterAccessList = state.userAccessList.filter((val) =>
        state.acceptableFeature.includes(val.id)
      );

      return filterAccessList
        .map((val) => {
          if (!val?.nama) return null;

          const namaParts = val.nama.split(" ");
          namaParts.shift();

          const joinedNama = namaParts.join(" ");
          const namaArray = joinedNama.split("-");

          const namaAccess = namaArray[0]
            ?.trim()
            .toLowerCase()
            .replace(/\s+/g, "-");

          const grantAccess =
            namaArray.length > 1
              ? namaArray.slice(1).map((part) => part.trim().toLowerCase())
              : null;

          const access = { name: namaAccess };
          if (grantAccess) access.grant = grantAccess;

          return access;
        })
        .filter(Boolean);
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

      const akses = await userAksesService.getUserAkses(userInfo.id);

      this.userAccessList = Array.isArray(akses) ? akses : [];
      localDisk.setLocalStorage("hakakses", this.userAccessList);

      console.log("hak akses loaded:", this.userAccessList);
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
