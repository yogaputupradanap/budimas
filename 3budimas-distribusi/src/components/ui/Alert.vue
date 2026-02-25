<script setup>
import { useAlert } from "@/src/store/alert";
import anime from "animejs";
import { enableAnimations } from "@/src/lib/settings";

defineProps(["message", "variant", "dissmissCountDown", "countDown"]);
const alert = useAlert();

const enter = (el, done) => {
  anime.set(el, { translateX: "100%", opacity: 0 });
  anime({
    targets: el,
    translateX: "0%",
    opacity: 1,
    duration: !enableAnimations ? 0 : 600,
    easing: "easeOutExpo",
    complete: done,
  });
};

const leave = (el, done) => {
  anime({
    targets: el,
    translateY: "-120%",
    duration: 800,
    opacity: 0,
    easing: "easeOutExpo",
    complete: done,
  });
};
</script>

<template>
  <Transition @enter="enter" @leave="leave" name="alert-transition">
    <BAlert
      v-model="alert.dissmissCountDown"
      dismissible
      :variant="variant"
      @close-countdown="countDown = $event"
      class="tw-fixed tw-top-3 tw-right-2 tw-z-50 tw-flex tw-flex-col tw-gap-4 tw-w-80"
    >
      <span class="tw-text-sm">Message : </span>
      <div
        class="tw-w-full tw-h-auto tw-max-h-32 tw-bg-white tw-rounded-lg tw-border tw-border-slate-300 tw-overflow-auto tw-bg-opacity-45"
      >
        <p class="tw-text-xs tw-text-slate-700 tw-px-2 tw-py-3 tw-capitalize">
          {{ message }}
        </p>
      </div>
      <BProgress
        :variant="variant"
        :max="alert.dissmissCountDown"
        :value="countDown"
        height="4px"
      />
    </BAlert>
  </Transition>
</template>
