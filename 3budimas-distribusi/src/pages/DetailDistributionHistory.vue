<script setup>
import Table from "../components/ui/table/Table.vue";
import { tableDistribusiHistoryDetail } from "../model/tableColumns";
import StatusBar from "../components/ui/StatusBar.vue";
import SlideRightX from "../components/animation/SlideRightX.vue";
import Card from "../components/ui/Card.vue";
import { useHistory } from "../store/history";
import { useRoute } from "vue-router";
import { getDateNow } from "../lib/utils";
import { ref, onMounted, computed } from "vue";
import { useKepalaCabang } from "../store/kepalaCabang";

const user = useKepalaCabang();
const history = useHistory();
const router = useRoute();
const currHistory = ref();
const idCabang = user?.kepalaCabangUser?.id_cabang;
const idRute = router?.params?.id_rute;
const tableKey = ref(0);
const isNotaProsesEmpty = computed(checkIsNotaProsesEmpty);
const isNotaTerkirimEmpty = computed(checkIsNotaTerkirimEmpty);
const isNotaGagalEmpty = computed(checkIsNotaGagalEmpty);

function checkIsNotaProsesEmpty() {
  return history?.listNotaProses?.listNota?.length;
}

function checkIsNotaTerkirimEmpty() {
  return history?.listNotaTerkirim?.listNota?.length;
}

function checkIsNotaGagalEmpty() {
  return history?.listNotagagal?.listNota?.length;
}

const NotaProses = computed(() => history?.listNotaProses?.listNota);
const NotaGagal = computed(() => history?.listNotagagal?.listNota);
const NotaTerkirim = computed(() => history?.listNotaTerkirim?.listNota);

const getResource = async () => {
  if (!history?.listRuteHistory?.listRute?.length) {
    await history.getRuteList(idCabang);
    await history.getAllNota(idCabang, idRute);
    tableKey.value++;
  }

  currHistory.value = history?.listRuteHistory?.listRute?.find(
    (val) => val.id_rute == router?.params?.id_rute
  );
};

onMounted(() => getResource());
</script>

<template>
  <div class="tw-flex tw-flex-col tw-gap-4 lg:tw-px-4 tw-px-0">
    <SlideRightX
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.1"
      :delay-out="0.1"
      :initial-x="-40"
      :x="40">
      <Card :no-subheader="true">
        <template #header>Detail Histori Distribusi</template>
        <template #content>
          <div class="status-field-container-4-col tw-pb-10">
            <StatusBar label="Kode Rute :" :value="currHistory?.kode || ''" />
            <StatusBar label="Rute :" :value="currHistory?.nama_rute || ''" />
            <StatusBar
              label="Tanggal Distribusi :"
              :value="getDateNow(new Date(), false)" />
          </div>
        </template>
      </Card>
    </SlideRightX>
    <SlideRightX
      v-if="isNotaGagalEmpty"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.2"
      :delay-out="0.2"
      :initial-x="-40"
      :x="40">
      <Card :no-subheader="true" class="tw-mt-5">
        <template #header>Nota Gagal</template>
        <template #content>
          <Table
            :key="tableKey"
            :table-data="NotaGagal"
            :columns="tableDistribusiHistoryDetail" />
        </template>
      </Card>
    </SlideRightX>
    <SlideRightX
      v-if="isNotaTerkirimEmpty"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.3"
      :delay-out="0.3"
      :initial-x="-40"
      :x="40">
      <Card :no-subheader="true" class="tw-mt-5">
        <template #header>Nota Terkirim</template>
        <template #content>
          <Table
            :key="tableKey"
            :table-data="NotaTerkirim"
            :columns="tableDistribusiHistoryDetail" />
        </template>
      </Card>
    </SlideRightX>
    <SlideRightX
      v-if="isNotaProsesEmpty"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.4"
      :delay-out="0.4"
      :initial-x="-40"
      :x="40">
      <Card :no-subheader="true" class="tw-mt-5">
        <template #header>Nota Proses</template>
        <template #content>
          <Table
            :key="tableKey"
            :table-data="NotaProses"
            :columns="tableDistribusiHistoryDetail" />
        </template>
      </Card>
    </SlideRightX>
  </div>
</template>
