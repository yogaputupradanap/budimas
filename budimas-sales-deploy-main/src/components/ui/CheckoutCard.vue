<script setup>
import { defineProps, ref } from "vue";
import { useRouter } from "vue-router";
import Loader from "./Loader.vue";

const props = defineProps({
  icon: {
    type: String,
    default: "mdi-logout-variant",
  },
  text: {
    type: String,
    default: "Check Out",
  },
  full: Boolean,
  trigger: Function,
  replaceUrl: String,
  active: {
    type: Boolean,
    default: true,
  },
});

const router = useRouter();
const loading = ref(false);

const handleClick = async () => {
  if (!props.active) return;

  if (props.trigger) {
    loading.value = true;
    await props.trigger();
    loading.value = false;
    return;
  }

  if (props.replaceUrl) {
    return router.replace(props.replaceUrl);
  }
};
</script>

<template>
  <div
    @click="handleClick"
    class="tw-h-48 lg:tw-min-h-[200px] tw-flex tw-flex-col tw-justify-center tw-items-center tw-gap-2 tw-px-6 tw-py-8 tw-rounded-lg tw-duration-300 tw-ease-out tw-cursor-pointer tw-w-full lg:tw-w-[206px]"
    :style="{
      backgroundColor: active ? '#BD2727' : '#E0A0A0',
      color: 'white',
      opacity: active ? '1' : '0.7',
      pointerEvents: active ? 'auto' : 'none',
      cursor: active ? 'pointer' : 'not-allowed',
    }">
    <i :class="['mdi tw-text-6xl', icon]" v-if="!loading"></i>
    <Loader v-else />
    <span class="tw-text-lg tw-font-semibold tw-text-center">{{ text }}</span>
  </div>
</template>
