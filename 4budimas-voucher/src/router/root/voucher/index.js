import Voucher from "@/src/pages/voucher/Voucher.vue";
import { addVoucher } from "./add";
import { editVoucher } from "./edit";

export const listVoucher = [
  {
    path: "/voucher-1",
    children: [
      {
        path: "",
        name: "Voucher 1",
        component: Voucher,
      },
      ...addVoucher,
      ...editVoucher
    ],
  },
];
