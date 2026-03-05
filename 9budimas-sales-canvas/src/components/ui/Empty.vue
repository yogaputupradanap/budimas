<script setup>
import FlexBox from "./FlexBox.vue";
import { defineProps } from "vue";
defineProps(["text"]);
</script>

<template>
  <FlexBox full flex-col jus-center it-center gap="small">
    <i class="mdi mdi-delete-empty tw-text-gray-500 tw-text-7xl"></i>
    <span class="tw-text-gray-500">{{ text }}</span>
  </FlexBox>
</template>
