import { defineStore } from "pinia";
import { apiUrl, fetchWithAuth, sessionDisk, localDisk } from "../lib/utils";
import { useDashboard } from "./dashboard";
import { usePrincipal } from "./principal";
import { usePembayaran } from "./pembayaran";

export const useKunjungan = defineStore("kunjungan", {
  state: () => ({
    listKunjungan: [],
    tableKey: 0,
    loading: true,
    error: null,
    activeKunjungan: {
      kunjungan: localDisk.getLocalStorage("activeKunjungan") || {},
      loading: false,
      error: null,
    },
  }),
  actions: {
    /**
     * Creates a new sales visit record for a user with the given userId.
     * @param {string} userId - The ID of the user for whom the sales visit is being created.
     * @returns None
     */
    async createKunjungan(userId) {
      try {
        await fetchWithAuth(
          "POST",
          `${apiUrl}/api/sales-kunjungan/create-sales-kunjungan`,
          {
            id_user: userId,
          }
        );
        this.kunjunganCreated(userId);
      } catch (error) {
        console.log(error);
      }
    },
    kunjunganCreated(userId) {
      const dashboard = useDashboard();
      dashboard.getDashboardInfo(userId);
    },
    /**
     * Asynchronously fetches a list of visits for a given user ID and updates the component state accordingly.
     * @param {string} userId - The ID of the user for whom the visits are being fetched.
     * @returns None
     */
    async getListKunjungan(userId) {
      this.loading = true;
      try {
        const listKunjungan = await fetchWithAuth(
          "GET",
          `${apiUrl}/api/sales-kunjungan/get-list-kunjungan/${userId}`
        );

        this.listKunjungan = [];

        listKunjungan.forEach((list_1, idx) => {
          this.listKunjungan.push({ no: idx + 1, ...list_1 });

          if (list_1.status === 1) this.activeKunjungan.kunjungan = list_1;
        });

        if (!this.listKunjungan.some((list_1) => list_1.status === 1)) {
          this.activeKunjungan.kunjungan = null;
          localDisk.removeLocalStorage("activeKunjungan");
        }

        this.tableKey++;
      } catch (error) {
        this.error = error;
      }

      this.loading = false;
    },
    /**
     * Asynchronously checks in or checks out a visit based on the provided visit ID and status.
     * @param {string} kunjunganId - The ID of the visit to check in or out.
     * @param {number} status - The status of the visit (1 for check-in, 2 for check-out).
     * @returns None
     */
    async checkInOutKunjungan(kunjunganId, status) {
      this.activeKunjungan.loading = true;
      const user = sessionDisk.getSession("authUser");
      const dashboard = useDashboard();
      const id_kunjungan_string = JSON.stringify(kunjunganId);
      const apiRoute = `${apiUrl}/api/sales-kunjungan/check-${
        status === 1 ? "in" : status === 2 ? "out" : ""
      }-kunjungan/${id_kunjungan_string}?id_user=${user?.id_user}`;

      try {
        const checkIn = await fetchWithAuth("PUT", apiRoute);
        const user = sessionDisk.getSession("authUser");

        this.activeKunjungan.kunjungan =
          status === 1 ? checkIn : status === 2 ? null : null;

        this.listKunjungan.forEach((list, idx) => {
          const listId = JSON.stringify(list.id);

          if (listId === id_kunjungan_string) {
            this.listKunjungan[idx].status = status;
          }
        });

        localDisk.setLocalStorage(
          "activeKunjungan",
          this.activeKunjungan.kunjungan
        );

        if (status === 2) {
          await dashboard.getDashboardInfo(user.id_user);
          dashboard.deactivateLoading();
        }

        this.tableKey++;
      } catch (error) {
        this.activeKunjungan.error = error;
      }
      this.activeKunjungan.loading = false;
      this.emptyVisitDashboardCache();
    },
    /**
     * Sets the active visit based on the provided visit ID.
     * @param {string} kunjunganId - The ID of the visit to set as active.
     * @returns None
     */
    async setActiveKunjungan(kunjunganId) {
      this.activeKunjungan.kunjungan = this.listKunjungan.find(
        (list) => JSON.stringify(list?.id) === JSON.stringify(kunjunganId)
      );

      localDisk.setLocalStorage(
        "activeKunjungan",
        this.activeKunjungan.kunjungan
      );
      this.emptyVisitDashboardCache();
    },
    emptyVisitDashboardCache() {
      const pembayaran = usePembayaran();
      const principal = usePrincipal();

      pembayaran.$reset();
      principal.$reset();
      principal.$reset();
    },
  },
});

// below is what activekunjungan.kunjungan looks like :

// {
//   "customer_id": 46678,
//   "id": 40,
//   "latitude": "-7.308338788974115",
//   "longitude": "108.5951603969662",
//   "nama_customer": "CV.SUMBER SEHAT BERSAMA",
//   "id_plafon": 15,
//   "status": 1,
//   "tanggal": "2024-02-28",
//   "user_id": 48,
//   "waktu_mulai": "09:29:25",
//   "waktu_selesai": null
// }
