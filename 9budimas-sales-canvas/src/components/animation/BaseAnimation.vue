<script setup>
import { useRoute } from "vue-router";
import { watch, ref, onMounted, defineProps } from "vue";
import { enableAnimations } from "../../lib/settings";
import anime from "animejs";

const route = useRoute();
const el = ref(null);
const showElement = ref(false);

const props = defineProps([
  "setInitialEnter",
  "enterAnimation",
  "leaveAnimation",
]);

const enterAnimation = (el, done) => {
  anime.set(el, props.setInitialEnter);

  anime({
    targets: el,
    ...props.enterAnimation,
    delay: !enableAnimations ? 0 : props.enterAnimation.delay,
    duration: !enableAnimations ? 0 : props.enterAnimation.duration,
    complete: done,
  });
};

const leaveAnimation = (el, done) => {
  anime({
    targets: el,
    ...props.leaveAnimation,
    delay: !enableAnimations ? 0 : props.leaveAnimation.delay,
    duration: !enableAnimations ? 0 : props.leaveAnimation.duration,
    complete() {
      done();
      showElement.value = true;
    },
  });
};

watch(route, () => {
  showElement.value = !showElement.value;
});

onMounted(() => {
  showElement.value = true;
});
</script>
<template>
  <transition
    @enter="enterAnimation"
    @leave="leaveAnimation"
    name="component-tansition">
    <div ref="el" v-if="showElement">
      <slot></slot>
    </div>
  </transition>
</template>
