<script setup>
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import Label from "@/src/components/ui/Label.vue";
import ServerTable from "@/src/components/ui/table/ServerTable.vue";
import Table from "@/src/components/ui/table/Table.vue";
import { useTableSearch } from "@/src/lib/useTableSearch";
import { useFetchPaginate } from "@/src/lib/useFetchPaginate";
import { ref, onMounted, computed } from "vue";
import { listCanvasOrderDetailColumn } from "@/src/model/tableColumns/canvas-order/detail";
import { useSorting } from "@/src/lib/useSorting";
import { usePagination } from "@/src/lib/usePagination";
import { useFiltering } from "@/src/lib/useFiltering";
import { salesCanvasService } from "@/src/services/salesCanvas";
import { breakdownToUOM, formatNumber } from "@/src/lib/utils";
import { useUser } from "@/src/store/user";
import { useRoute } from "vue-router";
import { useOthers } from "@/src/store/others";


const route = useRoute();
const userStore = useUser();
const othersStore = useOthers();

const user = userStore.user.value;
const canvasOrderId = route.params.id_canvas_order;
const userBranch = computed(() => user?.nama_cabang);
const principalName = computed(() => user?.principal)

const { endpoints } = salesCanvasService;
const { onSortingChange, sorting } = useSorting();
const { onPaginationChange, pagination } = usePagination();
const { onColumnFilterChange, globalFilters } = useFiltering();

const fetchUrl = computed(() => {
  const user = userStore.user.value;
  return user?.id ? `${endpoints}/detail-canvas-order?id_canvas_order=${canvasOrderId}` : null;
})
    
const [data, count, loading, totalPage, key] = useFetchPaginate(
  fetchUrl,
  {
    pagination,
    sorting,
    globalFilters,
    initialSortColumn: "nama_produk",
  }
);

const fieldPool = [];

const queryEntries = computed(() => {
  if (reset.value) return [];
  const entries = [];

  if (globalFilters.value?.text && globalFilters.value?.text.trim() !== "") {
    entries.push(["filters=", globalFilters.value?.text]);
  }
  return entries.filter(([_, v]) => v !== undefined && v !== null && v !== "");
});

const options = {
  initialColumnName: "nama_produk",
  checkFieldFilterFunc: (val) => val[1] === undefined || val[1] === null,
  filterFunction: (val) => val[1] !== undefined && val[1] !== null,
  asArgument: true,
};

const [
    clientData,  
    buttonText,
    ,    
    isServerTable,     
    clientKey,        
    searchQuery,       
    reset 
] = useTableSearch(fetchUrl, fieldPool, queryEntries, options);

const tableDataWithUOM = computed(() => {
  const rawData = Array.isArray(data.value?.pages) 
    ? data.value.pages : Array.isArray(data.value) 
    ? data.value : [];

    return rawData.map(row => {
    const totalPieces =
      (Number(row.qty_uom1) || 0) * (Number(row.uom1_factor) || 1) +
      (Number(row.qty_uom2) || 0) * (Number(row.uom2_factor) || 1) +
      (Number(row.qty_uom3) || 0) * (Number(row.uom3_factor) || 1);

    // Breakdown ke UOM
    const breakdown = breakdownToUOM(totalPieces, {
      uom1_factor: Number(row.uom1_factor) || 1,
      uom2_factor: Number(row.uom2_factor) || 1,
      uom3_factor: Number(row.uom3_factor) || 1,
    });

    console.log("Breakdown:", breakdown);
    console.log("Row before:", row);
    console.log("Row after:", {
      ...row,
      qty_uom1: breakdown.uom1,
      qty_uom2: breakdown.uom2,
      qty_uom3: breakdown.uom3,
      total_pieces: totalPieces,
    });
    console.log("Total Pieces:", totalPieces);

    return {
      ...row,
      qty_uom1: breakdown.uom1,
      qty_uom2: breakdown.uom2,
      qty_uom3: breakdown.uom3,
      total_pieces: totalPieces,
    };
  });
});

const customerName = computed(() => {
  const rows = tableDataWithUOM.value;
  if (Array.isArray(rows) && rows.length > 0) { return rows[0].nama_customer || "-" }
  return "-";
})

const tanggalOrder = computed(() => {
  const rows = tableDataWithUOM.value;
  if (Array.isArray(rows) && rows.length > 0) { return rows[0].tanggal_order || "-" }
  return "-";
})

const subTotalBeforeDiscount = computed(() => {
  const rows = tableDataWithUOM.value;
  if (!Array.isArray(rows)) return 0;
  return rows.reduce((total, row) => {
    return total + (Number(row.subtotal_harga) || 0);
  }, 0);
});

const totalDiskon = computed(() => {
  const rows = tableDataWithUOM.value;
  if (!Array.isArray(rows)) return 0;
  return rows.reduce((total, row) => total + (Number(row.total_diskon) || 0), 0);
});

