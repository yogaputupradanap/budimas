<script setup>
import SlideRightX from "../components/animation/SlideRightX.vue";
import Card from "../components/ui/Card.vue";
import {useKepalaCabang} from "../store/kepalaCabang";
import {useShipping} from "../store/shipping";
import {ref} from "vue";
import SelectInputV2 from "@/src/components/ui/formInput/SelectInputV2.vue";
import {useCustomer} from "@/src/store/customer";
import Button from "@/src/components/ui/Button.vue";
import RouterButton from "@/src/components/ui/RouterButton.vue";
import FlexBox from "@/src/components/ui/FlexBox.vue";
import {tableListKpr} from "@/src/model/tableColumns/listKpr";
import {useFetchPaginate} from "@/src/lib/useFetchPaginate";
import ServerTableV2 from "@/src/components/ui/table/ServerTableV2.vue";
import {usePagination} from "@/src/lib/usePagination";
import {useFiltering} from "@/src/lib/useFiltering";
import {useSorting} from "@/src/lib/useSorting";

const kepalaCabang = useKepalaCabang();
const {onPaginationChange, pagination} = usePagination();
const {onColumnFilterChange, globalFilters} = useFiltering();
const {onSortingChange, sorting} = useSorting();
const paginateReturUrl = '/api/retur/retur';
const shipping = useShipping();
const idCustomer = ref(null);
const customerStore = useCustomer()
const loadingSearch = ref(false);
const tableKey = ref(0);
const advancedFilters = ref([]);

const getResource = async () => {
  console.log("getResource called");
  console.log("idCustomer.value", idCustomer.value);

  console.log("getResource called");
  advancedFilters.value = [{
    column: "id_customer",
    value: idCustomer.value,
  }];

};

const [data, count, loading, totalPage, key] = useFetchPaginate(
    `${process.env.VUE_APP_API_URL}${paginateReturUrl}?id_cabang=${kepalaCabang.kepalaCabangUser.id_cabang}&`,
    {
      pagination,
      sorting,
      globalFilters,
      initialSortColumn: "tanggal_request",
      initialSortDirection: "desc",
      filterColum: "test",
      columNotUsed: ['"jumlah_barang"'],
      advancedFilters: advancedFilters,
    }
);
</script>

<template>
  <div class="tw-flex tw-flex-col tw-w-full tw-gap-4 lg:tw-px-4 tw-px-0">
    <SlideRightX class="" :duration-enter="0.6" :duration-leave="0.6" :delay-out="0.1" :delay-in="0.1" :initial-x="-40"
                 :x="40">
      <Card :no-subheader="true" class="tw-mb-6 ">
        <template #header>Cari KPR</template>
        <template #content>
          <div class="tw-grid tw-grid-cols-1 lg:tw-grid-cols-2 tw-mb-8 tw-w-full tw-gap-2">
            <BFormGroup
                class="tw-w-1/2"
                id="input-group-6"
                label="Customer"
                label-for="input-6"
            >
              <SelectInputV2
                  v-model="idCustomer"
                  :options="customerStore.customer.list"
                  placeholder="Pilih Customer"
                  text-field="nama"
                  value-field="id"
                  search="true"
                  virtual-scroll="true"
              />
            </BFormGroup>
            <FlexBox full jusEnd class="tw-mb-4">
              <Button
                  class="tw-w-32 tw-mt-6"
                  icon="mdi mdi-magnify"
                  :loading="loadingSearch"
                  :trigger="getResource"
              >
                Cari
              </Button>
            </FlexBox>
          </div>
        </template>
      </Card>
      <Card :no-subheader="true" class="tw-mb-6">
        <template #header>List KPR</template>
        <template #content>
          <div class="tw-w-full tw-py-6">
            <FlexBox full jusEnd class="tw-mb-4">
              <RouterButton
                  to="/retur/list-pengajuan"
                  icon="mdi mdi-plus-circle-outline"
                  class="tw-px-4">
                Buat KPR
              </RouterButton>
            </FlexBox>
            <ServerTableV2
                v-if="true"
                :columns="tableListKpr"
                :key="key"
                :loading="loading"
                :table-data="data"
                :on-pagination-change="onPaginationChange"
                :on-global-filters-change="onColumnFilterChange"
                :on-sorting-change="onSortingChange"
                :pagination="pagination"
                :sorting="sorting"
                :filter="globalFilters"
                :page-count="totalPage"
                :total-data="count"
            />
          </div>
        </template>
      </Card>
    </SlideRightX>
  </div>
</template>
