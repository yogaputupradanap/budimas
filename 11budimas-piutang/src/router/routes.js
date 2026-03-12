import { root } from "./root";
import { Loginn } from "./root/login";
import { dashboard } from "./root/dashboard";
import { listJurnal } from "./root/jurnal";
import { listTagihanSales } from "./root/surat-tagihan-sales";
import { listSetoranTunai } from "./root/setoran-tunai";
import { listSetoranNonTunai } from "./root/setoran-non-tunai";
import { listTagihanPurchasing } from "./root/tagihan-purchasing";

export const routes = root.concat(
  dashboard,
  Loginn,
  listJurnal,
  listTagihanSales,
  listSetoranTunai,
  listSetoranNonTunai,
  listTagihanPurchasing
);
