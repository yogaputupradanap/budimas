import { root } from "./root";
import { Loginn } from "./root/login";
import { dashboard } from "./root/dashboard";
import { canvasRequestRoute } from "./root/canvas-request";
import { canvasOrderRoute } from './root/canvas-order';
import { rekapPembayaranRoute } from './root/rekap-pembayaran';

export const routes = root.concat(
  dashboard,
  Loginn,
  canvasRequestRoute,
  canvasOrderRoute,
  rekapPembayaranRoute,
);
