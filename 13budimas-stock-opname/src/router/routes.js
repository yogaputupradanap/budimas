import { root } from "./root";
import { Loginn } from "./root/login";
import { dashboard } from "./root/dashboard";
import { stockOpname } from "./root/stock-opname";
import { laporanStock } from "./root/laporan-stock";
import { listEskalasi } from "@/src/router/root/list-eskalasi";

export const routes = root.concat(
  dashboard,
  Loginn,
  stockOpname,
  laporanStock,
  listEskalasi
);
