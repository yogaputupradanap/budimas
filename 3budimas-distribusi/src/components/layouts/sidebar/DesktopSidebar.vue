<script setup>
import SidebarButton from "./SidebarButton.vue";
import BudimasLogo from "../BudimasLogo.vue";
import {logout} from "@/src/lib/utils";
import {computed} from "vue";

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
  "retur",
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
  "mdi-sync",
];

// Function to convert route to display name
const getDisplayName = (route) => {
  return route
      .split("-")
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(" ");
};

// Or you can use computed property for route names
const routeNames = computed(() => {
  return routes.map((route) => getDisplayName(route));
});
</script>

<template>
  <aside
      id="sidebar"
      class="tw-w-72 tw-h-screen tw-bg-[#01579b] tw-hidden xl:tw-flex lg:tw-sticky tw-top-0 tw-z-50 tw-overflow-hidden">
    <FlexBox :flex-col="true" :full="true" gap="extra large">
      <BudimasLogo
          class="tw-w-full tw-flex tw-justify-start tw-items-center tw-gap-0 tw-mt-7 tw-px-4"
          :id="['sideNavLogo', 'sideNavTextLogo']"
          :alt="['logo budimas', 'logo budimas text']"/>
      <div
          class="tw-w-full tw-flex tw-flex-col tw-gap-3 tw-justify-start tw-items-start tw-px-4 tw-font-medium tw-mt-16">
        <SidebarButton
            v-for="(route, idx) in routes"
            id="navButt"
            :key="route"
            :name="getDisplayName(route)"
            :icon="icons[idx]"
            :to="`/${route}`"/>
        <div
            id="navButt"
            v-wave
            class="tw-w-full tw-overflow-hidden"
            @click="logout">
          <div
              class="tw-w-full tw-h-12 tw-flex tw-justify-start tw-pl-6 tw-items-center tw-bg-red-600/90 tw-rounded-md tw-cursor-pointer hover:tw-bg-red-600 tw-text-white/80 hover:tw-text-white tw-duration-200 tw-ease-in-out">
            <div class="tw-flex tw-justify-start tw-items-center tw-gap-4">
              <i id="navButtIcon" class="mdi mdi-logout tw-text-xl"></i>
              <span id="navButtText" class="tw-font-bold">Logout</span>
            </div>
          </div>
        </div>
      </div>
    </FlexBox>
  </aside>
</template>
