import { createRouter, createWebHistory, useRouter } from "vue-router";
import { routes } from "./routes";
import { sessionDisk } from "../lib/utils";
import { useUser } from "../store/user";

const router = createRouter({
  scrollBehavior() {
    return { top: 0, behavior: 'instant' };
  },
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach(async (to, from, next) => {
  const userStore = useUser();
  const isAuthenticated = sessionDisk.getSession("authUser");
  const routeList = [...userStore.userAccess].concat([{ name: "Dashboard" }]);

  const checkGrantedAccess = routeList.some((val) => {
    const regexp = new RegExp(`${val.name}`, "i");
    return regexp.test(to.path);
  });

  if (to.name !== "Login" && !isAuthenticated) {
    next({ name: "Login" });
  } else if (to.name === "Login" && isAuthenticated) {
    next({ name: "Dashboard" });
  } else if (to.name !== "Login" && isAuthenticated && !checkGrantedAccess) {
    next({ name: "Dashboard" });
  } else {
    next();
  }
});

export default router;
