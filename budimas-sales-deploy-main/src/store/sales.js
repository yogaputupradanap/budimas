/* eslint-disable no-unused-vars */
import { defineStore } from "pinia";
import { apiUrl, fetchWithAuth, localDisk } from "../lib/utils";

export const useSales = defineStore("sales", {
  state: () => ({
    salesUser: localDisk.getLocalStorage("user"),
    loading: true,
    error: null,
  }),
  actions: {
    /**
     * Asynchronously fetches sales data for a given sales ID.
     * @param {number} id_sales - The ID of the sales data to retrieve.
     * @returns None
     */
    async getSales(id_sales) {
      this.loading = true
      try {
        const sales = await fetchWithAuth(
          "GET",
          `${apiUrl}/api/sales/get-user/${id_sales}`
        );
        this.salesUser = sales;
        localDisk.setLocalStorage("user", this.salesUser)
      } catch (error) {
        this.error = error;
      }
    },
    deactivateLoading(){
      this.loading = false
    }
  },
});

// below is the example of what salesUser looks like

// {
//   "alamat": "Jalan tembus kadipiro kp.serut rt 04 rw 12",
//   "alamat_wp": null,
//   "departemen_id": null,
//   "email": "boysolo@gmail.com",
//   "id": 2,
//   "id_cabang": 5,
//   "id_jabatan": 2,
//   "id_wilayah1": 33,
//   "id_wilayah2": 3372,
//   "id_wilayah3": 3372040,
//   "id_wilayah4": 3372040011,
//   "kode": "A.IT",
//   "nama": "ADMIN IT",
//   "nama_wp": null,
//   "nik": "123456",
//   "no_rekening": null,
//   "npwp": null,
//   "password": "test",
//   "sales": {
//       "id": 3,
//       "id_principal": null,
//       "id_tipe": 1,
//       "id_user": 48,
//       "id_wilayah1": 12,
//       "id_wilayah2": 1204,
//       "nama_cabang": "SOLO",
//       "nama_jabatan": "ADMIN IT"
//   },
//   "tanggal_lahir": "2023-10-02",
//   "telepon": "0271856064",
//   "tokens": "AMQpJs2g9GTxQrj5ZoHA2384Rlox44MiOFxO1niJ0tPBtTQbO0NUxQWm3jao",
//   "username": "BoySolo"
// }
