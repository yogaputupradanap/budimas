<script setup>
import { isMinimize, setMinimize } from "../../../lib/useSideBar";
import { getClock } from "../../../lib/utils";
import { onMounted, onUnmounted, ref } from "vue";

const clockInterval = ref();
const clock = ref(getClock());
const toggle = () => setMinimize(!isMinimize.value);

onMounted(() => {
  clockInterval.value = setInterval(() => {
    clock.value = getClock();
  }, 1000);
});

onUnmounted(() => {
  clearInterval(clockInterval.value);
});
</script>

<template>
  <div class="tw-flex tw-gap-6">
    <span
      @click="toggle"
      class="tw-w-10 tw-h-10 tw-rounded-full tw-flex tw-justify-center tw-items-center tw-cursor-pointer">
      <i class="mdi mdi-menu tw-text-2xl" />
    </span>
    <div class="tw-flex tw-justify-center tw-items-center tw-gap-1 tw-text-sm">
      <i class="mdi mdi-clock-outline tw-text-base tw-text-blue-500"></i>
      <span class="tw-font-semibold tw-text-blue-500">
        {{ clock }}
      </span>
    </div>
  </div>
</template>
