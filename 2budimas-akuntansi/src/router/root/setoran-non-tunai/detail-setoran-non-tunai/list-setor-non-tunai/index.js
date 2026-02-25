import DetailSetoranNonTunaiSales
  from "@/src/pages/setoran-non-tunai/detail-setoran-non-tunai/DetailSetoranNonTunaiSales.vue";
import {buktiBayar} from "./bukti-bayar";


const children = [
    ...buktiBayar,
    {path: "", name: "Setoran Non Tunai  ", component: DetailSetoranNonTunaiSales},
];

export const listSetoranNonTunaiDetail = [
    {
        path: "detail-setoran-non-tunai/:id_sales_order",
        children,
    },
];
