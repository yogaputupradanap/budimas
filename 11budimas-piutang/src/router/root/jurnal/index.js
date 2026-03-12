import ListJurnal from "@/src/pages/jurnal/ListJurnal.vue";
import { detailJurnal } from "./detail-jurnal"


const children = [
  ...detailJurnal,
  { path: "", name: "jurnal", component: ListJurnal },
];

export const listJurnal = [
  {
    path: "/jurnal",
    children,
  },
];



