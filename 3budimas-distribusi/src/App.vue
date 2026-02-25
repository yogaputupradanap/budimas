<script setup>
import {RouterView, useRoute} from "vue-router";
import Layout from "./components/layouts/Layout.vue";
import {localDisk, sessionDisk} from "./lib/utils";
import {onMounted, watch} from "vue";
import {useKepalaCabang} from "./store/kepalaCabang";
import {Toaster} from "vue-sonner";
import {useCustomer} from "@/src/store/customer";
import {useListRute} from "@/src/store/listRute";

const kepalaCabang = useKepalaCabang();
const router = useRoute();
const customerStore = useCustomer();
const ruteStore = useListRute()


onMounted(async () => {
  const user = sessionDisk.getSession("authUser_distribusi");
  const storeList = [
    "user_distribusi",
    "add_picking",
    "detail_picking",
    "rute_shipping",
    "faktur_shipping",
    "detail_shipping",
    "",
  ];

  if (!user) return localDisk.removeLocalStorage(storeList);

  if (!kepalaCabang.kepalaCabangUser) {
    await kepalaCabang.getKepalaCabang(user.id_user);
  }
  customerStore.getCustomer()
  console.log(user)
  ruteStore.fetchSOD(user.id_cabang)
});

watch(
    router,
    () => {
      if (!router.name) return;

      const title = router.name[0].toUpperCase() + router.name.substring(1);
      document.title = `${title} | Budimas Distribusi`;
    },
    {immediate: true}
);
</script>

<template>
  <Layout>
    <Toaster rich-colors close-button position="top-right" expand/>
    <RouterView v-slot="{ Component }">
      <component :is="Component"/>
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
