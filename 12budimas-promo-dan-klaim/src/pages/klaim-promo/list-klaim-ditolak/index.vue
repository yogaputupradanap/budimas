<script setup>
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Button from "@/src/components/ui/Button.vue";
import Card from "@/src/components/ui/Card.vue";
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SelectInput from "@/src/components/ui/formInput/SelectInput.vue";
import Label from "@/src/components/ui/Label.vue";
import Table from "@/src/components/ui/table/Table.vue";
import ServerTable from "@/src/components/ui/table/ServerTable.vue";
import { listKlaimDitolakColumn } from "@/src/model/tableColumns/klaim-promo/list-klaim-ditolak";
import { useTableSearch } from "@/src/lib/useTableSearch";
import { ref, nextTick, onMounted, computed, watch, inject } from "vue";
import { promoService } from "@/src/services/promo";
import { useSorting } from "@/src/lib/useSorting";
import { useFiltering } from "@/src/lib/useFiltering";
import { usePagination } from "@/src/lib/usePagination";
import { useFetchPaginate } from "@/src/lib/useFetchPaginate";

const selectedPrincipal = ref(null);
const selectedNamaPromo = ref("");
const dropdownLoading = ref(false);

const dropdownData = ref({
  principal: [],
  kode_promo: [],
});

const { onPaginationChange, pagination } = usePagination();
const { onColumnFilterChange, globalFilters } = useFiltering();
const { onSortingChange, sorting } = useSorting();

const { endpoints } = promoService;

const fieldPool = [
  selectedPrincipal, 
  selectedNamaPromo,
];
  
const queryEntries = computed(() => {
  if (dropdownLoading.value) return [];

  const entries = [
    ["id_principal=", selectedPrincipal.value],
    ["nama_promo=", selectedNamaPromo.value],
  ];

  if (globalFilters.text && globalFilters.text.trim() !== "") {
    entries.push(["filters=", globalFilters.text]);
  }
  return entries.filter(([_, v]) => v !== undefined && v !== null && v !== "");
});

const options = {
  initialColumnName: "nomor_klaim",
  checkFieldFilterFunc: (val) => val[1] === undefined || val[1] === null,
  filterFunction: (val) => val[1] !== undefined && val[1] !== null,
  asArgument: true,
};

const [serverData, count, loading, totalPage, key] = useFetchPaginate(
  `${endpoints.klaimPromo}/ditolak?status_klaim=3`,
  {
    pagination,
    sorting,
    globalFilters,
    initialSortColumn: "nomor_klaim",
  }
);

const [
  clientData,
  ,
  searchLoading,
  isServerTable,
  clientKey,
  searchQuery,
] = useTableSearch(`${endpoints.klaimPromo}/ditolak?status_klaim=3`, fieldPool, queryEntries, options);

const filteredNamaPromo = computed(() => {
  if (!selectedPrincipal.value || !dropdownData.value.kode_promo) {
    return [];
  }
  
  return dropdownData.value.kode_promo.filter(
    item => item.id_principal === selectedPrincipal.value
  ).map(item => ({
    nama_promo: item.nama_promo,
    id_principal: item.id_principal
  }));
});

const loadDropdownData = async () => {
  dropdownLoading.value = true;
  try {
    const res = await promoService.getDropdownDataKlaim(3);
    if (!res) return;

    dropdownData.value = {
      principal: res.principal,
      kode_promo: res.kode_promo,
    };
  } catch (error) {
    console.error("Error loading dropdown data:", error);
  } finally {
    dropdownLoading.value = false;
  }
};

const displayData = computed(() => {
  return isServerTable.value ? serverData.value : (clientData.value?.pages || []);
});

watch(selectedPrincipal, (newValue, oldValue) => {
  if (newValue !== oldValue) {
    selectedPrincipal.value = newValue;
    selectedNamaPromo.value = "";
  }
}, { deep: false });

onMounted(loadDropdownData);
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
        <template #header>Form Cari Klaim Promo</template>
        <template #content>
          <form class="form-grid-card">
            <Label label="Principal">
              <SelectInput
                placeholder="Pilih Data"
                size="md"
                :search="true"
                :options="dropdownData.principal"
                :loading="dropdownLoading"
                v-model="selectedPrincipal"
                text-field="nama"
                value-field="id"
              />
            </Label>
            <Label label="Nama Promo">
              <SelectInput
                placeholder="Pilih Data"
                size="md"
                :search="true"
                :options="filteredNamaPromo"
                :disabled="!selectedPrincipal"
                :loading="dropdownLoading"
                v-model="selectedNamaPromo"
                text-field="nama_promo"
                value-field="nama_promo"
              />
            </Label>
            <Button
              :loading="searchLoading"
              :trigger="searchQuery"
              icon="mdi mdi-magnify"
              class="tw-h-[38px] tw-w-full xl:tw-w-32 tw-self-end"
            >
              Cari Data
            </Button>
          </form>
        </template>
      </Card>
    </SlideRightX>
    <SlideRightX
      class="slide-container tw-justify-end"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.2"
      :delay-out="0.2"
      :initial-x="-40"
      :x="40"
    >
      <Card no-subheader>
        <template #header>List Klaim Promo Ditolak</template>
        <template #content>
          <ServerTable
            v-if="isServerTable"
            table-width="tw-w-full"
            :columns="listKlaimDitolakColumn"
            :key="key"
            :table-data="displayData"
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
            :columns="listKlaimDitolakColumn"
            :loading="searchLoading"
            :table-data="displayData"
          />
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>
