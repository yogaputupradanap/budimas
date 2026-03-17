import listKlaimPromo from "@/src/pages/klaim-promo";
import { detailRoute } from "./detail";
import { listKlaimDitolakRoute } from "./list-klaim-ditolak";

export const listKlaimPromoRoute = [
  {
    path: "/klaim-promo",
    children: [
      detailRoute,
      listKlaimDitolakRoute,
      {
        path: "",
        name: "List Klaim Promo",
        component: listKlaimPromo
      }
    ]
  }
];