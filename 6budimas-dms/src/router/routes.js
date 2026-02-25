import { root } from "./root";
import { Loginn } from "./root/login";
import { dashboard } from "./root/dashboard";
import { dms } from "./root/dms";


export const routes = root.concat(
  dashboard,
  Loginn,
  dms
);
