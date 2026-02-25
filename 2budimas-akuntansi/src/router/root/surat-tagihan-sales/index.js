import ListTagihanSales from "@/src/pages/surat-tagihan-sales/ListTagihanSales.vue";
import { detailSuratTagihanSales } from "./detail-surat-tagihan-sales";
import { buatSuratTagihanSales } from "./buat-surat-tagihan-sales";

const children = [
  ...detailSuratTagihanSales.concat(buatSuratTagihanSales),
  { path: "", name: "Piutang", component: ListTagihanSales },
];

export const listTagihanSales = [
  {
    path: "/surat-tagihan-sales", children
  },
];


