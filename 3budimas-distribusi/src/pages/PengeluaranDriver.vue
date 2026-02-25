<script setup>
import { onMounted, watch, ref, onUnmounted, computed, nextTick } from "vue";
import {
  checkNaN,
  parseCurrency,
  fetchWithAuth,
  apiUrl,
  downloadPdf,
  getDateNow,
} from "../lib/utils";
import { listDriverFakturColumn } from "../model/formSchema";
import { pengeluaranSchema } from "../model/formSchema";
import { useCommonForm } from "../lib/useCommonForm";
import { useDriver } from "../store/driver";
import { useRoute } from "vue-router";
import { useAlert } from "../store/alert";
import Card from "../components/ui/Card.vue";
import Table from "../components/ui/table/Table.vue";
import Button from "../components/ui/Button.vue";
import Skeleton from "../components/ui/Skeleton.vue";
import TextField from "../components/ui/formInput/TextField.vue";
import SelectInput from "../components/ui/formInput/SelectInput.vue";
import SlideRightX from "../components/animation/SlideRightX.vue";
import VueDatePicker from "@vuepic/vue-datepicker";
import PengeluaranDriverPdf from "../components/pdf/PengeluaranDriverPdf.vue";
import { $swal } from "@/src/components/ui/SweetAlert.vue";

const driver = useDriver();
const alert = useAlert();
const tableKey = ref(0);
const fieldKey = ref(0);
const localStore = ref([]);
const route = useRoute();
const paramsId = ref(route.params?.id);
const checkParamsIdProperty = ref(route.params.hasOwnProperty("id"));
const operandString = ref(checkParamsIdProperty.value ? "Update" : "Input");
const subTotal = computed(getSubTotal);
const biayaLainnya = computed(getBiayaLainnya);
const total = computed(getTotal);

const { configProps, defineField, handleSubmit } = useCommonForm(
  pengeluaranSchema,
  driver.infoPengeluaran.info
);

const [id_driver, idDriverProps] = defineField("id_driver", configProps);
const [tanggal, tanggalBerangkatProps] = defineField("tanggal", configProps);
const [tujuan, tujuanProps] = defineField("tujuan", configProps);
const [helper, helperProps] = defineField("helper", configProps);
const [km_berangkat, kmBerangkatProps] = defineField(
  "km_berangkat",
  configProps
);
const [km_pulang, kmPulangProps] = defineField("km_pulang", configProps);
const [km_isi_bbm, kmIsiBbmProps] = defineField("km_isi_bbm", configProps);
const [isi_bbm_liter, isiBbmLiterProps] = defineField(
  "isi_bbm_liter",
  configProps
);
const [isi_bbm_rupiah, isiBbmRupiahProps] = defineField(
  "isi_bbm_rupiah",
  configProps
);
const [uang_saku, uangSakuProps] = defineField("uang_saku", configProps);

function getSubTotal() {
  const calcFakturs = localStore.value.flat().reduce((acc, val) => {
    if (val.id_tipe === 6 || val.id_tipe === 7) {
      const nominal = val?.nominal || 0;
      return nominal + acc;
    }

    return acc;
  }, 0);

  const addBbmRupiah = parseInt(calcFakturs) + parseInt(isi_bbm_rupiah.value);

  return checkNaN(addBbmRupiah);
}

function getBiayaLainnya() {
  const calcFaktursLainnya = localStore.value.flat().reduce((acc, val) => {
    if (val.id_tipe === 8) {
      const nominal = val?.nominal || 0;
      return nominal + acc;
    }

    return acc;
  }, 0);

  return parseInt(calcFaktursLainnya);
}

function getTotal() {
  return parseInt(subTotal.value) + parseInt(biayaLainnya.value);
}

const change = ({ value, rowIndex, columnId }) => {
  localStore.value = localStore.value.map((val, idx) => {
    if (rowIndex === idx) {
      if (columnId === "keterangan") {
        const resultKeterangan = val.map((v) => ({ ...v, keterangan: value }));
        return resultKeterangan;
      }

      const findIdTipe = val.find((v) => v.id_tipe == columnId);
      findIdTipe.nominal = value;
    }

    return val;
  });
};

const checkFakturs = () => {
  return localStore.value.flat().some((val) => val.nominal == null);
};

const cetak = () => {
  downloadPdf("pengeluaran-driver", `pengeluaran driver ${getDateNow()}`);
};

