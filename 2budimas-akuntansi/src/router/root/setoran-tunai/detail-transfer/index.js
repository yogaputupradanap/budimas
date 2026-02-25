import ListFaktur from "@/src/pages/setoran-tunai/detail-transfer/listFaktur.vue";
import { listSetoranTunaiDetail } from "./list-setor";

const children = [
  ...listSetoranTunaiDetail,
  { path: "", name: "Setoran Tunai ", component: ListFaktur },
];

export const listFaktur = [
  {
    path: "list-faktur",
    children,
  },
];
