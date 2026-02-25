<script setup>
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import ServerTable from "@/src/components/ui/table/ServerTable.vue";
import {listJurnalColumn} from "@/src/model/tableColumns/jurnal/listJurnal";
import Label from "@/src/components/ui/Label.vue";
import SelectInput from "@/src/components/ui/formInput/SelectInput.vue";
import VueDatePicker from "@vuepic/vue-datepicker";
import Button from "@/src/components/ui/Button.vue";
import {usePagination} from "@/src/lib/usePagination";
import {useFiltering} from "@/src/lib/useFiltering";
import {useSorting} from "@/src/lib/useSorting";
import {jurnalService} from "@/src/services/jurnal";
import {computed, ref} from "vue";
import Skeleton from "@/src/components/ui/Skeleton.vue";
import {format} from "date-fns";
import {useOthers} from "@/src/store/others";
import {useFetchPaginateV2} from "@/src/lib/useFetchPaginateV2";

const others = useOthers();

const {baseUrl} = jurnalService;
const {onPaginationChange, pagination} = usePagination();
const {onColumnFilterChange, globalFilters} = useFiltering();
const {onSortingChange, sorting} = useSorting();

const id_cabang = ref(null);
const advancedFilters = ref([]);
const id_perusahaan = ref(null);
const periodeAwal = ref(null);
const periodeAkhir = ref(null);

const containerKey = ref(0);

const formatPeriodeAwal = computed(() => {
  if (periodeAwal.value) {
    return format(new Date(periodeAwal.value), "yyyy-MM-dd");
  }
  return null;
});
const formatPeriodeAkhir = computed(() => {
  if (periodeAkhir.value) {
    return format(new Date(periodeAkhir.value), "yyyy-MM-dd");
  }
  return null;
});

const handleCariData = async () => {
  // await handleUnggah();
  advancedFilters.value = [];
  const dataFilter = []
  if (formatPeriodeAwal.value) {
    dataFilter.push({
      column: "periode_awal",
      value: formatPeriodeAwal.value,
    });
  }
  if (formatPeriodeAkhir.value) {
    dataFilter.push({
      column: "periode_akhir",
      value: formatPeriodeAkhir.value,
    });
  }
  if (id_cabang.value) {
    dataFilter.push({
      column: "id_cabang",
      value: id_cabang.value,
    });
  }
  if (id_perusahaan.value) {
    dataFilter.push({
      column: "id_perusahaan",
      value: id_perusahaan.value,
    });
  }
  advancedFilters.value = dataFilter;
};

const reset = () => {
  id_cabang.value = null;
  id_perusahaan.value = null;
  periodeAwal.value = null;
  periodeAkhir.value = null;
  advancedFilters.value = [];
}

const [data, count, loading, totalPage, key] = useFetchPaginateV2(`${baseUrl}?`, {
  pagination,
  sorting,
  globalFilters,
  initialSortColumn: "id_jurnal",
  initialSortDirection: "desc",
  advancedFilters: advancedFilters,
});
</script>

<template>
  <FlexBox full flex-col :key="containerKey">
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
        <template #header>Form Pencarian Jurnal</template>
        <template #content>
          <div class="form-grid-card tw-items-end">
            <Label label="Cabang">
              <Skeleton
                  class="tw-w-full tw-h-[34px]"
                  v-if="others.cabang.loading"
              />
              <SelectInput
                  v-else
                  v-model="id_cabang"
                  placeholder="Pilih Data"
                  size="md"
                  :search="true"
                  :options="others.cabang.list"
                  text-field="nama"
                  value-field="id"
              />
            </Label>
            <Label label="Perusahaan">
              <Skeleton
                  class="tw-w-full tw-h-[34px]"
                  v-if="others.perusahaan.loading"
              />
              <SelectInput
                  v-else
                  v-model="id_perusahaan"
                  placeholder="Pilih Data"
                  size="md"
                  :search="true"
                  :options="others.perusahaan.list"
                  text-field="nama"
                  value-field="id"
              />
            </Label>
            <Label label="Pilih Periode Awal">
              <VueDatePicker
                  v-model="periodeAwal"
                  format="yyyy-MM-dd"
                  model-type="yyyy-MM-dd"
                  :enable-time-picker="false"
                  placeholder="yyyy/mm/dd"
                  :teleport="true"
                  auto-apply
              />
            </Label>
            <Label label="Pilih Periode Akhir">
              <VueDatePicker
                  v-model="periodeAkhir"
                  format="yyyy-MM-dd"
                  model-type="yyyy-MM-dd"
                  :enable-time-picker="false"
                  placeholder="yyyy/mm/dd"
                  :teleport="true"
                  auto-apply
              />
            </Label>
            <div class="tw-flex tw-gap-2">
              <Button
                  :trigger="reset"
                  icon="mdi mdi-reload"
                  class="tw-h-[38px] tw-w-full xl:tw-w-32 tw-bg-red-500"
              >
                Reset
              </Button>
              <Button
                  :trigger="handleCariData"
                  icon="mdi mdi-magnify"
                  class="tw-h-[38px] tw-w-full xl:tw-w-32"
              >
                Cari Data
              </Button>
            </div>
          </div>
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
        <template #header>List jurnal</template>
        <template #content>
          <ServerTable
              :columns="listJurnalColumn"
              :key="key"
              :table-data="data?.result || data || []" 
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
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>