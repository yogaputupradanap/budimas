import { defineStore } from "pinia";
import { localDisk, status } from "../lib/utils";
import { transferService as service } from "../services/stockTransfer";

export const base = {
  list: [],
  loading: false,
  error: null,
  key: 0,
};

const sortByNewestItem = (itemA, itemB) => {
  const idDifference = itemB.id_stock_transfer - itemA.id_stock_transfer; 

  if (idDifference === 0) {
    return itemB.created_at.localeCompare(itemA.created_at); 
  }
  return idDifference;
}

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
      updateStockTransfer(id, data) {
        const filterStockTransfer = (val) => val.id_stock_transfer != id;

        const mainCopy = this.stockTransfer.list.filter(filterStockTransfer);
        mainCopy.push(data);

        const sortData = mainCopy.sort((a, b) =>
          b.created_at.localeCompare(a.created_at)
        );

        this.stockTransfer.list = sortData;
      },
      async getStockTransfer(status, columns, filtered_column) {
        const isArray = Array.isArray(status);
        try {
          this.stockTransfer.loading = true;
          const statusNum = isArray
            ? status.map((val) => this.status[val])
            : this.status[status];

          if (status) {
            this.stockTransfer.list = await service.baseGetStockTransfer(
              statusNum,
              columns,
              filtered_column
            );
            
            this.stockTransfer.list.sort(sortByNewestItem);
          } else {
            this.stockTransfer.list = await service.geAllStockTransfer(
              columns,
              filtered_column
            );
          }

          localDisk.setLocalStorage(storeId, this.stockTransfer.list);
        } catch (error) {
          this.stockTransfer.error = error;
          console.error(`error happen in ${storeId} store with -> ${error}`);
        } finally {
          this.stockTransfer.loading = false;
          this.stockTransfer.key++;
        }
      },
    },
  });
};

export const useStockTransfer = useBaseStore("stockTransfer");
export const useKonfirmasi = useBaseStore("konfirmasi");
export const usePengiriman = useBaseStore("pengiriman");
export const useStatusPengiriman = useBaseStore("status");
export const usePenerimaanBarang = useBaseStore("penerimaanbarang");
export const useListEskalasi = useBaseStore("listeskalasi");
