<script setup>
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import Label from "@/src/components/ui/Label.vue";
import { BFormInput } from "bootstrap-vue-next";
import { detailPenerimaanBarangColumn } from "@/src/model/tableColumns/penerimaan-barang/detailPenerimaanBarang";
import Table from "@/src/components/ui/table/Table.vue";
import Button from "@/src/components/ui/Button.vue";
import { useAlert } from "@/src/store/alert";
import { usePenerimaanBarang } from "@/src/store/mainStore";
import { useOthers } from "@/src/store/others";
import { onMounted, reactive, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { stockTransferDetailService as detailService } from "@/src/services/stockTransferDetail";
import { transferService } from "@/src/services/stockTransfer";
import SelectInput from "@/src/components/ui/formInput/SelectInput.vue";
import Skeleton from "@/src/components/ui/Skeleton.vue";
import { format } from "date-fns";
import { useUser } from "@/src/store/user";

const alert = useAlert();
const stockTransfer = usePenerimaanBarang();
const others = useOthers();
const localStore = ref();
const route = useRoute();
const navigation = useRouter();
const userStore = useUser();
const loadingTable = ref(false);
const listDetail = ref([]);
const keyTable = ref(0);
const buttonLoading = reactive({
  terima: false,
  eskalasi: false,
  tolak: false,
});
const buttonDisable = ref({
  tolak: false,
  eskalasi: false,
  terima: false,
});

const changeAllButtonDisable = (value) => {
  const entries = Object.entries({ ...buttonDisable.value });
  const allTrue = entries.map((val) => [val[0], value]);
  buttonDisable.value = Object.fromEntries(allTrue);
};

const navigateBack = () => {
  if (route.path != "" || route.path != "/") {
    navigation.back();
  }
};

const basePost = async (commit, loadingName, body, method = "POST") => {
  try {
    changeAllButtonDisable(true);
    buttonLoading[loadingName] = true;

    if (method === "POST") {
      await transferService.postStockTransfer(commit, body);
    } else if (method === "PUT") {
      const id = localStore.value.id_stock_transfer;
      await transferService.putStockTransfer(id, body);
    }
    alert.setMessage(
      `sukses melakukan ${commit || "update"} barang`,
      "success"
    );
    navigateBack();
  } catch (error) {
    changeAllButtonDisable(false);
    alert.setMessage(error, "danger");
  } finally {
    buttonLoading[loadingName] = false;
  }
};

const checkUomDiterima = () => {
  return new Promise((resolve, reject) => {
    const isValid = listDetail.value.every((item) => {
      return item.uom_1 || item.uom_2 || item.uom_3;
    });

    if (!isValid) {
      return reject("Jumlah diterima tidak boleh kosong, minimal salah satu kolom harus diisi");
    }

    return resolve("Jumlah diterima terisi semua");
  });
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

const terima = () => {
  let duration = 2000;

  checkUomDiterima()
    .then(() => {
      const listProducts = listDetail.value.map(item => ({
        ...item,
        uom_1: item.uom_1 || 0,
        uom_2: item.uom_2 || 0,
        uom_3: item.uom_3 || 0,
      }))

      const body = {
        ...localStore.value,
        list_produk: listProducts,
        id_user: userStore.user.value.id,
      };

      for (let i = 0; i < listDetail.value.length; i++) {
        const { pieces, box, carton, uom_1, uom_2, uom_3 } = listDetail.value[i];
        
        if ((uom_1 && Number(uom_1) !== pieces) ||
            (uom_2 && Number(uom_2) !== box) ||
            (uom_3 && Number(uom_3) !== carton)) {
          duration = 10000;
          throw "Jika jumlah barang yang diterima berbeda dengan jumlah yang direquest maka harus masuk ke list eskalasi";
        }
      }

      basePost("penerimaan", "terima", body);
    })
    .catch((err) => alert.setMessage(err, "danger", duration));
};

const tolak = () => {
  checkUomDiterima()
    .then(() => {
      const body = { ...localStore.value, list_produk: [...listDetail.value] };
      basePost("tolak", "tolak", body);
    })
    .catch((err) => {
      alert.setMessage(`${err} jika ingin menolak stock transfer`, "danger");
    });
};

const eskalasi = () => {
  const body = {
    status: 4,
    tanggal_diterima: format(new Date(), "yyyy-MM-dd"),
  };
  basePost(null, "eskalasi", body, "PUT");
};

const getDetail = async () => {
  const filterStore = (val) => val.id_stock_transfer == route.params.id;

  const current = stockTransfer.stockTransfer.list.find(filterStore);

  if (!current) navigation.back();

  try {
    loadingTable.value = true;
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
  } catch (error) {
    alert.setMessage(error, "danger");
  } finally {
    loadingTable.value = false;
    keyTable.value++;
  }

  localStore.value = current;
};

onMounted(() => getDetail());
</script>

<template>
  <FlexBox full flex-col>
    <SlideRightX
      class="slide-container"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.1"
      :delay-out="0.1"
      :initial-x="-40"
      :x="40">
      <Card no-subheader>
        <template #header>Detail Pengiriman</template>
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
                :model-value="localStore.created_at"
                disabled
                placeholder="12-07-2024" />
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
                :model-value="localStore.jumlah_picked"
                disabled
                placeholder="Jumlah Produk" />
            </Label>
            <Label label="Armada">
              <Skeleton v-if="others.armada.loading" class="tw-w-full tw-h-9" />
              <SelectInput
                v-else
                placeholder="Pilih Armada"
                :disabled="true"
                size="md"
                :model-value="localStore.id_armada"
                :search="true"
                :options="others.armada.list"
                text-field="nama"
                value-field="id" />
            </Label>
            <Label label="Pengambilan Oleh">
              <BFormInput
                :model-value="localStore.pengambilan_oleh"
                disabled
                placeholder="Pengambilan Oleh" />
            </Label>
            <Label full label="Tanggal Ambil">
              <BFormInput
                :model-value="localStore.tanggal_ambil"
                disabled
                placeholder="Tanggal Pengambilan" />
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
          <FlexBox full flex-col gap="medium">
            <Table
              @change="change"
              :key="keyTable"
              :loading="loadingTable"
              classic
              table-width="tw-w-[1500px]"
              :columns="detailPenerimaanBarangColumn"
              :table-data="listDetail" />
            <FlexBox full jus-end gap="medium">
              <Button
                :trigger="tolak"
                :loading="buttonLoading.tolak"
                :disabled="buttonDisable.tolak"
                icon="mdi mdi-close"
                class="tw-px-6 tw-py-2 tw-bg-red-600 tw-text-white">
                Tolak
              </Button>
              <Button
                :trigger="eskalasi"
                :disabled="buttonDisable.eskalasi"
                :loading="buttonLoading.eskalasi"
                icon="mdi mdi-arrow-top-right-thick"
                class="tw-bg-purple-600 tw-text-white tw-px-6 tw-py-2">
                Eskalasi
              </Button>
              <Button
                :disabled="buttonDisable.terima"
                :loading="buttonLoading.terima"
                :trigger="terima"
                icon="mdi mdi-check"
                class="tw-bg-green-600 tw-text-white tw-px-6 tw-py-2">
                Terima
              </Button>
            </FlexBox>
          </FlexBox>
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>
