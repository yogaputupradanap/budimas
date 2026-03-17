import { root } from "./root";
import { Loginn } from "./root/login";
import { dashboard } from "./root/dashboard";
import { listMasterPromoRoute } from "./root/master-promo";
import { listLogPenggunaanPromoRoute } from "./root/log-penggunaan-promo";
import { listKlaimPromoRoute } from "./root/klaim-promo";
import { listKasbonKlaimRoute } from './root/kasbon-klaim';

export const routes = root.concat(
  dashboard,
  Loginn,
  listMasterPromoRoute,
  listLogPenggunaanPromoRoute,
  listKlaimPromoRoute,
  listKasbonKlaimRoute
);
