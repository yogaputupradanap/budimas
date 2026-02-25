import DetailFakturPajak from "@/src/pages/draft-faktur-pajak/detaildraft-faktur-pajak/DetailFakturPajak.vue";
import DraftFakturPajak from "@/src/pages/draft-faktur-pajak/DraftFakturPajak.vue";

export const DraftDetailFakturPajakRoute = [
    {
        path: "/draft-faktur-pajak-detail/:id",
        name: "Draft Faktur Pajak Detail",
        component: DetailFakturPajak,
    },
];
