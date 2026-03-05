<script setup>
import { watch } from "vue";
import { useRoute } from "vue-router";
import { isMinimize } from "../../lib/useSideBar";
import LogoBudimas from "../../assets/images/logo-budimas-white.png";
import LogoBudimasText from "../../assets/images/logo-text-budimas.png";
import MobileSidebar from "./MobileSidebar.vue";
import FlexBox from "../ui/FlexBox.vue";
import { enableAnimations } from "../../lib/settings";
import anime from "animejs";
import { logout } from "@/src/lib/utils";

const route = useRoute();

// Konstanta untuk styling
const BUTTON_STYLES = {
  inactive: "tw-bg-blue-100 hover:tw-bg-white hover:tw-text-black",
  active: "tw-bg-[#1be1af] tw-text-white hover:tw-text-white",
};

const ANIMATION_CONFIG = {
  easing: "easeOutExpo",
  duration: enableAnimations ? 300 : 0,
};

// Konfigurasi menu navigasi
const navigationMenus = [
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

// Fungsi animasi untuk meminimize sidebar
const animateMinimize = () => {
  anime.set("#sidebar", { width: "288px" });
  anime.set("#navButt", { width: "100%" });

  anime
    .timeline(ANIMATION_CONFIG)
    .add(
      {
        targets: "#navButtText",
        opacity: 0,
        translateX: 100,
        duration: ANIMATION_CONFIG.duration,
      },
      "-=10"
    )
    .add(
      {
        targets: "#navButt",
        width: "100%",
        duration: enableAnimations ? 400 : 0,
      },
      "-=400"
    )
    .add(
      {
        targets: "#navButtIcon",
        translateX: "-8px",
        scale: 1.1,
        duration: ANIMATION_CONFIG.duration,
      },
      "-=1"
    )
    .add(
      {
        targets: "#sidebar",
        width: "86px",
        duration: ANIMATION_CONFIG.duration,
      },
      "-=400"
    )
    .add(
      {
        targets: "#sideNavLogo",
        translateX: "40%",
        scale: 2,
        duration: ANIMATION_CONFIG.duration,
      },
      "-=300"
    )
    .add(
      {
        targets: "#sideNavTextLogo",
        opacity: 0,
        duration: ANIMATION_CONFIG.duration,
      },
      "-=400"
    );
};

// Fungsi animasi untuk expand sidebar
const animateExpand = () => {
  anime.set("#navButt", { width: "35%" });

  anime
    .timeline(ANIMATION_CONFIG)
    .add({
      targets: "#sidebar",
      width: "288px",
      duration: ANIMATION_CONFIG.duration,
    })
    .add(
      {
        targets: "#navButt",
        width: "100%",
        duration: enableAnimations ? 400 : 0,
      },
      "-=100"
    )
    .add(
      {
        targets: "#sideNavLogo",
        translateX: "0%",
        scale: 1,
        duration: enableAnimations ? 400 : 0,
      },
      "-=300"
    )
    .add(
      {
        targets: "#sideNavTextLogo",
        opacity: 1,
        duration: ANIMATION_CONFIG.duration,
      },
      "-=300"
    )
    .add(
      {
        targets: "#navButtIcon",
        translateX: "0%",
        scale: 1,
        duration: ANIMATION_CONFIG.duration,
      },
      "-=0"
    )
    .add(
      {
        targets: "#navButtText",
        opacity: 1,
        translateX: 0,
        duration: ANIMATION_CONFIG.duration,
      },
      "-=650"
    );
};

// Watch untuk perubahan minimize state
watch(isMinimize, () => {
  if (isMinimize.value) {
    animateMinimize();
  } else {
    animateExpand();
  }
});

// Fungsi untuk mendapatkan class button berdasarkan status active
const getButtonClass = (isActive) => {
  const baseClass = `tw-w-full tw-h-12 tw-flex tw-justify-start tw-pl-3 tw-items-center 
                    tw-rounded-md tw-cursor-pointer tw-duration-200 tw-ease-in-out`;
  const statusClass = isActive ? BUTTON_STYLES.active : BUTTON_STYLES.inactive;
  return `${baseClass} ${statusClass}`;
};
</script>

<template>
  <MobileSidebar />

  <aside
    id="sidebar"
    class="tw-w-72 tw-h-screen tw-bg-[#01579b] tw-hidden lg:tw-flex lg:tw-sticky tw-top-0 tw-z-50 tw-overflow-hidden">
    <FlexBox :flex-col="true" :full="true" gap="extra large">
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
          v-for="menu in navigationMenus"
          :key="menu.name"
          id="navButt"
          v-wave
          class="tw-w-full tw-overflow-hidden">
          <RouterLink :to="menu.route" :class="getButtonClass(menu.isActive())">
            <div class="tw-flex tw-justify-start tw-items-center tw-gap-4">
              <i id="navButtIcon" :class="`mdi ${menu.icon} tw-text-xl`"></i>
              <span id="navButtText" class="tw-font-bold">{{ menu.name }}</span>
            </div>
          </RouterLink>
        </div>

        <!-- Logout Button -->
        <div id="navButt" v-wave class="tw-w-full tw-overflow-hidden">
          <button
            @click="logout"
            class="tw-w-full tw-h-12 tw-flex tw-justify-start tw-pl-3 tw-items-center tw-bg-red-600/90 tw-rounded-md tw-cursor-pointer hover:tw-bg-red-600 tw-text-white/80 hover:tw-text-white tw-duration-200 tw-ease-in-out">
            <div class="tw-flex tw-justify-start tw-items-center tw-gap-4">
              <i id="navButtIcon" class="mdi mdi-logout tw-text-xl"></i>
              <span id="navButtText" class="tw-font-bold">Logout</span>
            </div>
          </button>
        </div>
      </nav>
    </FlexBox>
  </aside>
</template>
