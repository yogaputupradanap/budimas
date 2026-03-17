import ListEskalasi from "@/src/pages/list-eskalasi/ListEskalasi.vue";
import DetailEskalasi from "@/src/pages/list-eskalasi/DetailEskalasi.vue";

export const listEskalasi = [
    {
        path: "/list-eskalasi",
        name: "List Eskalasi",
        component: ListEskalasi,
    },
    {
        path: "/list-eskalasi/detail-eskalasi-stock/:id",
        name: "Detail Eskalasi",
        component: DetailEskalasi
    },
]