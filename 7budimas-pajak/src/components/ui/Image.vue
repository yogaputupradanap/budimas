<script setup>
import { defineProps } from "vue";

defineProps(["src", "objectFit", "alt"]);
</script>

<template>
  <div class="tw-w-80 tw-h-40 tw-rounded-md tw-relative tw-overflow-hidden">
    <img
      loading="lazy"
      :alt="alt"
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
