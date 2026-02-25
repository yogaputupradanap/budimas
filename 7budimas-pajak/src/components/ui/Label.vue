<script setup>
import FlexBox from "./FlexBox.vue";
const props = defineProps({
  label: { type: String, default: "" },
  full: { type: Boolean, default: true },
});
</script>

<template>
  <FlexBox flex-col gap="small" :full="props.full" no-left-padding>
    <span class="tw-capitalize">{{ label }}</span>
    <slot></slot>
  </FlexBox>
</template>
