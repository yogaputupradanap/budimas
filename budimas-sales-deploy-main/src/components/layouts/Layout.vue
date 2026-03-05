<!-- eslint-disable vue/multi-word-component-names -->
<script setup>
import SideBar from "./SideBar.vue";
import Header from "./Header.vue";
import MainContent from "./MainContent.vue";
const currentYear = new Date().getFullYear();
import { useRoute } from "vue-router";
import { computed, ref, watchEffect } from "vue";

const route = useRoute();
const routeName = ref(route.name);
watchEffect(() => (routeName.value = route.name));
const loginRoute = computed(() => routeName.value === "Login");
</script>

<template>
  <div class="tw-w-full tw-flex tw-justify-start tw-items-start tw-gap-0">
    <!-- sidebar/left content -->
    <SideBar v-if="!loginRoute" />
    <!-- right content -->
    <div
      class="tw-w-full tw-h-auto tw-min-h-screen tw-flex tw-flex-col tw-gap-0 tw-bg-blue-100"
    >
      <!-- header -->
      <Header v-if="!loginRoute" />
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
