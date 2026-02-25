import { root } from "./root";
import { Loginn } from "./root/login";
import { dashboard } from "./root/dashboard";
import { listVoucher } from "./root/voucher";
import { listVoucher2 } from "./root/voucher-2";
import { listVoucher3 } from "./root/voucher-3";

export const routes = root.concat(
  dashboard,
  Loginn,
  listVoucher,
  listVoucher2,
  listVoucher3
);
