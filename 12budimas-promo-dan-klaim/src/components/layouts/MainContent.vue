<script setup>
import { computed, ref, watchEffect } from "vue";
import { useRoute, useRouter } from "vue-router";
import SlideRightX from "../animation/SlideRightX.vue";

const route = useRoute();
const router = useRouter();

const routeName = ref(route.path);

watchEffect(() => (routeName.value = route.path));
const beforeRoute = computed(() => {
    const routeArr = routeName.value.split("/").filter(val => val !== "" && isNaN(parseInt(val)))
    if(routeArr.length === 1) routeArr.unshift("home")
    return routeArr.slice(-2)[0]?.split("-").join(" ")
  }
);
const afterRoute = computed(() => {
   const routerArr = routeName.value.split("/").filter(val => val !== "" && isNaN(parseInt(val)))
   return routerArr.slice(-2)[routerArr.length == 1 ? 0 : 1]?.split("-").join(" ")
  }
);
const routePathLength = computed(() => routeName.value.split("/").length);
const loginRoute = computed(() => route.name === "Login");
</script>

<template>
  <div
    class="tw-w-full tw-flex tw-flex-col tw-gap-3 tw-mt-8 lg:tw-pl-4 lg:tw-pr-4 tw-pl-4 tw-pr-0"
  >
    <div
      v-if="!loginRoute"
      class="tw-w-full tw-flex lg:tw-flex-row tw-flex-col tw-justify-between lg:tw-px-6 tw-px-1 tw-gap-2"
    >
      <SlideRightX
        :duration-enter="0.2"
        :duration-leave="0.2"
        class="tw-font-bold lg:tw-text-xl tw-text-md tw-text-slate-700 tw-flex tw-flex-row lg:tw-gap-4 tw-gap-4 tw-items-center tw-capitalize"
      >
        <BButton
          @click="router.back()"
          v-if="routePathLength > 2"
          class="tw-bg-[#DF8F44] tw-border-none tw-h-8 lg:tw-h-auto"
          size="sm"
        >
          <i class="mdi mdi-step-backward tw-mr-1"></i>
          Kembali
        </BButton>
        <span>{{ route.name }}</span>
      </SlideRightX>
      <SlideRightX
        :duration-enter="0.3"
        :duration-leave="0.3"
        class="tw-flex tw-items-center tw-gap-2 tw-text-xs"
      >
        <span class="tw-text-gray-500 tw-capitalize">
          {{ beforeRoute }}
        </span>
        <i class="mdi mdi-chevron-right tw-text-lg"></i>
        <span class="tw-text-blue-500 tw-capitalize">
          {{ afterRoute }}
        </span>
      </SlideRightX>
    </div>
    <slot></slot>
  </div>
</template>
