<script setup>
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import Label from "@/src/components/ui/Label.vue";
import {BFormInput} from "bootstrap-vue-next";
import Table from "@/src/components/ui/table/Table.vue";
import Button from "@/src/components/ui/Button.vue";
import {useAlert} from "@/src/store/alert";
import {useListEskalasi} from "@/src/store/mainStore";
import {useOthers} from "@/src/store/others";
import {onMounted, ref} from "vue";
import {useRoute, useRouter} from "vue-router";
import {stockTransferDetailService as detailService} from "@/src/services/stockTransferDetail";
import {transferService} from "@/src/services/stockTransfer";
import SelectInput from "@/src/components/ui/formInput/SelectInput.vue";
import Skeleton from "@/src/components/ui/Skeleton.vue";
import {detailListProdukEskalasi} from "@/src/model/tableColumns/listEskalasi/detailListProduk";
import {useUser} from "@/src/store/user";

const alert = useAlert();
const localStore = ref({});
const userStore = useUser();

const loadingTable = ref(false);
const loadingButton = ref(false);
const disabledButton = ref(false);

const keyTable = ref(0);
const others = useOthers();
const listDetail = ref([]);
const stockTransfer = useListEskalasi();
const navigation = useRouter();
const route = useRoute();
const idStocktransfer = route.params.id;

const navigateBack = () => {
  if (route.path != "" || route.path != "/") {
    navigation.back();
  }
};

const checkUomDiterima = () => {
  return new Promise((resolve, reject) => {
    listDetail.value.forEach((val) => {
      const valueEntries = Object.entries(val);
      const keys = ["uom_1", "uom_2", "uom_3"];
      keys.forEach((key) => {
        const check = valueEntries.some((i) => i[0] === key);
        if (!check) return reject("Jumlah diterima UOM tidak boleh kosong");
      });
    });

    return resolve("Jumlah diterima uom terisi semua");
  });
};

const change = ({value, rowIndex, columnId}) => {
  const newValue = listDetail.value.map((val, idx) => {
    if (idx === rowIndex) {
      return {
        ...val,
        [columnId]: value,
      };
    }

    return {...val};
  });

  const removedNull = newValue.map((val) => {
    const entries = Object.entries(val);
    const filter = entries.filter((i) => i[1] !== null && i[1] !== "");
    const object = Object.fromEntries(filter);
    return object;
  });
  listDetail.value = removedNull;
};

const closeEskalasi = async () => {
  checkUomDiterima()
      .then(async () => {
        try {
          disabledButton.value = true;
          loadingButton.value = true;

          const body = {
            ...localStore.value,
            list_produk: [...listDetail.value],
            id_user: userStore.user.value.id,
          };

          await transferService.postStockTransfer("close-eskalasi", body);
          await transferService.putStockTransfer(idStocktransfer, {status: 6});

          alert.setMessage(`Sukses melakukan closing request`, "success");
          navigateBack();
        } catch (error) {
          disabledButton.value = false;
          alert.setMessage(error, "danger");
        } finally {
          loadingButton.value = false;
        }
      })
      .catch((err) => {
        alert.setMessage(err, "danger");
      });
};

const fillUoms = () => {
  listDetail.value = [...listDetail.value].map((val) => ({
    ...val,
    uom_1: val.pieces_diterima,
    uom_2: val.box_diterima,
    uom_3: val.carton_diterima,
  }));
};

const getDetail = async () => {
  const filterStore = (val) => val.id_stock_transfer == idStocktransfer;

  const current = stockTransfer.stockTransfer.list.find(filterStore);

  if (!current) navigation.back();

  try {
    loadingTable.value = true;
    localStore.value = current;

    const [jumlahDatas, jumlahDiterima] = await Promise.all([
      detailService.getDetailStockTransfer(
          idStocktransfer,
          null,
          "jumlah_picked"
      ),
      detailService.getDetailStockTransfer(
          idStocktransfer,
          null,
          "jumlah_diterima"
      ),
    ]);

    const jumlahDIterimaMap = jumlahDiterima?.map((val) => ({
      pieces_diterima: val?.pieces,
      box_diterima: val?.box,
      carton_diterima: val?.carton,
    }));

    const jumlahDatasMap = jumlahDatas.map((val, idx) => ({
      ...val,
      ...jumlahDIterimaMap[idx],
    }));

    listDetail.value = jumlahDatasMap;
  } catch (error) {
    alert.setMessage(error, "danger");
  } finally {
    // fillUoms();
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
                  :model-value="localStore?.nota_stock_transfer || ''"
                  disabled
                  placeholder="Nota Stock transfer"/>
            </Label>
            <Label label="Tanggal Pengajuan">
              <BFormInput
                  :model-value="localStore.created_at"
                  disabled
                  placeholder="12-07-2024"/>
            </Label>
            <Label label="Dari">
              <BFormInput
                  :model-value="localStore.nama_cabang_awal"
                  disabled
                  placeholder="Dari"/>
            </Label>
            <Label label="Ke">
              <BFormInput
                  :model-value="localStore.nama_cabang_tujuan"
                  disabled
                  placeholder="ke"/>
            </Label>
            <Label label="Jumlah Produk">
              <BFormInput
                  :model-value="localStore.jumlah_picked"
                  disabled
                  placeholder="Jumlah Produk"/>
            </Label>
            <Label label="Armada">
              <Skeleton v-if="others.armada.loading" class="tw-w-full tw-h-9"/>
              <SelectInput
                  v-else
                  placeholder="Pilih Armada"
                  :disabled="true"
                  size="md"
                  :model-value="localStore.id_armada"
                  :search="true"
                  :options="others.armada.list"
                  text-field="nama"
                  value-field="id"/>
            </Label>
            <Label label="Pengambilan Oleh">
              <BFormInput
                  :model-value="localStore.pengambilan_oleh"
                  disabled
                  placeholder="Pengambilan Oleh"/>
            </Label>
            <Label full label="Tanggal Ambil">
              <BFormInput
                  :model-value="localStore.tanggal_ambil"
                  disabled
                  placeholder="Tanggal Pengambilan"/>
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
                :columns="detailListProdukEskalasi"
                :table-data="listDetail"/>

            <FlexBox full jus-end>
              <Button
                  :loading="loadingButton"
                  :disabled="disabledButton"
                  :trigger="closeEskalasi"
                  class="tw-bg-red-500 tw-p-2"
                  icon="mdi mdi-close">
                Close Eskalasi
              </Button>
            </FlexBox>
          </FlexBox>
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>
