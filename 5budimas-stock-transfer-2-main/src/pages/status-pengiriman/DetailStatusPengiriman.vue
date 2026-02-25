<script setup>
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import Label from "@/src/components/ui/Label.vue";
import { BFormInput } from "bootstrap-vue-next";
import { detailPengirimanStockTransferColumn } from "@/src/model/tableColumns/pengiriman/detailPengirimanStockTransfer";
import Table from "@/src/components/ui/table/Table.vue";
import { onMounted, ref } from "vue";
import { useOthers } from "@/src/store/others";
import { useStatusPengiriman } from "@/src/store/mainStore";
import { useAlert } from "@/src/store/alert";
import { useRoute, useRouter } from "vue-router";
import SelectInput from "@/src/components/ui/formInput/SelectInput.vue";
import Skeleton from "@/src/components/ui/Skeleton.vue";
import { stockTransferDetailService as detailService } from "@/src/services/stockTransferDetail";
import { status as statuses } from "@/src/lib/utils";

const alert = useAlert();
const stockTransfer = useStatusPengiriman();
const others = useOthers();
const localStore = ref({});
const route = useRoute();
const navigation = useRouter();
const loadingTable = ref(false);
const listDetail = ref([]);
const listDetailRequest = ref([]);
const keyTable = ref(0);

const getDetail = async () => {
  const filterStore = (val) => val.id_stock_transfer == route.params.id;

  const current = stockTransfer.stockTransfer.list.find(filterStore);

  if (!current) navigation.back();

  try {
    loadingTable.value = true;

    const { status, id_stock_transfer } = current;
    const jumlahString =
      status === statuses["picked"] ||
      status === statuses["konfirmasi"] ||
      status === statuses["pengiriman"]
        ? "jumlah_picked"
        : status === statuses["diterima"] ||
          status === statuses["eskalasi closed"]
        ? "jumlah_diterima"
        : status === statuses["tolak diterima"]
        ? "jumlah_ditolak"
        : "jumlah";

    const details = await detailService.getDetailStockTransfer(
      id_stock_transfer,
      null,
      jumlahString
    );

    if (
      status === statuses["eskalasi closed"] ||
      status === statuses["tolak diterima"]
    ) {
      const detailRequest = await detailService.getDetailStockTransfer(
        id_stock_transfer,
        null,
        "jumlah"
      );

      listDetailRequest.value = detailRequest;
    }

    const jumlah = details.reduce(
      (acc, detail) => acc + detail[jumlahString],
      0
    );

    localStore.value = { ...current, jumlah };
    listDetail.value = details;
  } catch (error) {
    alert.setMessage(error, "danger");
  } finally {
    loadingTable.value = false;
    keyTable.value++;
  }
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
                :model-value="localStore?.nota_stock_transfer"
                disabled
                placeholder="Nota Stock transfer" />
            </Label>
            <Label label="Tanggal Pengajuan">
              <BFormInput
                :model-value="localStore?.created_at"
                disabled
                placeholder="12-07-2024" />
            </Label>
            <Label label="Dari">
              <BFormInput
                :model-value="localStore?.nama_cabang_awal"
                disabled
                placeholder="Dari" />
            </Label>
            <Label label="Ke">
              <BFormInput
                :model-value="localStore?.nama_cabang_tujuan"
                disabled
                placeholder="ke" />
            </Label>
            <Label label="Jumlah Produk">
              <BFormInput
                :model-value="localStore?.jumlah"
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
                :model-value="localStore?.pengambilan_oleh"
                disabled
                placeholder="Pengambilan Oleh" />
            </Label>
            <Label full label="Tanggal Ambil">
              <BFormInput
                :model-value="localStore?.tanggal_ambil"
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
          <Table
            :key="keyTable"
            :loading="loadingTable"
            :columns="detailPengirimanStockTransferColumn"
            :table-data="listDetail" />
        </template>
      </Card>
      <Card
        no-subheader
        v-if="
          localStore?.status === statuses['eskalasi closed'] ||
          localStore?.status === statuses['tolak diterima']
        ">
        <template #header>List Produk Yang Direquest</template>
        <template #content>
          <Table
            :key="keyTable"
            :loading="loadingTable"
            :columns="detailPengirimanStockTransferColumn"
            :table-data="listDetailRequest" />
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>
