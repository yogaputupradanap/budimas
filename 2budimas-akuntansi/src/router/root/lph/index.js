import Lph from "@/src/pages/lph/Lph.vue";
import { addLph } from "./add-lph";
import { addLphCustomer } from './add-lph-by-customer';
import { detailLph } from "./detail";

const children = [
  ...addLph.concat(addLphCustomer).concat(detailLph),
  {
    path: "",
    name: "LPH",
    component: Lph,
  },
];

export const lph = [
  {
    path: "/lph",
    children,
  },
];
