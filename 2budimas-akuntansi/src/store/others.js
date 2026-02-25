import {defineStore} from "pinia";
import {base} from "./mainStore";
import {localDisk} from "../lib/utils";
import {salesService} from "../services/sales";
import {customerService} from "../services/customer";
import {principalService} from "../services/principal";
import {perusahaanService} from "../services/perusahaan";
import {cabangService} from "../services/cabang";
import {useUser} from "@/src/store/user";
import {jurnalService} from "@/src/services/jurnal";

const localSales = localDisk.getLocalStorage("sales") || [];
const localCustomer = localDisk.getLocalStorage("customer") || [];
const localPrincipal = localDisk.getLocalStorage("principal") || [];

export const useOthers = defineStore("others", {
    state: () => ({
        sales: {...base, list: localSales},
        customer: {
            ...base,
            list: localCustomer,
            fullData: [],
            totalItems: 0,
            displayData: [],
            currentPage: 1,
            itemsPerPage: 100,
            searchResults: [],
            isSearching: false,
            fullDataLoaded: false,
            initialLoadComplete: false,
        },
        principal: {...base, list: localPrincipal},
        jurnal: {...base, list: []},
        perusahaan: {...base, list: []},
        cabang: {...base, list: []},
    }),
    getters: {
        customerOptions: (state) =>
            state.customer.isSearching
                ? state.customer.searchResults : state.customer.displayData.length
                    ? state.customer.displayData : state.customer.list,

        customerTotalPages: (state) => Math.ceil(
            state.customer.totalItems / state.customer.itemsPerPage
        ),
    },
    actions: {
        async getOthers() {
            const loadingStates = ['sales', 'customer', 'principal', 'jurnal', 'cabang', 'perusahaan'];

            try {
                this.setLoadingStates(loadingStates, true);
                const userStore = useUser();
                const initialCustomerLoad = this.loadInitialCustomers();

                // 1. Ambil raw responses dari Promise.all
                const [rawSales, rawCustomer, rawPrincipal, rawJurnal, rawCabang, rawPerusahaan] =
                    await Promise.all([
                        salesService.getAllSales(userStore.user.value.id_cabang),
                        initialCustomerLoad,
                        principalService.getAllprincipal(),
                        jurnalService.getJurnal(),
                        cabangService.getAllCabang(),
                        perusahaanService.getAllPerusahaan(),
                    ]);

                // 2. Ekstrak .result dengan fallback array kosong [] agar tidak crash
                const sales = rawSales?.result || [];
                const customer = rawCustomer?.result || [];
                const principal = rawPrincipal?.result || [];
                const jurnal = rawJurnal?.result || [];
                const cabang = rawCabang?.result || [];
                const perusahaan = rawPerusahaan?.result || [];

                // 3. Simpan ke LocalStorage
                localDisk.setLocalStorage("sales", sales);
                localDisk.setLocalStorage("customer", customer);
                localDisk.setLocalStorage("principal", principal);

                // 4. Update State
                this.sales.list = sales;
                this.customer.list = customer;
                
                // Sekarang .slice() aman karena 'customer' pasti sebuah Array
                this.customer.displayData = Array.isArray(customer) ? customer.slice(0, 100) : [];
                
                this.principal.list = principal;
                this.jurnal.list = jurnal;
                this.cabang.list = cabang;
                this.perusahaan.list = perusahaan;

                this.loadAllCustomersBackground();
            } catch (error) {
                console.error("error happen in others store: ", error);
            } finally {
                this.setLoadingStates(loadingStates, false);
            }
        },

        setLoadingStates(states, loading) {
            states.forEach(state => {
                if (this[state]) this[state].loading = loading;
            });
        },

        async loadInitialCustomers() {
            try {
                const customers = await customerService.getAllCustomer();
                this.customer.initialLoadComplete = true;
                return customers || [];
            } catch (error) {
                console.error("Error loading initial customers:", error);
                throw error;
            }
        },

        async loadAllCustomersBackground() {
            try {
                const allCustomers = await customerService.getAllCustomersFull();

                if (allCustomers && allCustomers.length > 0) {
                    this.customer.fullData = allCustomers;
                    this.customer.totalItems = allCustomers.length;
                    this.customer.fullDataLoaded = true;
                    this.customer.displayData = allCustomers.slice(0, this.customer.itemsPerPage);
                    localDisk.setLocalStorage("customer_full", allCustomers);
                }
            } catch (error) {
                console.error("Error loading full customer data:", error);
            }
        },

        setCustomerPage(page) {
            if (!this.customer.fullDataLoaded) {
                console.warn("Full data not loaded yet, using limited data");
                return;
            }

            const start = (page - 1) * this.customer.itemsPerPage;
            const end = start + this.customer.itemsPerPage;

            this.customer.displayData = this.customer.fullData.slice(start, end);
            this.customer.currentPage = page;
        },

        async searchCustomer(query) {
            if (!query || query.length < 2) {
                this.customer.searchResults = [];
                this.customer.isSearching = false;

                if (this.customer.fullDataLoaded) {
                    this.setCustomerPage(1);
                } else {
                    this.customer.displayData = this.customer.list.slice(0, 100);
                }
                return this.customerOptions;
            }

            try {
                this.customer.isSearching = true;

                let searchResults = [];

                if (this.customer.fullDataLoaded) {
                    searchResults = this.searchCustomersLocal(query);
                } else {
                    searchResults = await customerService.searchCustomerServer(query, 200);
                }
                this.customer.searchResults = searchResults;
                return this.customer.searchResults;
            } catch (error) {
                console.error("Error in search:", error);
                return this.searchCustomersLocal(query);
            }
        },

        searchCustomersLocal(query) {
            const searchTerm = query.toLowerCase();
            const dataToSearch = this.customer.fullDataLoaded
                ? this.customer.fullData
                : this.customer.list;

            return dataToSearch.filter(customer =>
                customer.nama?.toLowerCase().includes(searchTerm) ||
                customer.kode?.toLowerCase().includes(searchTerm) ||
                customer.id?.toString().includes(searchTerm)
            );
        },

        async getCustomerById(id) {
            const searchSources = [
                () => this.customer.fullDataLoaded ? this.customer.fullData.find(cust => cust.id === id) : null,
                () => this.customer.list.find(cust => cust.id === id),
                () => this.customer.searchResults.find(cust => cust.id === id)
            ];

            for (const source of searchSources) {
                const customer = source();
                if (customer) return customer;
            }

            if (!this.customer.fullDataLoaded) {
                try {
                    const searchResult = await customerService.searchCustomerServer(id.toString(), 10);
                    const foundCustomer = searchResult?.find(c => c.id === id);
                    if (foundCustomer) {
                        this.customer.list.push(foundCustomer);
                        return foundCustomer;
                    }
                } catch (error) {
                    console.error("Error fetching customer by ID:", error);
                }
            }

            return null;
        },

        resetCustomerSearch() {
            this.customer.searchResults = [];
            this.customer.isSearching = false;

            if (this.customer.fullDataLoaded) {
                this.setCustomerPage(1);
            } else {
                this.customer.displayData = this.customer.list.slice(0, 100);
            }
        }
    },
});
