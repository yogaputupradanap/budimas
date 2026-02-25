<script setup>
import SlideRightX from "../components/animation/SlideRightX.vue";
import Card from "../components/ui/Card.vue";
import SelectInput from "../components/ui/formInput/SelectInput.vue";
import StatusBar from "../components/ui/StatusBar.vue";
import {apiUrl, fetchWithAuth} from "../lib/utils";
import {useRoute, useRouter} from "vue-router";
import {useKepalaCabang} from "../store/kepalaCabang";
import VueDatePicker from "@vuepic/vue-datepicker";
import {computed, inject, onMounted, ref} from "vue";
import Skeleton from "../components/ui/Skeleton.vue";
import Button from "../components/ui/Button.vue";
import {useAlert} from "../store/alert";
import {useArmada} from "../store/armada.js";
import {useDriver} from "../store/driver";
import {fakturJadwalColumn} from "../model/tableColumns/fakturJadwalColumn.js";
import Table from "../components/ui/table/Table.vue";

// Initialize services & stores
const $swal = inject("$swal");
const route = useRoute();
const router = useRouter();
const alert = useAlert();
const armadaStore = useArmada();
const driverStore = useDriver();
const kepalaCabang = useKepalaCabang();

// State variables
const idRute = route.params.id_rute;
const idCabang = kepalaCabang.kepalaCabangUser.id_cabang;
const selectedArmada = ref("");
const selectedDriver = ref("");
const tanggalPengiriman = ref(null);
const listFakturJadwal = ref([]);
const tableKey = ref(0);
const isLoading = ref(null);
const tableRef = ref(null);
const columns = fakturJadwalColumn(listFakturJadwal);

// Computed properties
const formattedArmadaOptions = computed(() => {
  return armadaStore.armada.list.map((item) => ({
    ...item,
    namaDisplay: `${item.nama} - [${item.kubikasi || 0} CBM]`,
  }));
});

const selectedFakturData = computed(() => {
  if (!tableRef.value) return [];

  const selectedRows = tableRef.value.getSelectedRow();
  return Object.keys(selectedRows).map((index) => {
    const row = listFakturJadwal.value[parseInt(index)];
    return {
      id_sales_order: row.id_sales_order,
      estimasi_kubikasi: parseFloat(row.estimasi_kubikasi) || 0,
    };
  });
});

const selectedArmadaData = computed(() => {
  return armadaStore.armada.list.find(
    (item) => item.id == selectedArmada.value
  );
});

const selectedArmadaKubikasi = computed(() => {
  return parseFloat(selectedArmadaData.value?.kubikasi || 0);
});

const totalEstimasiKubikasi = computed(() => {
  return selectedFakturData.value.reduce(
    (total, item) => total + item.estimasi_kubikasi,
    0
  );
});

const isKubikasiValid = computed(() => {
  return totalEstimasiKubikasi.value <= selectedArmadaKubikasi.value;
});

// Initialize default values when data is available
const handleSod = () => {
  const armadaInfoList = armadaStore.infoArmada.list;

  if (armadaStore.armada.list.length > 0) {
    selectedArmada.value = armadaInfoList[0].id_armada;
    selectedDriver.value = armadaInfoList[0].id_driver;
    tanggalPengiriman.value = armadaInfoList[0].tanggal_pengiriman;
  } else {
    const errorMessage = "Error: No data returned from the API";
    console.error(errorMessage);
    $swal.error(errorMessage);
  }
};

