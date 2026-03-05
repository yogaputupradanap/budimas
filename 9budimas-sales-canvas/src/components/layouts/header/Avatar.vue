<script setup>
import { sessionDisk } from "../../../lib/utils";
import { ref, watch } from "vue";
import User1 from "../../../assets/images/users/1.jpg";
import { enableAnimations } from "../../../lib/settings";
import anime from "animejs";

const props = defineProps({
  headerWrapperId: String,
});

const userMenumodal = ref(true);
const setModal = (val) => (userMenumodal.value = val);
const userMenuRef = ref(null);

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

watch(userMenumodal, function () {
  showUserMenu();
});

watch(userMenumodal, function () {
  const checkifClickedOutside = (event) => {
    const current = document.getElementById(props.headerWrapperId);
    if (userMenumodal && current && !current.contains(event.target)) {
      setModal(true);
    }
  };

  document.addEventListener("mousedown", checkifClickedOutside, false);
});
</script>

<template>
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
        <img :src="User1" alt="user" class="rounded-circle" width="30" />
      </span>
    </div>
    <ul
      ref="userMenuRef"
      class="tw-absolute tw-z-50 tw-right-0 -tw-top-48 tw-bg-white tw-w-64 tw-drop-shadow-xl tw-rounded-md tw-px-4 tw-pt-6 tw-pb-6"
      aria-labelledby="2">
      <div
        class="tw-flex tw-flex-col tw-justify-between tw-items-start tw-gap-8">
        <span
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
</template>
