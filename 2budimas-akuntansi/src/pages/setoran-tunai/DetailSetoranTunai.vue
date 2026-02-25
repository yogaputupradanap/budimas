<script setup>
import FlexBox from '@/src/components/ui/FlexBox.vue';
import SlideRightX from '@/src/components/animation/SlideRightX.vue';
import Card from '@/src/components/ui/Card.vue';
import Skeleton from '@/src/components/ui/Skeleton.vue';
import Label from '@/src/components/ui/Label.vue';
import {$swal} from '@/src/components/ui/SweetAlert.vue';
import {onMounted, ref} from 'vue';
import {fetchWithAuth, formatCurrencyAuto} from "@/src/lib/utils";
import {useRoute, useRouter} from "vue-router";
import Button from "@/src/components/ui/Button.vue";
import Table from "@/src/components/ui/table/Table.vue";
import {listSetoranDetailTunai} from "@/src/model/tableColumns/setoran-tunai/listDetailSetoranTunai";

const loadingData = ref(false)
const loadingDataFaktur = ref(false);
const loadingProses = ref(false);
const route = useRoute()
const router = useRouter()
const tableRef = ref(null);
const data = ref([]);
const dataDetail = ref({
  jumlah_customer: 0,
  total_setoran: 0,
  nama_kasir: 0
});

const getResource = async () => {
  try {
    const response = await fetchWithAuth(
        "GET",
        `/api/akuntansi/get-detail-setoran-tunai/${route.params.nama_pj}/${route.params.draft_tanggal_input}`,
    );
    const dataTemp = response.data;
    data.value = dataTemp.list_setoran
    dataDetail.value = dataTemp.detail_setoran

  } catch (error) {
    console.error("Error fetching data:", error);
    $swal.error(
        "Terjadi kesalahan saat mengambil data detail setoran non tunai. Silakan coba lagi.",
    )
  }
};

const handleKonfirmasi = async () => {

  const confirm = await $swal.confirm(
      "Apakah Anda yakin ingin mengkonfirmasi setoran ini?",
  )

  if (!confirm) {
    return;
  }

  try {
    const response = await fetchWithAuth(
        "POST",
        `/api/akuntansi/konfirmasi-setoran-tunai`,
        {
          nama_pj: route.params.nama_pj,
          draft_tanggal_input: route.params.draft_tanggal_input,
        }
    );

    $swal.success(response.message);
    router.replace('/setoran-tunai');
    data.value = [];
  } catch (error) {
    console.error("Error confirming deposit:", error);
    $swal.error(
        error || "Terjadi kesalahan saat mengkonfirmasi setoran tunai. Silakan coba lagi.",
    );
  }
};

onMounted(
    () => {
      getResource();
    }
)

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
        :x="40">
      <Card no-subheader>
        <template #header>Informasi Piutang</template>
        <template #content>
          <div class="form-grid-card-5-col">
            <Label label="Nama PJ">
              <Skeleton v-if="loadingData" class="skeleton"/>
              <BFormInput
                  v-else
                  :model-value="route.params.nama_pj"
                  disabled/>
            </Label>
            <Label label="Jumlah Customer">
              <Skeleton v-if="loadingData" class="skeleton"/>
              <BFormInput
                  v-else
                  :model-value="dataDetail.jumlah_customer"
                  disabled/>
            </Label>
            <Label label="Total Setoran">
              <Skeleton v-if="loadingData" class="skeleton"/>
              <BFormInput
                  v-else
                  :model-value="formatCurrencyAuto(dataDetail.total_setoran)"
                  disabled/>
            </Label>
            <Label label="Tanggal Setor">
              <Skeleton v-if="loadingData" class="skeleton"/>
              <BFormInput
                  v-else
                  :model-value="route.params.draft_tanggal_input"
                  disabled/>
            </Label>
            <Label label="Nama Kasir">
              <Skeleton v-if="loadingData" class="skeleton"/>
              <BFormInput
                  v-else
                  :model-value="dataDetail.nama_kasir"
                  disabled/>
            </Label>
          </div>
        </template>
      </Card>
    </SlideRightX>
    <SlideRightX
        class="slide-container tw-z-10"
        :duration-enter="0.6"
        :duration-leave="0.6"
        :delay-in="0.1"
        :delay-out="0.1"
        :initial-x="-40"
        :x="40">
      <Card no-subheader>
        <template #header>List Setoran Customer</template>
        <template #content>
          <Table
              :key="data.length"
              ref="tableRef"
              :table-data="data"
              :loading="loadingData"
              :columns="listSetoranDetailTunai"/>
          <FlexBox full jusEnd class="tw-mt-4">
            <Button
                class="tw-w-32"
                :loading="loadingProses"
                icon="mdi mdi-check"
                :trigger="handleKonfirmasi"
            >
              Konfirmasi
            </Button>
          </FlexBox>
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>
