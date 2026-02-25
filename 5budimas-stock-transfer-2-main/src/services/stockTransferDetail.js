import { fetchWithAuth, status } from "../lib/utils";

class stockTransferDetail {
  #baseGetURL
  #detailStockTransferURL
  #status

  constructor() {
    this.#baseGetURL = "/api/base/stock_transfer_detail";
    this.#detailStockTransferURL = "/api/stock-transfer/detail-stock-transfer";
    this.#status = status;
  }

  async getDetailStockTransfer(id, status = null, col = 'jumlah') {
    try {
      const numStatus = status ? `&status=${this.#status[status]}` : '';
      const colName = `&select_jumlah=${col}`
      const url = `${this.#detailStockTransferURL}?id=${id}${numStatus}${colName}`;
      const data = await fetchWithAuth("GET", url);
      return Promise.resolve(data);
    } catch (error) {
      const errorMessage = `error while requesting stock transfer detail with detail : ${error}`;
      console.log(errorMessage);
      return Promise.reject(errorMessage);
    }
  }
}

const stockTransferDetailService = new stockTransferDetail();
export { stockTransferDetailService };
