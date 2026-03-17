<script setup>
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import Table from "@/src/components/ui/table/Table.vue";
import ServerTable from "@/src/components/ui/table/ServerTable.vue";
import Label from "@/src/components/ui/Label.vue";
import { BFormInput } from "bootstrap-vue-next";
import { AjukanUlangColumn } from "@/src/model/tableColumns/klaim-promo/list-klaim-ditolak/ajukan-ulang";
import { ref, onMounted, computed, inject } from "vue";
import { parseCurrency, simpleDateNow } from "@/src/lib/utils";
import { useSorting } from "@/src/lib/useSorting";
import { promoService } from "@/src/services/promo";
import { useFiltering } from "@/src/lib/useFiltering";
import { usePagination } from "@/src/lib/usePagination";
import { useRoute, useRouter } from "vue-router";
import { useTableSearch } from "@/src/lib/useTableSearch";

const klaimId = computed(() => route.params.id);
const klaimDitolak = ref({});

const route = useRoute();
const router = useRouter();
const $swal = inject("$swal");

const { onSortingChange, sorting } = useSorting();
const { onPaginationChange, pagination } = usePagination();
const { onColumnFilterChange, globalFilters } = useFiltering();

const { endpoints } = promoService;

const fieldPool = [klaimId];
const queryEntries = computed(() => [
  ["id=", klaimId.value]
]);

const options = {
  initialColumnName: "no_faktur",
  checkFieldFilterFunc: (val) => val[1] === undefined || val[1] === null,
  filterFunction: (val) => val[1] !== undefined && val[1] !== null,
  asArgument: true,
};

const [
  klaimData,
  ,
  klaimLoading,
  isServerTable,
  klaimKey,
  searchQuery,
] = useTableSearch(endpoints.promoListFaktur, fieldPool, queryEntries, options);

const fakturList = computed(() => {
  const arr = Array.isArray(klaimData.value?.pages) ? klaimData.value.pages : [];
  return arr;
});

const totalEstimasiKlaim = computed(() => {
  return fakturList.value.reduce((sum, faktur) => sum + Number(faktur.estimasi_klaim || 0), 0);
});

const formattedTotalEstimasiKlaim = computed(() => parseCurrency(totalEstimasiKlaim.value));

const fetchKlaimDetail = async () => {
  if (!klaimId.value) {
    $swal.error("ID klaim tidak ditemukan!");
    return;
  }

  try {
    const response = await promoService.getKlaimDetail(klaimId.value);
    klaimDitolak.value = response;
  } catch (error) {
    console.error("Error fetching klaim details:", error);  
    klaimDitolak.value = {};
  }
};

const validateForm = () => {
  if (!selectedKategoriKlaim.value) {
    $swal.error("Kategori Klaim harus dipilih");
    return false;
  }
  if (fakturList.value.length === 0) {
    $swal.error("Tidak ada data faktur untuk diajukan klaimnya");
    return false;
  }
  return true;
}

onMounted(async () => {
  fetchKlaimDetail();
  if (klaimId.value) await searchQuery();
})
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
        <template #header>Ajukan Klaim</template>
        <template #content>
          <div
            full
            class="tw-grid tw-grid-cols-1 sm:tw-grid-cols-2 lg:tw-grid-cols-3 gap-4 tw-w-full tw-px-2"
          >
            <Label label="Tanggal">
              <BFormInput
                :model-value="simpleDateNow(klaimDitolak?.tanggal_pengajuan_klaim)"
                disabled
                placeholder="Tanggal"
              />
            </Label>
            <Label label="No Klaim">
              <BFormInput
                :model-value="klaimDitolak?.nomor_klaim"
                disabled
                placeholder="No Klaim"
              />
            </Label>
            <Label label="Principal">
              <BFormInput
                :model-value="klaimDitolak?.principal"
                disabled
                placeholder="Principal"
              />
            </Label>
            <Label label="Kode Promo">
              <BFormInput
                :model-value="klaimDitolak?.kode_promo"
                disabled
                placeholder="Kode Promo"
              />
            </Label>
            <Label label="Nama Promo">
              <BFormInput
                :model-value="klaimDitolak?.nama_promo"
                disabled
                placeholder="Nama Promo"
              />
            </Label>
            <Label label="Total Klaim">
              <BFormInput
                :model-value="formattedTotalEstimasiKlaim"
                placeholder="Total klaim"
                disabled
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
        <template #header>List Faktur</template>
        <template #content>
          <ServerTable
            v-if="isServerTable"
            table-width="tw-w-full"
            :columns="AjukanUlangColumn"
            :key="klaimKey"
            :table-data="fakturList"
            :loading="klaimLoading"
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
            :key="`table-${klaimKey}`"
            :columns="AjukanUlangColumn"
            :table-data="klaimData?.pages || []"
          />
          <div class="tw-flex tw-flex-col tw-gap-4 tw-w-full tw-px-2">
            <div class="tw-grid tw-grid-cols-3 tw-gap-4">
              <Label label="DPP">
                <BFormInput 
                  placeholder="Nominal DPP" 
                  readonly
                  :model-value="parseCurrency(klaimDitolak?.total_dpp)"
                  class="tw-bg-gray-200"
                  />
              </Label>
              <Label :label="`PPN`">
                <BFormInput 
                  placeholder="Nominal PPN" 
                  readonly
                  :model-value="parseCurrency(klaimDitolak?.total_ppn)"
                  class="tw-bg-gray-200"
                  />
              </Label>
              <Label label="PPH">
                <BFormInput 
                  placeholder="Nominal PPh" 
                  readonly
                  :model-value="parseCurrency(klaimDitolak?.total_pph)"
                  class="tw-bg-gray-200"
                  />
              </Label>
            </div>
             <div class="tw-grid tw-grid-cols-3 tw-gap-4">
              <Label label="Kategori Klaim">
                <BFormInput 
                  placeholder="Kategori Klaim" 
                  readonly
                  :model-value="klaimDitolak?.nama_kategori_klaim"
                  class="tw-bg-gray-200"
                />
              </Label>
              <Label label="Total">
                <BFormInput
                  :model-value="parseCurrency(klaimDitolak?.total_klaim_diajukan)"
                  readonly
                  class="tw-bg-gray-200"
                  placeholder="Total"
                />
              </Label>
            </div>
          </div>
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>
