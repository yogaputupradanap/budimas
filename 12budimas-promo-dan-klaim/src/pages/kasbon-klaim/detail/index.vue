<script setup>
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import Label from "@/src/components/ui/Label.vue";
import Button from "@/src/components/ui/Button.vue";
import Table from "@/src/components/ui/table/Table.vue";
import { BFormInput } from "bootstrap-vue-next";
import { ref, onMounted, computed, inject} from "vue";
import { kasbonKlaimDetailColumn } from "@/src/model/tableColumns/kasbon-klaim/detail/index";
import { promoService } from "@/src/services/promo";
import { parseCurrency } from "@/src/lib/utils";
import { useRoute } from "vue-router";
import { useUser } from "@/src/store/user";

const route = useRoute();
const user = useUser();
const $swal = inject("$swal");

const userId = ref(user?.user?.value?.id || null);
const kasbonId = route.params.id;
const selectedKlaimIds = ref([]);
const klaimList = ref([]);
const kasbonData = ref(null);
const tableRef = ref(null);

const isLoading = ref(false);
const dataLoading = ref(true);

const klaimData = computed(() => {
  return Array.isArray(klaimList.value) ? klaimList.value : [];
});

const fetchKasbonData = async () => {
  try {
    const response = await promoService.getKasbonKlaimDetail(kasbonId);
    kasbonData.value = response.data || response;
  } catch (error) {
    console.error('Error fetching kasbon data:', error);
    $swal.error('Gagal memuat data kasbon klaim');
  }
};

const fetchKlaimList = async () => {
  try {
    const response = await promoService.getListKlaimForKasbonKlaim(kasbonId);
    const data = (response?.pages && Array.isArray(response.pages) && response.pages) ||
      (response?.data && Array.isArray(response.data) && response.data) ||
      (Array.isArray(response) && response) ||
      [];

    klaimList.value = data;
  } catch (error) {
    console.error('Error fetching klaim list:', error);
    $swal.error('Gagal memuat list klaim');
    klaimList.value = [];
  }
};

const handleConfirmKlaim = async () => {
  const selectedRows = tableRef.value?.getSelectedRow() || {};
  const selectedIds = Object.keys(selectedRows).map(id => parseInt(id, 10));

  if (selectedIds.length === 0) {
    $swal.warning('Pilih minimal satu klaim untuk dikonfirmasi');
    return;
  }

  const klaimTerpilih = klaimData.value.filter(item => selectedIds.includes(item.id));
  const klaimText = klaimTerpilih.map(value => `${value.kode_promo}`);

  const result = await $swal.confirm(
    `Apakah Anda yakin ingin mengkonfirmasi klaim terpilih?
    \nDetail Klaim: [${klaimText}]`
  );
  if (result) {
    confirmKlaim(selectedIds);
  }
};

const confirmKlaim = async (ids) => {
  try {
    isLoading.value = true;
    
    await promoService.konfirmasiDetailKasbonKlaim(kasbonId, {
      selectedKlaimIds: ids,
      id_user_approval: userId.value
    });
    
    await $swal.success('Berhasil mengkonfirmasi klaim!');
    selectedKlaimIds.value = [];
    await fetchKasbonData();
    await fetchKlaimList();
  } catch (error) {
    console.error('Error confirming klaim:', error);
    await $swal.error('Terjadi kesalahan saat konfirmasi klaim');
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  dataLoading.value = true;
  if(!kasbonId) return;
  try {
    fetchKasbonData();
    fetchKlaimList();
  } catch (error) {
    console.error('Error during onMounted:', error);
  } finally {
    dataLoading.value = false;
  }
})
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
        <template #header>Detail Kasbon Klaim</template>
        <template #content>
          <div class="tw-grid tw-grid-cols-3 form-grid-card">
           <Label label="Kode Kasbon Klaim">
              <BFormInput
                :model-value="kasbonData?.kode_kasbon_klaim"
                :class="'tw-bg-gray-200'"
                readonly
              />
            </Label>
            <Label label="Principal">
              <BFormInput
                :model-value="kasbonData?.principal"
                :class="'tw-bg-gray-200'"
                readonly
              />
            </Label>
            <Label label="Tanggal Kasbon">
              <BFormInput
                :model-value="kasbonData?.tanggal_pengajuan"
                :class="'tw-bg-gray-200'"
                readonly
              />
            </Label>
            <Label label="Nominal Kasbon">
              <BFormInput
                :model-value="parseCurrency(kasbonData?.nominal_kasbon_diajukan)"
                :class="'tw-bg-gray-200'"
                readonly
              />
            </Label>
            <Label label="Nominal Kasbon Ditangguhkan">
              <BFormInput
                :model-value="parseCurrency(kasbonData?.nominal_kasbon_disetujui)"
                :class="'tw-bg-gray-200'"
                readonly
              />
            </Label>
          </div>
        </template>
      </Card>
      <Card no-subheader class="tw-mt-4">
        <template #header>List Klaim</template>
        <template #content>
          <Table
            ref="tableRef"
            :tableData="klaimData"
            :columns="kasbonKlaimDetailColumn"
            :loading="dataLoading"
          />
          <FlexBox full jusEnd>
            <Button
              class="tw-mt-4 tw-px-4 tw-p-2"
              variant="primary"
              :trigger="handleConfirmKlaim"
              :loading="isLoading"
            >
              <i class="mdi mdi-check tw-mr-2"></i>
              Konfirmasi Klaim
            </Button>
          </FlexBox>
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>
