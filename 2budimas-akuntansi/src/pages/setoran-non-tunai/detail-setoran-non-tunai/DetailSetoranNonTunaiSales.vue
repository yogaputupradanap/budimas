<script setup>
import FlexBox from '@/src/components/ui/FlexBox.vue';
import SlideRightX from '@/src/components/animation/SlideRightX.vue';
import Card from '@/src/components/ui/Card.vue';
import Skeleton from '@/src/components/ui/Skeleton.vue';
import Label from '@/src/components/ui/Label.vue';
import {$swal} from '@/src/components/ui/SweetAlert.vue';
import {computed, onMounted, ref} from 'vue';
import SelectInput from "@/src/components/ui/formInput/SelectInput.vue";
import {useOthers} from "@/src/store/others";
import {fetchWithAuth, formatCurrencyAuto} from "@/src/lib/utils";
import {useRoute, useRouter} from "vue-router";
import Button from "@/src/components/ui/Button.vue";
import {useUser} from "@/src/store/user";
import Table from "@/src/components/ui/table/Table.vue";
import {listFakturNonTunaiSales} from "@/src/model/tableColumns/setoran-non-tunai/listFakturNonTunai";
import Modal from "@/src/components/ui/Modal.vue";

const others = useOthers()
const user = useUser()
const loadingData = ref(false)
const loadingDataFaktur = ref(false);
const loadingProses = ref(false);
const loadingDataModal = ref(false);
const route = useRoute()
const router = useRouter()
const selectedSales = ref(null);
const tableRef = ref(null);
const dataFaktur = ref([]);
const formUseCN = ref(null);
const clientKey = ref(0);
const creditNoteOptions = ref([])
const selectedCN = ref(null);
const selectedFaktur = ref(null);
const selectedPrincipal = ref(null);
const selectedNominalCNFormat = computed(
    () => {
      const data = selectedCN.value;
      if (data) {
        const dataSelected = creditNoteOptions.value.find(
            (item) => item.id_cn === data
        );
        return dataSelected ? formatCurrencyAuto(dataSelected.total_cn) : 0;
      } else {
        return 0;
      }
    }
);
const data = ref({
  kode_mutasi: '',
  nominal_mutasi: '',
  tanggal_setor: new Date().toISOString().split('T')[0],
  nama: '',
  nama_auditor: '',
  total_retur: 0,
});

const totalSetoran = computed(() => {
  if (typeof tableRef.value?.getSelectedRow !== 'function') {
    return 0;
  }

  const selectedRows = tableRef.value?.getSelectedRow();
  if (!selectedRows || typeof selectedRows !== 'object') {
    return 0;
  }

  if (Object.keys(selectedRows).length === 0) {
    return 0;
  }

  const selectedValues = dataFaktur.value.filter(
      (_, index) => selectedRows[index]
  ) || [];

  return selectedValues.reduce((total, item) => {
    return total + item.jumlah_setoran
  }, 0);


});

const totalRetur = computed(() => {
  if (typeof tableRef.value?.getSelectedRow !== 'function') {
    return 0;
  }

  const selectedRows = tableRef.value?.getSelectedRow();
  if (!selectedRows || typeof selectedRows !== 'object') {
    return 0;
  }

  if (Object.keys(selectedRows).length === 0) {
    return 0;
  }

  const selectedValues = dataFaktur.value.filter(
      (_, index) => selectedRows[index]
  ) || [];

  return selectedValues.reduce((total, item) => {
    return total + parseFloat(item.total_retur ? item.total_retur : 0);
  }, 0);


});

const getResource = async () => {
  try {
    const response = await fetchWithAuth(
        "GET",
        `/api/akuntansi/get-detail-setoran-nontunai/${route.params.id_mutasi}`,
    );

    data.value = {
      ...response.data,
      nominal_mutasi: response.data.sisa ? response.data.sisa : response.data.nominal_mutasi,
      format_nominal_mutasi: formatCurrencyAuto(response.data.sisa ? response.data.sisa : response.data.nominal_mutasi),
      nama_auditor: user.user.value.nama,
      tanggal_setor: new Date().toISOString().split('T')[0],
    };

  } catch (error) {
    console.error("Error fetching data:", error);
    $swal.error(
        "Terjadi kesalahan saat mengambil data detail setoran non tunai. Silakan coba lagi.",
    )
  }
};

