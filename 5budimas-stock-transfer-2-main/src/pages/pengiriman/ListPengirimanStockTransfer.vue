<script setup>
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import { listPengirimanStockTransferColumn } from "@/src/model/tableColumns/pengiriman/listPengirimanStockTransfer";
import Table from "@/src/components/ui/table/Table.vue";
import Button from "@/src/components/ui/Button.vue";
import { usePengiriman } from "@/src/store/mainStore";
import { computed, onMounted, ref, watch } from "vue";
import { definition } from "@/src/model/pdf/mutasiGudang";
import { fetchWithAuth } from "@/src/lib/utils";
import { useAlert } from "@/src/store/alert";
import { useGeneratePdf } from "@/src/lib/useGeneratePdf";
import { format } from "date-fns";
import { id } from "date-fns/locale";
import { useUser } from "@/src/store/user";

const alert = useAlert();
const stockTransfer = usePengiriman();
const userStore = useUser();
const tableRef = ref();
const count = ref(0);
const selectedRow = computed(() => tableRef.value?.getSelectedRow());
const loadingCetak = ref(false);

const filterData = () => {
  const keysArray = Object.keys(selectedRow.value);
  const getFilterData = (value) => {
    const atData = stockTransfer.stockTransfer.list.at(parseInt(value));
    return atData;
  };
  const returnedData = keysArray.map(getFilterData);
  return returnedData;
};

const getPengiriman = () => {
  stockTransfer.getStockTransfer(
    ["picked", "pengiriman"],
    [
      "id_stock_transfer",
      "nota_stock_transfer",
      "created_at",
      "id_cabang_awal",
      "id_cabang_tujuan",
      "nama_cabang_awal",
      "nama_cabang_tujuan",
      "jumlah_picked",
      "id_armada",
      "jumlah",
      "status",
      "pengambilan_oleh",
      "tanggal_ambil",
    ]
  );
};

const cetak = async () => {
  const datas = filterData();

  if (!datas.length) return;

  try {
    loadingCetak.value = true;
    const encodeIds = encodeURIComponent(
      `[${datas.map((val) => val.id_stock_transfer)}]`
    );
    const ids = `id_stock_transfers=${encodeIds}`;
    const userId = `&id_user=${userStore.user.value.id}`; 
    const res = await fetchWithAuth(
      "GET",
      `/api/stock-transfer/pengiriman-stock-transfer?${ids}${userId}` 
    );
    const detail = { user: userStore.user.value, listStockTransfer: [...res] };
    const currDate = format(new Date(), "PPPP", {
      locale: id,
    });

    const filename = `Mutasi Gudang ${currDate}`;
    useGeneratePdf(definition, detail, filename);
  } catch (error) {
    console.error(error);
    alert.setMessage(error, "danger");
  } finally {
    loadingCetak.value = false;
    getPengiriman();
  }
};

watch(selectedRow, (newValue) => {
  if (newValue) count.value = Object.values(newValue).length;
});
onMounted(() => getPengiriman());
</script>

<template>
  <FlexBox full flex-col>
    <SlideRightX
      class="slide-container"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.2"
      :delay-out="0.1"
      :initial-x="-40"
      :x="40">
      <Card no-subheader>
        <template #header>Pengiriman Stock Transfer</template>
        <template #content>
          <FlexBox full flex-col>
            <FlexBox
              full
              jus-between
              it-center
              class="tw-flex-wrap md:tw-flex-nowrap tw-sticky tw-top-0 tw-bg-white tw-py-4 tw-z-10">
              <FlexBox it-center no-left-padding>
                <Button
                  :trigger="cetak"
                  class="tw-w-28 tw-h-9"
                  icon="mdi mdi-printer">
                  Cetak
                </Button>
                <span class="tw-text-xs md:tw-text-sm">
                  <span class="tw-font-bold tw-text-xs md:tw-text-base tw-mr-1">
                    {{ count }}
                  </span>
                  Pengiriman dipilih untuk dicetak
                </span>
              </FlexBox>
              <span
                class="tw-text-[10px] tw-w-72 tw-text-left md:tw-text-right tw-pr-4">
                <span class="tw-text-red-500 tw-font-bold">**</span>
                Nota yang dicetak akan otomatif berubah status menjadi
                "pengiriman"
              </span>
            </FlexBox>
            <Table
              ref="tableRef"
              class="tw-mb-8"
              :loading="stockTransfer.stockTransfer.loading"
              :key="stockTransfer.stockTransfer.key"
              :columns="listPengirimanStockTransferColumn"
              :table-data="stockTransfer.stockTransfer.list" />
          </FlexBox>
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>