// Form submission handler
const handleSubmit = async () => {
  // Validasi input dasar
  if (!tanggalPengiriman.value) {
    $swal.error("Pilih tanggal pengiriman terlebih dahulu");
    return;
  }
  if (!selectedArmada.value) {
    $swal.error("Pilih armada terlebih dahulu");
    return;
  }
  if (!selectedDriver.value) {
    $swal.error("Pilih driver terlebih dahulu");
    return;
  }

  // Jika tidak ada data yang dipilih, tampilkan pesan alert
  if (selectedFakturData.value.length === 0) {
    $swal.error("Pilih setidaknya satu faktur dari tabel");
    return;
  }

  // Validasi kubikasi
  if (!isKubikasiValid.value) {
    $swal.error(
      `Total estimasi kubikasi (${totalEstimasiKubikasi.value}) melebihi kapasitas armada (${selectedArmadaKubikasi.value}). Silakan pilih faktur yang lebih sedikit atau armada dengan kapasitas lebih besar.`
    );
    return;
  }

  // Persiapkan data untuk submit
  const id_sales_orders = selectedFakturData.value.map(
    (item) => item.id_sales_order
  ).flat();
  const body = {
    id_sales_orders,
    id_driver: selectedDriver.value,
    id_armada: selectedArmada.value,
    tanggal_pengiriman: tanggalPengiriman.value,
  };

  try {
    // Konfirmasi dan submit
    const isConfirmed = await $swal.confirmSubmit(
      "Apakah anda yakin ingin menjadwalkan armada ini?"
    );

    if (!isConfirmed) return;

    await fetchWithAuth("POST", `${apiUrl}/api/distribusi/update`, body);
    $swal.success("Berhasil menjadwalkan armada!");
    router.go(-2);
  } catch (error) {
    console.error("Error submitting data:", error);
    $swal.error(error);
  }
};

// Data fetching methods
const getResource = async () => {
  await Promise.all([
    armadaStore.getDistribusi(idCabang, idRute),
    armadaStore.getAllArmada(idCabang),
  ]);

  if (!driverStore.driver.list.length) {
    await driverStore.getAllDriver(idCabang);
  }

  handleSod();
};

const getFakturJadwal = async () => {
  try {
    isLoading.value = true;
    const response = await fetchWithAuth(
      "GET",
      `${apiUrl}/api/distribusi/get-list-faktur-jadwal?id_cabang=${idCabang}&id_rute=${idRute}`
    );
    listFakturJadwal.value = response;
    tableKey.value++;
  } catch (error) {
    console.error("Error fetching data:", error);
  } finally {
    isLoading.value = false;
  }
};

// Lifecycle hooks
onMounted(async () => {
  isLoading.value = true;
  await getResource();
  await getFakturJadwal();
});
</script>

