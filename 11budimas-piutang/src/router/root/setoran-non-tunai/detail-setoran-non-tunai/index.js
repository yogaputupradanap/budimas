import { listSetoranNonTunaiDetail } from "./list-setor-non-tunai";
import ListFaktur from "@/src/pages/setoran-non-tunai/listFaktur.vue";

const children = [
  ...listSetoranNonTunaiDetail,
  { path: "", name: "Setoran Non Tunai ", component: ListFaktur },
];

export const listFaktur = [
  {
    path: "list-faktur",
    children,
  },
];
