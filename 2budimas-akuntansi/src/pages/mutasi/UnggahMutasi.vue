<script setup>
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import Table from "@/src/components/ui/table/Table.vue";
import Label from "@/src/components/ui/Label.vue";
import SelectInput from "@/src/components/ui/formInput/SelectInput.vue";
import Button from "@/src/components/ui/Button.vue";
import {$swal} from "@/src/components/ui/SweetAlert.vue";
import {computed, ref, watch} from "vue";
import Skeleton from "@/src/components/ui/Skeleton.vue";
import {useOthers} from "@/src/store/others";
import FIleInput from "@/src/components/ui/formInput/FIleInput.vue";
import {listPreviewMutasi, summaryPreviewMutasi} from "@/src/model/tableColumns/mutasi/listPreviewMutasi";
import {fetchWithAuth, getDateNow} from "@/src/lib/utils";
import useMutasi from "@/src/lib/useMutasi";
import useRekening from "@/src/lib/useRekeningPerusahaan";

const others = useOthers();
const id_perusahaan = ref(null);
const id_rekening_perusahaan = ref(null);
const selectedTanggal = ref(getDateNow());
const mutasiFile = ref(null);
const isUploaded = ref(false);
const containerKey = ref(0);
const clientKey = ref(0);
const dataPreviewMutasi = ref([]);
const {handleCsvBCA, handleCsvBCADIFI, handleCsvMandiri} = useMutasi()
const {loading: loadingPerusahaan, getRekeningPerusahaan, rekeningPerusahaan} = useRekening()
const dataSummaryMutasi = ref({});
const laodingSubmit = ref(false);

const isValidSummary = computed(
    () => {
      const rounded = (num) => Math.round(num * 100) / 100;
      const saldo_close_awal = dataPreviewMutasi.value[0]?.saldo;
      const data_credit_temp = dataPreviewMutasi.value[0]?.kredit;
      const data_debit_temp = dataPreviewMutasi.value[0]?.debit;
      const nama_bank = rekeningPerusahaan.value.find(
          (item) => item.id_rekening_perusahaan === id_rekening_perusahaan.value
      )?.nama_bank?.toLowerCase()
      const bankHaveReverseLogicCreditDebit = ["bca", "bca difi"];
      const isBca = bankHaveReverseLogicCreditDebit.includes(nama_bank);
      console.log(isBca);
      const saldo_awal = rounded((
          () => {
            if (isBca) {
              return data_credit_temp > 0 ? saldo_close_awal + data_credit_temp : saldo_close_awal - data_debit_temp;
            } else {
              return data_credit_temp > 0 ? saldo_close_awal - data_credit_temp : saldo_close_awal + data_debit_temp;
            }
          }
      )())

      const summaryTemp = dataPreviewMutasi.value.reduce(
          (acc, item) => {
            if (item.tipe.toLowerCase() === 'cr') {
              if (isBca) {
                acc -= item.jumlah;
              } else {
                acc += item.jumlah;
              }
            } else if (item.tipe.toLowerCase() === 'db') {
              if (isBca) {
                acc += item.jumlah;
              } else {
                acc -= item.jumlah;
              }
            }
            return acc;
          }, saldo_awal
      );
      // console.log("Saldo Awal:", saldo_awal);
      // console.log("Saldo Akhir Perhitungan:", summaryTemp);
      // console.log("Saldo Akhir dari Data:", dataSummaryMutasi.value?.saldo_akhir);
      // console.log("Nama Bank:", nama_bank);
      return (
          rounded(summaryTemp) === rounded(parseFloat(dataSummaryMutasi.value?.saldo_akhir))
      );

    }
)


const handleUnggah = async () => {
  if (!id_rekening_perusahaan.value) {
    $swal.error(
        "Mohon pilih rekening perusahaan terlebih dahulu.",
    )
    return;
  }
  if (!mutasiFile.value) {
    $swal.error(
        "Mohon pilih file mutasi terlebih dahulu.",
    )
    return;
  }

  try {
    if (!mutasiFile.value.name?.endsWith('.csv')) {
      $swal.error(
          "File yang diunggah harus berformat CSV.",
      )
      return;
    }
    const name_bank = rekeningPerusahaan.value.find(
        (item) => item.id_rekening_perusahaan === id_rekening_perusahaan.value
    )?.nama_bank?.toLowerCase();
    let transactions = [];
    let summary = {};
    switch (name_bank) {
      case "bca":
        ({transactions, summary} = await handleCsvBCA(mutasiFile.value));
        break;
      case "mandiri":
        ({transactions, summary} = await handleCsvMandiri(mutasiFile.value));
        break
      case "bca difi":
        ({transactions, summary} = await handleCsvBCADIFI(mutasiFile.value));
        break;
      default:
        console.log("Bank tidak dikenali:", name_bank);
        $swal.error("Format file tidak didukung untuk bank ini.");
        return;
    }


    dataPreviewMutasi.value = transactions
    dataSummaryMutasi.value = summary;

    isUploaded.value = true;
  } catch (error) {
    console.error("Error reading file:", error);
    $swal.error("Gagal membaca file mutasi: " + error.message);
  }
};

