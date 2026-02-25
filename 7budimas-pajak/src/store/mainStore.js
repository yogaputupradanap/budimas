import { defineStore } from "pinia";
import { localDisk } from "../lib/utils";

export const base = {
  list: [],
  loading: false,
  error: null,
  key: 0,
};

// Creating a reusable base store
const useBaseStore = (storeId) => {
  return defineStore(storeId, {
    state: () => ({
      list: [],
      loading: false,
      error: null
    }),
    actions: {
      async getter() {
        try {

        } catch (error) {

        }
      }
    },
  });
};

// Export the store with correct name
export const useJurnal = useBaseStore("jurnal");
export const usePiutang = useBaseStore("piutang");
