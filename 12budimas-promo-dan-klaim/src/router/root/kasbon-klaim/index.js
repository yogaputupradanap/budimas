import listKasbonKlaim from "@/src/pages/kasbon-klaim";
import { detailKasbonRoute } from "./detail";

export const listKasbonKlaimRoute = [
  {
    path: "/kasbon-klaim",
    children: [
      detailKasbonRoute,
      {
        path: "",
        name: "Kasbon Klaim",
        component: listKasbonKlaim
      }
    ]
  }
];