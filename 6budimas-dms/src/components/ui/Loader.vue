<script setup>
import { computed, defineProps } from "vue";

const props = defineProps(["width", "height"]);

const styles = computed(() => {
  return {
    width: props.width ? props.height : "40px",
    height: props.height ? props.height : "40px",
  };
});
</script>

<template>
  <svg
    v-bind:style="styles"
    class="spinner"
    viewBox="0 0 66 66"
    xmlns="http://www.w3.org/2000/svg"
  >
    <circle
      class="path"
      fill="none"
      stroke-width="7"
      stroke-linecap="round"
      cx="33"
      cy="33"
      r="27"
    ></circle>
  </svg>
</template>

<style lang="scss" scoped>
$offset: 187;
$duration: 1.4s;

.spinner {
  animation: circle-rotator $duration linear infinite;
  * {
    line-height: 0;
    box-sizing: border-box;
  }
}

@keyframes circle-rotator {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(270deg);
  }
}

.path {
  stroke: #0064d0;
  stroke-dasharray: $offset;
  stroke-dashoffset: 0;
  transform-origin: center;
  animation: circle-dash $duration ease-in-out infinite;
}

@keyframes circle-dash {
  0% {
    stroke-dashoffset: $offset;
  }
  50% {
    stroke-dashoffset: $offset/4;
    transform: rotate(135deg);
  }
  100% {
    stroke-dashoffset: $offset;
    transform: rotate(450deg);
  }
}
</style>
