import ListSetoranNonTunai from "@/src/pages/setoran-non-tunai/ListSetoranNonTunai.vue";
import {listFaktur} from "./detail-setoran-non-tunai";
import DetailSetoranNonTunaiSales
  from "@/src/pages/setoran-non-tunai/detail-setoran-non-tunai/DetailSetoranNonTunaiSales.vue";
import DetailSetoranNonTunaiCustomer
  from "@/src/pages/setoran-non-tunai/detail-setoran-non-tunai/DetailSetoranNonTunaiCustomer.vue";

const children = [
    ...listFaktur,
    {path: "", name: "Setoran Non Tunai", component: ListSetoranNonTunai},
];

export const listSetoranNonTunai = [
    {
        path: "/setoran-non-tunai",
        children,
    },
    {
        path: "/setoran-non-tunai/customer/:id_mutasi",
        name: "Setoran Non Tunai ",
        component: DetailSetoranNonTunaiCustomer,
    },
    {
        path: "/setoran-non-tunai/sales/:id_mutasi",
        name: "Setoran Non Tunai  ",
        component: DetailSetoranNonTunaiSales,
    }
];
