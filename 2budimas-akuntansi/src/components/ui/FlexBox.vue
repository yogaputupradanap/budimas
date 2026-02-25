<script setup>
const props = defineProps({
  full: Boolean,
  hFull: Boolean,
  minScreen: Boolean,
  itBetween: Boolean,
  itCenter: Boolean,
  itEnd: Boolean,
  jusBetween: Boolean,
  jusCenter: Boolean,
  jusEnd: Boolean,
  flexCol: Boolean,
  gap: String,
  wrap: Boolean,
  noLeftPadding: Boolean
});

const width = props.full ? "tw-w-full" : "lg:tw-w-auto tw-w-full";
const height = props.hFull
  ? "md:tw-h-[75vh] tw-h-auto"
  : props.minScreen
  ? "tw-min-h-screen"
  : "tw-h-auto";
const wrap = props.wrap && "tw-flex-wrap";
const justify = props.jusCenter
  ? "tw-justify-center"
  : props.jusEnd
  ? "tw-justify-end"
  : props.jusBetween
  ? "tw-justify-between"
  : "tw-justify-start";
const items = props.itCenter
  ? "tw-items-center"
  : props.itEnd
  ? "tw-items-end"
  : props.itBetween
  ? "tw-justify-between"
  : "tw-items-start";
const gap =
  props.gap === "small"
    ? "tw-gap-4 md:tw-gap-1"
    : props.gap === "medium"
    ? "tw-gap-4"
    : props.gap === "large"
    ? "tw-gap-6"
    : props.gap === "extra large"
    ? "tw-gap-8"
    : "tw-gap-4";
const flexDirection = props.flexCol ? "tw-flex-col" : "tw-flex-row";
const noLeftPadding = !props.noLeftPadding && 'tw-pl-0 md:tw-pl-4'
</script>

<template>
  <div
    :class="[
      'tw-flex',
      width,
      height,
      wrap,
      justify,
      items,
      gap,
      flexDirection,
      noLeftPadding
    ]">
    <slot></slot>
  </div>
</template>
