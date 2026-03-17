import listLogPenggunaanPromo from "@/src/pages/log-penggunaan-promo";

const children = [
  {
    path: "", name: "Log Penggunaan Promo", component: listLogPenggunaanPromo
  }
]

export const listLogPenggunaanPromoRoute = [
  {
    path: "/log-penggunaan-promo", children
  },
];