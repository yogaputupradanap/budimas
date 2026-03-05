<script setup>
import { watch, ref } from "vue";
import { useRoute } from "vue-router";
import { isMobileMinimize } from "../../lib/useSideBar";
import LogoBudimas from "../../assets/images/logo-budimas-white.png";
import LogoBudimasText from "../../assets/images/logo-text-budimas.png";
import anime from "animejs";
import { logout } from "@/src/lib/utils";

const route = useRoute();
const mobileSidebar = ref(null);

// Konstanta untuk styling
const BUTTON_STYLES = {
  inactive: "tw-bg-blue-100 hover:tw-bg-white hover:tw-text-black",
  active: "tw-bg-[#1be1af] tw-text-white hover:tw-text-white",
};

const ANIMATION_CONFIG = {
  duration: 500,
  easing: "easeOutExpo",
};

// Konfigurasi menu navigasi mobile
const mobileNavigationMenus = [
  {
    name: "Dashboard",
    icon: "mdi-view-dashboard",
    route: "/dashboard/summary-report",
    isActive: () => route.name === "Dashboard",
  },
  {
    name: "Kunjungan",
    icon: "mdi-account-check",
    route: "/kunjungan/daftar-kunjungan-toko",
    isActive: () => /kunjungan/gi.test(route.path),
  },
  {
    name: "History",
    icon: "mdi-history",
    route: "/dashboard/history",
    isActive: () => route.name === "history",
  },
  {
    name: "Rekap Pembayaran",
    icon: "mdi-cash-multiple",
    route: "/dashboard/rekap-pembayaran",
    isActive: () => route.name === "rekap pembayaran",
  },
];

// Watch untuk animasi mobile sidebar
watch(isMobileMinimize, () => {
  anime({
    targets: mobileSidebar.value,
    duration: ANIMATION_CONFIG.duration,
    translateX: isMobileMinimize.value ? -300 : 300,
    easing: ANIMATION_CONFIG.easing,
  });
});

// Fungsi untuk mendapatkan class button berdasarkan status active
const getButtonClass = (isActive) => {
  const baseClass = `tw-w-full tw-h-12 tw-flex tw-justify-start tw-pl-6 tw-items-center 
                    tw-rounded-md tw-cursor-pointer tw-duration-200 tw-ease-in-out`;
  const statusClass = isActive ? BUTTON_STYLES.active : BUTTON_STYLES.inactive;
  return `${baseClass} ${statusClass}`;
};
</script>

<template>
  <aside
    ref="mobileSidebar"
    class="tw-w-72 tw-h-screen tw-bg-[#01579b] tw-fixed lg:tw-hidden tw-top-0 tw-z-50 tw-overflow-hidden -tw-left-[300px]">
    <div class="tw-w-full tw-flex tw-flex-col tw-gap-6">
      <!-- Logo Section -->
      <div
        class="tw-w-full tw-flex tw-justify-start tw-items-center tw-gap-0 tw-mt-7 tw-px-4">
        <img
          id="sideNavLogo"
          :src="LogoBudimas"
          alt="Logo Budimas"
          width="30" />
        <img
          id="sideNavTextLogo"
          :src="LogoBudimasText"
          alt="Logo Budimas Text"
          width="180" />
      </div>

      <!-- Navigation Menu Section -->
      <nav
        class="tw-w-full tw-flex tw-flex-col tw-gap-3 tw-justify-start tw-items-start tw-px-4 tw-font-medium tw-mt-6">
        <!-- Dynamic Navigation Menu -->
        <div
          v-for="menu in mobileNavigationMenus"
          :key="menu.name"
          v-wave
          class="tw-w-full tw-overflow-hidden">
          <RouterLink :to="menu.route" :class="getButtonClass(menu.isActive())">
            <div class="tw-flex tw-justify-start tw-items-center tw-gap-4">
              <i :class="`mdi ${menu.icon} tw-text-xl`"></i>
              <span class="tw-font-bold">{{ menu.name }}</span>
            </div>
          </RouterLink>
        </div>

        <!-- Logout Button -->
        <div v-wave class="tw-w-full tw-overflow-hidden">
          <button
            @click="logout"
            class="tw-w-full tw-h-12 tw-flex tw-justify-start tw-pl-6 tw-items-center tw-bg-red-600/90 tw-rounded-md tw-cursor-pointer hover:tw-bg-red-600 tw-text-white/80 hover:tw-text-white tw-duration-200 tw-ease-in-out">
            <div class="tw-flex tw-justify-start tw-items-center tw-gap-4">
              <i class="mdi mdi-logout tw-text-xl"></i>
              <span class="tw-font-bold">Logout</span>
            </div>
          </button>
        </div>
      </nav>
    </div>
  </aside>
</template>
