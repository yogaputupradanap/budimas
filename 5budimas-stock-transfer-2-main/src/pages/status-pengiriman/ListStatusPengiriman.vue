<script setup>
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import { listStatusPengirimanColumn } from "@/src/model/tableColumns/status-pengiriman/listStatusPengiriman";
import Table from "@/src/components/ui/table/Table.vue";
import { onMounted } from "vue";
import { useStatusPengiriman } from "@/src/store/mainStore";

const stockTransfer = useStatusPengiriman();
const getPengiriman = () => {
  stockTransfer.getStockTransfer(null);
};

onMounted(() => getPengiriman());
</script>

<template>
  <FlexBox full flex-col>
    <SlideRightX
      class="slide-container"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.2"
      :delay-out="0.1"
      :initial-x="-40"
      :x="40">
      <Card no-subheader>
        <template #header>List Status Pengiriman Stock Transfer</template>
        <template #content>
          <Table
            :loading="stockTransfer.stockTransfer.loading"
            :key="stockTransfer.stockTransfer.key"
            :columns="listStatusPengirimanColumn"
            :table-data="stockTransfer.stockTransfer.list" />
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>
