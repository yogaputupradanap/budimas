<script setup>
import { defineProps } from "vue";
import NoImage from "../../assets/images/no-picture-taking.png"

defineProps(["src", "objectFit", "alt"]);

function handleError(event) {
  event.target.src = NoImage
}
</script>

<template>
  <div class="tw-w-80 tw-h-40 tw-rounded-md tw-relative tw-overflow-hidden">
    <img
      @error="handleError"
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