const submit = handleSubmit(async (value) => {
  const isUpdate = checkParamsIdProperty.value ? "update" : "tambah";

  try {
    if (checkFakturs()) throw "ada kolom faktur yang kosong";

    const body = {
      ...value,
      fakturs: localStore.value.flat(),
    };

    if (checkParamsIdProperty.value) body["id"] = parseInt(paramsId.value);

    const result = await fetchWithAuth(
      "POST",
      `${apiUrl}/api/distribusi/${isUpdate}-pengeluaran-driver`,
      body
    );

    if (checkParamsIdProperty.value) {
      driver.updatePengeluaranDriver(result);
    } else {
      driver.addPengeluaranDriver(result);
    }

    $swal.success(`Berhasil ${isUpdate} pengeluaran driver`);

    const namaDriver = driver.driver.list.find((i) => i.id == value.id_driver)[
      "nama"
    ];

    driver.infoPengeluaran.info = { ...value, namaDriver };
    await driver.getDriverFaktur(result.id_info_driver, "update");

    nextTick(() => {
      cetak();
    });
  } catch (error) {
    console.log(`Some error occured : ${error}`);

    $swal.error(`Gagal ${isUpdate} pengeluaran driver : ${error}`);
  }
});

const getPengeluaranInfo = async () => {
  await driver.getInfoPengeluaran(paramsId.value);
  const infoPengeluaran = driver.infoPengeluaran.info;

  id_driver.value = infoPengeluaran.id_driver;
  helper.value = infoPengeluaran.helper;
  isi_bbm_liter.value = infoPengeluaran.isi_bbm_liter;
  isi_bbm_rupiah.value = infoPengeluaran.isi_bbm_rupiah;
  km_berangkat.value = infoPengeluaran.km_berangkat;
  km_isi_bbm.value = infoPengeluaran.km_isi_bbm;
  km_pulang.value = infoPengeluaran.km_pulang;
  tanggal.value = infoPengeluaran.tanggal;
  tujuan.value = infoPengeluaran.tujuan;
  uang_saku.value = infoPengeluaran.uang_saku;
};

const getResource = async () => {
  const checkIsUpdateAndInfo =
    !Object.keys(driver.infoPengeluaran.info).length &&
    checkParamsIdProperty.value;

  if (!driver.driver.list.length) {
    await driver.getAllDriver();
  }

  if (checkIsUpdateAndInfo) {
    await getPengeluaranInfo();
  }
};

const handleDriverChange = async () => {
  const checkIsUpdate = checkParamsIdProperty.value ? "update" : "add";
  const id = checkParamsIdProperty.value ? paramsId.value : id_driver.value;

  await driver.getDriverFaktur(id, checkIsUpdate);
  tableKey.value++;

  localStore.value = driver.listInfoFaktur.list.map((val, idx) => {
    const listOfTipe = [];
    for (let i = 6; i < 9; i++) {
      const newValueFromVal = {
        ...val,
        id_tipe: i,
        nominal: null,
        keterangan: "",
      };

      if (checkParamsIdProperty.value) {
        const idTipe = newValueFromVal?.id_tipe ?? 0;
        const nominalParkir = newValueFromVal?.nominal_parkir ?? 0;
        const nominalBongkar = newValueFromVal?.nominal_bongkar ?? 0;
        const nominalLainnya = newValueFromVal?.nominal_lainnya ?? 0;
        const keterangan = val?.keterangan || "";

        let nominal =
          idTipe === 6
            ? nominalParkir
            : idTipe === 7
            ? nominalBongkar
            : idTipe === 8
            ? nominalLainnya
            : null;

        newValueFromVal.nominal = nominal;
        newValueFromVal.keterangan = keterangan;
      }

      delete newValueFromVal["nominal_parkir"];
      delete newValueFromVal["nominal_bongkar"];
      delete newValueFromVal["nominal_lainnya"];

      listOfTipe.push(newValueFromVal);
    }
    return listOfTipe;
  });
};

const cleanDriver = () => {
  driver.listInfoFaktur.list = [];
  driver.infoPengeluaran.info = {};
};

watch(
  id_driver,
  () => {
    handleDriverChange();
  },
  { immediate: checkParamsIdProperty.value }
);

onMounted(() => getResource());
onUnmounted(() => cleanDriver());
</script>

