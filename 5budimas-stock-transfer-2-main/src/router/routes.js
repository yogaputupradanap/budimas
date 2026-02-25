import { root } from "./root";
import { Loginn } from "./root/login";
import { dashboard } from "./root/dashboard";
import { listEskalasi } from "./root/list-eskalasi";
import { detailListEskalasi } from "./root/list-eskalasi/detail";
import { listPenerimaanBarang } from "./root/penerimaan-barang";
import { detailPenerimaanBarang } from "./root/penerimaan-barang/detail";
import { listPengajuanTransfer } from "./root/konfirmasi";
import { detailPengajuanTransfer } from "./root/konfirmasi/detail";
import { listPengirimanStockTransfer } from "./root/pengiriman";
import { detailPengirimanStockTransfer } from "./root/pengiriman/detail";
import { listStatusPengiriman } from "./root/status-pengiriman";
import { detailStatusPengiriman } from "./root/status-pengiriman/detail";
import { listStockTransfer } from "./root/stock-transfer";
import { addStockTransfer } from "./root/stock-transfer/add";

export const routes = root.concat(
  dashboard,
  Loginn,
  listEskalasi,
  detailListEskalasi,
  listPenerimaanBarang,
  detailPenerimaanBarang,
  listPengajuanTransfer,
  detailPengajuanTransfer,
  listPengirimanStockTransfer,
  detailPengirimanStockTransfer,
  listStatusPengiriman,
  detailStatusPengiriman,
  listStockTransfer,
  addStockTransfer
);
