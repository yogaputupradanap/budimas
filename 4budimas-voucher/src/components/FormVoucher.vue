<script setup>
import { BForm, BFormGroup } from "bootstrap-vue-next";
import SelectInput from "./ui/formInput/SelectInput.vue";
import { useCommonForm } from "../lib/useCommonForm";
import { voucherSchema } from "../model/formSchema/voucherSchema";
import TextField from "./ui/formInput/TextField.vue";
import FIleInput from "./ui/formInput/FIleInput.vue";
import { useCustomer } from "../store/customer";
import { usePrincipal } from "../store/principal";
import Skeleton from "./ui/Skeleton.vue";
import {
  googleStorageUrl,
  statusDiskonOption,
  tipeVoucher3Options,
  tipeVoucherOption,
  kategoriDiskonOption,
  levelUOMOptions,
  jenisVoucherOptions,
} from "../lib/constant";
import FlexBox from "./ui/FlexBox.vue";
import Card from "./ui/Card.vue";
import VueDatePicker from "@vuepic/vue-datepicker";
import Button from "./ui/Button.vue";
import { onMounted, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import {
  compressImage,
  fetchWithAuth,
  parseNumberFromCurrency,
} from "../lib/utils";
import { useAlert } from "../store/alert";
import Label from "./ui/Label.vue";
import { useProduk } from "../store/produk";
import { useCabang } from "../store/cabang";
import MultiselectWithSelectAll from "./ui/MultiselectWithSelectAll.vue";
import { inject } from "vue";

const props = defineProps(["initialValue"]);

const statusText = props.initialValue ? "edit" : "tambah";
const route = useRoute();
const alert = useAlert();

const tipeVoucherQuery = route.name.split(" ").at(-1);

const initRef = ref(null);

const produkStore = useProduk();
const customerStore = useCustomer();
const principalStore = usePrincipal();
const cabangStore = useCabang();

const produkOption = ref([]);
const produkLoading = ref(true);
const $swal = inject("$swal");
const router = useRouter();

const key = ref(0);

const { configProps, defineField, handleSubmit } = useCommonForm(
  voucherSchema,
  props.initialValue
);

const formMode = props.initialValue ? "Edit" : "Add";

const [idPrincipal, idPrincipalProps] = defineField(
  "id_principal",
  configProps
);
const [idProduk, idProdukProps] = defineField("id_produk", configProps);
const [idCabang, idCabangProps] = defineField("id_cabang", configProps);
const [levelUOM, levelUOMProps] = defineField("level_uom", configProps);
const [minimalJumlahProduk, minimalJumlahProdukProps] = defineField(
  "minimal_jumlah_produk",
  configProps
);
const [nama, namaProps] = defineField("nama", configProps);
const [tipeVoucher, tipeVoucherProps] = defineField(
  "tipe_voucher",
  configProps
);
const [kategoriVoucher, kategoriVoucherProps] = defineField(
  "kategori_voucher",
  configProps
);
const [persenDiskon, persenDiskonProps] = defineField(
  "persen_diskon",
  configProps
);
const [nilaiDiskon, nilaiDiskonProps] = defineField(
  "nilai_diskon",
  configProps
);
// const [minimalTotalPembelian, minimalTotalPembelianProps] = defineField(
//   "minimal_total_pembelian",
//   configProps
// );
const [minimalSubtotalPembelian, minimalSubtotalPembelianProps] = defineField(
  "minimal_subtotal_pembelian",
  configProps
);
const [keterangan, keteranganProps] = defineField("keterangan", configProps);
const [idCustomer, idCustomerProps] = defineField("id_customer", configProps);
const [tanggalMulai, tanggalMulaiProps] = defineField(
  "tanggal_mulai",
  configProps
);
const [tanggalKadaluarsa, tanggalKadaluarsaProps] = defineField(
  "tanggal_kadaluarsa",
  configProps
);
const [statusDiskon, statusDiskonProps] = defineField(
  "status_diskon",
  configProps
);
const [limit, limitProps] = defineField("limit", configProps);
const [uploadFile, uploadFileProps] = defineField("upload_file", configProps);
const [syaratKetentuan, syaratKetentuanProps] = defineField(
  "syarat_ketentuan",
  configProps
);
const [syaratWajib, syaratWajibProps] = defineField(
  "syarat_wajib",
  configProps
);

const [jenisVoucher, jenisVoucherProps] = defineField(
  "jenis_voucher",
  configProps
);

defineOptions({ inheritAttrs: false });


onMounted(() => {
  setInitialVoucherType();
  if (!props.initialValue?.level_uom) {
    levelUOM.value = 3;
  }

  // Jika mode edit dan principal sudah dipilih, lakukan fetch produk
  if (props.initialValue?.id_principal) {
    produkfetcher();
  }
});

watch(tipeVoucher, trackFieldDefaultValue);
watch(idPrincipal, trackPrincipalChange);
watch(kategoriVoucher, handleKategoriVoucherChange);

function handleKategoriVoucherChange() {
  if (kategoriVoucher.value === 1) {
    nilaiDiskon.value = "";
  } else if (kategoriVoucher.value === 2) {
    persenDiskon.value = "";
  }
}

const submitVoucher = handleSubmit(
  async (values) => {
    try {
      console.log("values : ", values);
      // convert values to entries
      const valuesEntries = Object.entries(values);

      // filter entries, remove [1] value === 0
      const filteredEntries = valuesEntries.filter(
        (val) =>
          (val[0] === "jenis_voucher" || val[1] !== 0) &&
          val[1] !== "n/a" &&
          val[1] !== null &&
          val[1] !== undefined
      );

      const numberedCurrency = filteredEntries.map((val) => {
        const checkCurrency =
          val[0] === "nilai_diskon" ||
          val[0] === "limit" ||
          // val[0] === "minimal_total_pembelian" ||
          val[0] === "minimal_subtotal_pembelian";

        if (checkCurrency) {
          val[1] = parseNumberFromCurrency(val[1]);
        }

        return val;
      });

      // convert converted entries to object
      const entriesObject = Object.fromEntries(numberedCurrency);
      const { upload_file } = entriesObject;

      if (upload_file) {
        // compress image size
        const upload_file_compressed = await compressImage(upload_file, {
          quality: 0.7,
        });

        const form = new FormData();
        form.append("file", upload_file_compressed);

        // upload photo ke google storage
        const { filename } = await fetchWithAuth(
          "POST",
          `/api/extra/upload-foto`,
          form
        );

        entriesObject.upload_file = filename;
      } else if (props.initialValue?.pic_voucher) {
        entriesObject.upload_file = props.initialValue.pic_voucher;
      } else {
        delete entriesObject.upload_file;
      }

      // decide if edit form or not, if it is then http method = PUT
      const method = props.initialValue ? "PUT" : "POST";
      const isConfirm = await $swal.confirmSubmit();
      if (!isConfirm) return;
      // insert voucher ke database
      const res = await fetchWithAuth(
        method,
        `/api/voucher/${tipeVoucherQuery}`,
        entriesObject
      );

      alert.setMessage(
        `Sukses ${statusText} voucher dengan nama : ${res.nama_voucher}`,
        "success"
      );
      router.back();
    } catch (error) {
      console.error(error);
      alert.setMessage(error, "danger");
    } finally {
      uploadFile.value = undefined;
    }
  },
  (error) => {
    console.log("validatuin error : ", error);
  }
);

async function produkfetcher() {
  try {
    produkLoading.value = true;
    const param = new URLSearchParams();
    param.append("where", `{"id_principal = ": "${idPrincipal.value}"}`);

    const api = "/api/base/produk";
    const url = `${api}?${param.toString()}`;

    if (!produkOption.value.length) {
      const res = await fetchWithAuth("GET", url);
      const addIdProdukRemap = res.map((val) => ({
        ...val,
        id_produk: val.id,
      }));
      produkOption.value = addIdProdukRemap;
    }
  } catch (error) {
    alert.setMessage(error, "danger");
  } finally {
    produkLoading.value = false;
    if (props.initialValue) {
      initRef.value = props.initialValue;
    }
  }
}

async function trackPrincipalChange(newValue, oldValue) {
  if (props.initialValue) {
    setInitialVoucherType();
  }

  const CHECK_IF_ID_PRINCIPAL_NOT_NULL =
    idPrincipal.value != 0 && idPrincipal.value != null;

  const CHECK_IF_TIPE_VOUCHER_MATCH =
    tipeVoucher.value == 1 || tipeVoucher.value == 2 || tipeVoucher.value == 3;

  if (CHECK_IF_ID_PRINCIPAL_NOT_NULL && CHECK_IF_TIPE_VOUCHER_MATCH) {
    produkOption.value = [];
    await produkfetcher();

    // Hanya reset jika principal berubah oleh pengguna dan bukan mode edit
    if (
      newValue !== oldValue &&
      oldValue !== undefined &&
      !props.initialValue
    ) {
      idProduk.value = [];
    }
  }
}

function selectProductsAfterFetch() {
  if (
    !props.initialValue?.id_produk ||
    !Array.isArray(props.initialValue.id_produk) ||
    !produkOption.value.length
  ) {
    return; // Guard clause untuk mencegah eksekusi yang tidak perlu
  }

  const selectedProducts = props.initialValue.id_produk
    .map((id) =>
      produkOption.value.find((p) => p.id === id || p.id_produk === id)
    )
    .filter(Boolean); // Filter undefined values

  if (selectedProducts.length > 0) {
    idProduk.value = selectedProducts;
  }
}

watch(
  produkOption,
  (newValue) => {
    if (newValue.length > 0 && props.initialValue?.id_produk) {
      selectProductsAfterFetch();
    }
  },
  { deep: true }
);
function trackFieldDefaultValue() {
  if (tipeVoucher.value == 1) {
    idProduk.value = [];
    jenisVoucher.value = null;
    idCabang.value = [];
    kategoriVoucher.value = null;
    levelUOM.value = null;
    minimalJumlahProduk.value = null;
    tanggalMulai.value = null;
    tanggalKadaluarsa.value = null;
    nilaiDiskon.value = "";
    idCustomer.value = [];
  }

  if (
    (tipeVoucher.value == 2 || tipeVoucher.value == 3) &&
    jenisVoucher.value == 1
  ) {
    idProduk.value = [];
    kategoriVoucher.value = null;
    tanggalMulai.value = null;
    tanggalKadaluarsa.value = null;
    idCabang.value = [];
    nilaiDiskon.value = "";
    levelUOM.value = null;
    minimalJumlahProduk.value = null;
    idCustomer.value = [];
  }

  if (
    tipeVoucher.value != 3 ||
    (tipeVoucher.value == 3 && jenisVoucher.value == 1)
  ) {
    idCustomer.value = [];
  }

  if (tipeVoucher.value == 3) {
    if (jenisVoucher.value !== 1) {
      minimalSubtotalPembelian.value = "n/a";
    }
    levelUOM.value = null;
    minimalJumlahProduk.value = null;
  }

  if (tipeVoucher.value == 2 && jenisVoucher.value == 0 && !levelUOM.value) {
    levelUOM.value = 3;
  }
}

function setInitialVoucherType() {
  console.log("tipeVoucherQuery : ", tipeVoucherQuery);
  tipeVoucher.value = parseInt(tipeVoucherQuery);

  if (tipeVoucher.value === 3) {
    if (!props.initialValue && jenisVoucher.value !== 1) {
      minimalSubtotalPembelian.value = "n/a";
    }
  }
}

watch(jenisVoucher, handleJenisVoucherChange);

function handleJenisVoucherChange() {
  if (jenisVoucher.value === 1) {
    idProduk.value = [];
    tanggalMulai.value = null;
    tanggalKadaluarsa.value = null;
    idCabang.value = [];
    nilaiDiskon.value = "";
    kategoriVoucher.value = null;
    levelUOM.value = null;
    minimalJumlahProduk.value = null;
    idCustomer.value = [];

    if (tipeVoucher.value == 3) {
      minimalSubtotalPembelian.value = "";
    }
  } else if (jenisVoucher.value === 0) {
    persenDiskon.value = "";

    if (tipeVoucher.value == 2) {
      levelUOM.value = 3;
    } else if (tipeVoucher.value == 3) {
      minimalSubtotalPembelian.value = "n/a";
    }
  }
}
</script>

<template>
  <FlexBox full no-left-padding :key="key">
    <Card no-subheader>
      <template #header>Form {{ formMode }} Voucher</template>
      <template #content>
        <BForm
          novalidate
          class="tw-w-full tw-grid tw-grid-cols-1 xl:tw-grid-cols-2 tw-gap-6">
          <FlexBox full flex-col no-left-padding>
            <!-- Basic Info Section -->
            <TextField
              group-id="input-group-2"
              label-for="input-2"
              :config-props="namaProps"
              v-model="nama"
              type="text"
              label="Nama :"
              placeholder="Masukkan Nama Dari Voucher" />

            <!-- Tipe Voucher Selection -->
            <BFormGroup
              class="tw-w-full"
              id="input-group-3"
              label="Tipe Voucher:"
              label-for="input-3"
              v-bind="tipeVoucherProps">
              <SelectInput
                :disabled="true"
                placeholder="Pilih Data"
                text-field="nama"
                value-field="id"
                size="md"
                :options="tipeVoucherOption"
                v-model="tipeVoucher" />
            </BFormGroup>

            <BFormGroup
              v-if="tipeVoucher == 2 || tipeVoucher == 3"
              class="tw-w-full"
              id="input-group-jenis"
              label="Jenis Voucher:"
              label-for="input-jenis"
              v-bind="jenisVoucherProps">
              <SelectInput
                :disabled="!!props.initialValue"
                text-field="nama"
                value-field="id"
                size="md"
                :options="jenisVoucherOptions"
                v-model="jenisVoucher" />
            </BFormGroup>

            <!-- Principal Selection -->
            <BFormGroup
              class="tw-w-full"
              id="input-group-1"
              label="ID Principal:"
              label-for="input-1"
              v-bind="idPrincipalProps">
              <SelectInput
                placeholder="Pilih Data"
                text-field="nama"
                :search="true"
                value-field="id"
                size="md"
                :options="principalStore.principal.list"
                v-model="idPrincipal" />
            </BFormGroup>

            <!-- Product Multi-select -->
            <FlexBox
              no-left-padding
              full
              v-if="
                idPrincipal != null &&
                idPrincipal != 0 &&
                idPrincipal != '' &&
                (tipeVoucher == 2 || tipeVoucher == 3) &&
                jenisVoucher == 0
              ">
              <Label
                v-if="produkLoading && !produkOption.length"
                label="ID Produk :"
                full>
                <Skeleton class="tw-w-full tw-h-8" />
              </Label>
              <BFormGroup
                v-else
                class="tw-w-full"
                id="input-group-produk"
                label="ID Produk :"
                label-for="input-produk"
                v-bind="idProdukProps">
                <MultiselectWithSelectAll
                  v-model="idProduk"
                  :options="produkOption"
                  label="nama"
                  track-by="id_produk"
                  :loading="produkLoading" />
              </BFormGroup>
            </FlexBox>

            <!-- Kategori Voucher untuk V2 dan V3 -->
            <BFormGroup
              v-if="(tipeVoucher == 2 || tipeVoucher == 3) && jenisVoucher == 0"
              class="tw-w-full"
              id="input-group-kategori"
              label="Kategori Voucher:"
              label-for="input-kategori"
              v-bind="kategoriVoucherProps">
              <SelectInput
                placeholder="Pilih Data"
                text-field="nama"
                value-field="id"
                size="md"
                :options="kategoriDiskonOption"
                v-model="kategoriVoucher" />
            </BFormGroup>

            <!-- Persen Diskon untuk V1 atau V2/V3 jenis reguler -->
            <TextField
              v-if="
                tipeVoucher == 1 ||
                ((tipeVoucher == 2 || tipeVoucher == 3) && jenisVoucher == 1)
              "
              type="number"
              group-id="input-group-100"
              label-for="input-100"
              :config-props="persenDiskonProps"
              v-model="persenDiskon"
              label="Persen Diskon (%) :"
              placeholder="Masukkan Nilai Persen Dari Voucher" />

            <!-- Persen/Nominal Diskon untuk V2 dan V3 jenis produk berdasarkan kategori -->
            <TextField
              v-if="
                (tipeVoucher == 2 || tipeVoucher == 3) &&
                jenisVoucher == 0 &&
                kategoriVoucher == 1
              "
              type="number"
              group-id="input-group-100"
              label-for="input-100"
              :config-props="persenDiskonProps"
              v-model="persenDiskon"
              label="Persen Diskon (%) :"
              placeholder="Masukkan Nilai Persen Dari Voucher" />

            <TextField
              v-if="
                (tipeVoucher == 2 || tipeVoucher == 3) &&
                jenisVoucher == 0 &&
                kategoriVoucher == 2
              "
              type="currency"
              group-id="input-group-7"
              label-for="input-7"
              :config-props="nilaiDiskonProps"
              v-model="nilaiDiskon"
              label="Nilai Nominal Diskon :"
              placeholder="Masukkan Nilai Dari Voucher" />

            <!-- Cabang Multi-select untuk V2 dan V3 -->
            <FlexBox
              no-left-padding
              full
              v-if="
                (tipeVoucher == 2 || tipeVoucher == 3) && jenisVoucher == 0
              ">
              <BFormGroup
                class="tw-w-full"
                id="input-group-cabang"
                label="ID Cabang :"
                label-for="input-cabang"
                v-bind="idCabangProps">
                <MultiselectWithSelectAll
                  v-model="idCabang"
                  :options="cabangStore.cabang.list"
                  label="nama"
                  track-by="id" />
              </BFormGroup>
            </FlexBox>

            <!-- Customer Selection - Only for Voucher 3 -->
            <FlexBox
              no-left-padding
              full
              v-if="tipeVoucher == 3 && jenisVoucher == 0">
              <BFormGroup
                class="tw-w-full"
                id="input-group-6"
                label="ID Customer :"
                label-for="input-6"
                v-bind="idCustomerProps">
                <MultiselectWithSelectAll
                  v-model="idCustomer"
                  :options="customerStore.customer.list"
                  label="nama"
                  track-by="id" />
              </BFormGroup>
            </FlexBox>

            <!-- Keterangan -->
            <BFormGroup
              class="tw-w-full"
              id="input-group-5"
              label="Keterangan :"
              label-for="input-5"
              v-bind="keteranganProps">
              <BFormTextarea
                v-model="keterangan"
                placeholder="Masukkan Keterangan"
                rows="3" />
            </BFormGroup>

            <!-- Date Selection -->
            <FlexBox
              v-if="(tipeVoucher == 2 || tipeVoucher == 3) && jenisVoucher == 0"
              no-left-padding
              class="tw-flex-col lg:tw-flex-row">
              <BFormGroup
                class="tw-w-full"
                id="input-group-8"
                label="Tanggal Mulai :"
                label-for="input-8"
                v-bind="tanggalMulaiProps">
                <VueDatePicker
                  v-model="tanggalMulai"
                  :enable-time-picker="false"
                  placeholder="mm/dd/yyyy"
                  :teleport="true"
                  auto-apply />
              </BFormGroup>
              <BFormGroup
                class="tw-w-full"
                id="input-group-9"
                label="Tanggal Kadaluarsa :"
                label-for="input-9"
                v-bind="tanggalKadaluarsaProps">
                <VueDatePicker
                  v-model="tanggalKadaluarsa"
                  :enable-time-picker="false"
                  placeholder="mm/dd/yyyy"
                  :teleport="true"
                  auto-apply />
              </BFormGroup>
            </FlexBox>

            <!-- Status Diskon -->
            <BFormGroup
              class="tw-w-full"
              id="input-group-6"
              label="Status Diskon :"
              label-for="input-6"
              v-bind="statusDiskonProps">
              <SelectInput
                placeholder="Pilih Data"
                text-field="nama"
                value-field="id"
                size="md"
                :options="statusDiskonOption"
                v-model="statusDiskon" />
            </BFormGroup>
          </FlexBox>

          <!-- Right Column -->
          <FlexBox no-left-padding flex-col>
            <!-- Limit - Optional for V2 and V3 -->
            <TextField
              v-if="false"
              type="currency"
              group-id="input-group-10"
              label-for="input-10"
              :config-props="limitProps"
              v-model="limit"
              label="Limit :"
              placeholder="Masukkan Limit Dari Voucher" />

            <!-- Minimal Pembelian berdasarkan tipe -->
            <TextField
              v-if="
                tipeVoucher == 1 ||
                ((tipeVoucher == 2 || tipeVoucher == 3) && jenisVoucher == 1)
              "
              type="currency"
              group-id="input-group-101"
              label-for="input-101"
              :config-props="minimalSubtotalPembelianProps"
              v-model="minimalSubtotalPembelian"
              label="Minimal Subtotal Pembelian :"
              placeholder="Masukkan minimal subtotal pembelian Voucher" />

            <template v-if="tipeVoucher == 2 && jenisVoucher == 0">
              <!-- Level UOM Selection -->
              <BFormGroup
                class="tw-w-full"
                id="input-group-uom"
                label="Level UOM :"
                label-for="input-uom"
                v-bind="levelUOMProps">
                <SelectInput
                  placeholder="Pilih Level UOM"
                  text-field="nama"
                  value-field="id"
                  size="md"
                  :options="levelUOMOptions"
                  v-model="levelUOM" />
              </BFormGroup>

              <!-- Jumlah Produk -->
              <TextField
                type="number"
                group-id="input-group-jumlah"
                label-for="input-jumlah"
                :config-props="minimalJumlahProdukProps"
                v-model="minimalJumlahProduk"
                label="Minimal Jumlah Produk :"
                placeholder="Masukkan minimal jumlah produk" />
            </template>

            <!-- File Upload -->
            <FIleInput
              :config-props="uploadFileProps"
              v-model="uploadFile"
              group-id="file-1"
              label="Upload File :"
              :web-filename="initialValue?.pic_voucher"
              :web-url="`${googleStorageUrl}${initialValue?.pic_voucher}`"
              :image-viewer="true"
              label-for="input-file-1"
            />

            <!-- Terms and Conditions -->
            <BFormGroup
              class="tw-w-full"
              id="input-group-11"
              label="Syarat Ketentuan :"
              label-for="input-11"
              v-bind="syaratKetentuanProps">
              <BFormTextarea
                v-model="syaratKetentuan"
                placeholder="Syarat Ketentuan"
                rows="6" />
            </BFormGroup>

            <BFormGroup
              class="tw-w-full"
              id="input-group-12"
              label="Syarat Wajib :"
              label-for="input-12"
              v-bind="syaratWajibProps">
              <BFormTextarea
                v-model="syaratWajib"
                placeholder="Syarat Wajib"
                rows="6" />
            </BFormGroup>
          </FlexBox>
        </BForm>

        <!-- Submit Button -->
        <FlexBox full jus-end class="tw-mt-4">
          <Button :trigger="submitVoucher" class="tw-h-9 tw-px-6 tw-capitalize">
            {{ statusText }}
          </Button>
        </FlexBox>
      </template>
    </Card>
  </FlexBox>
</template>
