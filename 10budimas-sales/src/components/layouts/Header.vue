<!-- eslint-disable vue/multi-word-component-names -->
<script setup>
import User1 from "../../assets/images/users/1.jpg";
import { ref, onMounted, onUnmounted, watch } from "vue";
import { getClock, sessionDisk } from "../../lib/utils";
import anime from "animejs";
import {
  isMinimize,
  setMinimize,
  isMobileMinimize,
  setMobileMinimize,
} from "../../lib/useSideBar";
import LogoBudimas from "../../assets/images/logo-budimas-white.png";
import LogoBudimasText from "../../assets/images/logo-text-budimas.png";
import { enableAnimations } from "../../lib/settings";
import { useRouter } from "vue-router";
import { useSales } from "@/src/store/sales";
import Skeleton from "../ui/Skeleton.vue";

const clock = ref(getClock());
const clockInterval = ref();
const userMenumodal = ref(true);
const setModal = (val) => (userMenumodal.value = val);
const userMenuRef = ref(null);
const wrapperRef = ref(null);
const toggle = () => setMinimize(!isMinimize.value);
const toggleMobile = () => setMobileMinimize(!isMobileMinimize.value);
const router = useRouter();
const sales = useSales();

const showUserMenu = () => {
  anime({
    targets: userMenuRef.value,
    translateY: userMenumodal.value ? -200 : 260,
    opacity: userMenumodal.value ? 0 : 1,
    duration: !enableAnimations ? 0 : 1200,
    easing: "spring(1, 80, 10, 6.5)",
  });
};

const logout = () => {
  sessionDisk.clearSession();
  window.location.reload();
};

onMounted(() => {
  clockInterval.value = setInterval(() => {
    clock.value = getClock();
  }, 1000);
});

onUnmounted(() => {
  clearInterval(clockInterval.value);
});

watch(userMenumodal, function () {
  showUserMenu();
});

watch(userMenumodal, function () {
  const checkifClickedOutside = (event) => {
    const current = wrapperRef.value;
    if (
      // eslint-disable-next-line vue/no-ref-as-operand
      userMenumodal &&
      wrapperRef.value &&
      !current.contains(event.target)
    ) {
      setModal(true);
    }
  };

  document.addEventListener("mousedown", checkifClickedOutside, false);
});
</script>

<template>
  <header
    class="tw-w-full tw-h-16 tw-bg-[#01579b] lg:tw-hidden tw-flex tw-justify-between tw-items-center tw-px-4">
    <div class="tw-flex tw-justify-start tw-items-center tw-gap-0 tw-px-4">
      <img id="sideNavLogo" :src="LogoBudimas" alt="logo budimas" width="30" />
      <img
        id="sideNavTextLogo"
        :src="LogoBudimasText"
        alt="logo budimas text"
        width="180" />
    </div>
    <div
      @click="toggleMobile"
      class="tw-w-16 tw-h-full tw-flex tw-justify-center tw-items-center hover:tw-bg-[#284f6d] tw-cursor-pointer">
      <i class="mdi mdi-dots-horizontal tw-text-2xl tw-text-white"></i>
    </div>
  </header>
  <header
    ref="wrapperRef"
    class="tw-w-full tw-h-16 tw-bg-white tw-hidden lg:tw-flex tw-justify-between tw-items-center tw-px-4">
    <div class="tw-flex tw-gap-6">
      <span
        @click="toggle"
        class="tw-w-10 tw-h-10 tw-rounded-full tw-flex tw-justify-center tw-items-center tw-cursor-pointer">
        <i class="mdi mdi-menu tw-text-2xl" />
      </span>
      <div class="tw-flex tw-justify-center tw-items-center tw-gap-2">
        <i class="mdi mdi-clock tw-text-lg tw-text-blue-500"></i>
        <span class="tw-font-semibold tw-text-blue-500">
          {{ clock }}
        </span>
      </div>
    </div>
    <div
      class="tw-flex tw-justify-start tw-items-center tw-gap-6 tw-text-blue-500">
      <div class="tw-flex tw-items-center tw-gap-2 tw-capitalize">
        <i class="mdi mdi-account"></i>
        <Skeleton v-if="sales.loading" class="tw-w-16 tw-h-4" />
        <span v-else>{{ sales.salesUser?.nama }}</span>
      </div>
      <div class="tw-flex tw-items-center tw-gap-2">
        <i class="mdi mdi-tag"></i>
        <Skeleton v-if="sales.loading" class="tw-w-16 tw-h-4" />
        <span v-else>{{ sales.salesUser?.sales.nama_jabatan }}</span>
      </div>
      <div class="tw-flex tw-items-center tw-gap-2">
        <i class="mdi mdi-store"></i>
        <Skeleton v-if="sales.loading" class="tw-w-16 tw-h-4" />
        <span v-else>{{ sales.salesUser?.sales.nama_cabang }}</span>
      </div>
      <li
        class="tw-w-12 tw-h-12 tw-relative tw-flex tw-justify-center tw-items-center tw-mr-4">
        <div
          v-wave
          @click="setModal(!userMenumodal)"
          class="tw-w-full tw-h-full tw-flex tw-justify-center tw-items-center">
          <span
            href="#"
            id="2"
            role="button"
            data-bs-toggle="dropdown"
            aria-expanded="false">
            <img
              :src="User1"
              alt="user"
              class="rounded-circle tw-mt-1"
              width="31" />
          </span>
        </div>
        <ul
          ref="userMenuRef"
          class="tw-absolute tw-z-50 tw-right-0 -tw-top-48 tw-bg-white tw-w-64 tw-drop-shadow-xl tw-rounded-md tw-px-4 tw-pt-6 tw-pb-6"
          aria-labelledby="2">
          <div
            class="tw-flex tw-flex-col tw-justify-between tw-items-start tw-gap-8">
            <span
              href=""
              class="tw-flex tw-gap-6 tw-justify-start tw-items-center hover:tw-text-blue-500 tw-transition-all tw-duration-300 tw-ease-in-out">
              <span
                class="tw-w-10 tw-h-10 tw-rounded-full tw-bg-blue-500 tw-flex tw-justify-center tw-items-center">
                <i class="mdi mdi-account fs-6 tw-text-white"></i>
              </span>
              <span class="tw-text-xl">Profile</span>
            </span>
            <span
              @click="logout"
              class="tw-flex tw-cursor-pointer tw-gap-6 tw-justify-start tw-items-center hover:tw-text-blue-500 tw-transition-all tw-duration-300 tw-ease-in-out">
              <span
                class="tw-w-10 tw-h-10 tw-rounded-full tw-bg-orange-500 tw-flex tw-justify-center tw-items-center">
                <i class="mdi mdi-power tw-text-white fs-6"></i>
              </span>
              <span class="tw-text-xl">Log Out</span>
            </span>
          </div>
        </ul>
      </li>
    </div>
  </header>
</template>
