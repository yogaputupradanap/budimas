<script setup>
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import Table from "@/src/components/ui/table/Table.vue";
import { listTagihanPurchasing } from "@/src/model/tableColumns/tagihan-purchasing/listTagihanPurchasing";
import Label from "@/src/components/ui/Label.vue";
import SelectInput from "@/src/components/ui/formInput/SelectInput.vue";
import VueDatePicker from "@vuepic/vue-datepicker";
import Button from "@/src/components/ui/Button.vue";
import RouterButton from "@/src/components/ui/RouterButton.vue";
import { useOthers } from "@/src/store/others";
import { useFetchPaginate } from "@/src/lib/useFetchPaginate";
import { useTableSearch } from "@/src/lib/useTableSearch";
import { computed, ref } from "vue";
import { useSorting } from "@/src/lib/useSorting";
import { useFiltering } from "@/src/lib/useFiltering";
import { usePagination } from "@/src/lib/usePagination";
import { hutangService } from "@/src/services/hutang";
import ServerTable from "@/src/components/ui/table/ServerTable.vue";
import { format } from "date-fns";
import { id } from "date-fns/locale";

const others = useOthers();

const { getHutangUrl } = hutangService;
const { onPaginationChange, pagination } = usePagination();
const { onColumnFilterChange, globalFilters } = useFiltering();
const { onSortingChange, sorting } = useSorting();

const principal = ref(null);
const jatuhTempo = ref(null);

const datePickerLocale = {
  locale: id,
  format: "yyyy-MM-dd",
};
const formatJatuhTempo = computed(() => {
  if (!jatuhTempo.value) return null;

  try {
    const dateValue =
      jatuhTempo.value instanceof Date
        ? jatuhTempo.value
        : new Date(jatuhTempo.value);

    return format(dateValue, "yyyy-MM-dd");
  } catch (error) {
    console.error("Error formatting date:", error);
    return null;
  }
});

const fieldPool = [principal, jatuhTempo];
const queryEntries = computed(() => [
  ["principal=", principal.value],
  ["jatuh_tempo=", formatJatuhTempo.value],
]);

const options = {
  initialColumnName: "surat_tagihan",
  checkFieldFilterFunc: (val) => val[1] === null,
  filterFunction: (val) => val[1] !== null,
  asArgument: true,
};

const [data, count, loading, totalPage, key] = useFetchPaginate(
  `${getHutangUrl}?`,
  {
    pagination,
    sorting,
    globalFilters,
    initialSortColumn: "surat_tagihan",
  }
);

const [clientData, , , isServerTable, clientKey, searchQuery] = useTableSearch(
  getHutangUrl,
  fieldPool,
  queryEntries,
  options
);

const reset = () => {
  fieldPool.forEach((val) => (val.value = null));
  isServerTable.value = true;
};
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
        <template #header>Form Pencarian Surat Tagihan Purchasing</template>
        <template #content>
          <div class="form-grid-card tw-items-end">
            <Label label="Principal">
              <SelectInput
                placeholder="Pilih Principal"
                size="md"
                :search="true"
                :options="others.principal.list"
                v-model="principal"
                text-field="nama"
                value-field="id"
              />
            </Label>
            <Label label="Tangal Jatuh Tempo">
              <VueDatePicker
                v-model="jatuhTempo"
                :enable-time-picker="false"
                placeholder="yyyy-mm-dd"
                :locale="datePickerLocale.locale"
                :format="datePickerLocale.format"
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
                :trigger="searchQuery"
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
      <RouterButton
        icon="mdi mdi-plus-thick"
        class="tw-px-4 tw-py-2"
        to="/tagihan-purchasing/buat-tagihan-purchasing"
      >
        Buat Tagihan Purchasing
      </RouterButton>
    </SlideRightX>
    <SlideRightX
      class="slide-container"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.3"
      :delay-out="0.3"
      :initial-x="-40"
      :x="40"
    >
      <Card no-subheader>
        <template #header>List Tagihan</template>
        <template #content>
          <ServerTable
            v-if="isServerTable"
            table-width="tw-w-[90vw]"
            :columns="listTagihanPurchasing"
            :key="key"
            :table-data="data?.result || []"
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
            table-width="tw-w-[90vw]"
            :key="clientKey"
            :columns="listTagihanPurchasing"
            :table-data="clientData.pages"
          />
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>
