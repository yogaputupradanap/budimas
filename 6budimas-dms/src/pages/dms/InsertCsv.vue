<script setup>
import SelectInput from "@/src/components/ui/formInput/SelectInput.vue";
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Skeleton from "@/src/components/ui/Skeleton.vue";
import Card from "@/src/components/ui/Card.vue";
import Label from "@/src/components/ui/Label.vue";
import { BFormInput } from "bootstrap-vue-next";
import Table from "@/src/components/ui/table/Table.vue";
import { listStockColumns } from "@/src/model/tableColumns/stock-opname/listStock";
import RouterButton from "@/src/components/ui/RouterButton.vue";
import Button from "@/src/components/ui/Button.vue";
import {
  computed,
  onBeforeUnmount,
  onMounted,
  reactive,
  ref,
  watch,
} from "vue";
import Papa from "papaparse";
import { useAlert } from "@/src/store/alert";
import { useUser } from "@/src/store/user";
import { useOthers } from "@/src/store/others";
import { storeToRefs } from "pinia";
import { listPreviewFile } from "@/src/model/tableColumns/dms/listPreviewFile";
import { dmsService } from "@/src/services/dms";

const others = useOthers();
const loadingSubmit = ref(false);
const { principal, stockOpname } = storeToRefs(others);

const alert = useAlert();
const userStore = useUser();

const fileInput = ref(null);

const cariData = ref(false);
const sumberSelected = ref("");

const valueInvoiceHDR = reactive([]);
const listStockOpname = ref([]);
const nameFile1 = ref("");
const nameFile2 = ref("");
const id_cabang = userStore.user.value.id_cabang;
const datePickerLocale = {
  locale: "id",
  format: "yyyy-MM-dd",
};

onMounted(() => {
  listStockOpname.value = stockOpname.value.list;
});
onBeforeUnmount(() => {
  if (cariData.value) {
    others.getAllStockOpname();
  }
});

const localStore = ref(null);
const searchLoading = ref(false);
const searchEntries = ref([]);
const buttonText = ref({
  text: "Import File",
  icon: "mdi mdi-file-plus",
});

const uploadFile = () => {
  fileInput.value.click();
};

const readFile = async (e) => {
  const files = e.target.files;
  const sorted = [];

  valueInvoiceHDR.values = [];
  nameFile1.value = "";
  nameFile2.value = "";

  if (files.length < 2 || files.length > 2) {
    alert.setMessage("Harus memasukakkan 2 File", "danger");
    return;
  }
  if (files[0].name.includes("HDR") && files[1].name.includes("HDR")) {
    alert.setMessage("File Harus Berbeda", "danger");
    return;
  }

  if (files[0].name.includes("DTL") && files[1].name.includes("DTL")) {
    alert.setMessage("File Harus Berbeda", "danger");
    return;
  }

  if (!files[0].name.includes("HDR") && !files[1].name.includes("HDR")) {
    alert.setMessage("Salah satu file Harus Memiliki Nama HDR", "danger");
    return;
  }

  if (!files[0].name.includes("DTL") && !files[1].name.includes("DTL")) {
    alert.setMessage("Salah satu file Harus Memiliki Nama DTL", "danger");
    return;
  }

  if (files[0].name.includes("HDR")) {
    sorted[0] = files[0];
    nameFile1.value = files[0].name;
    sorted[1] = files[1];
    nameFile2.value = files[1].name;
  } else {
    sorted[1] = files[0];
    nameFile2.value = files[0].name;
    sorted[0] = files[1];
    nameFile1.value = files[1].name;
  }
  const [file1, file2] = sorted;
  if (file1.type !== "text/csv" || file2.type !== "text/csv") {
    alert.setMessage("File Harus Berformat CSV", "danger");
    return;
  }

  console.log("masuk");
  await Papa.parse(file1, {
    header: true,
    transformHeader: (header) => header.replace(/\s+/g, "_").toLowerCase(),
    skipEmptyLines: true,
    complete: async (results) => {
      const data = results.data;
      valueInvoiceHDR.values = data;
      console.log(valueInvoiceHDR.values);
    },
    error: (error) => {
      console.log(error);
      alert.setMessage("Error Parsing File", "danger");
    },
  });
  await Papa.parse(file2, {
    header: true,
    transformHeader: (header) => header.replace(/\s+/g, "_").toLowerCase(),
    skipEmptyLines: true,
    complete: async (results) => {
      const data = results.data;
      valueInvoiceHDR.values.forEach((item, index) => {
        const newValues = data.filter((value) => {
          return value.invoice_no === item.invoice_no;
        });
        valueInvoiceHDR.values[index].detail = newValues;
      });
    },
    error: (error) => {
      console.log(error);
      alert.setMessage("Error Parsing File", "danger");
    },
  });
};

