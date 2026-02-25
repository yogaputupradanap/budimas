<script setup>
import { RouterView } from "vue-router";
import Layout from "./components/layouts/Layout.vue";
import { localDisk, sessionDisk } from "./lib/utils";
import { onMounted, watch } from "vue";
import { useRoute } from "vue-router";
import { useOthers } from "./store/others";
import { useUser } from "./store/user";
import { Toaster } from "vue-sonner";

const userStore = useUser();
const router = useRoute();
const others = useOthers();

const handleFirstPaintPage = async () => {
  const user = sessionDisk.getSession("authUser");
  const storeList = [
    "user",
    "generate-faktur",
    "list-nomor-pajak",
    "add-faktur-pajak",
    "list-pajak",
    "hakakses",
  ];

  if (!user) return localDisk.removeLocalStorage(storeList);

  if (!userStore.user.value) {
    await userStore.getUserInfo(user.id_user);
  }

  console.log("test");
  await others.getOthers();
};

const watchTitle = () => {
  if (!router.name) return;

  const title = router.name[0].toUpperCase() + router.name.substring(1);
  document.title = `${title} | Faktur Pajak`;
};

onMounted(() => {
  handleFirstPaintPage();
});

watch(
  router,
  () => {
    watchTitle();
  },
  { immediate: true }
);
</script>

<template>
  <Layout>
    <Toaster rich-colors close-button position="top-right" expand />
    <RouterView v-slot="{ Component }">
      <component :is="Component" />
    </RouterView>
  </Layout>
</template>

<style lang="scss">
.dp__theme_light {
  --dp-background-color: #fff;
  --dp-text-color: #212121;
  --dp-hover-color: #f3f3f3;
  --dp-hover-text-color: #212121;
  --dp-hover-icon-color: #959595;
  --dp-primary-color: #1976d2;
  --dp-primary-disabled-color: #6bacea;
  --dp-primary-text-color: #f8f5f5;
  --dp-secondary-color: #c0c4cc;
  --dp-border-color: #7e7e7e;
  --dp-menu-border-color: #ddd;
  --dp-border-color-hover: #aaaeb7;
  --dp-border-color-focus: #aaaeb7;
  --dp-disabled-color: #f6f6f6;
  --dp-scroll-bar-background: #f3f3f3;
  --dp-scroll-bar-color: #959595;
  --dp-success-color: #76d275;
  --dp-success-color-disabled: #a3d9b1;
  --dp-icon-color: #535353;
  --dp-danger-color: #ff6f60;
  --dp-marker-color: #ff6f60;
  --dp-tooltip-color: #fafafa;
  --dp-disabled-color-text: #8e8e8e;
  --dp-highlight-color: rgb(25 118 210 / 10%);
  --dp-range-between-dates-background-color: var(--dp-hover-color, #f3f3f3);
  --dp-range-between-dates-text-color: var(--dp-hover-text-color, #212121);
  --dp-range-between-border-color: var(--dp-hover-color, #f3f3f3);
}
.make-z-hight {
  z-index: -99 !important;
}
</style>
