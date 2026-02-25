export const DetailRevisiFakturRoutes = [
  {
    path: "/revisi-faktur/faktur/:id_rute/detail/:id_sales_order",
    name: "Detail Revisi Faktur",
    component: () => import("@/src/pages/revisi-faktur/DetailRevisiFaktur.vue"),
  },
];
