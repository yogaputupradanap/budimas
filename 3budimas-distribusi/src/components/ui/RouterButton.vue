<script setup>
import { RouterLink } from "vue-router";

const props = defineProps({
  to: String,
  icon: String
});
</script>

<template>
  <RouterLink
    :to="props.to"
    class="tw-h-8 tw-text-white tw-bg-blue-500 tw-rounded-lg tw-px-2 tw-py-2 tw-flex tw-justify-center tw-items-center 
    hover:tw-bg-gray-500 hover:tw-text-white hover:tw-transition-all hover:tw-duration-300 hover:tw-ease-in-out">
    <i v-if="icon" :class="[icon, 'tw-mr-1']"></i>
    <slot></slot>
  </RouterLink>
</template>
