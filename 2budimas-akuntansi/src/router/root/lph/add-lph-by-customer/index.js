import AddLphByCustomer from "@/src/pages/lph/add-lph/AddLphByCustomer.vue";

const children = [{ path: "", name: "LPH By Customer", component: AddLphByCustomer }];

export const addLphCustomer = [
  {
    path: "add-lph-customer",
    children,
  },
];
