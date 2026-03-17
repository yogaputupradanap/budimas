<script setup>
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Button from "@/src/components/ui/Button.vue";
import Card from "@/src/components/ui/Card.vue";
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SelectInput from "@/src/components/ui/formInput/SelectInput.vue";
import Label from "@/src/components/ui/Label.vue";
import Modal from "@/src/components/ui/Modal.vue";
import Skeleton from "@/src/components/ui/Skeleton.vue";
import Table from "@/src/components/ui/table/Table.vue";
import ServerTable from "@/src/components/ui/table/ServerTable.vue";
import { useFiltering } from "@/src/lib/useFiltering";
import { usePagination } from "@/src/lib/usePagination";
import { useSorting } from "@/src/lib/useSorting";
import { formatNominalPromo } from "@/src/lib/utils";
import { listMasterPromoColumn } from "@/src/model/tableColumns/master-promo";
import { promoService } from "@/src/services/promo";
import { BFormInput, BFormTextarea } from "bootstrap-vue-next";
import { useTableSearch } from "@/src/lib/useTableSearch";
import { useFetchPaginate } from "@/src/lib/useFetchPaginate";
import { nextTick, ref, onMounted, computed, watch } from "vue";

const modal = ref();
const modalData = ref({});
const selectedPrincipal = ref(null);
const selectedKodePromo = ref(null);
const selectedNamaPromo = ref("");

const dropdownData = ref({
  principal: [],
  kode_promo: []
});
const dropdownLoading = ref(false);

const { onPaginationChange, pagination } = usePagination();
const { onColumnFilterChange, globalFilters } = useFiltering();
const { onSortingChange, sorting } = useSorting();

const { endpoints } = promoService;

const [data, count, loading, totalPage, key] = useFetchPaginate(
  endpoints.promo,
  {
    pagination,
    sorting,
    globalFilters,
    initialSortColumn: "kode_promo",
  }
);

const fieldPool = [
  selectedPrincipal, 
  selectedKodePromo,
  selectedNamaPromo,
];
const queryEntries = computed(() => {
  const entries = [
    ["id_principal=", selectedPrincipal.value],
    ["kode_promo=", selectedKodePromo.value],
    ["nama_promo=", selectedNamaPromo.value],
  ];
  if (globalFilters.text && globalFilters.text.trim() !== "") {
    entries.push(["nama_promo=", globalFilters.text]);
    entries.push(["kode_promo=", globalFilters.text]);
  }
  return entries.filter(([_, v]) => v !== undefined && v !== null && v !== "");
});

const options = {
  initialColumnName: "kode_promo",
  checkFieldFilterFunc: (val) => val[1] === undefined || val[1] === null,
  filterFunction: (val) => val[1] !== undefined && val[1] !== null,
  asArgument: true,
};

const [
  clientData,
  ,
  searchLoading,
  isServerTable,
  clientKey,
  searchQuery,
] = useTableSearch(endpoints.promo, fieldPool, queryEntries, options);

const filteredKodePromo = computed(() => {
  if (!selectedPrincipal.value || !Array.isArray(dropdownData.value.kode_promo)) {
    return [];
  }
  
  return dropdownData.value.kode_promo.filter(
    item => item && 
            typeof item === 'object' &&
            item.id_principal === selectedPrincipal.value &&
            item.kode_promo
  );
});

const loadDropdownData = async () => {
  try {
    dropdownLoading.value = true;

    const response = await promoService.getDropdownData();
    const data = Array.isArray(response) ? response[0] : response;

    if (data && data.principal && data.kode_promo) {
      dropdownData.value.principal = data.principal;
      dropdownData.value.kode_promo = data.kode_promo;
    } 
  } catch (error) {
    console.error('Error loading dropdown data:', error);
  } finally {
    dropdownLoading.value = false;
  }
};

const showModalWithData = async ({ value, rowIndex, columnId }) => {
  try {
    const response = await promoService.getDetailPromo(value);
    modalData.value = response[0];

    nextTick(() => {
      modal.value.show();
    });
  } catch (error) {
    console.error("Error fetching promo details:", error);
  }
};

const resetFormModal = () => {
  modalData.value = {};
};

const hideModal = () => {
  modal.value.hide();
};

watch(selectedPrincipal, (newValue, oldValue) => {
  if (newValue !== oldValue) {
    selectedKodePromo.value = null;
    selectedNamaPromo.value = "";
  }
}, { deep: false });

