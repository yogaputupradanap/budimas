import ListSetoranTunai from "@/src/pages/setoran-tunai/ListSetoranTunai.vue";
import {listFaktur} from "./detail-transfer";
import DetailSetoranTunai from "@/src/pages/setoran-tunai/DetailSetoranTunai.vue";

const children = [
    ...listFaktur,
    {path: "", name: "Setoran Tunai", component: ListSetoranTunai},
    {
        path: ':nama_pj/:draft_tanggal_input',
        name: "Setoran Tunai      ",
        component: DetailSetoranTunai,
    }
];

export const listSetoranTunai = [
    {
        path: "/setoran-tunai",
        children,
    },
];
