<script setup>
import { defineProps, ref } from "vue";
import Loader from "./Loader.vue";
import { RouterLink } from "vue-router";

const props = defineProps({
  icon: String,
  text: String,
  full: Boolean,
  trigger: Function,
  url: String,
  replaceUrl: String,
  active: {
    type: Boolean,
    default: true,
  },
});
const loading = ref(false);

</script>

<template>
  <RouterLink
    :to="url"
    :class="[
      'tw-h-48 lg:tw-min-h-[200px] tw-flex tw-flex-col tw-justify-center tw-items-center tw-gap-2 tw-px-6 tw-py-8 tw-rounded-lg tw-duration-300 tw-ease-out tw-cursor-pointer',
      full ? 'tw-w-full' : 'tw-w-full lg:tw-w-[206px]',
      !active
        ? 'tw-bg-gray-50 tw-text-gray-400 tw-border tw-border-slate-300'
        : 'hover:tw-bg-white tw-text-white hover:tw-scale-105 hover:tw-text-gray-800 tw-bg-[#01579B] tw-shadow-lg',
    ]"
  >
    <i :class="['mdi tw-text-6xl', icon]" v-if="!loading"></i>
    <Loader v-else />
    <span class="tw-text-lg tw-font-semibold tw-text-center">{{ text }}</span>
  </RouterLink>
</template>
