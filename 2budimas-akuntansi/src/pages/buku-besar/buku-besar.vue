<script setup>
import { ref, computed, watch, h } from "vue";
import { format } from "date-fns";
import { useOthers } from "@/src/store/others";
import { usePagination } from "@/src/lib/usePagination";
import { useFiltering } from "@/src/lib/useFiltering";
import { useSorting } from "@/src/lib/useSorting";
import { useFetchPaginateV2 } from "@/src/lib/useFetchPaginateV2";
import { jurnalService } from "@/src/services/jurnal";
import { listBukuBesarColumn } from "@/src/model/tableColumns/jurnal/listBukuBesar";
import { parseCurrency } from "@/src/lib/utils";
import T from "@/src/components/ui/table/T.vue";
import { useBukuBesar } from "@/src/lib/useBukuBesar";


// --- UI COMPONENTS ---
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import ServerTable from "@/src/components/ui/table/ServerTable.vue";
import Label from "@/src/components/ui/Label.vue";
import SelectInput from "@/src/components/ui/formInput/SelectInput.vue";
import VueDatePicker from "@vuepic/vue-datepicker";
import Button from "@/src/components/ui/Button.vue";
import Skeleton from "@/src/components/ui/Skeleton.vue";

const others = useOthers();
const { basebukubesarUrl } = jurnalService;

// --- TABLE HOOKS ---
const { onPaginationChange, pagination } = usePagination();
const { onColumnFilterChange, globalFilters } = useFiltering();
const { onSortingChange, sorting } = useSorting();

const filter = ref({
  value: {
    text: "",
    state: "",
  }
});

// --- FILTER FORM ---
const id_coa = ref(null);
const id_cabang = ref(null);

const periodeAwal = ref(
  new Date(new Date().getFullYear(), new Date().getMonth(), 1)
);
const periodeAkhir = ref(new Date());

// --- ADVANCED FILTER PAYLOAD (REACTIVE) ---
const filterPayload = computed(() => [
  { id: "id_coa", value: id_coa.value || "" },
  { id: "periode_awal", value: format(periodeAwal.value, "yyyy-MM-dd") },
  { id: "periode_akhir", value: format(periodeAkhir.value, "yyyy-MM-dd") },
  { id: "id_cabang", value: id_cabang.value || "" },
]);


// --- FETCH DATA ---
const [fetchResponse, count, loading, totalPage, key, summary] =
  useBukuBesar(basebukubesarUrl, {
    pagination,
    sorting,
    globalFilters,
    advancedFilters: filterPayload,
  });

  console.log("=== DEBUG FETCH BUKU BESAR ===");
console.log("fetchResponse:", fetchResponse);
console.log("fetchResponse.value:", fetchResponse?.value);
console.log("count:", count?.value);
console.log("totalPage:", totalPage?.value);
console.log("loading:", loading?.value);

// --- TABLE DATA SAFE ---
const tableData = computed(() => {
  const flat = [];

  groupedData.value.forEach(group => {
    flat.push(group); // parent row
    flat.push(...group.children); // children
  });

  return flat;
});

const groupedData = computed(() => {
  if (!Array.isArray(fetchResponse.value)) return [];

  const groups = {};

  fetchResponse.value.forEach(item => {
    const parentKey = item.parent_id || item.id_coa;

    if (!groups[parentKey]) {
      groups[parentKey] = {
        isParent: true,
        nama_akun: item.nama_akun,
        children: []
      };
    }

    groups[parentKey].children.push({
      ...item,
      isChild: true
    });
  });

  return Object.values(groups);
});

// --- ACTIONS ---
const handleCariData = () => {
  pagination.value.pageIndex = 0;
};

const reset = () => {
  id_coa.value = null;
  id_cabang.value = null;
  periodeAwal.value = new Date(
    new Date().getFullYear(),
    new Date().getMonth(),
    1
  );
  periodeAkhir.value = new Date();
  pagination.value.pageIndex = 0;
};

const safeTotalPage = computed(() =>
  Number(totalPage.value) > 0 ? totalPage.value : 0
);

const safeCount = computed(() =>
  Number(count.value) > 0 ? count.value : 0
);

// --- DEBUG WATCH ---
watch(fetchResponse, (val) => {
  console.log("WATCH fetchResponse:", val);
  console.log("WATCH result:", val?.result);
});
</script>

