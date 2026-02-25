<script setup>
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import Table from "@/src/components/ui/table/Table.vue";
import Label from "@/src/components/ui/Label.vue";
import SelectInput from "@/src/components/ui/formInput/SelectInput.vue";
import VueDatePicker from "@vuepic/vue-datepicker";
import Button from "@/src/components/ui/Button.vue";
import { buatTagihanPurchasingColumn } from "@/src/model/tableColumns/tagihan-purchasing/buat-tagihan-purchasing/buatTagihanPurchasing";
import { useOthers } from "@/src/store/others";
import { computed, ref, watch } from "vue";
import { useTableSearch } from "@/src/lib/useTableSearch";
import { hutangService } from "@/src/services/hutang";
import { getSelectedRow } from "@/src/lib/utils";
import { useAlert } from "@/src/store/alert";
import { format } from "date-fns";
import { id } from "date-fns/locale";

const others = useOthers();
const alert = useAlert();
const { getTagihanPurchaseUrl } = hutangService;
const tableRef = ref(null);
const selectedRow = computed(() => tableRef.value?.getSelectedRow());
// console.log("selectedRow", selectedRow);

const principal = ref(null);
const mulaiJatuhtempo = ref(null);
const selesaiJatuhTempo = ref(null);
const loadingSubmit = ref(false);

const kodePrincipal = computed(() => {
  if (principal.value) {
    return others.principal.list.find((val) => val.id === principal.value)[
      "kode"
    ];
  }

  return "";
});

const datePickerLocale = "id";

const formatMulaiJatuhTempo = computed(() => {
  if (!mulaiJatuhtempo.value) return null;

  try {
    const dateValue =
      mulaiJatuhtempo.value instanceof Date
        ? mulaiJatuhtempo.value
        : new Date(mulaiJatuhtempo.value);

    return format(dateValue, "yyyy-MM-dd");
  } catch (error) {
    console.error("Error formatting date:", error);
    return null;
  }
});

const formatSelesaiJatuhTempo = computed(() => {
  if (!selesaiJatuhTempo.value) return null;

  try {
    const dateValue =
      selesaiJatuhTempo.value instanceof Date
        ? selesaiJatuhTempo.value
        : new Date(selesaiJatuhTempo.value);

    return format(dateValue, "yyyy-MM-dd");
  } catch (error) {
    console.error("Error formatting date:", error);
    return null;
  }
});

const fieldPool = [principal, mulaiJatuhtempo, selesaiJatuhTempo];
const queryEntries = computed(() => [
  ["principal=", principal.value],
  ["mulai_jatuh_tempo=", formatMulaiJatuhTempo.value],
  ["selesai_jatuh_tempo=", formatSelesaiJatuhTempo.value],
]);

const options = {
  initialColumnName: "no_transaksi",
  checkFieldFilterFunc: (val) => val[1] === null,
  filterFunction: (val) => val[1] !== null,
  asArgument: true,
};

const [data, , , , key, searchQuery, reset] = useTableSearch(
  getTagihanPurchaseUrl,
  fieldPool,
  queryEntries,
  options
);

// PERBAIKAN: Gunakan normalisasi yang lebih kuat
const processedTableData = computed(() => {
  if (!data.value) return [];
  // Cek apakah data ada di .result (seperti log sebelumnya) atau .pages
  return data.value.result || data.value.data || data.value.pages || (Array.isArray(data.value) ? data.value : []);
});

// Debug untuk melihat data mentah dan data yang sudah diproses
watch(
  () => data.value,
  (newVal) => {
    // console.log("Data dari API:", newVal);
    // console.log("Data untuk tabel:", processedTableData.value);
  }
);

const submitTagihan = async () => {
  // Pastikan mengambil nilai terbaru dari computed selectedRow
  const selectedIndices = selectedRow.value; 
  
  // Ambil data aslinya berdasarkan index yang dipilih
  const purchase_transaksis = getSelectedRow(
    selectedIndices,
    processedTableData.value
  );

  if (!purchase_transaksis || purchase_transaksis.length === 0) {
    alert.setMessage("Silahkan pilih minimal satu transaksi", "warning");
    return;
  }

  try {
    loadingSubmit.value = true;
    const result = await hutangService.postTagihanPurchase({
      purchase_transaksis, // Pastikan backend menerima key ini
    });
    
    // Biasanya result berisi message string atau object { message: '...' }
    alert.setMessage(result?.message || result || "Tagihan berhasil dibuat", "success");
    
    // Reset form dan tabel setelah sukses
    reset();
  } catch (error) {
    console.error("Submit Error:", error);
    alert.setMessage(error.message || "Gagal mengirim data", "danger");
  } finally {
    loadingSubmit.value = false;
  }
};
  // console.log(
  //   "Data yang akan dikirim:",
  //   JSON.stringify(
  //     {
  //       purchase_transaksis,
  //     },
  //     null,
  //     2
  //   )
  // );

 
const hasSelectedRows = computed(() => {
  const selected = selectedRow.value;
  if (!selected) return false;
  // Mengecek apakah ada minimal satu key yang nilainya truthy
  return Object.values(selected).some(val => val === true);
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
        <template #header>Form Buat Surat Tagihan purchasing</template>
        <template #content>
          <div class="form-grid-card-container-4-col">
            <Label label="Principal">
              <SelectInput
                placeholder="Pilih Data"
                size="md"
                :search="true"
                v-model="principal"
                :options="others.principal.list"
                text-field="nama"
                value-field="id"
              />
            </Label>
            <Label label="Kode Principal">
              <BFormInput
                v-model="kodePrincipal"
                placeholder="Pilih Principal"
                disabled
              />
            </Label>
            <Label label="Mulai Jatuh Tempo">
              <VueDatePicker
                v-model="mulaiJatuhtempo"
                :enable-time-picker="false"
                placeholder="yyyy-mm-dd"
                :locale="datePickerLocale"  auto-apply
              />
            </Label>
            <Label label="Selesai Jatuh Tempo">
              <VueDatePicker
                  v-model="selesaiJatuhTempo"
                  :enable-time-picker="false"
                  placeholder="yyyy-mm-dd"
                  :locale="datePickerLocale"  auto-apply
                />
            </Label>
          </div>
          <div class="tw-w-full tw-flex tw-gap-2">
            <Button
              :trigger="reset"
              icon="mdi mdi-reload"
              class="tw-h-[38px] tw-w-full xl:tw-w-32 tw-bg-red-500"
            >
              Reset
            </Button>
            <Button
              :trigger="searchQuery"
              icon="mdi mdi-magnify"
              class="tw-h-[38px] tw-w-full xl:tw-w-32"
            >
              Cari Data
            </Button>
          </div>
        </template>
      </Card>
    </SlideRightX>
    <SlideRightX
      class="slide-container"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.1"
      :delay-out="0.1"
      :initial-x="-40"
      :x="40"
    >
      <Card no-subheader>
        <template #header>List Tagihan</template>
        <template #content>
          <Table
            ref="tableRef"
            :key="key"
            :columns="buatTagihanPurchasingColumn"
            :table-data="processedTableData"
          />
          <FlexBox full jus-end>
            <Button
              :disabled="!hasSelectedRows"
              :trigger="submitTagihan"
              icon="mdi mdi-check"
              class="tw-bg-green-500 tw-px-4 tw-h-[34px]"
            >
              Submit
            </Button>
          </FlexBox>
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>
