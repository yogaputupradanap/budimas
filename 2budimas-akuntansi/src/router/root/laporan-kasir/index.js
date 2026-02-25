import ListLaporanKasir from "@/src/pages/laporan-kasir/ListLaporanKasir.vue";
import { detailLaporanKasir } from "./detail";

const children = [
  ...detailLaporanKasir,
  { path: "", name: "Laporan Kasir", component: ListLaporanKasir },
];

export const listLaporanKasir = [
  {
    path: "/laporan-kasir",
    children,
  },
];
