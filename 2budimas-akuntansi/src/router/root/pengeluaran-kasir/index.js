import ListPengeluaranKasir from "@/src/pages/pengeluaran-kasir/ListPengeluaranKasir.vue";

const children = [
  { path: "", name: "Pengeluaran Kasir", component: ListPengeluaranKasir },
];

export const listPengeluaranKasir = [
  {
    path: "/pengeluaran-kasir",
    children,
  },
];
