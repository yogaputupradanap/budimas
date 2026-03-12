import ListSetoranTunai from "@/src/pages/setoran-tunai/ListSetoranTunai.vue";
import { listFaktur } from "./detail-transfer";

const children = [
    ...listFaktur,
    { path: "", name: "Setoran Tunai", component: ListSetoranTunai },
];

export const listSetoranTunai = [
  {
    path: "/setoran-tunai",
    children,
  },
];
