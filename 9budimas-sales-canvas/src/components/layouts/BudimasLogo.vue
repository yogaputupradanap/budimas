<script setup>
import LogoBudimas from "../../assets/images/logo-budimas-white.png";
import LogoBudimasText from "../../assets/images/logo-text-budimas.png";

defineProps({
  id: {
    type: Array,
    default() {
      return ["logo", "text-logo"];
    },
  },
  alt: {
    type: Array,
    default() {
      return ["logo", "text logo"];
    },
  },
  width: {
    type: Array,
    default() {
      return ['30', '180'];
    },
  },
});
</script>

<template>
  <div class="tw-flex tw-justify-start tw-items-center tw-gap-0 tw-px-4">
    <img :id="id[0]" :src="LogoBudimas" :alt="alt[0]" :width="width[0]" />
    <img :id="id[1]" :src="LogoBudimasText" :alt="alt[1]" :width="width[1]" />
  </div>
</template>
