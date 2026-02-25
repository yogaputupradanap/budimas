export const listFakturRoutes = [
  {
    path: "/revisi-faktur/faktur/:id_rute",
    name: "List Revisi Faktur",
    component: () => import("@/src/pages/revisi-faktur/ListFaktur.vue"),
  },
];
