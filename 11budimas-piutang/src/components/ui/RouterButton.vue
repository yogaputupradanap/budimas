<script setup>
import { useSlots } from "vue";
import { RouterLink } from "vue-router";

const props = defineProps({
  to: String,
  icon: String
});

const isHasSlot = !!useSlots().default;
</script>

<template>
  <RouterLink
    :to="props.to"
    class="tw-text-white tw-bg-blue-500 tw-rounded-lg tw-px-2 tw-py-1 tw-flex tw-justify-center tw-items-center 
    hover:tw-bg-gray-500 hover:tw-text-white hover:tw-transition-all hover:tw-duration-300 hover:tw-ease-in-out">
    <i v-if="icon" :class="[icon, isHasSlot && 'tw-mr-1']"></i>
    <slot></slot>
  </RouterLink>
</template>
