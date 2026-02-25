<script setup>
import SlideRightX from "../components/animation/SlideRightX.vue";
import Card from "../components/ui/Card.vue";
import { ref, onMounted } from "vue";
import { apiUrl, fetchWithAuth } from "../lib/utils";
import { useKepalaCabang } from "../store/kepalaCabang";

import Table from "../components/ui/table/Table.vue";
import { tableRuteDanArmada } from "../model/tableColumns";

const listRuteDanArmada = ref([]);
const columns = tableRuteDanArmada(listRuteDanArmada);

const tableKey = ref(0);
const kepalaCabang = useKepalaCabang();
const idCabang = kepalaCabang.kepalaCabangUser.id_cabang;
const isLoading = ref(null);

const getResource = async () => {
  try {
    const id = `id=${idCabang}`;

    isLoading.value = true;
    const response = await fetchWithAuth(
      "GET",
      `${apiUrl}/api/distribusi/get-rute-armada?${id}`
    );
    listRuteDanArmada.value = response;
    tableKey.value++;
    isLoading.value = false;
  } catch (error) {
    console.error("Error fetching data:", error);
  }
};

onMounted(() => {
  getResource();
});
</script>

<template>
  <div class="tw-flex tw-flex-col tw-gap-4 lg:tw-px-4 tw-px-0 tw-min-h-[80vh]">
    <SlideRightX
      class=""
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.2"
      :delay-out="0.2"
      :initial-x="-40"
      :x="40">
      <Card :no-subheader="true" class="tw-mb-6 tw-pb-12">
        <template #header>List Rute dan Armada</template>
        <template #content>
          <Table
            :loading="isLoading"
            :table-data="listRuteDanArmada"
            :columns="columns"
            :key="tableKey" />
        </template>
      </Card>
    </SlideRightX>
  </div>
</template>