const handleSubmit = async () => {

  if (!id_perusahaan.value) {
    $swal.error(
        "Mohon pilih perusahaan terlebih dahulu.",
    )
    return;
  }

  if (dataPreviewMutasi.value.length === 0) {
    $swal.error(
        "Tidak ada data mutasi yang ditemukan di file yang diunggah.",
    )
    return;
  }

  const isConfirm = await $swal.confirm(
      "Apakah Anda yakin ingin mengunggah data mutasi ini?",
  );

  if (!isConfirm) {
    return;
  }

  try {
    const payload = {
      data_mutasi: dataPreviewMutasi.value,
      id_perusahaan: id_perusahaan.value,
      id_rekening_perusahaan: id_rekening_perusahaan.value,
    };

    await fetchWithAuth(
        "POST",
        `/api/akuntansi/insert-mutasi`,
        payload,
    )
    $swal.success("Data mutasi berhasil diunggah.");

    isUploaded.value = false;
    dataPreviewMutasi.value = [];
    id_perusahaan.value = null;
    dataSummaryMutasi.value = {};
  } catch (error) {
    console.log("Error uploading data:", error);
    $swal.error("Gagal mengunggah data mutasi: " + error);
  }
};

watch(
    () => id_perusahaan.value,
    async (newValue) => {
      if (newValue) {
        await getRekeningPerusahaan(newValue);
        // console.log("Perusahaan changed to:", rekeningPerusahaan.value);
      } else {
        rekeningPerusahaan.value = [];
      }

      id_rekening_perusahaan.value = null;
    },
    {immediate: true}
)

watch(
    () => id_rekening_perusahaan.value,
    (newValue) => {
      if (newValue) {
        dataPreviewMutasi.value = [];
        dataSummaryMutasi.value = {};
        clientKey.value += 1; // Trigger re-render of the table
      }
    }
)

</script>

<template>
  <FlexBox full flex-col :key="containerKey">
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
        <template #header>Form Unggah Mutasi</template>
        <template #content>
          <div class="form-grid-card-5-col tw-items-end">
            <Label label="Tanggal">
              <BFormInput
                  :model-value="selectedTanggal"
                  disabled/>
            </Label>
            <Label label="Perusahaan">
              <Skeleton
                  class="tw-w-full tw-h-[34px]"
                  v-if="others.perusahaan.loading"
              />
              <SelectInput
                  v-else
                  v-model="id_perusahaan"
                  placeholder="Pilih Data"
                  size="md"
                  :search="true"
                  :options="others.perusahaan.list"
                  :disabled="loadingPerusahaan"
                  text-field="nama"
                  value-field="id"
              />
            </Label>
            <Label label="Bank">
              <Skeleton
                  class="tw-w-full tw-h-[34px]"
                  v-if="loadingPerusahaan"
              />
              <SelectInput
                  v-else
                  v-model="id_rekening_perusahaan"
                  placeholder="Pilih Data"
                  size="md"
                  :search="true"
                  :disabled="!id_perusahaan || loadingPerusahaan"
                  :options="rekeningPerusahaan"
                  text-field="nama_bank"
                  value-field="id_rekening_perusahaan"
              />
            </Label>
            <Label label="Upload Mutasi:">
              <FIleInput
                  class="tw-w-full"
                  :model-value="mutasiFile"
                  @update:model-value="
                  (file) => (mutasiFile = file)
                "
              />
            </Label>
            <div class="tw-flex tw-gap-2">

              <Button
                  :trigger="handleUnggah"
                  icon="mdi mdi-file-upload-outline"
                  class="tw-h-[38px] tw-w-full xl:tw-w-44"
              >
                Unggah Mutasi
              </Button>
            </div>
          </div>
        </template>
      </Card>
    </SlideRightX>

    <SlideRightX
        class="slide-container tw-justify-end"
        :duration-enter="0.6"
        :duration-leave="0.6"
        :delay-in="0.2"
        :delay-out="0.2"
        :initial-x="-40"
        :x="40"
    >
      <Card v-if="isUploaded" no-subheader>
        <template #header>Preview Unggah Mutasi</template>
        <template #content>
          <Table
              :key="clientKey"
              :columns="listPreviewMutasi"
              :table-data="dataPreviewMutasi"
          />
          <div class=" tw-flex tw-flex-col tw-items-start tw-w-full tw-justify-start">
            <h4 class="tw-font-bold lg:tw-text-2xl tw-text-xl tw-text-blue-500">
              Preview Saldo
            </h4>
            <Table
                :loading="!dataSummaryMutasi"
                :columns="summaryPreviewMutasi"
                :table-data="[dataSummaryMutasi]"
                class="tw-mt-4"
            />
          </div>
          <FlexBox full jusEnd class="tw-mt-4">
            <div class="tw-flex tw-flex-col tw-gap-2 tw-items-end">
              <p>
              <span v-if="!isValidSummary" class="tw-text-red-500 tw-font-semibold">
                Periksa kembali data mutasi, saldo akhir tidak sesuai dengan perhitungan.
              </span>
              </p>
              <Button
                  class="tw-w-32"
                  icon="mdi mdi-check"
                  :disabled="!isValidSummary"
                  :loading="laodingSubmit"
                  :trigger="handleSubmit"
              >
                Simpan
              </Button>
            </div>
          </FlexBox>
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>