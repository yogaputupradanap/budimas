<script setup>
import SlideRightX from "../components/animation/SlideRightX.vue";
import FlexBox from "../components/ui/FlexBox.vue";
import Card from "../components/ui/Card.vue";
import TextField from "../components/ui/formInput/TextField.vue";
import { apiUrl, dateNow, fetchWithAuth, formatCurrencyAuto, getCompactTimestamp } from "../lib/utils";
import { computed, inject, onMounted, ref } from "vue";
import Table from "../components/ui/table/Table.vue";
import { useSales } from "../store/sales";
import { useAlert } from "../store/alert";
import { listRekapPembayaran } from "../model/tableColumns";
import Button from "../components/ui/Button.vue";
import FIleInput from "../components/ui/formInput/FIleInput.vue";

const dataTable = ref([]);
const loadingTable = ref(false);
const tanggal = ref(dateNow());
const buktiTransfer = ref(null);
const sales = useSales();
const id_sales = sales.salesUser.sales.id;
const namaSales = sales.salesUser.nama;
const alert = useAlert();
const $swal = inject("$swal");
const fileInputKey = ref(0);

// Computed untuk total setoran tunai
const totalSetoranTunai = computed(() => {
  return dataTable.value.reduce((total, row) => {
    return total + (row.tunai || 0);
  }, 0);
});

// Computed untuk total setoran non tunai
const totalSetoranNonTunai = computed(() => {
  return dataTable.value.reduce((total, row) => {
    return total + (row.non_tunai || 0);
  }, 0);
});

// Computed untuk total setoran keseluruhan
const totalSetoran = computed(() => {
  return totalSetoranTunai.value + totalSetoranNonTunai.value;
});

const getResource = async () => {
  try {
    loadingTable.value = true;
    const res = await fetchWithAuth(
      "GET",
      `${apiUrl}/api/finance/rekap-pembayaran-sales?id_sales=${id_sales}`
    );

    // Initialize data dengan default values
    const rawData = res.data || res;
    dataTable.value = rawData.map((row) => ({
      ...row,
      tunai: row.tunai || 0,
      non_tunai: row.non_tunai || row.jumlah_setoran || 0
    }));
  } catch (error) {
    alert.setMessage(error, "danger");
  } finally {
    loadingTable.value = false;
  }
};

const onSubmit = async () => {
  try {
    if (!dataTable.value.length) {
      alert.setMessage("Tidak ada data untuk disubmit", "warning");
      return;
    }

    // Check validation state dan data
    const hasInvalidData = dataTable.value.some(
      (row) => row.tunai > row.jumlah_setoran || row.hasError
    );

    if (hasInvalidData) {
      alert.setMessage(
        "Masih ada input yang tidak valid. Silakan perbaiki terlebih dahulu.",
        "warning"
      );
      return;
    }

    const totalNonTunai = dataTable.value.reduce((sum, row) => sum + (row.non_tunai || 0), 0);

    if (!buktiTransfer.value && totalNonTunai > 0) {
      alert.setMessage("Bukti transfer harus diupload", "warning");
      return;
    }

    const isConfirm = await $swal.confirmSubmit();
    if (!isConfirm) return;

    // Upload file TERLEBIH DAHULU
    let uploadedFileName = null;

    if (buktiTransfer.value) {
      const formData = new FormData();

      // Generate timestamp
      const timestamp = getCompactTimestamp();

      // Generate custom filename: namasales_timestamp
      const customFileName = `${namaSales.replace(/\s+/g, "_")}_${timestamp}`;

      // Ambil ekstensi file asli
      const fileExtension = buktiTransfer.value.name.split(".").pop();

      // Buat file baru dengan nama custom
      const renamedFile = new File(
        [buktiTransfer.value],
        `${customFileName}.${fileExtension}`,
        { type: buktiTransfer.value.type }
      );

      formData.append("file", renamedFile);

      const upload = await fetchWithAuth(
        "POST",
        `${apiUrl}/api/extra/upload-foto`,
        formData
      );

      // Gunakan nama file yang sudah di-rename
      uploadedFileName =
        upload?.filename || `${customFileName}.${fileExtension}`;
    }

    // Submit data dengan filename yang sudah terupload
    const submitData = dataTable.value.map((row) => ({
      id: row.id,
      id_sales_order: row.id_sales_order,
      no_faktur: row.no_faktur,
      tunai: parseFloat((row.tunai || 0).toFixed(2)),
      non_tunai: parseFloat((row.non_tunai || 0).toFixed(2)),
      jumlah_setoran: row.jumlah_setoran
    }));

    const res = await fetchWithAuth(
      "POST",
      `${apiUrl}/api/finance/submit-rekap-pembayaran-sales`,
      {
        id_sales,
        tanggal: tanggal.value,
        nama_sales: namaSales,
        data: submitData,
        buktiTransfer: uploadedFileName
      }
    );

    alert.setMessage(
      res.message || "Rekap pembayaran berhasil di proses",
      "success"
    );
    buktiTransfer.value = null;
    fileInputKey.value++;
    getResource();
  } catch (error) {
    alert.setMessage(error, "danger");
  }
};

onMounted(() => {
  getResource();
});
</script>
<template>
  <FlexBox full flex-col class="lg:tw-pl-6 tw-pl-2">
    <SlideRightX
      class="tw-w-full tw-z-10"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.1"
      :delay-out="0.1"
      :initial-x="-40"
      :x="40">
      <Card no-subheader>
        <template #header>Rekap Pembayaran Sales</template>
        <template #content>
          <FlexBox full class="tw-mb-8 tw-px-4">
            <TextField label="Tanggal" type="text" v-model="tanggal" disable />
          </FlexBox>
        </template>
      </Card>
    </SlideRightX>
    <SlideRightX
      class="tw-w-full"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.2"
      :delay-out="0.2"
      :initial-x="-40"
      :x="40">
      <Card no-subheader class="tw-pb-16 tw-px-4">
        <template #header>Daftar Setoran Toko</template>
        <template #content>
          <FlexBox full flexCol class="tw-mb-6">
            <Table
              :loading="loadingTable"
              :columns="listRekapPembayaran"
              :table-data="dataTable" />
            <FlexBox full class="tw-px-4">
              <TextField
                class="tw-w-full"
                label="Jumlah Setoran Tunai"
                type="text"
                :model-value="formatCurrencyAuto(totalSetoranTunai)"
                disable />
              <TextField
                class="tw-w-full"
                label="Jumlah Setoran Non Tunai"
                type="text"
                :model-value="formatCurrencyAuto(totalSetoranNonTunai)"
                disable />
              <TextField
                class="tw-w-full"
                label="Jumlah Setoran"
                type="text"
                :model-value="formatCurrencyAuto(totalSetoran)"
                disable />
            </FlexBox>
            <FlexBox full class="tw-px-4">
              <FIleInput
                :key="fileInputKey"
                class="tw-w-full"
                accept="image/*"
                v-model="buktiTransfer"
                group-id="file-1"
                label="Upload Bukti Transfer"
                label-for="input-file-1" />
            </FlexBox>
            <FlexBox full jusEnd class="tw-px-4 tw-mt-4">
              <Button
                :trigger="onSubmit"
                class="tw-px-8 tw-py-2 tw-bg-green-500">
                Submit
              </Button>
            </FlexBox>
          </FlexBox>
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>
