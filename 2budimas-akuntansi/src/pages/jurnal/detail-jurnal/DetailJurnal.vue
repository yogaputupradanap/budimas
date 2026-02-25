<script setup>
import FlexBox from "@/src/components/ui/FlexBox.vue";
import {useRoute} from "vue-router";
import {onMounted, ref} from "vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import Table from "@/src/components/ui/table/Table.vue";
import {
  listDetailJurnalColumn,
  listDetailJurnalKeteranganIdFiturMal1,
  listDetailJurnalKeteranganIdFiturMal10,
  listDetailJurnalKeteranganIdFiturMal12,
  listDetailJurnalKeteranganIdFiturMal13,
  listDetailJurnalKeteranganIdFiturMal14,
  listDetailJurnalKeteranganIdFiturMal16,
  listDetailJurnalKeteranganIdFiturMal17,
  listDetailJurnalKeteranganIdFiturMal18,
  listDetailJurnalKeteranganIdFiturMal19,
  listDetailJurnalKeteranganIdFiturMal2,
  listDetailJurnalKeteranganIdFiturMal20,
  listDetailJurnalKeteranganIdFiturMal21,
  listDetailJurnalKeteranganIdFiturMal22,
  listDetailJurnalKeteranganIdFiturMal23,
  listDetailJurnalKeteranganIdFiturMal3,
  listDetailJurnalKeteranganIdFiturMal4,
  listDetailJurnalKeteranganIdFiturMal5,
  listDetailJurnalKeteranganIdFiturMal6,
  listDetailJurnalKeteranganIdFiturMal7,
  listDetailJurnalKeteranganIdFiturMal8,
  listDetailJurnalKeteranganIdFiturMal9
} from "@/src/model/tableColumns/jurnal/detail-jurnal/detailJurnal";
import {jurnalService} from "@/src/services/jurnal";
import Label from "@/src/components/ui/Label.vue";
import TextField from "@/src/components/ui/formInput/TextField.vue";


const route = useRoute();
const id_jurnal = ref(route.params.id_jurnal);
const detailData = ref({
  tanggal: "",
  nama_perusahaan: "",
  keterangan_detail: "",
  id_fitur_mal: null,
  nama_cabang: "",
  jenis_transaksi: "",
  created_by: "",
  info_jurnal: [],
});
const loading = ref(false);
const getKeteranganColumns = (id) => {
  const mapping = {
    1: listDetailJurnalKeteranganIdFiturMal1,
    2: listDetailJurnalKeteranganIdFiturMal2,
    3: listDetailJurnalKeteranganIdFiturMal3,
    4: listDetailJurnalKeteranganIdFiturMal4,
    5: listDetailJurnalKeteranganIdFiturMal5,
    6: listDetailJurnalKeteranganIdFiturMal6,
    7: listDetailJurnalKeteranganIdFiturMal7,
    8: listDetailJurnalKeteranganIdFiturMal8,
    9: listDetailJurnalKeteranganIdFiturMal9,
    10: listDetailJurnalKeteranganIdFiturMal10,
    12: listDetailJurnalKeteranganIdFiturMal12,
    13: listDetailJurnalKeteranganIdFiturMal13,
    14: listDetailJurnalKeteranganIdFiturMal14,
    16: listDetailJurnalKeteranganIdFiturMal16,
    17: listDetailJurnalKeteranganIdFiturMal17,
    18: listDetailJurnalKeteranganIdFiturMal18,
    19: listDetailJurnalKeteranganIdFiturMal19,
    20: listDetailJurnalKeteranganIdFiturMal20,
    21: listDetailJurnalKeteranganIdFiturMal21,
    22: listDetailJurnalKeteranganIdFiturMal22,
    23: listDetailJurnalKeteranganIdFiturMal23
  };
  return mapping[id] || [];
};

const getDetailJurnal = async () => {
  try {
    loading.value = true;
    detailData.value = await jurnalService.detailJurnal(id_jurnal.value);
    detailData.value.tanggal = new Date(detailData.value.tanggal).toISOString().split("T")[0];
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
        class="slide-container tw-z-10"
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
          <div class="form-grid-card tw-items-end">
            <Label label="Tanggal">
              <TextField class="tw-w-full" v-model="detailData.tanggal" :disable="true"/>
            </Label>
            <Label label="Perusahaan">
              <TextField class="tw-w-full" v-model="detailData.nama_perusahaan" :disable="true"/>
            </Label>
            <Label label="Cabang">
              <TextField class="tw-w-full" v-model="detailData.nama_cabang" :disable="true"/>
            </Label>
            <Label label="Transaksi">
              <TextField class="tw-w-full" v-model="detailData.jenis_transaksi" :disable="true"/>
            </Label>
            <Label label="User">
              <TextField class="tw-w-full" v-model="detailData.created_by" :disable="true"/>
            </Label>
          </div>
          <Table
              :key="detailData"
              :columns="listDetailJurnalColumn"
              :table-data="detailData.info_jurnal"
              :show-search="false"
              :loading="loading"
          />
          <!-- ✅ Bagian refactor dimulai di sini -->
          <template v-if="Array.isArray(detailData.keterangan_detail)">
            <div class="tw-mt-6 tw-mb-2 tw-px-4 tw-w-full tw-text-start">
              <h1>Keterangan</h1>
            </div>

            <Table
                :key="detailData.keterangan_detail"
                :columns="getKeteranganColumns(detailData.id_fitur_mal)"
                :table-data="detailData.keterangan_detail"
                :show-search="false"
                :loading="loading"
            />
          </template>

          <template v-else>
            <div class="tw-w-full tw-flex tw-items-start tw-flex-col tw-justify-start">
              <div class="tw-mt-6 tw-mb-2 tw-px-4 tw-w-full tw-text-start">
                <h1>Keterangan</h1>
              </div>
              <div class="tw-px-4 tw-w-full tw-pb-4">
        <textarea
            class="tw-w-full tw-border tw-border-gray-300 tw-rounded-md tw-p-2 tw-resize-none"
            rows="4"
            :value="detailData.keterangan_detail"
            disabled>
        </textarea>
              </div>
            </div>
          </template>
          <!-- ✅ Bagian refactor selesai -->
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>
