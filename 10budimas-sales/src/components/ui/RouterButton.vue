<script setup>
import { BButton } from "bootstrap-vue-next";
import { RouterLink } from "vue-router";

const props = defineProps({
  to: String,
  icon: String,
  disabled: Boolean,
});
</script>

<template>
  <RouterLink
    v-if="!disabled"
    :to="props.to"
    class="tw-bg-blue-500 tw-rounded-lg tw-px-2 tw-py-1 tw-flex tw-justify-center tw-items-center 
    hover:tw-bg-gray-500 hover:tw-text-white hover:tw-transition-all hover:tw-duration-300 hover:tw-ease-in-out">
    <i v-if="icon" :class="[icon, 'tw-mr-1']"></i>
    <slot></slot>
  </RouterLink>
  <button
    v-else
    class="tw-rounded-lg tw-py-1 tw-flex tw-justify-center tw-items-center
    tw-text-xs tw-w-full">
    <i v-if="icon" :class="[icon, 'tw-mr-1']"></i>
    <slot></slot>
  </button>
</template>
