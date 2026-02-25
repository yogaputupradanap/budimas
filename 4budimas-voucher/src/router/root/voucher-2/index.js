import Voucher2 from "@/src/pages/voucher/Voucher2.vue";
import { addVoucher } from "./add";
import { editVoucher2 } from "./edit";

export const listVoucher2 = [
  {
    path: "/voucher-2",
    children: [
      {
        path: "",
        name: "Voucher 2",
        component: Voucher2,
      },
      ...addVoucher,
      ...editVoucher2
    ],
  },
];
