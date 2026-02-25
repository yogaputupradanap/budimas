<script setup>
import BudimasLogo from "../BudimasLogo.vue";
import { isMobileMinimize, setMobileMinimize } from "../../../lib/useSideBar";

const toggleMobile = () => setMobileMinimize(!isMobileMinimize.value);
</script>
<template>
  <header
  class="tw-w-full tw-h-16 tw-bg-[#01579b] xl:tw-hidden tw-flex tw-justify-between tw-items-center tw-px-4">
    <BudimasLogo
      :id="['sideNavLogo', 'sideNavLogoText']"
      :alt="['logo budimas', 'logo budimas text']" />
    <div
      @click="toggleMobile"
      class="tw-w-16 tw-h-full tw-flex tw-justify-center tw-items-center hover:tw-bg-[#284f6d] tw-cursor-pointer">
      <i class="mdi mdi-dots-horizontal tw-text-2xl tw-text-white"></i>
    </div>
  </header>
</template>