<template>
  <FlexBox full flex-col class="tw-gap-4">
    <SlideRightX :initial-x="-40" :x="40">
      <Card no-subheader>
        <template #header>Filter Buku Besar</template>
        <template #content>
          <div class="tw-grid tw-grid-cols-1 md:tw-grid-cols-5 tw-gap-4 tw-items-end">
            <Label label="Pilih Akun (COA)">
              <SelectInput
                v-model="id_coa"
                placeholder="Pilih Akun"
                :search="true"
                :options="others.coa?.list || []"
                text-field="nama"
                value-field="id"
              />
            </Label>

            <Label label="Cabang">
              <SelectInput
                v-model="id_cabang"
                placeholder="Semua Cabang"
                :search="true"
                :options="others.cabang?.list || []"
                text-field="nama"
                value-field="id"
              />
            </Label>

            <Label label="Periode Awal">
              <VueDatePicker
                v-model="periodeAwal"
                :enable-time-picker="false"
                auto-apply
                format="yyyy-MM-dd"
              />
            </Label>

            <Label label="Periode Akhir">
              <VueDatePicker
                v-model="periodeAkhir"
                :enable-time-picker="false"
                auto-apply
                format="yyyy-MM-dd"
              />
            </Label>

            <div class="tw-flex tw-gap-2">
              <Button
                :trigger="reset"
                class="tw-bg-red-500 tw-flex-1"
                icon="mdi mdi-reload"
              >
                Reset
              </Button>
              <Button
                :trigger="handleCariData"
                class="tw-flex-1"
                icon="mdi mdi-magnify"
              >
                Cari
              </Button>
            </div>
          </div>
        </template>
      </Card>
    </SlideRightX>

    <SlideRightX :initial-x="-40" :x="40" :delay-in="0.1">
      <div class="tw-grid tw-grid-cols-1 md:tw-grid-cols-3 tw-gap-4">
        <div class="tw-p-4 tw-bg-white tw-rounded-lg tw-shadow-sm tw-border tw-text-center">
          <p class="tw-text-gray-500 tw-text-sm">Saldo Awal</p>
          <p class="tw-text-xl tw-font-bold">
            {{ parseCurrency(summary.saldo_awal) }}
          </p>
        </div>

        <div class="tw-p-4 tw-bg-white tw-rounded-lg tw-shadow-sm tw-border tw-text-center">
          <p class="tw-text-gray-500 tw-text-sm">Mutasi (D/K)</p>
          <p class="tw-text-lg tw-font-bold">
            <span class="tw-text-green-600">
              {{ parseCurrency(summary.total_debet) }}
            </span>
            <span class="tw-mx-1">/</span>
            <span class="tw-text-red-600">
              {{ parseCurrency(summary.total_kredit) }}
            </span>
          </p>
        </div>

        <div class="tw-p-4 tw-bg-blue-600 tw-rounded-lg tw-text-white tw-text-center">
          <p class="tw-opacity-90 tw-text-sm">Saldo Akhir</p>
          <p class="tw-text-xl tw-font-bold">
            {{ parseCurrency(summary.saldo_akhir) }}
          </p>
        </div>
      </div>
    </SlideRightX>

    <SlideRightX :initial-x="-40" :x="40" :delay-in="0.2">
      <Card no-subheader>
        <template #header>Detail Transaksi</template>
        <template #content>
          <div v-if="listBukuBesarColumn.length">
            <ServerTable
  :columns="listBukuBesarColumn"
  :key="key"
  :table-data="tableData || []"
  :loading="loading"
  :on-pagination-change="onPaginationChange"
  :on-global-filters-change="onColumnFilterChange"
  :on-sorting-change="onSortingChange"
  :pagination="pagination"
  :sorting="sorting"
  :filter="globalFilters"
  :page-count="totalPage"
  :total-data="count"
  table-width="tw-w-full"
            />
          </div>

          <div v-else-if="loading" class="tw-p-6">
            <Skeleton class="tw-h-10 tw-w-full tw-mb-2" />
            <Skeleton class="tw-h-10 tw-w-full tw-mb-2" />
            <Skeleton class="tw-h-10 tw-w-full" />
          </div>
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>