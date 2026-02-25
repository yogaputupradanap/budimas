import { createRouter, createWebHistory, useRouter } from "vue-router";
import { routes } from "./routes";
import { sessionDisk } from "../lib/utils";
import { useUser } from "../store/user";

const router = createRouter({
  scrollBehavior() {
    return { top: 0, behavior: 'instant'  };
  },
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach(async (to, from, next) => {
  const isAuthenticated = sessionDisk.getSession("authUser");

  // Jika pengguna belum login, arahkan ke login
  if (to.name !== "Login" && !isAuthenticated) {
    next({ name: "Login" });
  }
  // Jika pengguna login dan mencoba mengakses login, arahkan ke dashboard
  else if (to.name === "Login" && isAuthenticated) {
    next({ name: "Dashboard" });
  }
  // Selain itu, izinkan akses ke halaman yang diminta
  else {
    next();
  }
});

export default router;
