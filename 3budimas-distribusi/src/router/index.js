import { createRouter, createWebHistory } from "vue-router";
import { routes } from "./routes";
import { sessionDisk } from "../lib/utils";

const router = createRouter({
  // scrollBehavior(__to, __from, __savedPosition) {
  //   return { top: 0 };
  // },
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach(async (to, from, next) => {
  const isAuthenticated = sessionDisk.getSession("authUser_distribusi");

  if (to.name !== "Login" && !isAuthenticated) {
    next({ name: "Login" });
  } else if (to.name === "Login" && isAuthenticated) {
    next({ name: "Dashboard" });
  } else {
    next();
  }
});

export default router;
