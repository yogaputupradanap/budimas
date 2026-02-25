<script setup>
import SlideRightX from "../components/animation/SlideRightX.vue";
import Card from "../components/ui/Card.vue";
import Table from "../components/ui/table/Table.vue";
import StatusBar from "../components/ui/StatusBar.vue";

import { tableListShipping } from "../model/tableColumns";
import { currentDate } from "../lib/date";
import { useKepalaCabang } from "../store/kepalaCabang";
import { useShipping } from "../store/shipping";
import { ref, computed, watch } from "vue";

// const kepalaCabang = useKepalaCabang();
const shipping = useShipping();

const tableKey = ref(0);

// const idCabang = computed(() => kepalaCabang.kepalaCabangUser?.id_cabang);
const user = useKepalaCabang();

/*
  Ambil id cabang secara reactive dari store
*/
const idCabang = computed(() => user.kepalaCabangUser?.id_cabang);

/*
  Nama cabang (aman dari undefined)
*/
const namaCabang = computed(() => {
  return (
    user.kepalaCabangUser?.kepalaCabang?.nama_cabang ||
    user.kepalaCabangUser?.nama_cabang ||
    "-"
  );
});

watch(
  idCabang,
  async (val) => {
    if (!val) return;

    await shipping.getListRuteShipping(val);
    tableKey.value++;
  },
  { immediate: true }
);
</script>

<template>
  <div class="tw-flex tw-flex-col tw-gap-4 lg:tw-px-4 tw-min-h-[80vh]">
    <SlideRightX
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-out="0.1"
      :delay-in="0.1"
      :initial-x="-40"
      :x="40"
    >
      <Card :no-subheader="true" class="tw-mb-6">
        <template #header>Cabang</template>
        <template #content>
          <div class="status-field-container-2-col">
            <StatusBar
              label="Cabang :"
              :value="namaCabang || '-'"
            />
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
              :table-data="shipping.listRuteShipping?.ruteShipping || []"
              :columns="tableListShipping"
              :loading="shipping.listRuteShipping.loading"
            />
          </div>
        </template>
      </Card>
    </SlideRightX>
  </div>
</template>
