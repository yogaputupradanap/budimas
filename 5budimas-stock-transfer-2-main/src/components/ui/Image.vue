<script setup>
import { defineProps } from "vue";
defineProps(["src", "objectFit"]);
</script>

<template>
  <div class="tw-w-80 tw-h-40 tw-rounded-md tw-relative tw-overflow-hidden">
    <BImg
      :src="src"
      :class="[
        'tw-w-full tw-h-full',
        objectFit === 'contain'
          ? 'tw-object-contain'
          : objectFit === 'fill'
          ? 'tw-object-fill'
          : 'tw-object-cover',
      ]"
    />
  </div>
</template>
