<script setup>
import FlexBox from "@/src/components/ui/FlexBox.vue";
import { useRoute } from "vue-router";
import { ref, onMounted } from "vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import Table from "@/src/components/ui/table/Table.vue";
import { listDetailJurnalColumn } from "@/src/model/tableColumns/jurnal/detail-jurnal/detailJurnal";
import { jurnalService } from "@/src/services/jurnal";

const route = useRoute();
const id_jurnal = ref(route.params.id_jurnal);
const detailData = ref([]);
const loading = ref(false);

const getDetailJurnal = async () => {
  try {
    loading.value = true;
    detailData.value = await jurnalService.detailJurnal(id_jurnal.value);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  getDetailJurnal();
});
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
      :x="40"
    >
      <Card no-subheader>
        <template #header>Detail Jurnal</template>
        <template #content>
          <Table
            :key="detailData"
            :columns="listDetailJurnalColumn"
            :table-data="detailData"
            :show-search="false"
            :loading="loading"
            table-width="tw-w-[100vw]"
          />
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>