const getResourceFaktur = async () => {
  if (!selectedSales.value) {
    $swal.error("Pilih Customer terlebih dahulu");
    return;
  }
  
  try {
    const response = await fetchWithAuth(
      "GET",
      `/api/akuntansi/get-list-faktur-setoran/sales?id_sales=${selectedSales.value}`,
    );

    // DEBUG: Cek struktur aslinya di console
    console.log("Raw Response Faktur:", response);

    if (response && response.data) {
      /**
       * PERBAIKAN:
       * Cek apakah datanya ada di response.data.result (seperti pola sebelumnya)
       * Jika tidak ada, coba response.data (sebagai array)
       */
      const rawData = response.data.result || response.data;
      
      // Pastikan hasil akhirnya adalah Array
      dataFaktur.value = Array.isArray(rawData) ? rawData : [];
      
      console.log("Data Faktur yang disimpan ke state:", dataFaktur.value);
    } else {
      dataFaktur.value = [];
      console.warn("API response sukses tapi data kosong");
    }

  } catch (error) {
    console.error("Error fetching data:", error);
    $swal.error(
      "Terjadi kesalahan saat mengambil data faktur non tunai. Silakan coba lagi.",
    );
  } finally {
    // Memastikan tabel refresh dengan key baru
    clientKey.value++;
  }
};

