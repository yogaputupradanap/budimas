<script setup>
import { defineProps } from "vue";
defineProps({
  full: Boolean,
  hFull: Boolean,
  itBetween: Boolean,
  itCenter: Boolean,
  itEnd: Boolean,
  jusBetween: Boolean,
  jusCenter: Boolean,
  jusEnd: Boolean,
  flexCol: Boolean,
  gap: String,
  wrap: Boolean,
});
</script>

<template>
  <div
    :class="[
      'tw-flex',
      full ? 'tw-w-full' : 'lg:tw-w-auto tw-w-full',
      hFull ? 'tw-h-[100vh]' : '',
      wrap && 'tw-flex-wrap',
      jusCenter
        ? 'tw-justify-center'
        : jusEnd
        ? 'tw-justify-end'
        : jusBetween
        ? 'tw-justify-between'
        : 'tw-justify-start',
      itCenter
        ? 'tw-items-center'
        : itEnd
        ? 'tw-items-end'
        : itBetween
        ? 'tw-justify-between'
        : 'tw-items-start',
      gap === 'small'
        ? 'tw-gap-1'
        : gap === 'medium'
        ? 'tw-gap-4'
        : gap === 'large'
        ? 'tw-gap-6'
        : gap === 'extra large'
        ? 'tw-gap-8'
        : 'tw-gap-4',
      flexCol ? 'tw-flex-col' : 'tw-flex-row',
    ]">
    <slot></slot>
  </div>
</template>
