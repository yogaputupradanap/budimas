<script setup>
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import Label from "@/src/components/ui/Label.vue";
import { BFormInput } from "bootstrap-vue-next";
import { detailPengirimanStockTransferColumn } from "@/src/model/tableColumns/pengiriman/detailPengirimanStockTransfer";
import Table from "@/src/components/ui/table/Table.vue";
import Button from "@/src/components/ui/Button.vue";
import { useOthers } from "@/src/store/others";
import { usePengiriman } from "@/src/store/mainStore";
import { onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import SelectInput from "@/src/components/ui/formInput/SelectInput.vue";
import { useAlert } from "@/src/store/alert";
import { stockTransferDetailService as detailService } from "@/src/services/stockTransferDetail";
import { useGeneratePdf } from "@/src/lib/useGeneratePdf";
import { definition } from "@/src/model/pdf/pengeluaranGudang";
import { format } from "date-fns";
import { id } from "date-fns/locale";
import { fetchWithAuth } from "@/src/lib/utils";
import { useUser } from "@/src/store/user";

const alert = useAlert();
const stockTransfer = usePengiriman();
const others = useOthers();
const localStore = ref();
const userStore = useUser();
const route = useRoute();
const navigation = useRouter();
const loadingTable = ref(false);
const listDetail = ref([]);
const keyTable = ref(0);
const loadingCetak = ref(false);

const cetak = async () => {
  try {
    loadingCetak.value = true;
    const param = `id_stock_transfers=[${route.params.id}]`;
    const userId = `&id_user=${userStore.user.value.id}`;
    await fetchWithAuth(
      "GET",
      `/api/stock-transfer/pengiriman-stock-transfer?${param}${userId}`
    );

    const data = { ...localStore.value, listProduk: [...listDetail.value] };
    const filename = `Bukti Pengeluaran Gudang ${format(new Date(), "PPPP", {
      locale: id,
    })}`;

    useGeneratePdf(definition, data, filename);
  } catch (error) {
    alert.setMessage(error, "danger");
  } finally {
    loadingCetak.value = false;
  }
};

const getDetail = async () => {
  const filterStore = (val) => val.id_stock_transfer == route.params.id;

  const current = stockTransfer.stockTransfer.list.find(filterStore);

  if (!current) navigation.back();

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
  } catch (error) {
    alert.setMessage(error, "danger");
  } finally {
    loadingTable.value = false;
    keyTable.value++;
  }

  localStore.value = current;
};

onMounted(() => {
  getDetail();
});
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
          <Table
            :key="keyTable"
            :loading="loadingTable"
            :columns="detailPengirimanStockTransferColumn"
            :table-data="listDetail" />
          <FlexBox full jus-end>
            <Button
              :loading="loadingCetak"
              :trigger="cetak"
              icon="mdi mdi-printer"
              class="tw-px-6 tw-py-2">
              Cetak
            </Button>
          </FlexBox>
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>
