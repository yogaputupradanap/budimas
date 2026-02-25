<script setup>
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import Label from "@/src/components/ui/Label.vue";
import { BFormInput } from "bootstrap-vue-next";
import { detailPengajuanTransferColumn } from "@/src/model/tableColumns/konfirmasi/detailPengajuanTransfer";
import VueDatePicker from "@vuepic/vue-datepicker";
import Table from "@/src/components/ui/table/Table.vue";
import Button from "@/src/components/ui/Button.vue";
import { useKonfirmasi } from "@/src/store/mainStore";
import { computed, onMounted, reactive } from "vue";
import { stockTransferDetailService as detailService } from "@/src/services/stockTransferDetail";
import { useAlert } from "@/src/store/alert";
import { useRoute, useRouter } from "vue-router";
import { ref } from "vue";
import { format, formatISO } from "date-fns";
import { transferService } from "@/src/services/stockTransfer";
import { deepCopy, status } from "@/src/lib/utils";
import SelectInput from "@/src/components/ui/formInput/SelectInput.vue";
import Skeleton from "@/src/components/ui/Skeleton.vue";
import { useOthers } from "@/src/store/others";
import { useUser } from "@/src/store/user";

const alert = useAlert();
const router = useRoute();
const navigation = useRouter();
const userStore = useUser();

const stockTransfer = useKonfirmasi();
const others = useOthers();

const localStore = ref({});

const id = parseInt(router.params.id);
const konfirmasiStatus = ref(localStore.status);

const loadingTable = ref(false);
const keyTable = ref(0);
const loadingButton = reactive({
  send: false,
  tolak: false,
});
const disabledButton = ref(false);
const submitDisableButton = ref(false);

const buttonText = reactive({
  send: "Terima",
  tolak: "Tolak",
  picking: "Submit",
});

const form = reactive({
  armada: null,
  pengambil: null,
  tanggal_ambil: null,
});

const listDetail = ref([]);

const checkGrantAccess = (access) => {
  const konfirmasiAccess = userStore.userAccess?.find(
    (val) => val.name === "konfirmasi"
  );
  const isGranted = konfirmasiAccess.grant.some((val) => val === access);
  return isGranted;
};

const isHaveKonfirmasiAccess = computed(() => checkGrantAccess("konfirmasi"));
const isHavePickingAccess = computed(() => checkGrantAccess("picking"));

const navigateBack = () => {
  if (router.path != "" || router.path != "/") {
    navigation.back();
  }
};

const checkFields = (obj) => {
  const check = Object.values(obj).some((val) => val === "" || val === null);
  if (check) {
    throw "semua field tidak boleh kosong";
  }
};

const getDetail = async () => {
  const currentStockTransfer = (val) =>
    val.id_stock_transfer === id &&
    (val.status === status["request"] || val.status === status["konfirmasi"]);

  const current = stockTransfer.stockTransfer.list.find(currentStockTransfer);

  if (!current) navigation.back();

  konfirmasiStatus.value = current.status;

  try {
    loadingTable.value = true;

    console.log("localStore:", localStore);
    const id = current.id_stock_transfer;
    localStore.value = current;
    // Menentukan kolom berdasarkan status
    const columnToSelect = current.status === 0 ? "jumlah" : "jumlah_picked";

    // Memanggil service dengan parameter status dan kolom yang sesuai
    listDetail.value = await detailService.getDetailStockTransfer(
      id,
      null,
      columnToSelect
    );

    form.armada = current.id_armada;
    form.pengambil = current.pengambilan_oleh;
    form.tanggal_ambil = current.tanggal_ambil;

    if (current.status === 0) submitDisableButton.value = true;
    if (!listDetail.value.length || current.status === 1) {
      disabledButton.value = true;
    }
  } catch (error) {
    alert.setMessage(error, "danger");
  } finally {
    loadingTable.value = false;
    keyTable.value++;
  }
};

const konfirmasi = async () => {
  const copyForm = deepCopy(form);
  delete copyForm.pengambil;
  delete copyForm.tanggal_ambil;

  try {
    checkFields(copyForm);
    loadingButton.send = true;

    const { armada } = form;
    const body = {
      armada,
      ...localStore.value,
      products: [...listDetail.value],
    };

    await transferService.postStockTransfer("konfirmasi", body);

    disabledButton.value = true;
    buttonText.send = "Telah diterima";
    konfirmasiStatus.value = 1;
    alert.setMessage("request berhasil dikonfirmasi", "success");
    navigateBack();
  } catch (error) {
    alert.setMessage(error, "danger");
  } finally {
    loadingButton.send = false;
  }
};

const tolak = async () => {
  try {
    loadingButton.tolak = true;
    const body = { status: status["tolak konfirmasi"] };
    await transferService.putStockTransfer(id, body);

    disabledButton.value = true;
    buttonText.tolak = "Telah ditolak";
    alert.setMessage("request telah ditolak");
    navigateBack();
  } catch (error) {
    alert.setMessage(error, "danger");
  } finally {
    loadingButton.tolak = false;
  }
};

