import ListTagihanPurchasing from "@/src/pages/tagihan-purchasing/ListTagihanPurchasing.vue";
import {detailTagihanPurchasing} from "./detail-tagihan-purchasing";
import {buatTagihanPurchasing} from "./buat-tagihan-purchasing";
import {bayarTagihanPurchasing} from "@/src/router/root/tagihan-purchasing/bayar-tagihan-purchasing";

const children = [
    ...detailTagihanPurchasing.concat(buatTagihanPurchasing, bayarTagihanPurchasing),
    {path: "", name: "Hutang", component: ListTagihanPurchasing},
];

export const listTagihanPurchasing = [
    {
        path: "/tagihan-purchasing", children
    },
];
