<script setup>
import FlexBox from "./FlexBox.vue";
defineProps({ label: String, full: Boolean });
</script>

<template>
  <FlexBox flex-col gap="small" :full="full">
    <span class="tw-capitalize">{{ label }}</span>
    <slot></slot>
  </FlexBox>
</template>
