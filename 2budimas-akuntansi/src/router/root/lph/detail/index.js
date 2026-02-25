import DetailLph from "@/src/pages/lph/detail-lph/DetailLph.vue";

const children = [{ path: "", name: "LPH  ", component: DetailLph }];

export const detailLph = [
  {
    path: "detail-lph/:id_lph",
    children,
  },
];
