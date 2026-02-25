<script setup>
import SlideRightX from "../components/animation/SlideRightX.vue";
import Card from "../components/ui/Card.vue";
import Skeleton from "../components/ui/Skeleton.vue";

import Table from "../components/ui/table/Table.vue";
import { ref, watchEffect } from "vue";

import { tableOrderDistribusi } from "../model/tableColumns";
import { useOrder } from "../store/order";
import { useKepalaCabang } from "../store/kepalaCabang";

const order = useOrder();
const user = useKepalaCabang();
const idCabang = ref(user?.kepalaCabangUser?.id_cabang);
const tableKey = ref(0);

const getResource = async () => {
  await order.getListOrder(idCabang.value);
  tableKey.value++;
};

watchEffect(() => {
  if (idCabang.value) {
      getResource();
    }
})
</script>

<template>
  <div class="tw-flex tw-flex-col tw-gap-4 lg:tw-px-4 tw-px-0 tw-min-h-[80vh]">
    <SlideRightX
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.2"
      :delay-out="0.2"
      :initial-x="-40"
      :x="40">
      <Card :no-subheader="true">
        <template #header>List Order</template>
        <template #content>
          <div class="tw-w-full tw-flex tw-flex-col tw-py-8">
            <div
              class="tw-text-m tw-flex tw-flex-row tw-gap-4 tw-mb-3 tw-mt-[-10px] tw-ml-4">
              Last Update :
              <Skeleton class="tw-w-48 tw-h-6" v-if="order.loading" />
              <p v-else>
                {{ order.lastUpdate }}
              </p>
            </div>
            <div>
              <Table
                :loading="order.loading"
                :key="tableKey"
                :table-data="order?.listOrder || []"
                :columns="tableOrderDistribusi" />
            </div>
          </div>
        </template>
      </Card>
    </SlideRightX>
  </div>
</template>
