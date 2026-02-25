<script setup>
import SidebarButton from "./SidebarButton.vue";
import BudimasLogo from "../BudimasLogo.vue";
import { useUser } from "@/src/store/user";
import { computed } from "vue";
import { logout } from "@/src/lib/utils";

const userStore = useUser();

const buttons = [
  {
    title: "Stock Transfer",
    route: "stock-transfer",
    icon: "mdi-treasure-chest",
  },
  {
    title: "Konfirmasi",
    route: "konfirmasi",
    icon: "mdi-checkbox-marked",
  },
  {
    title: "Pengiriman",
    route: "pengiriman",
    icon: "mdi-truck-delivery",
  },
  {
    title: "Status Pengiriman",
    route: "status-pengiriman",
    icon: "mdi-package-variant",
  },
  {
    title: "Penerimaan Barang",
    route: "penerimaan-barang",
    icon: "mdi-dolly",
  },
  {
    title: "List Eskalasi",
    route: "list-eskalasi",
    icon: "mdi-list-box",
  },
];

const userAccessButtons = computed(() => {
  const arr = userStore.userAccess?.map((val) => {
    return { ...buttons.find((i) => i["route"] === val["name"]) };
  });

  arr.unshift({
    title: "Dashboard",
    route: "dashboard",
    icon: "mdi-view-dashboard",
  });

  return arr;
});
</script>

<template>
  <aside
    id="sidebar"
    class="tw-w-72 tw-h-screen tw-bg-[#01579b] tw-hidden lg:tw-flex lg:tw-sticky tw-top-0 tw-z-50 tw-overflow-hidden">
    <FlexBox :flex-col="true" :full="true" gap="extra large">
      <BudimasLogo
        class="tw-w-full tw-flex tw-justify-start tw-items-center tw-gap-0 tw-mt-7 tw-px-4"
        :id="['sideNavLogo', 'sideNavTextLogo']"
        :alt="['logo budimas', 'logo budimas text']" />
      <div
        class="tw-w-full tw-flex tw-flex-col tw-gap-3 tw-justify-start tw-items-start
        tw-px-4 tw-font-medium tw-mt-16"
      >
        <SidebarButton
          v-for="button in userAccessButtons"
          id="navButt"
          :key="button['title']"
          :name="button['title']"
          :icon="button['icon']"
          :to="`/${button['route']}`" />
        <div id="navButt" v-wave class="tw-w-full tw-overflow-hidden">
          <div
            @click="logout"
            class="tw-w-full tw-h-12 tw-flex tw-justify-start tw-px-3 tw-items-center tw-bg-red-600/90 tw-rounded-md tw-cursor-pointer hover:tw-bg-red-600 tw-text-white/80 hover:tw-text-white tw-duration-200 tw-ease-in-out">
            <div class="tw-flex tw-justify-start tw-items-center tw-gap-3">
              <i id="navButtIcon" class="mdi mdi-logout tw-text-xl"></i>
              <span id="navButtText" class="tw-font-medium tw-text-sm">
                Logout
              </span>
            </div>
          </div>
        </div>
      </div>
    </FlexBox>
  </aside>
</template>
