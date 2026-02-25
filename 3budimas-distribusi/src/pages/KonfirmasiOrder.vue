<script setup>
import SlideRightX from "../components/animation/SlideRightX.vue";
import Card from "../components/ui/Card.vue";
import Table from "../components/ui/table/Table.vue";
import { onBeforeMount, onMounted, ref, watchEffect } from "vue";
import { useRouter, useRoute } from "vue-router";
import { listOrderVerifikasi } from "../model/tableColumns";
import { useOrder } from "../store/order";
import { useKepalaCabang } from "../store/kepalaCabang";

const LOCALSTORAGEPAGINATION = "Pagination_Order_Konfirmasi";

const router = useRouter(); const route = useRoute();
const order = useOrder();
const user = useKepalaCabang();
const idCabang = ref(user?.kepalaCabangUser?.id_cabang);
const tableKey = ref(0);

const getResource = async () => {
  await order.getListOrder(idCabang.value, true);
  tableKey.value++;
};

watchEffect(() => {
  if (idCabang.value) {
    getResource();
  }
});

function onPageChange(p){
  localStorage.setItem(LOCALSTORAGEPAGINATION, JSON.stringify(p));
}

onMounted(() => {
  // localStorage.setItem("Pagination_Order_Konfirmasi", JSON.stringify({pageIndex:0,pageSize:10}))
});
</script>

<template>
  <div class="tw-flex tw-flex-col tw-gap-4 lg:tw-px-4 tw-px-0 tw-min-h-[80vh]">
    <SlideRightX :duration-enter="0.6" :duration-leave="0.6" :delay-in="0.2" :delay-out="0.2" :initial-x="-40" :x="40">
      <Card :no-subheader="true">
        <template #header>List Order</template>
        <template #content>
          <div class="tw-w-full tw-flex tw-flex-col tw-py-8 tw-pb-16">
            <div>
              <Table :loading="order.loading" :key="tableKey" :table-data="order?.listOrder || []"
                :columns="listOrderVerifikasi" :key-local-storage="LOCALSTORAGEPAGINATION" @refreshData="getResource" @paginationChange="onPageChange" />
            </div>
          </div>
        </template>
      </Card>
    </SlideRightX>
  </div>
</template>
