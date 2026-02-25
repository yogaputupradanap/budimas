<script setup>
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import Table from "@/src/components/ui/table/Table.vue";
import { listPengajuanStockTransferColumn } from "@/src/model/tableColumns/konfirmasi/listPengajuanTransfer";
import { onMounted } from "vue";
import { useKonfirmasi } from "@/src/store/mainStore";

const stockTransfer = useKonfirmasi();
const getStockTransfer = () => {
  stockTransfer.getStockTransfer(["request", "konfirmasi"]);
};

onMounted(() => getStockTransfer());
</script>

<template>
  <FlexBox full flex-col>
    <SlideRightX
      class="slide-container"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.1"
      :delay-out="0.1"
      :initial-x="-40"
      :x="40">
      <Card no-subheader>
        <template #header>List Pengajuan Stock Transfer</template>
        <template #content>
          <Table
            :key="stockTransfer.stockTransfer.key"
            :loading="stockTransfer.stockTransfer.loading"
            :columns="listPengajuanStockTransferColumn"
            :table-data="stockTransfer.stockTransfer.list" />
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>
