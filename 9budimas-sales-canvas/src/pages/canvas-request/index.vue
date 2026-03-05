<script setup>
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import Label from "@/src/components/ui/Label.vue";
import Button from "@/src/components/ui/Button.vue";
import ServerTable from "@/src/components/ui/table/ServerTable.vue";
import Table from "@/src/components/ui/table/Table.vue";
import { useTableSearch } from "@/src/lib/useTableSearch";
import { useFetchPaginate } from "@/src/lib/useFetchPaginate";
import { ref, onMounted, computed, reactive, watch } from "vue";
import { listCanvasRequestColumn } from "@/src/model/tableColumns/canvas-request";
import { useSorting } from "@/src/lib/useSorting";
import { usePagination } from "@/src/lib/usePagination";
import { useFiltering } from "@/src/lib/useFiltering";
import { salesCanvasService } from "@/src/services/salesCanvas";
import { simpleDateNow, parseCurrency } from "@/src/lib/utils";
import { useRouter } from "vue-router";
import { useUser } from "@/src/store/user";
import { useOthers } from "@/src/store/others";

const router = useRouter();
const userStore = useUser();
const othersStore = useOthers();

const tanggalRequest = ref(new Date());
const userBranch = computed(() => userStore.user.value?.nama_cabang);

const salesCanvasState = reactive({
  plafonLimit: 0,
  sisaPlafon: 0,
});

const fetchTableUrl = computed(() => {
  const user = userStore.user.value;
  
  // Gunakan optional chaining (?.) untuk mencegah error reading property
  const userId = user?.id_user || user?.id;

  if (!userId) {
    console.warn("DEBUG: ID User belum siap...");
    return null;
  }

  return `${endpoints}/all-canvas-request?id_user=${userId}`;
});

const { endpoints } = salesCanvasService;
const { onSortingChange, sorting } = useSorting();
const { onPaginationChange, pagination } = usePagination();
const { onColumnFilterChange, globalFilters } = useFiltering();

const fieldPool = [tanggalRequest];

const queryEntries = computed(() => {
  if (reset.value) return [];

  const entries = [
    ["tanggal_request=", tanggalRequest.value],
  ];

  if (globalFilters.text && globalFilters.text.trim() !== "") {
    entries.push(["filters=", globalFilters.text]);
  }
  return entries.filter(([_, v]) => v !== undefined && v !== null && v !== "");
});

const options = {
  initialColumnName: "tanggal_request",
  checkFieldFilterFunc: (val) => val[1] === undefined || val[1] === null,
  filterFunction: (val) => val[1] !== undefined && val[1] !== null,
  asArgument: true,
};

const [data, count, loading, totalPage, key] = useFetchPaginate(
  fetchTableUrl,
  {
    pagination,
    sorting,
    globalFilters,
    initialSortColumn: "tanggal_request",
  }
);

const [
    clientData,  
    buttonText,
    ,    
    isServerTable,     
    clientKey,        
    searchQuery,
    reset
] = useTableSearch(fetchTableUrl, fieldPool, queryEntries, options);

const redirectToAddCanvasRequest = () => router.push({ name: "Tambah Canvas Request" });

const plafonLimitDisplay = computed(() => {
  if (salesCanvasState.plafonLimit === null) return "Loading...";
  return parseCurrency(salesCanvasState.plafonLimit);
});

const sisaPlafonDisplay = computed(() => {
  if (salesCanvasState.sisaPlafon === null) return "Loading...";
  return parseCurrency(salesCanvasState.sisaPlafon);
});

watch(() => othersStore.salesCanvas.list,
  (newVal) => {
    if (newVal) {
      salesCanvasState.plafonLimit = Number(newVal.plafon_limit) || 0;
      salesCanvasState.sisaPlafon = Number(newVal.sisa_plafon) || 0;
    }
  },{ immediate: true });

onMounted(async () => { await othersStore.getOthers() });

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
            <div class="form-grid-card tw-items-end">
            <Label label="Tanggal Request">
              <BFormInput
                size="md"
                readonly
                placeholder="yyyy-mm-dd"
                :class="'tw-bg-gray-200'"
                :model-value="simpleDateNow(tanggalRequest)"
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
            <Label label="Limit Plafon">
              <BFormInput
                size="md"
                readonly
                placeholder="Rp. 0"
                :class="'tw-bg-gray-200'"
                :model-value="plafonLimitDisplay"
              />
            </Label>
            <Label label="Sisa Plafon">
              <BFormInput
                size="md"
                readonly
                placeholder="Rp. 0"
                :class="'tw-bg-gray-200'"
                :model-value="sisaPlafonDisplay"
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
            <template #header>List Request</template>
            <template #content>
            <FlexBox full jusEnd class="tw-px-4">
              <Button
                :trigger="redirectToAddCanvasRequest"
                icon="mdi mdi-plus"
                class="tw-py-2 tw-px-4"
              >
                Tambah
              </Button>
            </FlexBox>
            <ServerTable
                v-if="isServerTable"
                table-width="tw-w-full"
                :columns="listCanvasRequestColumn"
                :key="key"
                :table-data="data"
                :loading="loading"
                :on-pagination-change="onPaginationChange"
                :on-global-filters-change="onColumnFilterChange"
                :on-sorting-change="onSortingChange"
                :pagination="pagination"
                :sorting="sorting"
                :filter="globalFilters"
                :page-count="totalPage"
                :total-data="count"
            />
            <Table
                v-else
                :key="clientKey"
                :columns="listCanvasRequestColumn"
                :table-data="clientData?.pages || []"
            />
          </template>
        </Card>
    </SlideRightX>
  </FlexBox>
</template>