<template>
  <div class="tw-flex tw-flex-col tw-gap-4 lg:tw-px-4 tw-px-0 tw-min-h-[700px]">
    <PengeluaranDriverPdf
      v-show="false"
      :info="driver.infoPengeluaran.info"
      :list="driver.listInfoFaktur.list" />
    <SlideRightX
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-out="0.1"
      :delay-in="0.1"
      :initial-x="-40"
      :x="40">
      <Card no-subheader no-header>
        <template #content>
          <div class="tw-w-full tw-flex tw-flex-col tw-gap-6 tw-py-8 tw-px-2">
            <BForm
              novalidate
              class="tw-w-full tw-grid tw-grid-cols-1 md:tw-grid-cols-2 tw-gap-4">
              <div
                v-if="driver.driver.loading"
                class="tw-w-full tw-h-[69px] tw-flex tw-items-end">
                <Skeleton class="tw-w-full tw-h-10" />
              </div>
              <BFormGroup
                v-else
                id="input-group-1"
                label="Nama Driver :"
                label-for="input-1"
                v-bind="idDriverProps">
                <SelectInput
                  :key="fieldKey"
                  placeholder="Pilih Driver"
                  text-field="nama"
                  search
                  value-field="id"
                  size="md"
                  :options="driver.driver.list"
                  v-model="id_driver"
                  :disabled="checkParamsIdProperty" />
              </BFormGroup>
              <BFormGroup
                id="input-group-2"
                label="Tanggal Berangkat :"
                label-for="input-2"
                v-bind="tanggalBerangkatProps">
                <VueDatePicker
                  :key="fieldKey"
                  id="input-2"
                  v-model="tanggal"
                  :enable-time-picker="false"
                  placeholder="mm/dd/yyyy"
                  :teleport="true"
                  auto-apply />
              </BFormGroup>
              <TextField
                :config-props="tujuanProps"
                v-model="tujuan"
                label="Tujuan"
                placeholder="Masukkan Tujuan" />
              <TextField
                :config-props="helperProps"
                v-model="helper"
                label="Nama helper"
                placeholder="Masukkan nama helper" />
              <TextField
                :config-props="kmBerangkatProps"
                v-model="km_berangkat"
                type="number"
                label="Km Berangkat"
                placeholder="Masukkan Km Berangkat" />
              <TextField
                :config-props="kmPulangProps"
                v-model="km_pulang"
                type="number"
                label="Km Pulang"
                placeholder="Masukkan Km Pulang" />
              <TextField
                :config-props="kmIsiBbmProps"
                v-model="km_isi_bbm"
                type="number"
                label="Km Isi Bbm"
                placeholder="Masukkan Km Isi Bbm" />
              <TextField
                :config-props="isiBbmLiterProps"
                v-model="isi_bbm_liter"
                type="number"
                label="Km Isi Bbm Liter"
                placeholder="Masukkan Km Isi Bbm Liter" />
              <TextField
                :config-props="isiBbmRupiahProps"
                v-model="isi_bbm_rupiah"
                type="number"
                label="Km Isi Bbm Rupiah"
                placeholder="Masukkan Km Isi Bbm Rupiah" />
              <TextField
                :config-props="uangSakuProps"
                v-model="uang_saku"
                type="number"
                label="Uang Saku"
                placeholder="Masukkan Uang Saku" />
            </BForm>
            <div class="tw-w-full tw-flex tw-flex-col tw-gap-10">
              <span class="tw-text-xl tw-font-bold">List Faktur</span>
              <Table
                :hideFooter="true"
                :hideToolbar="true"
                :loading="driver.listInfoFaktur.loading"
                :key="tableKey"
                :table-data="driver.listInfoFaktur.list"
                :columns="listDriverFakturColumn"
                @change="change" />
            </div>
            <div class="tw-w-full tw-flex tw-flex-col tw-items-end tw-gap-8">
              <table class="tw-w-full lg:tw-w-auto">
                <tr>
                  <td class="tw-font-bold">Subtotal</td>
                  <td class="tw-w-6 tw-text-center">:</td>
                  <td>Rp. {{ parseCurrency(subTotal) }}</td>
                </tr>
                <tr class="[&_td]:tw-pb-6">
                  <td class="tw-font-bold">Biaya Lainnya</td>
                  <td class="tw-w-6 tw-text-center">:</td>
                  <td>Rp. {{ parseCurrency(biayaLainnya) }}</td>
                </tr>
                <tr class="tw-border-t tw-border-gray-900 [&_td]:tw-pt-3">
                  <td class="tw-font-bold">Total</td>
                  <td class="tw-w-6 tw-text-center">:</td>
                  <td>Rp. {{ parseCurrency(total) }}</td>
                </tr>
              </table>
              <Button
                :trigger="submit"
                icon="mdi mdi-check"
                class="tw-w-full lg:tw-w-32 tw-h-10 lg:tw-h-9">
                {{ operandString }}
              </Button>
            </div>
          </div>
        </template>
      </Card>
    </SlideRightX>
  </div>
</template>
