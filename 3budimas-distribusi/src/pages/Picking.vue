<script setup>
import SlideRightX from "../components/animation/SlideRightX.vue";
import Card from "../components/ui/Card.vue";
import Table from "../components/ui/table/Table.vue";
import StatusBar from "../components/ui/StatusBar.vue";
import { ref, computed, watch, watchEffect, onMounted } from "vue";
import { tableListPicking } from "../model/tableColumns";
import { currentDate } from "../lib/date";
import { usePicking } from "../store/picking";
import { useKepalaCabang } from "../store/kepalaCabang";

const tableKey = ref(0);
const picking = usePicking();
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

/*
  Fetch data saat idCabang tersedia
*/
watch(
  idCabang,
  async (val) => {
    if (!val) return;

    await picking.getRutePicking(val);
    tableKey.value++;
  },
  { immediate: true }
);

/*
  Debug store
*/
// watchEffect(() => {
//   console.log("kepalaCabangUser:", user.kepalaCabangUser);
//   console.log("API USER:", user.kepalaCabangUser);
// });

/*
  Load user cabang dari localStorage / API
*/
onMounted(async () => {
  if (!user.kepalaCabangUser?.id_cabang) {
    // ganti ID sesuai kebutuhan (misalnya dari auth)
    await user.getKepalaCabang(5);
  }
});
</script>

<template>
  <div class="tw-flex tw-flex-col tw-gap-4 lg:tw-px-4 tw-px-0 tw-min-h-[80vh]">
    <SlideRightX
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-out="0.1"
      :delay-in="0.1"
      :initial-x="-40"
      :x="40"
    >
      <Card :no-subheader="true">
        <template #header>Cabang</template>
        <template #content>
          <div class="status-field-container-2-col">
            <StatusBar label="Cabang :" :value="namaCabang" />
            <StatusBar label="Tanggal :" :value="currentDate" />
          </div>
        </template>
      </Card>
    </SlideRightX>

    <SlideRightX
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.2"
      :delay-out="0.2"
      :initial-x="-40"
      :x="40"
    >
      <Card :no-subheader="true">
        <template #header>List Rute</template>
        <template #content>
          <div class="tw-w-full tw-pb-10">
            <Table
              :loading="picking.listPicking.loading"
              :table-data="picking.listPicking.rutePicking || []"
              :columns="tableListPicking"
              :key="tableKey"
            />
          </div>
        </template>
      </Card>
    </SlideRightX>
  </div>
</template>
