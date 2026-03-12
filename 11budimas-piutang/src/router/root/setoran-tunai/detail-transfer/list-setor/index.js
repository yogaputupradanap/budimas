import DetailSetoranTunai from "@/src/pages/setoran-tunai/detail-transfer/DetailSetoranTunai.vue";
import { buktiBayar } from "./bukti-bayar";


const children = [
  ...buktiBayar,
  { path: "", name: "Setoran Tunai  ", component: DetailSetoranTunai },
];

export const listSetoranTunaiDetail = [
  {
    path: "detail-setoran-tunai/:id_sales_order",
    children,
  },
];