onMounted(() => {
  loadDropdownData();
});
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
        <template #header>Form Cari Promo</template>
        <template #content>
          <form class="form-grid-card">
            <Label label="Principal">
              <Skeleton
                class="tw-w-full tw-h-[34px]"
                v-if="dropdownLoading"
              />
              <SelectInput
                v-else
                placeholder="Pilih Data"
                v-model="selectedPrincipal"
                size="md"
                :search="true"
                :options="dropdownData.principal"
                text-field="nama"
                value-field="id"
              />
            </Label>
            <Label label="Kode Promo">
              <SelectInput
                placeholder="Pilih Data"
                size="md"
                v-model="selectedKodePromo"
                :search="true"
                :options="filteredKodePromo"
                text-field="kode_promo"
                value-field="kode_promo"
                :disabled="!selectedPrincipal"
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
        <template #header>List Promo</template>
        <template #content>
          <Modal
            id="modal"
            @modal-closed="resetFormModal"
            ref="modal"
            size="xl"
          >
            <Card
              no-subheader
              class="modal-lg tw-w-full md:tw-max-w-4xl lg:tw-max-w-6xl"
            >
              <template #header>
                <header
                  class="tw-flex tw-justify-between tw-items-center tw-pb-4"
                >
                  <h3 class="tw-text-lg tw-font-semibold">
                    Detail Promo {{ modalData.kode_promo }}
                  </h3>
                  <Button
                    icon="close"
                    @click="modal.hide()"
                    class="tw-bg-transparent tw-text-gray-500 hover:tw-text-red-600"
                  />
                </header>
              </template>
              <template #content>
                <!-- Detail Promo Section -->
                <div class="tw-mb-6 tw-pb-4">
                  <h4 class="tw-font-bold tw-mb-4 tw-pb-2">
                    Detail Promo
                  </h4>
                  <div class="tw-flex tw-flex-wrap tw-gap-4">
                    <Label label="Nama Promo" class="tw-flex-1">
                      <BFormInput
                        :model-value="modalData.nama_promo"
                        disabled
                        class="tw-mt-1 tw-bg-gray-100"
                      />
                    </Label>
                    <Label label="Nominal Promo" class="tw-flex-1">
                      <BFormInput
                          :model-value="formatNominalPromo(modalData)"
                        disabled
                        class="tw-mt-1 tw-bg-gray-100"
                      />
                    </Label>
                    <Label label="Tipe Promo" class="tw-flex-1">
                      <BFormInput
                        :model-value="modalData.tipe_promo"
                        disabled
                        class="tw-mt-1 tw-bg-gray-100"
                      />
                    </Label>
                    <Label label="Status Promo" class="tw-flex-1">
                      <BFormInput
                        :model-value="modalData.status_promo"
                        disabled
                        class="tw-mt-1 tw-bg-gray-100"
                      />
                    </Label>
                    <Label label="Keterangan" class="tw-flex-1">
                      <BFormTextarea
                        :model-value="modalData.keterangan"
                        disabled
                      />
                    </Label>
                  </div>
                </div>

                <!-- Pemberlakuan Promo Section -->
                <div class="tw-w-full tw-mb-6">
                  <h4 class="tw-font-bold tw-mb-4 tw-border-b tw-pb-2">
                    Pemberlakuan Promo
                  </h4>
                  <div class="tw-flex tw-flex-wrap tw-gap-4">
                    <Label label="Principal" class="tw-flex-1">
                      <BFormInput
                        :model-value="modalData.principal"
                        disabled
                        class="tw-mt-1 tw-bg-gray-100"
                      />
                    </Label>
                    <Label label="Cabang" class="tw-flex-1">
                      <BFormInput
                        :model-value="modalData.cabang"
                        disabled
                        class="tw-mt-1 tw-bg-gray-100"
                      />
                    </Label>
                    <Label label="Tanggal Mulai" class="tw-flex-1">
                      <BFormInput
                        :model-value="modalData.tanggal_mulai"
                        disabled
                        class="tw-mt-1 tw-bg-gray-100"
                      />
                    </Label>
                    <Label label="Tanggal Selesai" class="tw-flex-1">
                      <BFormInput
                        :model-value="modalData.tanggal_selesai"
                        disabled
                        class="tw-mt-1 tw-bg-gray-100"
                      />
                    </Label>
                  </div>
                </div>

                <!-- Syarat dan Ketentuan Section -->
                <div class="tw-w-full">
                  <h4 class="tw-font-bold tw-mb-4 tw-border-b tw-pb-2">
                    Syarat dan Ketentuan
                  </h4>
                  <div class="tw-flex tw-flex-wrap tw-gap-4">
                    <Label label="Syarat Ketentuan" class="tw-flex-1">
                      <BFormTextarea
                        :model-value="modalData.syarat_ketentuan"
                        disabled
                      />
                    </Label>
                    <Label label="Syarat Wajib" class="tw-flex-1">
                      <BFormTextarea
                        :model-value="modalData.syarat_wajib"
                        disabled
                      />
                    </Label>

                    <Label label="Lampiran Syarat Ketentuan">
                      <a
                        :href="modalData.lampiran"
                        class="tw-text-blue-600 hover:tw-underline"
                        target="_blank"
                      >
                        Lihat/Unduh File
                      </a>
                    </Label>
                  </div>
                  <FlexBox full class="tw-flex-row tw-justify-end tw-mt-4">
                    <Button
                      :trigger="hideModal"
                      class="tw-bg-red-500 hover:tw-bg-red-600 tw-text-white tw-px-4"
                    >
                      Close
                    </Button>
                  </FlexBox>
                </div>
              </template>
            </Card>
          </Modal>
          <ServerTable
            v-if="isServerTable"
            table-width="tw-w-full"
            :columns="listMasterPromoColumn"
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
            @open-row-modal="(val) => showModalWithData(val)"
          />
          <Table
            v-else
            :key="clientKey"
            :columns="listMasterPromoColumn"
            :table-data="clientData?.pages || []"
            @open-row-modal="(val) => showModalWithData(val)"
          />
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>
