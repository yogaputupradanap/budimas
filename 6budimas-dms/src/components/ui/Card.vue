<script setup>
import { defineProps } from "vue";

const {
  main = true,
  noHeader = false,
  noMainCenter = true,
  noSubheader = false,
} = defineProps({
  main: Boolean,
  noHeader: Boolean,
  noMainCenter: Boolean,
  noSubheader: Boolean,
  dense: Boolean,
});
</script>
<template>
  <div
    :class="[
      'tw-w-full tw-flex tw-gap-6 tw-flex-col tw-px-4 tw-bg-white tw-rounded-lg tw-pb-10'
    ]">
    <div
      v-if="!noHeader"
      :class="[
        'tw-w-full tw-mt-6 tw-flex tw-items-center',
        !noMainCenter ? 'tw-justify-center' : 'tw-justify-start',
        dense ? 'lg:tw-h-8 tw-h-4' : 'lg:tw-h-16 tw-h-6',
      ]">
      <span
        :class="[
          'tw-font-bold lg:tw-text-2xl tw-text-xl',
          !main && 'tw-text-blue-500',
        ]">
        <slot name="header"></slot>
      </span>
    </div>
    <hr v-if="!noHeader" />
    <div
      v-if="!noSubheader"
      :class="[
        'tw-w-full tw-flex tw-justify-center tw-items-center',
        dense ? 'tw-h-6' : 'tw-h-16',
      ]">
      <span
        class="tw-text-red-500 tw-font-bold lg:tw-text-lg tw-text-xs tw-text-center lg:tw-text-start">
        <slot name="subheader"></slot>
      </span>
    </div>
    <hr v-if="!noSubheader" />
    <div class="tw-w-full tw-flex tw-flex-wrap tw-justify-center tw-gap-4">
      <slot name="content"></slot>
    </div>
  </div>
</template>
