import DetailLaporanKasir from "@/src/pages/laporan-kasir/detail/DetailLaporanKasir.vue";

const children = [
  { path: "", name: "Laporan Kasir ", component: DetailLaporanKasir },
];

export const detailLaporanKasir = [
  {
    path: "detail",
    children,
  },
];
