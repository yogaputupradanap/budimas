import { defineStore } from "pinia";
import { apiUrl, dateNow, fetchWithAuth, localDisk } from "../lib/utils";
import { usePrincipal } from "./principal";
import { format } from "date-fns";

export const useDashboard = defineStore("dashboard", {
  /**
   * @todo delete dashboardinfo initial data
   * now each time user visit dashboard user will
   * always run getDashboardInfo() function
   * @returns
   */
  state: () => ({
    dashboardInfo: {
      updateTerakhir: "",
      totalCustomerOrder: 0,
      totalOrder: 0,
      sudahBerkunjung: 0,
      belumKunjungan: 0,
      totalTransaksi: 0,
    },
    activeButtons: {},
    dashboardInfoMonth: {
      dashboardInfo: {
        updateTerakhir: "",
        totalCustomerOrder: 0,
        totalOrder: 0,
        sudahBerkunjung: 0,
        belumKunjungan: 0,
        totalTransaksi: 0,
      },
      year: null,
      month: null,
      seriesData: [],
      optionsdata: [],
      loading: false,
      error: null,
    },
    chart: {
      currentChart: {
        order: [],
        realisasi: [],
        retur: [],
      },
      loading: true,
      error: null,
    },
    loading: true,
    error: null,
  }),
  getters: {
    getIdPlafon(state) {
      const principal = usePrincipal();
      const id_plafon = JSON.stringify(principal.idPlafons);

      return id_plafon;
    },
    opnameName(state) {
      const opname = `${this.getIdPlafon}_${dateNow()}_opname_btn`;
      return opname;
    },
    sRequestName(state) {
      const requestName = `${this.getIdPlafon}_${dateNow()}_srequest_btn`;
      return requestName;
    },
    pembayaranName(state) {
      const pembayaran = `${this.getIdPlafon}_${dateNow()}_pembayaran_btn`;
      return pembayaran;
    },
  },
  actions: {
    initActiveButton() {
      this.activeButtons = localDisk.getLocalStorage("active-buttons") || {};
    },
    // digunakan untuk setiap setelah user mengunjungi page
    setActiveButton(btnName, value = true, permanent = false) {
      const activeButtonLocalStorage =
        localDisk.getLocalStorage("active-buttons") || {};
      const btnNameWithSuffix =
        btnName === "stock opname"
          ? this.opnameName
          : btnName === "sales request"
          ? this.sRequestName
          : btnName === "pembayaran"
          ? this.pembayaranName
          : null;

      const activeButton = {
        ...activeButtonLocalStorage,
        [btnNameWithSuffix]: value,
      };
      localDisk.setLocalStorage("active-buttons", activeButton);
      this.activeButtons = activeButton;
    },
    // di gunakan untuk mendapatkan active button di array of object dashboard
    getActiveButton(btnName) {
      const btnNameWithPrefix =
        btnName === "stock opname"
          ? this.opnameName
          : btnName === "sales request"
          ? this.sRequestName
          : btnName === "pembayaran"
          ? this.pembayaranName
          : null;
      return this.activeButtons[btnNameWithPrefix] || false;
    },
    /**
     * Asynchronously fetches dashboard information for a given user ID and updates the component state accordingly.
     * @param {number} id_user - The ID of the user for whom the dashboard information is being fetched.
     * @returns None
     */
    async getDashboardInfo(id_user) {
      this.loading = true;
      try {
        const dashboard = await fetchWithAuth(
          "GET",
          `${apiUrl}/api/sales/get-user-info/${id_user}`
        );
        this.dashboardInfo = dashboard;
        localDisk.setLocalStorage("dashboard", this.dashboardInfo);
      } catch (err) {
        this.error = err;
      }
    },
    /**
     * Retrieves dashboard information for a specific month based on the provided user ID, year, and month.
     * @param {number} id_user - The ID of the user for whom the dashboard information is being fetched.
     * @param {number} tahun - The year for which the dashboard information is being fetched.
     * @param {number} bulan - The month for which the dashboard information is being fetched.
     * @param {object} options - Additional options for the dashboard.
     * @param {object} series - Data series for the dashboard.
     * @returns None
     * @throws {Error} If there is an error during the fetch operation.
     */
    async getDashboardInfoMonth(id_user, tahun, bulan, options, series) {
      this.dashboardInfoMonth.loading = true;
      try {
        const dashboard = await fetchWithAuth(
          "GET",
          `${apiUrl}/api/sales/get-user-info-month?user_id=${id_user}&tahun=${tahun}&bulan=${bulan}`
        );
        this.dashboardInfoMonth.dashboardInfo = dashboard;
        this.dashboardInfoMonth.optionsdata = options;
        this.dashboardInfoMonth.seriesData = series;
        this.dashboardInfoMonth.year = tahun;
        this.dashboardInfoMonth.month = bulan;
      } catch (err) {
        this.dashboardInfoMonth.error = err;
      } finally {
        this.dashboardInfoMonth.loading = false;
      }
    },
    /**
     * Retrieves chart data for a specific user, year, and month.
     * @param {string} userId - The ID of the user for whom the chart data is being fetched.
     * @param {number} yearUsr - The year for which the chart data is being fetched.
     * @param {number} monthUsr - The month for which the chart data is being fetched.
     * @param {boolean} removeDate - Flag to indicate whether to remove the date from the data.
     * @returns {Promise<Object>} An object containing order, realisasi, and retur data sorted by date.
     * @throws {Error} If there is an error fetching the data.
     */
    async getChart(userId, yearUsr, monthUsr, removeDate) {
      const currentDate = new Date();
      const year = currentDate.getFullYear();
      const month = currentDate.getMonth() + 1;
      const day = currentDate.getDate();

      try {
        const url = new URL("/api/sales/get-omset", apiUrl);

        url.searchParams.set("user_id", userId);
        url.searchParams.set("bulan", monthUsr || month);
        url.searchParams.set("tahun", yearUsr || year);

        if (!removeDate) {
          url.searchParams.set("tanggal", day);
        }

        const order = await fetchWithAuth("GET", url.toString());

        url.searchParams.set("status_faktur", 5);
        const realisasi = await fetchWithAuth("GET", url.toString());

        url.searchParams.set("status_faktur", 0);
        url.searchParams.set("jenis_faktur", "retur");
        const retur = await fetchWithAuth("GET", url.toString());

        return {
          order: order?.sort((a, b) => a?.tanggal?.localeCompare(b?.tanggal)),
          realisasi: realisasi?.sort((a, b) =>
            a?.tanggal?.localeCompare(b?.tanggal)
          ),
          retur: retur?.sort((a, b) => a?.tanggal?.localeCompare(b?.tanggal)),
        };
      } catch (error) {
        console.log(error);
      }
    },
    /**
     * Asynchronously fetches the current chart data for a specific user.
     * @param {string} userId - The ID of the user for whom the chart data is being fetched.
     * @returns None
     */
    async getCurrentChart(userId) {
      this.chart.loading = true;
      const current = await this.getChart(userId);

      this.chart.currentChart.order = current?.order;
      this.chart.currentChart.realisasi = current?.realisasi;
      this.chart.currentChart.retur = current?.retur;

      this.chart.loading = false;
    },
    deactivateLoading() {
      this.loading = false;
    },
  },
});
