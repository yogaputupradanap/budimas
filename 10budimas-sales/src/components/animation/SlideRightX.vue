<script setup>
import BaseAnimation from "./BaseAnimation.vue";
import { defineProps } from "vue";

const props = defineProps([
  "initialX",
  "x",
  "durationEnter",
  "durationLeave",
  "delayIn",
  "delayOut",
]);

const initialEnter = { translateX: props.initialX ? props.initialX : -10, opacity: 0 };
const enterAnimation = {
  translateX: 0,
  opacity: 1,
  duration: props.durationEnter ? props.durationEnter * 1000 : 400,
  easing: "easeOutExpo",
  delay: props.delayIn ? props.delayIn * 1000 : 0,
};
const leaveAnimation = {
  translateX: props.x ? props.x : 20,
  opacity: 0,
  duration: props.durationLeave ? props.durationLeave * 1000 : 400,
  easing: "easeOutExpo",
  delay: props.delayOut ? props.delayOut * 1000 : 0,
};
</script>

<template>
  <BaseAnimation
    :set-initial-enter="initialEnter"
    :enter-animation="enterAnimation"
    :leave-animation="leaveAnimation"
  >
    <slot></slot>
  </BaseAnimation>
</template>
