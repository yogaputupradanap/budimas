import listMasterPromo from "@/src/pages/master-promo";
import { ajukanKlaim } from "./ajukan-klaim";

const children = [
  ...ajukanKlaim,
  {
    path: "", name: "Master Promo", component: listMasterPromo
  }
]

export const listMasterPromoRoute = [
  {
    path: "/master-promo", children
  },
];