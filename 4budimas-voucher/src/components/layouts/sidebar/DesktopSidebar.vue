<script setup>
import SidebarButton from "./SidebarButton.vue";
import BudimasLogo from "../BudimasLogo.vue";
// import { useUser } from "@/src/store/user";
// import { useRouter } from "vue-router";
// import { computed } from "vue";
// // Import sessionDisk from utils.js
// import { sessionDisk } from "@/src/lib/utils"; // Adjust the path if needed

// const userStore = useUser();
// const router = useRouter(); // Initialize router

const buttons = [
  {
    title: "Dashboard",
    route: "dashboard",
    icon: "mdi-view-dashboard",
  },
  {
    icon: "mdi-cash",
    title: "Voucher 1",
    route: "voucher-1",
  },
  {
    icon: "mdi-package",
    title: "Voucher 2",
    route: "voucher-2",
  },
  {
    icon: "mdi-store",
    title: "Voucher 3",
    route: "voucher-3",
  },
];

// // Fungsi handleLogout
// const handleLogout = () => {
//   localStorage.removeItem("user");
//   localStorage.removeItem("hakakses");
//   userStore.$reset(); // Reset store jika menggunakan Pinia

//   sessionDisk.clearSession();

//   // Redirect ke halaman login
//   router.replace("/login");
// };
</script>

<template>
  <aside id="sidebar"
    class="tw-w-72 tw-h-screen tw-bg-[#01579b] tw-hidden lg:tw-flex lg:tw-sticky tw-top-0 tw-z-50 tw-overflow-hidden">
    <FlexBox :flex-col="true" :full="true" gap="extra large">
      <BudimasLogo class="tw-w-full tw-flex tw-justify-start tw-items-center tw-gap-0 tw-mt-7 tw-px-4"
        :id="['sideNavLogo', 'sideNavTextLogo']" :alt="['logo budimas', 'logo budimas text']" />
      <div class="tw-w-full tw-flex tw-flex-col tw-gap-3 tw-justify-start tw-items-start
        tw-px-4 tw-font-medium tw-mt-16">
        <SidebarButton v-for="button in buttons" id="navButt" :key="button['title']" :name="button['title']" :icon="button['icon']"
          :to="`/${button['route']}`" />
        <div id="navButt" v-wave class="tw-w-full tw-overflow-hidden">
          <a class="tw-w-full tw-h-12 tw-flex tw-justify-start tw-px-3 tw-items-center tw-bg-red-600/90 tw-rounded-md tw-cursor-pointer hover:tw-bg-red-600 tw-text-white/80 hover:tw-text-white tw-duration-200 tw-ease-in-out"
            @click="handleLogout">
            <div class="tw-flex tw-justify-start tw-items-center tw-gap-3">
              <i id="navButtIcon" class="mdi mdi-logout tw-text-xl"></i>
              <span id="navButtText" class="tw-font-medium tw-text-sm">
                Logout
              </span>
            </div>
          </a>
        </div>
      </div>
    </FlexBox>
  </aside>
</template>
