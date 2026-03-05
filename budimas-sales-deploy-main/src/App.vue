<script setup>
import { RouterView, useRoute } from "vue-router";
import Layout from "./components/layouts/Layout.vue";
import { localDisk, sessionDisk } from "./lib/utils";
import { useSales } from "./store/sales";
import { onMounted, watch } from "vue";
import { useDashboard } from "./store/dashboard";
import { useKunjungan } from "./store/kunjungan";
import { Toaster } from "vue-sonner";

const sales = useSales();
const dashboard = useDashboard();
const kunjungan = useKunjungan();
const router = useRoute();

onMounted(async () => {
  const user = sessionDisk.getSession("authUser");
  const storeList = ["dashboard", "activeKunjungan", "principal", "user", "active-buttons"];

  if (!user) return localDisk.removeLocalStorage(storeList);

  if (!sales.salesUser) {
    sales.getSales(user.id_sales);
  }

  await kunjungan.createKunjungan(user.id_user);
  await dashboard.getDashboardInfo(user.id_user);

  sales.deactivateLoading();
  dashboard.deactivateLoading();
  dashboard.initActiveButton();
});

watch(
  router,
  () => {
    if (!router.name) return;

    const title = router.name[0].toUpperCase() + router.name.substring(1);
    document.title = `${title} | Budimas Sales`;
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
