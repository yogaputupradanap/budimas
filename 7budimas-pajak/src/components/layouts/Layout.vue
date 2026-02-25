<script setup>
import MainHeader from './header/MainHeader.vue'
import MainSidebar from './sidebar/MainSidebar.vue'
import MainContent from "./MainContent.vue";
import { useRoute } from "vue-router";
import { computed, ref, watchEffect } from "vue";

const currentYear = new Date().getFullYear();
const route = useRoute();
const routeName = ref(route.name);
const loginRoute = computed(() => routeName.value === "Login");

watchEffect(() => (routeName.value = route.name));
</script>

<template>
  <div class="tw-w-full tw-flex tw-justify-start tw-items-start tw-gap-0">
    <!-- sidebar/left content -->
    <MainSidebar v-if="!loginRoute" />
    <!-- right content -->
    <div
      class="tw-w-full tw-h-fit tw-min-h-screen tw-flex tw-flex-col tw-gap-0 tw-bg-background"
    >
      <!-- header -->
      <MainHeader v-if="!loginRoute" />
      <!-- main content -->
      <main
        class="tw-w-full tw-flex tw-flex-col tw-items-center lg:tw-pr-6 tw-pr-5"
      >
        <MainContent>
          <slot></slot>
        </MainContent>
        <footer
          v-if="!loginRoute"
          class="tw-flex tw-justify-center tw-items-center tw-p-4 tw-text-center tw-text-[0.8rem] lg:tw-text-[0.9rem] tw-mt-8 tw-select-none"
        >
          <div class="mb-2">
            Copyright&copy;
            {{ currentYear }}
            PT. BUDIMAS MAKMUR MULIA
            <br />
            Designed and Developed by
            <a
              class="tw-text-blue-500"
              href="https://www.horus.co.id"
              target="_blank"
            >
              HORUS TECHNOLOGY
            </a>
          </div>
        </footer>
      </main>
    </div>
  </div>
</template>