const submit = async () => {
  loadingSubmit.value = true;
  const data = valueInvoiceHDR.values;
  const payload = {
    data,
  };
  try {
    await dmsService.insertDms(payload);
    alert.setMessage("Berhasil Insert Data", "success");
    nameFile1.value = "";
    nameFile2.value = "";
    valueInvoiceHDR.values = [];
  } catch (error) {
    console.log(error);
    alert.setMessage(error, "danger");
  } finally {
    loadingSubmit.value = false;
  }
};

const listSubmerFile = ref([
  {
    nama: "DMS",
    id: 1,
  },
  {
    nama: "VDist",
    id: 2,
  },
  {
    nama: "BOSNET",
    id: 3,
  },
  {
    nama: "UVIC",
    id: 4,
  },
]);
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
        <template #header>Upload File CSV</template>
        <template #content>
          <div class="form-grid-card-3-menu tw-items-center">
            <Label label="Sumber File :" class="z-10">
              <Skeleton class="skeleton" v-if="principal.loading" />
              <BFormInput
                v-else
                model-value="DMS"
                disabled="true"
                placeholder="Pilih Sumber File"
                size="md"
                :search="true"
                class=""
                :options="listSubmerFile"
                text-field="nama"
                value-field="nama"
              />
            </Label>
            <input
              @change="readFile"
              type="file"
              multiple
              class="tw-hidden"
              ref="fileInput"
            />
            <div class="tw-flex tw-justify-center tw-items-center tw-gap-2">
              <h3>
                {{ nameFile1 }}
              </h3>
              <h3>
                {{ nameFile2 }}
              </h3>
            </div>
            <Button
              :trigger="uploadFile"
              class="tw-text-white tw-bg-blue-500 tw-rounded-lg tw-px-2 tw-py-2 tw-flex tw-justify-center tw-items-center hover:tw-bg-gray-500 hover:tw-text-white hover:tw-transition-all hover:tw-duration-300 hover:tw-ease-in-out"
              :icon="buttonText.icon"
            >
              {{ buttonText.text }}
            </Button>
          </div>
        </template>
      </Card>
    </SlideRightX>

    <SlideRightX
      class="slide-container tw-z-0"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.3"
      :delay-out="0.1"
      :initial-x="-40"
      :x="40"
    >
      <Card no-subheader>
        <template #header>Preview File CSV</template>
        <template #content>
          <Table
            :key="localStore || []"
            :columns="listPreviewFile"
            :loading="stockOpname.loading"
            :classic="true"
            :table-data="valueInvoiceHDR.values"
          />
          <div
            class="tw-flex tw-w-full tw-justify-end tw-items-start tw-mx-4 tw-mt-4"
          >
            <Button
              class="btn-c-success tw-text-base tw-py-2 tw-px-5"
              icon="mdi mdi-check"
              v-if="valueInvoiceHDR.values.length > 0"
              :loading="loadingSubmit"
              :trigger="submit"
              >Submit</Button
            >
          </div>
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>