<template>
  <div class="tw-flex tw-flex-col tw-gap-4 lg:tw-px-4 tw-px-0">
    <SlideRightX
      class=""
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.2"
      :delay-out="0.2"
      :initial-x="-40"
      :x="40">
      <Card :no-subheader="true" class="tw-mb-6">
        <template #header>{{ "Data Jadwal & Rute" }}</template>
        <template #content>
          <div
            class="tw-w-full tw-grid tw-grid-cols-1 md:tw-grid-cols-4 tw-mb-5 tw-gap-2">
            <div class="tw-flex tw-flex-col tw-gap-2">
              <span>Tanggal :</span>
              <Skeleton
                v-if="armadaStore.infoArmada.loading"
                class="tw-w-full tw-h-10" />
              <VueDatePicker
                v-else
                v-model="tanggalPengiriman"
                :enable-time-picker="false"
                placeholder="mm/dd/yyyy"
                :teleport="true"
                auto-apply />
            </div>
            <StatusBar
              :loading="armadaStore.infoArmada.loading"
              label="Cabang :"
              :value="
                kepalaCabang.kepalaCabangUser?.kepalaCabang?.nama_cabang || ''
              " />
            <StatusBar
              :loading="armadaStore.infoArmada.loading"
              label="Kode Rute :"
              :value="armadaStore.infoArmada.list[0]?.kode_rute || ''" />
            <StatusBar
              :loading="armadaStore.infoArmada.loading"
              label="Rute :"
              :value="armadaStore.infoArmada.list[0]?.nama_rute" />
          </div>
          <div
            class="tw-w-full tw-grid tw-grid-cols-1 md:tw-grid-cols-4 tw-mb-5 tw-gap-2">
            <StatusBar
              :loading="armadaStore.infoArmada.loading"
              label="Jumlah Toko :"
              :value="String(armadaStore.infoArmada.list[0]?.jumlah_toko)" />
            <StatusBar
              :loading="armadaStore.infoArmada.loading"
              label="Jumlah Nota :"
              :value="String(armadaStore.infoArmada.list[0]?.jumlah_nota)" />
            <StatusBar
              :loading="armadaStore.infoArmada.loading"
              label="Jumlah Kubikal :"
              :value="String(armadaStore.infoArmada.list[0]?.jumlah_kubikal)" />
          </div>
        </template>
      </Card>
      <Card :no-subheader="true" class="tw-mb-6">
        <template #header>{{ "Pilih Armada & Driver" }}</template>
        <template #content>
          <!-- Table dengan loading state -->
          <div v-if="isLoading" class="tw-mb-4">
            <Skeleton class="tw-w-full tw-h-[300px]" />
          </div>
          <Table
            v-else
            ref="tableRef"
            :loading="isLoading"
            :table-data="listFakturJadwal"
            :columns="columns"
            :key="tableKey" />

          <!-- Form inputs dan button -->
          <div
            class="tw-w-full tw-grid tw-grid-cols-1 md:tw-grid-cols-4 tw-gap-4 md:tw-gap-2 tw-pb-16">
            <!-- Armada Selection -->
            <div class="tw-flex tw-flex-col">
              <Skeleton
                v-if="armadaStore.infoArmada.loading || isLoading"
                class="tw-h-10" />
              <div v-else class="tw-flex tw-flex-col">
                <p class="tw-mb-1">Armada :</p>
                <SelectInput
                  :options="formattedArmadaOptions"
                  v-model="selectedArmada"
                  size="sm"
                  textField="namaDisplay"
                  valueField="id"
                  class="tw-w-full tw-h-[40px]" />

                <!-- Informasi kubikasi -->
                <div
                  v-if="
                    selectedArmada && tableRef && selectedFakturData.length > 0
                  "
                  class="tw-mt-2 tw-text-xs tw-font-medium tw-p-2 tw-rounded"
                  :class="{
                    'tw-bg-red-50 tw-text-red-700': !isKubikasiValid,
                    'tw-bg-green-50 tw-text-green-700': isKubikasiValid,
                  }">
                  <div class="tw-flex tw-gap-1 tw-items-center">
                    <i
                      :class="
                        isKubikasiValid
                          ? 'mdi mdi-check-circle'
                          : 'mdi mdi-alert-circle'
                      "
                      class="tw-text-base"></i>
                    <span>
                      Estimasi: {{ totalEstimasiKubikasi.toFixed(2) }} CBM /
                      Kapasitas: {{ selectedArmadaKubikasi }} CBM
                    </span>
                  </div>
                  <div v-if="!isKubikasiValid" class="tw-mt-1 tw-font-bold">
                    Melebihi kapasitas armada!
                  </div>
                </div>
              </div>
            </div>

            <!-- Driver Selection -->
            <div class="tw-flex tw-flex-col md:tw-mt-0">
              <Skeleton
                v-if="armadaStore.infoArmada.loading || isLoading"
                class="tw-h-10" />
              <div v-else class="tw-flex tw-flex-col">
                <p class="tw-mb-1">Pilih Driver :</p>
                <SelectInput
                  :options="driverStore.driver.list"
                  v-model="selectedDriver"
                  size="sm"
                  textField="nama"
                  valueField="id"
                  class="tw-w-full tw-h-[40px]" />
              </div>
            </div>

            <!-- Spacer untuk MD dan ukuran lebih besar -->
            <div class="tw-hidden md:tw-block"></div>

            <!-- Submit Button -->
            <div class="tw-flex tw-items-end md:tw-justify-end">
              <Skeleton
                v-if="armadaStore.infoArmada.loading || isLoading"
                class="tw-w-32 tw-h-10" />
              <Button
                v-else
                class="tw-h-10 md:tw-w-32 tw-w-full"
                :class="{
                  'tw-bg-green-500 hover:tw-bg-green-600':
                    isKubikasiValid || !selectedFakturData.length,
                }"
                :disabled="!selectedFakturData.length || !isKubikasiValid"
                :trigger="handleSubmit"
                icon="mdi mdi-check">
                Submit
              </Button>
            </div>
          </div>
        </template>
      </Card>
    </SlideRightX>
  </div>
</template>