const subTotal = computed(() => {
  return subTotalBeforeDiscount.value - totalDiskon.value;
});

const pajak = computed(() => {
  const rows = tableDataWithUOM.value;
  if (!Array.isArray(rows)) return 0;
  return rows.reduce((total, row) => {
    const ppn = Number(row.ppn) || 0;
    const jumlahHargaSementara = Number(row.subtotal_harga) || 0;
    return total + (jumlahHargaSementara * ppn / 100);
  }, 0);
});

const total = computed(() => { 
  return subTotal.value + pajak.value;
});

const checkCurrencyMinus = (value) => { 
  return value < 1 ? 0 : formatNumber(value);
};

onMounted(async () => { await othersStore.getOthers()});

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
        <template #header>Informasi Sales Canvas</template>
        <template #content>
            <div class="form-grid-card tw-grid-cols-3 tw-items-end">
            <Label label="Tanggal">
              <BFormInput
                size="md"
                readonly
                placeholder="yyyy-mm-dd"
                :class="'tw-bg-gray-200'"
                :model-value="tanggalOrder"
              />
            </Label>
            <Label label="Cabang">
              <BFormInput
                size="md"
                readonly
                placeholder="Pilih Data"
                :class="'tw-bg-gray-200'"
                :model-value="userBranch"
              />
            </Label>
            <Label label="Principal">
              <BFormInput
                size="md"
                readonly
                placeholder="Principal"
                :model-value="principalName"
                :class="'tw-bg-gray-200'"
              />
            </Label>
             <Label label="Customer">
              <BFormInput
                size="md"
                readonly
                placeholder="Customer"
                :model-value="customerName"
                :class="'tw-bg-gray-200'"
              />
            </Label>
          </div>
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
  <FlexBox full flex-col>
    <SlideRightX
      class="slide-container"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.1"
      :delay-out="0.1"
      :initial-x="-40"
      :x="40"
    >
      <Card no-subheader>
        <template #header>Form Canvas Request</template>
        <template #content>
          <div class="tw-w-full tw-pb-10">
            <ServerTable
                v-if="isServerTable"
                table-width="tw-w-full"
                :columns="listCanvasOrderDetailColumn"
                :key="key"
                :table-data="tableDataWithUOM"
                :loading="loading"
                :on-pagination-change="onPaginationChange"
                :on-global-filters-change="onColumnFilterChange"
                :on-sorting-change="onSortingChange"
                :pagination="pagination"
                :sorting="sorting"
                :filter="globalFilters"
                :page-count="totalPage"
                :total-data="count"
                :hideFooter="false"
            />
            <Table
                v-else
                :key="clientKey"
                :columns="listCanvasOrderDetailColumn"
                :table-data="clientData"
                :hideFooter="false"
            />
            <div>
              <FlexBox gap="small" flex-col full class="tw-px-4 tw-mt-6">
                <div
                  class="tw-w-full md:tw-w-96 tw-ml-auto tw-bg-gray-50 tw-rounded-lg tw-p-4 tw-shadow-sm">
                  <h3
                    class="tw-font-semibold tw-text-gray-700 tw-mb-3 tw-text-base">
                    Rincian Pembayaran
                  </h3>

                  <div class="tw-flex tw-justify-between tw-py-2">
                    <span class="tw-text-gray-600">Sub Total (Sebelum Diskon)</span>
                    <span class="tw-font-medium">
                      Rp. {{ checkCurrencyMinus(subTotalBeforeDiscount) }}
                    </span>
                  </div>

                  <div
                    class="tw-flex tw-justify-between tw-py-2 tw-border-b tw-border-gray-400">
                    <span class="tw-text-gray-600">Total Diskon</span>
                    <span class="tw-font-medium tw-text-red-500">
                      - Rp. {{ checkCurrencyMinus(totalDiskon) }}
                    </span>
                  </div>

                  <div class="tw-flex tw-justify-between tw-py-2">
                    <span class="tw-text-gray-600">Sub Total</span>
                    <span class="tw-font-medium">
                      Rp. {{ checkCurrencyMinus(subTotal) }}
                    </span>
                  </div>

                  <div
                    class="tw-flex tw-justify-between tw-py-2 tw-border-b tw-border-gray-400">
                    <span class="tw-text-gray-600">PPN</span>
                    <span class="tw-font-medium">
                      + Rp. {{ checkCurrencyMinus(pajak) }}
                    </span>
                  </div>

                  <div
                    class="tw-flex tw-justify-between tw-py-3 tw-mt-2 tw-bg-blue-50 tw-rounded-md tw-px-3">
                    <span class="tw-font-bold tw-text-gray-800">Total</span>
                    <span class="tw-font-bold tw-text-lg tw-text-blue-700">
                      Rp. {{ checkCurrencyMinus(total) }}
                    </span>
                  </div>
                </div>
              </FlexBox>
            </div>
          </div>
      </template>

      </Card>
    </SlideRightX>
  </FlexBox>
</template>
