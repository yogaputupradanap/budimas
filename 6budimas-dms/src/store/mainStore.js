import { defineStore } from "pinia";
import { localDisk, status } from "../lib/utils";


export const base = {
  list: [],
  loading: false,
  error: null,
  key: 0,
};

const useBaseStore = (storeId) => {
  return defineStore(storeId, {
    state: () => ({
      status,
      stockTransfer: {
        ...base,
        list: localDisk.getLocalStorage(storeId) || [],
      },
    }),
    actions: {

    },
  });
};

export const useStockTransfer = useBaseStore("stockTransfer");
export const useKonfirmasi = useBaseStore("konfirmasi");
export const usePengiriman = useBaseStore("pengiriman");
export const useStatusPengiriman = useBaseStore("status");
export const usePenerimaanBarang = useBaseStore("penerimaanbarang");
export const useListEskalasi = useBaseStore("listeskalasi");
