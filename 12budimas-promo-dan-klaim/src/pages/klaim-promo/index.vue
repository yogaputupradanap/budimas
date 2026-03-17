<script setup>
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Button from "@/src/components/ui/Button.vue";
import Card from "@/src/components/ui/Card.vue";
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SelectInput from "@/src/components/ui/formInput/SelectInput.vue";
import Label from "@/src/components/ui/Label.vue";
import Modal from "@/src/components/ui/Modal.vue";
import RouterButton from "@/src/components/ui/RouterButton.vue";
import Table from "@/src/components/ui/table/Table.vue";
import ServerTable from "@/src/components/ui/table/ServerTable.vue";
import { listKlaimPromoColumn } from "@/src/model/tableColumns/klaim-promo";
import { BFormInput } from "bootstrap-vue-next";
import { useTableSearch } from "@/src/lib/useTableSearch";
import { ref, nextTick, onMounted, computed, watch, inject } from "vue";
import { promoService } from "@/src/services/promo";
import { useSorting } from "@/src/lib/useSorting";
import { useFiltering } from "@/src/lib/useFiltering";
import { usePagination } from "@/src/lib/usePagination";
import { useFetchPaginate } from "@/src/lib/useFetchPaginate";

const modal = ref();
const modalValue = ref({});
const $swal = inject("$swal");

const selectedPrincipal = ref(null);
const selectedNamaPromo = ref("");
const selectedStatusKlaim = ref(null);
const dropdownLoading = ref(false);

const dropdownData = ref({
  principal: [],
  kode_promo: [],
  status_klaim: [],
});

const { onPaginationChange, pagination } = usePagination();
const { onColumnFilterChange, globalFilters } = useFiltering();
const { onSortingChange, sorting } = useSorting();

const { endpoints } = promoService;

const fieldPool = [
  selectedPrincipal, 
  selectedNamaPromo,
  selectedStatusKlaim
];
  
const queryEntries = computed(() => {
  if (dropdownLoading.value) return [];

  const entries = [
    ["id_principal=", selectedPrincipal.value],
    ["nama_promo=", selectedNamaPromo.value],
    ["status_klaim=", selectedStatusKlaim.value],
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
  endpoints.klaimPromo,
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
] = useTableSearch(endpoints.klaimPromo, fieldPool, queryEntries, options);

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
    const res = await promoService.getDropdownDataKlaim();
    if (res && res.principal && res.kode_promo) {
      dropdownData.value.principal = res.principal;
      dropdownData.value.kode_promo = res.kode_promo;
      dropdownData.value.status_klaim = res.status_klaim;
    }
  } catch (error) {
    console.error("Error loading dropdown data:", error);
  } finally {
    dropdownLoading.value = false;
  }
};

const resetQuery = async () => {
  selectedNamaPromo.value = "";
  selectedStatusKlaim.value = null;

  if (globalFilters && typeof globalFilters === "object") {
    globalFilters.text = "";
  }

  onPaginationChange({ ...pagination.value, page: 1 });
  if (isServerTable.value) {
    await nextTick();
    await searchQuery();
  }
}

const handleUpdateStatusKlaim = async () => {
  await promoService.updateKlaimStatus({
    id: modalValue.value.id,
    status_klaim: selectedStatusKlaim.value
  });

  $swal.success("Status klaim berhasil diubah");
  await resetQuery();
  modal.value.hide();
}

const showModalWithData = ({ value, rowIndex, columnId }) => {
  modalValue.value = value

  const statusOption = dropdownData.value.status_klaim.find(
    option => option.nama === value.status_klaim
  );
  selectedStatusKlaim.value = statusOption ? statusOption.id : null;
  nextTick(() => { modal.value.show() });
};

const resetFormModal = () => {
  modal.value.hide();
};

const displayData = computed(() => {
  return isServerTable.value ? serverData.value : (clientData.value?.pages || []);
});

watch(selectedPrincipal, (newValue, oldValue) => {
  if (newValue !== oldValue) {
    selectedPrincipal.value = newValue;
    selectedNamaPromo.value = "";
    selectedStatusKlaim.value = null;
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
        <template #header>List Klaim Promo</template>
        <template #content>
          <Modal
            id="modal"
            @modal-closed="resetFormModal"
            ref="modal"
            size="lg"
          >
            <Card no-subheader>
              <template #header>Edit Status Pengajuan Klaim</template>
              <template #content>
                <div class="tw-w-full tw-grid tw-grid-cols-1 tw-gap-5 lg:tw-grid-cols-2">
                  <Label label="No Klaim" full>
                    <BFormInput :model-value="modalValue.nomor_klaim" disabled />
                  </Label>
                  <Label label="Principal" full>
                    <BFormInput :model-value="modalValue.principal" disabled />
                  </Label>
                  <Label label="Nama Promo" full>
                    <BFormInput :model-value="modalValue.nama_promo" disabled />
                  </Label>
                  <Label label="Kode Promo" full>
                    <BFormInput :model-value="modalValue.kode_promo" disabled />
                  </Label>
                  <Label 
                    label="Status Klaim"
                    class="tw-col-span-1 lg:tw-col-span-2"
                  >
                    <SelectInput
                      placeholder="Pilih Data"
                      size="md"
                      :search="true"
                      :options="dropdownData.status_klaim"
                      :loading="dropdownLoading"
                      v-model="selectedStatusKlaim"
                      text-field="nama"
                      value-field="id"
                    />
                  </Label>
                  
                </div>
                <FlexBox
                  full
                  jus-center
                  class="tw-mt-4 lg:tw-justify-end lg:tw-flex-row tw-flex-wrap-reverse"
                >
                  <Button
                    :trigger="resetFormModal"
                    class="tw-px-14 tw-py-2 tw-text-xs tw-bg-red-500"
                  >
                    Cancel
                  </Button>
                  <Button 
                  :trigger="handleUpdateStatusKlaim"
                    class="tw-px-14 tw-py-2 tw-text-xs tw-bg-green-500"
                  >
                    Submit
                  </Button>
                </FlexBox>
              </template>
            </Card>
          </Modal>
          <FlexBox full jus-end>
            <RouterButton
              class="tw-bg-red-500 tw-px-4 tw-text-sm tw-py-2 tw-me-3"
              to="/klaim-promo/list-klaim-ditolak"
            >
              Lihat Klaim Ditolak
            </RouterButton>
          </FlexBox>
          <ServerTable
            v-if="isServerTable"
            table-width="tw-w-full"
            :columns="listKlaimPromoColumn"
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
            @open-row-modal="(val) => showModalWithData(val)"
          />
          <Table
            v-else
            :key="clientKey"
            :columns="listKlaimPromoColumn"
            :loading="searchLoading"
            :table-data="displayData"
            @open-row-modal="(val) => showModalWithData(val)"
          />
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>
