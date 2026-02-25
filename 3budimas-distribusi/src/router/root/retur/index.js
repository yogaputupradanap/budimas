import Retur from "@/src/pages/Retur.vue";
import ListPengajuan from "@/src/pages/ListPengajuan.vue";
import DetailRetur from "@/src/pages/DetailRetur.vue";
import InsertRetur from "@/src/pages/InsertRetur.vue";

export const ReturRoutes = [
    {
        path: "/retur",
        name: "Retur",
        component: Retur,
    },
    {
        path: "/retur/list-pengajuan",
        name: "Retur ",
        component: ListPengajuan,
    },
    {
        path: "/retur/list-pengajuan/:id_request",
        name: "Retur  ",
        component: DetailRetur,
    },
    {
        path: "/retur/insert-retur/:id_request",
        name: "Retur   ",
        component: InsertRetur,
    }
];
