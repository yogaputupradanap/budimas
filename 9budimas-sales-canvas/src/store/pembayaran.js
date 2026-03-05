import { defineStore } from "pinia";
import { apiUrl, encode, fetchWithAuth } from "../lib/utils";
import { usePrincipal } from "./principal";

export const usePembayaran = defineStore("pembayaran", {
  state: () => ({
    pembayaran: [],
    listPembayaran: [],
    activePembayaran: {},
    visited: false,
    tableKeyActive: 0,
    tableKey: 0,
    loading: true,
    error: null,
  }),
  actions: {
    /**
     * Asynchronously fetches payment data and processes it to display in a table.
     * @returns None
     */
    async getFaktur() {
      const principal = usePrincipal();
      const id_plafon = JSON.stringify(principal.idPlafons);

      const columnSetoran = encode(["id", "id_sales_order", "jumlah_setoran"]);
      this.loading = true;

      try {
        const fakturs = await fetchWithAuth(
          "GET",
          `${apiUrl}/api/finance/list-tagihan-jatuh-tempo/${id_plafon}`
        );

        const idSalesOrder = fakturs.map((val) => val.id_sales_order);

        const arrayValue =
          idSalesOrder.length > 0
            ? `array[${idSalesOrder}]`
            : `array[]::integer[]`;

        const clauseSetoran = encode({
          "setoran.id_sales_order = ": `any (${arrayValue})`,
          "setoran.status_setoran = ": 3,
        });

        const setoran = await fetchWithAuth(
          "GET",
          `${apiUrl}/api/base/setoran/all?columns=${columnSetoran}&clause=${clauseSetoran}`
        );

        const includeSetoranSumInFaktur = fakturs.reduce((acc, val) => {
          let sumSetoran = 0;
          const filterSetoran = setoran.filter(
            (i) => i.id_sales_order == val.id_sales_order
          );

          if (filterSetoran.length) {
            sumSetoran = filterSetoran.reduce(
              (accI, i) => accI + i?.jumlah_setoran ?? 0,
              0
            );
          }

          acc.push({
            ...val,
            jumlah_bayar: sumSetoran,
          });

          return acc;
        }, []);

        this.listPembayaran = includeSetoranSumInFaktur;
      } catch (err) {
        console.log("error happen when fetch fakturs : ", err);
      } finally {
        this.loading = false;
        this.tableKey++;
      }
    },
    /**
     * Sets the active payment based on the provided invoice note.
     * @param {string} notaTagihan - The invoice note to set as active payment.
     * @returns None
     */
    setActivePembayaran(notaTagihan) {
      /**
       * Finds and sets the active payment from the list of payments based on the provided notaTagihan.
       * @param {string} notaTagihan - The notaTagihan to search for in the list of payments.
       * @returns None
       */
      this.activePembayaran = this.listPembayaran.find(
        (list) => list.notaTagihan === notaTagihan
      );
    },
    /**
     * Update the state of a faktur with the given id.
     * @param {number} id_faktur - The id of the faktur to update.
     * @param {string} status - The new status to set for the faktur.
     * @param {number} jumlah_setoran - The amount of the deposit.
     * @returns None
     */
    updateFakturState(id_faktur, status, jumlah_setoran) {
      /**
       * Find and return the active faktur based on the provided faktur ID.
       * @param {number} id_faktur - The ID of the faktur to find.
       * @returns The active faktur object with the matching ID, or undefined if not found.
       */
      const activeFaktur = this.activePembayaran.faktur.find(
        (val) => val.id === id_faktur
      );

      /**
       * Find a specific payment in the list of payments based on the notaTagihan property of the active payment.
       * @returns The payment object that matches the notaTagihan of the active payment, or undefined if not found.
       */
      const listPembayaran = this.listPembayaran.find(
        (val) => val.notaTagihan === this.activePembayaran.notaTagihan
      );

      /**
       * Find a specific faktur object in the list of pembayaran faktur based on the provided id.
       * @param {number} id_faktur - The id of the faktur to find.
       * @returns The faktur object if found, otherwise undefined.
       */
      const listFaktur = listPembayaran.faktur.find(
        (val) => val.id === id_faktur
      );

      /**
       * Update the status of a faktur to the given status value.
       * @param {string} status - The new status value to set for the faktur.
       * @returns None
       */
      listFaktur.status_faktur = status;
      activeFaktur.status_faktur = status;

      /**
       * Determines the status of a payment based on the status of its invoices.
       * If all invoices have a status of 12, the payment status is "Lunas" (Paid).
       * If at least one invoice has a status of 11, the payment status is "Pending".
       * Otherwise, the payment status is "Pending".
       * @param {Object} listPembayaran - The payment object containing invoices.
       * @returns None
       */
      if (listPembayaran.faktur.every((val) => val.status_faktur === 12)) {
        listPembayaran.status = "Lunas";
      } else if (
        listPembayaran.faktur.some((val) => val.status_faktur === 11)
      ) {
        listPembayaran.status = "Pending";
      } else {
        listPembayaran.status = "Pending";
      }

      // this.activePembayaran.totalBayar =
      //   this.activePembayaran.totalBayar - jumlah_setoran;

      this.tableKeyActive++;
      this.tableKey++;
    },
    checkPembayaran() {
      /**
       * Checks if there is any payment in the list that has a status of "Lunas".
       * @returns {boolean} True if there is at least one payment with status "Lunas", false otherwise.
       */
      return this.listPembayaran.some(
        (pembayaran) => pembayaran.status === "Lunas"
      );
    },
  },
});
