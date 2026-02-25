<script setup>
import { useRoute } from "vue-router";
const inActiveButton = "tw-bg-blue-100 hover:tw-bg-white hover:tw-text-black";
const activeButton = "tw-bg-[#1be1af] tw-text-white hover:tw-text-white";

const props = defineProps({
  name: String,
  to: String,
  icon: String,
});

const route = useRoute();

const isActive = () => {
  if (route.path === props.to) return true;

  if (props.to !== "/" && route.path.startsWith(props.to)) return true;

  return false;
};
</script>

<template>
  <div v-wave class="tw-w-full tw-overflow-hidden">
    <RouterLink
      :to="to"
      :class="[
        `tw-w-full tw-h-12 tw-flex tw-justify-start tw-pl-6 tw-items-center  tw-rounded-md
        tw-cursor-pointer tw-duration-200 tw-ease-in-out `,
        isActive() ? activeButton : inActiveButton,
      ]">
      <div class="tw-flex tw-justify-start tw-items-center tw-gap-3">
        <i id="navButtIcon" :class="['mdi tw-text-2xl', icon]"></i>
        <span id="navButtText" class="tw-font-bold">{{ name }}</span>
      </div>
    </RouterLink>
  </div>
</template>
