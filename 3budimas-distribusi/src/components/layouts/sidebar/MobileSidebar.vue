<script setup>
import {ref, watch} from "vue";
import {isMobileMinimize} from "../../../lib/useSideBar";
import anime from "animejs";
import BudimasLogo from "../BudimasLogo.vue";
import SidebarButton from "./SidebarButton.vue";
import {logout} from "@/src/lib/utils";

const mobileSidebar = ref(null);
const routes = [
  "dashboard",
  "konfirmasi",
  "order",
  "jadwal",
  "picking",
  "shipping",
  "history",
  "realisasi",
  "revisi-faktur",
  "driver",
  "retur"
];

const icons = [
  "mdi-view-dashboard",
  "mdi-file-check",
  "mdi-archive",
  "mdi-map",
  "mdi-hook",
  "mdi-checkbox-marked-circle-outline",
  "mdi-history",
  "mdi-book-open-variant",
  "mdi-file-document-edit-outline",
  "mdi-truck-delivery",
  "mdi-sync"
];

// Function to convert route to display name
const getDisplayName = (route) => {
  return route
      .split("-")
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(" ");
};

watch(isMobileMinimize, () => {
  anime({
    targets: mobileSidebar.value,
    duration: 500,
    translateX: isMobileMinimize.value ? "-300px" : "300px",
    easing: "easeOutExpo",
  });
});
</script>

<template>
  <aside
      ref="mobileSidebar"
      class="tw-w-72 tw-h-screen tw-bg-[#01579b] tw-fixed xl:tw-hidden tw-top-0 tw-z-50 tw-overflow-hidden -tw-left-[300px]">
    <div class="tw-w-full tw-flex tw-flex-col tw-gap-6">
      <BudimasLogo
          class="tw-w-full tw-flex tw-justify-start tw-items-center tw-gap-0 tw-mt-7 tw-px-4"
          :id="['sideNavLogo', 'sideNavTextLogo']"/>
      <!-- menu sidebar untuk navigasi -->
      <div
          class="tw-w-full tw-flex tw-flex-col tw-gap-3 tw-justify-start tw-items-start tw-px-4 tw-font-medium tw-mt-6">
        <SidebarButton
            v-for="(route, idx) in routes"
            :key="idx"
            :name="getDisplayName(route)"
            :icon="icons[idx]"
            :to="`/${route}`"/>
        <div v-wave class="tw-w-full tw-overflow-hidden">
          <div
              @click="logout"
              class="tw-w-full tw-h-12 tw-flex tw-justify-start tw-pl-6 tw-items-center tw-bg-red-600/90 tw-rounded-md tw-cursor-pointer hover:tw-bg-red-600 tw-text-white/80 hover:tw-text-white tw-duration-200 tw-ease-in-out">
            <div class="tw-flex tw-justify-start tw-items-center tw-gap-4">
              <i class="mdi mdi-logout tw-text-xl"></i>
              <span class="tw-font-bold">Logout</span>
            </div>
          </div>
        </div>
      </div>
      <!-- menu sidebar nanvigasi -->
    </div>
  </aside>
</template>
