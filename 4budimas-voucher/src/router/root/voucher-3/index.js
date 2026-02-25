import Voucher3 from "@/src/pages/voucher/Voucher3.vue";
import { addVoucher } from "./add";
import { editVoucher3 } from "./edit";

export const listVoucher3 = [
  {
    path: "/voucher-3",
    children: [
      {
        path: "",
        name: "Voucher 3",
        component: Voucher3,
      },
      ...addVoucher,
      ...editVoucher3
    ],
  },
];
