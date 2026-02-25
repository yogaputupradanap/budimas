<script setup>
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import { listEskalasiColumn } from "@/src/model/tableColumns/listEskalasi/listEskalasi";
import Table from "@/src/components/ui/table/Table.vue";
import { useListEskalasi } from "@/src/store/mainStore";
import { onMounted } from "vue";

const stockTransfer = useListEskalasi();
const getListEskalasi = () => {
  stockTransfer.getStockTransfer(
    "eskalasi",
    [
      "id_stock_transfer",
      "nota_stock_transfer",
      "created_at",
      "id_cabang_awal",
      "id_cabang_tujuan",
      "nama_cabang_awal",
      "nama_cabang_tujuan",
      "jumlah_picked",
      "id_armada",
      "jumlah",
      "pengambilan_oleh",
      "tanggal_ambil",
      "status",
      "tanggal_diterima"
    ],
    "id_cabang_tujuan"
  );
};

onMounted(() => getListEskalasi());
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
        <template #header>List Eskalasi Stock Transfer</template>
        <template #content>
          <Table
            :key="stockTransfer.stockTransfer.key"
            :loading="stockTransfer.stockTransfer.loading"
            :columns="listEskalasiColumn"
            :table-data="stockTransfer.stockTransfer.list" />
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>
