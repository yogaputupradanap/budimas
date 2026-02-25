<script setup>
import SlideRightX from "../components/animation/SlideRightX.vue";
import Card from "../components/ui/Card.vue";
import Table from "../components/ui/table/Table.vue";
import StatusBar from "../components/ui/StatusBar.vue";

import { fakturRealisasi } from "../model/tableColumns";
import { useShipping } from "../store/shipping";
import { useRoute } from "vue-router";
import { useKepalaCabang } from "../store/kepalaCabang";
import { onMounted, ref, computed } from "vue";

const shipping = useShipping();
const kepalaCabang = useKepalaCabang();
const router = useRoute();
const tableKey = ref(0);
const fakturInfo = ref({});
const idCabang = kepalaCabang.kepalaCabangUser.id_cabang;
const idRute = router.params.id_rute;
const idArmada = router.query.id_armada;
const idDriver = router.query.id_driver;
const deliveringDate = router.query.delivering_date;

const getResource = async () => {
  fakturInfo.value = shipping.listRuteShipping.ruteShipping.find((val) => val.id_rute == router.params.id_rute);
  await shipping.getListFakturShipping(idCabang, idRute, true, idArmada, idDriver, deliveringDate);
  tableKey.value++;
};

const namaCabang = computed(() => {
  return (
    kepalaCabang.kepalaCabangUser?.kepalaCabang?.nama_cabang ||
    kepalaCabang.kepalaCabangUser?.nama_cabang ||
    "-"
  );
});
onMounted(async () => {
  getResource();
});
</script>

<template>
  <div class="tw-flex tw-flex-col tw-gap-4 lg:tw-px-4 tw-px-0">
    <SlideRightX class="" :duration-enter="0.6" :duration-leave="0.6" :delay-in="0.2" :delay-out="0.2" :initial-x="-40" :x="40">
      <Card :no-subheader="true">
        <template #header>Daftar Faktur</template>
        <template #content>
          <div class="tw-w-full tw-grid tw-grid-cols-1 md:tw-grid-cols-4 tw-gap-4 tw-mb-5">
            <StatusBar label="Cabang :" :value="namaCabang" />
            <StatusBar label="Rute :" :value="fakturInfo?.nama_rute || ''" />
            <StatusBar label="Jumlah Toko :" :value="String(fakturInfo?.jumlah_toko || '')" />
            <StatusBar label="Jumlah Nota :" :value="String(fakturInfo?.jumlah_nota || '')" />
          </div>
          <div class="tw-w-full tw-grid tw-grid-cols-1 md:tw-grid-cols-4 tw-gap-4 tw-mb-5">
            <StatusBar label="Armada :" :value="fakturInfo?.nama_armada || ''" />
            <StatusBar label="Driver :" :value="fakturInfo?.nama_driver || ''" />
          </div>
        </template>
      </Card>
      <Card :no-subheader="true" class="tw-mt-10">
        <template #header>List Faktur Realisasi</template>
        <template #content>
          <div class="tw-w-full tw-pb-12">
            <Table :key="tableKey" :loading="shipping.listFakturShipping.loading" :table-data="shipping.listFakturShipping.fakturShipping" :columns="fakturRealisasi" />
          </div>
        </template>
      </Card>
    </SlideRightX>
  </div>
</template>
