<script setup>
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";

import Table from "@/src/components/ui/table/Table.vue";
import StatusBar from "@/src/components/ui/StatusBar.vue";

import { currentDate } from "@/src/lib/date";
import { useKepalaCabang } from "@/src/store/kepalaCabang";
import { useShipping } from "@/src/store/shipping";
import { onMounted, ref, computed } from "vue";
import { revisiFakturCol } from "@/src/model/tableColumns";

const kepalaCabang = useKepalaCabang();
const shipping = useShipping();
const tableKey = ref(0);
const tableLoading = ref(true);
const tableData = ref([]);

const getResource = async () => {
  const res = await shipping.getListRuteRevisiFaktur(
    kepalaCabang.kepalaCabangUser.id_cabang
  );
  tableData.value = res;
  tableKey.value++;
  tableLoading.value = false;
};
const namaCabang = computed(() => {
  return (
    kepalaCabang.kepalaCabangUser?.kepalaCabang?.nama_cabang ||
    kepalaCabang.kepalaCabangUser?.nama_cabang ||
    "-"
  );
});

onMounted(() => {
  getResource();
});
</script>

<template>
  <div class="tw-flex tw-flex-col tw-gap-4 lg:tw-px-4 tw-px- tw-min-h-[80vh]">
    <SlideRightX
      class=""
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-out="0.1"
      :delay-in="0.1"
      :initial-x="-40"
      :x="40">
      <Card :no-subheader="true" class="tw-mb-6">
        <template #header>Cabang</template>
        <template #content>
          <div class="status-field-container-2-col">
            <StatusBar
              label="Cabang :"
              :value="namaCabang" />
            <StatusBar label="Tanggal :" :value="currentDate" />
          </div>
        </template>
      </Card>
      <Card :no-subheader="true" class="tw-mb-6">
        <template #header>List Rute dan Armada</template>
        <template #content>
          <div class="tw-w-full tw-py-16">
            <Table
              :key="tableKey"
              :table-data="tableData"
              :columns="revisiFakturCol"
              :loading="tableLoading" />
          </div>
        </template>
      </Card>
    </SlideRightX>
  </div>
</template>
