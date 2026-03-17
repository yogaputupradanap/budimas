import listKlaimDitolak from "@/src/pages/klaim-promo/list-klaim-ditolak"
import { ajukanUlangRoute } from "./ajukan-ulang"

export const listKlaimDitolakRoute = {
    path: "list-klaim-ditolak",
    children: [
        ajukanUlangRoute,
        {
            path: "",
            name: "List Klaim Ditolak",
            component: listKlaimDitolak
        }
    ],
}