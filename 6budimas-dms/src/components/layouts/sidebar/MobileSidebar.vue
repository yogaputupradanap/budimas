<script setup>
import { watch, ref, computed } from "vue";
import { isMobileMinimize, setMobileMinimize } from "../../../lib/useSideBar";
import BudimasLogo from "../BudimasLogo.vue";
import anime from "animejs";
import { useUser } from "../../../store/user";
import SidebarButton from "./SidebarButton.vue";
import { logout } from "../../../lib/utils";
import { useToogleClickOutside } from "../../../lib/useToogleClickOutside";

const mobileSidebar = ref(null);
const userStore = useUser();

const buttons = [
  {
    icon: " mdi-file-excel",
    title: "Import CSV",
    route: "import-csv",
  },
];

const userAccessButtons = computed(() => {
  if (!userStore.userAccess?.length) {
    return [
      {
        title: "Dashboard",
        route: "dashboard",
        icon: "mdi-view-dashboard",
      },
      ...buttons,
    ];
  }

  return userStore.userAccess
    .map((val) => buttons.find((i) => i.route === val.name))
    .filter(Boolean);
});

const [, elementRef] = useToogleClickOutside(
  "mobile-side-ref",
  {
    axis: "translateX",
    duration: 500,
    easing: "easeOutExpo",
    hideValue: "-300px",
    showValue: "300px",
  },
  {
    outsideRef: isMobileMinimize,
    setOutsideRef: setMobileMinimize,
  }
);
</script>

<template>
  <aside
    id="mobile-side-ref"
    ref="elementRef"
    class="tw-w-72 tw-h-screen tw-bg-[#01579b] tw-fixed lg:hidden tw-top-0 tw-z-[99999] tw-overflow-hidden -tw-left-[300px] tw-shadow-xl"
  >
    <div class="tw-w-full tw-flex tw-flex-col tw-gap-6">
      <BudimasLogo
        class="tw-w-full tw-flex tw-justify-start tw-items-center tw-gap-0 tw-mt-7 tw-px-4"
        :id="['sideNavLogo', 'sideNavTextLogo']"
      />
      <!-- menu sidebar untuk navigasi -->
      <div
        class="tw-w-full tw-flex tw-flex-col tw-gap-3 tw-justify-start tw-items-start tw-px-4 tw-font-medium tw-mt-6"
      >
        <SidebarButton
          v-for="button in userAccessButtons"
          :key="button['title']"
          :name="button['title']"
          :icon="button['icon']"
          :to="`/${button['route']}`"
        />
        <div v-wave class="tw-w-full tw-overflow-hidden">
          <div
            @click="logout"
            class="tw-w-full tw-h-12 tw-flex tw-justify-start tw-pl-6 tw-items-center tw-bg-red-600/90 tw-rounded-md tw-cursor-pointer hover:tw-bg-red-600 tw-text-white/80 hover:tw-text-white tw-duration-200 tw-ease-in-out"
          >
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
