import ListSetoranNonTunai from "@/src/pages/setoran-non-tunai/ListSetoranNonTunai.vue";
import { listFaktur } from "./detail-setoran-non-tunai";

const children = [
  ...listFaktur,
  { path: "", name: "Setoran Non Tunai", component: ListSetoranNonTunai },
];

export const listSetoranNonTunai = [
  {
    path: "/setoran-non-tunai",
    children,
  },
];