const handleKonfirmasi = async () => {
  if (!selectedSales.value) {
    $swal.error("Pilih Sales terlebih dahulu");
    return;
  }

  if (totalSetoran.value <= 0) {
    $swal.error("Total setoran tidak boleh kurang dari atau sama dengan nol");
    return;
  }

  const selectedRows = tableRef.value?.getSelectedRow();
  if (!selectedRows || Object.keys(selectedRows).length === 0) {
    $swal.error("Pilih setoran yang ingin dikonfirmasi");
    return;
  }

  const selectedValues = dataFaktur.value.filter(
      (_, index) => selectedRows[index]
  ).sort(
      (a, b) => a.tanggal_jatuh_tempo.localeCompare(b.tanggal_jatuh_tempo)
  );

  let totalMutasi = data.value.nominal_mutasi;

  if (totalMutasi !== totalSetoran.value) {
    $swal.error(
        `Total setoran tidak sesuai dengan total mutasi. Total Mutasi: ${formatCurrencyAuto(totalMutasi)}, Total Setoran: ${formatCurrencyAuto(totalSetoran.value)}`
    );
    return;
  }

  const confirm = await $swal.confirm(
      "Apakah Anda yakin ingin mengkonfirmasi setoran ini?",
  )

  if (!confirm) {
    return;
  }

  try {
    const response = await fetchWithAuth(
        "POST",
        `/api/akuntansi/insert-setoran-konfirmasi-non-tunai/sales/${route.params.id_mutasi}`,
        {
          id_sales:  selectedSales.value,
          data_faktur: selectedValues,
        }
    );

    $swal.success(response.message);
    router.replace('/setoran-non-tunai');
    dataFaktur.value = [];
    selectedSales.value = null
  } catch (error) {
    console.error("Error confirming deposit:", error);
    $swal.error(
        error || "Terjadi kesalahan saat mengkonfirmasi setoran non tunai. Silakan coba lagi.",
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
    <Modal ref="formUseCN" id="formUseCN" size="xl" :centered="true">
      <SlideRightX
          :duration-enter="0.3"
          :duration-leave="0.3"
          :delay-in="0.1"
          :delay-out="0.1"
          :initial-x="-20"
          :x="20">
        <Card no-subheader>
          <template #header>
            <div class="tw-flex tw-justify-between tw-items-center">
              <span>Aktivasi Credit Note</span>
            </div>
          </template>
          <template #content>
            <div class="tw-space-y-4 tw-w-full">
              <Label label="Pilih Credit Note">
                <Skeleton v-if="loadingDataModal" class="skeleton"/>
                <SelectInput
                    v-else
                    v-model="selectedCN"
                    placeholder="Pilih Nominal Credit Note"
                    size="md"
                    :search="true"
                    :options="creditNoteOptions"
                    :virtual-scroll="true"
                    text-field="kode_cn"
                    value-field="id_cn"/>
              </Label>
              <Label label="Principal">
                <Skeleton v-if="loadingDataModal" class="skeleton"/>
                <BFormInput
                    v-else
                    :model-value="selectedPrincipal"
                    disabled/>
              </Label>
              <Label label="Nominal Credit Notel">
                <Skeleton v-if="loadingDataModal" class="skeleton"/>
                <BFormInput
                    v-else
                    :model-value="selectedNominalCNFormat"
                    disabled/>
              </Label>
              <div class="tw-mt-4 tw-flex tw-gap-4 tw-justify-end">
                <Button
                    :loading="loadingDataModal"
                    :trigger="() => formUseCN.hide()"
                    icon="mdi mdi-close"
                    class="tw-h-[38px] tw-w-auto tw-px-6 tw-bg-gray-500 hover:tw-bg-gray-600">
                  Batal
                </Button>
                <Button
                    :loading="loadingDataModal"
                    :trigger="submitAddCn"
                    :disabled="!selectedCN"
                    icon="mdi mdi-check"
                    class="tw-h-[38px] tw-w-auto tw-px-6 tw-bg-green-500 hover:tw-bg-green-600">
                  Submit
                </Button>
              </div>
            </div>
          </template>
        </Card>
      </SlideRightX>
    </Modal>
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
          <div class="form-grid-card">
            <Label label="Kode Mutasi">
              <Skeleton v-if="loadingData" class="skeleton"/>
              <BFormInput
                  v-else
                  :model-value="data.kode_mutasi"
                  disabled/>
            </Label>
            <Label label="Nominal Mutasi">
              <Skeleton v-if="loadingData" class="skeleton"/>
              <BFormInput
                  v-else
                  :model-value="data.format_nominal_mutasi"
                  disabled/>
            </Label>
            <Label label="Sales">
              <Skeleton v-if="others.sales.loading" class="skeleton"/>
              <SelectInput
                  v-else
                  v-model="selectedSales"
                  placeholder="Pilih Data"
                  size="md"
                  virtual-scroll="true"
                  :search="true"
                  :options="others.sales.list"
                  text-field="nama"
                  value-field="id"/>
            </Label>
            <Label label="Total Setoran">
              <Skeleton v-if="loadingData" class="skeleton"/>
              <BFormInput
                  v-else
                  :model-value="formatCurrencyAuto(totalSetoran)"
                  disabled/>
            </Label>
            <Label label="Tanggal Setor">
              <Skeleton v-if="loadingData" class="skeleton"/>
              <BFormInput
                  v-else
                  :model-value="data.tanggal_setor"
                  disabled/>
            </Label>
            <Label label="Nama Kasir">
              <Skeleton v-if="loadingData" class="skeleton"/>
              <BFormInput
                  v-else
                  :model-value="data.nama"
                  disabled/>
            </Label>
            <Label label="Nama Auditor">
              <Skeleton v-if="loadingData" class="skeleton"/>
              <BFormInput
                  v-else
                  :model-value="data.nama_auditor"
                  disabled/>
            </Label>
            <Label label="Total Retur">
              <Skeleton v-if="loadingData" class="skeleton"/>
              <BFormInput
                  v-else
                  :model-value="formatCurrencyAuto(totalRetur)"
                  disabled/>
            </Label>
          </div>
          <FlexBox full jusEnd class="tw-mt-4">
            <Button
                class="tw-w-32"
                :loading="loadingDataFaktur"
                icon="mdi mdi-magnify"
                :trigger="getResourceFaktur"
            >
              Cari
            </Button>
          </FlexBox>
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
              :key="dataFaktur.length"
              ref="tableRef"
              :table-data="dataFaktur"
              :loading="loadingDataFaktur"
              :columns="listFakturNonTunaiSales"/>
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