const submitPicking = async () => {
  const copyForm = deepCopy(form);
  delete copyForm["armada"];

  try {
    checkFields(copyForm);
    loadingButton.send = true;

    const { pengambil: pengambilan_oleh, tanggal_ambil: t } = form;
    const tanggal_ambil = formatISO(new Date(t));

    const body = {
      armada: form.armada,
      ...localStore.value,
      products: [...listDetail.value],
      pengambilan_oleh,
      tanggal_ambil,
      status: status["picked"],
    };

    await transferService.postStockTransfer("konfirmasi-admin", body);

    submitDisableButton.value = true;
    buttonText.picking = "Berhasil Submit";
    alert.setMessage("Berhasil dikonfirmasi ", "success");
    navigateBack();
  } catch (error) {
    alert.setMessage(error, "danger");
  } finally {
    loadingButton.send = false;
  }
};
const change = ({ value, rowIndex, columnId }) => {
  const newValue = listDetail.value.map((val, idx) => {
    if (idx === rowIndex) {
      return {
        ...val,
        [columnId]: value,
      };
    }

    return { ...val };
  });

  const removedNull = newValue.map((val) => {
    const entries = Object.entries(val);
    const filter = entries.filter((i) => i[1] !== null && i[1] !== "");
    const object = Object.fromEntries(filter);
    return object;
  });
  listDetail.value = removedNull;
};

onMounted(() => getDetail());
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
      <Card>
        <template #header>Detail Pengajuan</template>
        <template #subheader>
          <h2
            v-if="konfirmasiStatus === 0"
            class="tw-text-red-500 tw-font-bold">
            Request belum di konfirmasi
          </h2>
          <h2
            v-else-if="konfirmasiStatus === 1"
            class="tw-text-yellow-500 tw-font-bold">
            Request sudah di konfirmasi oleh Kepala Gudang
          </h2>
          <h2 v-else class="tw-text-green-500 tw-font-bold">
            Request sudah di konfirmasi oleh Admin Gudang
          </h2>
        </template>
        <template #content>
          <div class="form-grid-card">
            <Label label="Nota Stock Transfer">
              <BFormInput
                :model-value="localStore.nota_stock_transfer"
                disabled
                placeholder="Nota Stock transfer" />
            </Label>
            <Label label="Tanggal Pengajuan">
              <BFormInput
                :model-value="format(new Date(localStore.created_at), 'P')"
                disabled
                placeholder="Tanggal Pengiriman" />
            </Label>
            <Label label="Dari">
              <BFormInput
                :model-value="localStore.nama_cabang_awal"
                disabled
                placeholder="Dari" />
            </Label>
            <Label label="Ke">
              <BFormInput
                :model-value="localStore.nama_cabang_tujuan"
                disabled
                placeholder="ke" />
            </Label>
            <Label label="Jumlah Produk">
              <BFormInput
                :model-value="localStore.jumlah"
                disabled
                placeholder="Jumlah Produk" />
            </Label>
            <Label label="Armada">
              <Skeleton v-if="others.armada.loading" class="tw-w-full tw-h-9" />
              <SelectInput
                v-else
                placeholder="Pilih Armada"
                :disabled="!isHaveKonfirmasiAccess"
                size="md"
                v-model="form.armada"
                :search="true"
                :options="others.armada.list"
                text-field="nama"
                value-field="id" />
            </Label>
            <Label label="Pengambilan Oleh">
              <BFormInput
                :model-value="localStore.pengambilan_oleh"
                placeholder="Pengambilan Oleh"
                :disabled="!isHavePickingAccess"
                v-model="form.pengambil" />
            </Label>
            <Label full label="Tanggal Ambil">
              <VueDatePicker
                :disabled="!isHavePickingAccess"
                v-model="form.tanggal_ambil"
                :enable-time-picker="false"
                placeholder="mm/dd/yyyy"
                :teleport="true"
                auto-apply />
            </Label>
          </div>
        </template>
      </Card>
    </SlideRightX>
    <SlideRightX
      class="slide-container"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.2"
      :delay-out="0.1"
      :initial-x="-40"
      :x="40">
      <Card no-subheader>
        <template #header>List Produk</template>
        <template #content>
          <FlexBox full flex-col>
            <Table
              @change="change"
              :key="keyTable"
              :loading="loadingTable"
              :columns="detailPengajuanTransferColumn"
              :table-data="listDetail" />
            <FlexBox v-if="isHaveKonfirmasiAccess" full jus-end>
              <Button
                :trigger="tolak"
                :disabled="disabledButton"
                :loading="loadingButton.tolak"
                icon="mdi mdi-close"
                class="tw-px-6 tw-py-2 tw-bg-red-600">
                {{ buttonText.tolak }}
              </Button>
              <Button
                :trigger="konfirmasi"
                :disabled="disabledButton"
                :loading="loadingButton.send"
                icon="mdi mdi-check"
                class="tw-px-6 tw-py-2 tw-bg-green-600">
                {{ buttonText.send }}
              </Button>
            </FlexBox>
            <FlexBox v-if="isHavePickingAccess" full jus-end>
              <Button
                :trigger="submitPicking"
                :disabled="submitDisableButton"
                :loading="loadingButton.send"
                icon="mdi mdi-check"
                class="tw-px-6 tw-py-2 tw-bg-green-600">
                {{ buttonText.picking }}
              </Button>
            </FlexBox>
          </FlexBox>
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>
