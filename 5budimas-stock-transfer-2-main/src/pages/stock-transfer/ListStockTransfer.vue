<script setup>
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import Label from "@/src/components/ui/Label.vue";
import { BFormInput } from "bootstrap-vue-next";
import Table from "@/src/components/ui/table/Table.vue";
import { listStockColumns } from "@/src/model/tableColumns/stock-transfer/listStock";
import RouterButton from "@/src/components/ui/RouterButton.vue";
import Button from "@/src/components/ui/Button.vue";
import { computed, ref, watch } from "vue";
import { usePagination } from "@/src/lib/usePagination";
import { useFiltering } from "@/src/lib/useFiltering";
import { useSorting } from "@/src/lib/useSorting";
import { useFetchPaginate } from "@/src/lib/useFetchPaginate";
import ServerTable from "@/src/components/ui/table/ServerTable.vue";
import { fetchWithAuth, sessionDisk } from "@/src/lib/utils";
import { useAlert } from "@/src/store/alert";
import { transferService } from "@/src/services/stockTransfer";
import { useUser } from "@/src/store/user";

const { onPaginationChange, pagination } = usePagination();
const { onColumnFilterChange, globalFilters } = useFiltering();
const { onSortingChange, sorting } = useSorting();

const { stockBase, paginateStockBase } = transferService;

const alert = useAlert();
const userStore = useUser();

const isServerTable = ref(true);

const nama = ref("");
const sku = ref("");
const cabang = ref("");

/*
|--------------------------------------------------------------------------
| AUTH USER
|--------------------------------------------------------------------------
*/
const authUser = sessionDisk.getSession("authUser");

/*
|--------------------------------------------------------------------------
| SAFE CABANG
|--------------------------------------------------------------------------
*/
const id_cabang = computed(() => {
  return (
    userStore.user?.value?.id_cabang ||
    authUser?.id_cabang ||
    null
  );
});

/*
|--------------------------------------------------------------------------
| DEBUG
|--------------------------------------------------------------------------
*/
watch(id_cabang, (val) => {
  console.log("ID CABANG:", val);
});

/*
|--------------------------------------------------------------------------
| PAGINATE URL (STRING REF)
|--------------------------------------------------------------------------
*/
const paginateUrl = ref(`${paginateStockBase}&`);

/*
|--------------------------------------------------------------------------
| WATCH ID CABANG
|--------------------------------------------------------------------------
*/
watch(id_cabang, (val) => {
  if (!val) {
    paginateUrl.value = `${paginateStockBase}&`;
    return;
  }

  paginateUrl.value =
    `${paginateStockBase}&clause=` +
    encodeURIComponent(
      JSON.stringify({ "cabang.id =": val })
    ) +
    "&";

  console.log("UPDATED PAGINATE URL:", paginateUrl.value);
}, { immediate: true });

/*
|--------------------------------------------------------------------------
| FETCH PAGINATE
|--------------------------------------------------------------------------
*/
const [data, count, loading, totalPage, key] = useFetchPaginate(
  paginateUrl.value,
  {
    pagination,
    sorting,
    globalFilters,
    initialSortColumn: "id",
  }
);

/*
|--------------------------------------------------------------------------
| LOCAL SEARCH
|--------------------------------------------------------------------------
*/
const localStore = ref(null);
const searchLoading = ref(false);
const searchEntries = ref([]);

const buttonText = ref({
  text: "Cari Data",
  icon: "mdi mdi-magnify",
});

const checkAllSearchField = computed(() => {
  const withoutCabang = [...searchEntries.value].filter(
    (val) => !val[0].includes("cabang.id")
  );
  return withoutCabang.every((val) => val[1] === "");
});

const buildClause = () => {
  const filterArray = (val) => val[1] !== "";

  searchEntries.value = [
    ["produk.nama ILIKE", nama.value],
    ["produk.kode_sku ILIKE", sku.value],
    ["cabang.nama ILIKE", cabang.value],
    ["cabang.id =", id_cabang.value],
  ];

  const searchFilter = searchEntries.value.filter(filterArray);

  return encodeURIComponent(
    JSON.stringify(Object.fromEntries(searchFilter))
  );
};

const getButtonText = () => {
  buildClause();

  buttonText.value =
    !isServerTable.value && checkAllSearchField.value
      ? { text: "Reload", icon: "mdi mdi-reload" }
      : { text: "Cari Data", icon: "mdi mdi-magnify" };
};

const searchQuery = async () => {
  const clause = buildClause();
  const url = `${stockBase}&clause=${clause}`;

  console.log("SEARCH URL:", url);

  try {
    searchLoading.value = true;
    localStore.value = await fetchWithAuth("GET", url);
  } catch (error) {
    alert.setMessage(error, "danger");
  } finally {
    searchLoading.value = false;
    isServerTable.value = checkAllSearchField.value;
    getButtonText();
  }
};

watch([nama, sku, cabang], getButtonText);

watch(data, (v) => {
  console.log("SERVER TABLE DATA:", v);
});

watch(count, (v) => {
  console.log("COUNT:", v);
});

watch(loading, (v) => {
  console.log("LOADING:", v);
});


watch(data, (val) => {
  console.log("TABLE ARRAY:", val?.result);
});

</script>




<template>
  <FlexBox full flex-col>
    <SlideRightX
      class="slide-container"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.1"
      :delay-out="0.1"
      :initial-x="-40"
      :x="40">
      <Card no-subheader>
        <template #header>Cari Data Stock</template>
        <template #content>
          <div class="form-grid-card tw-items-end">
            <Label label="Nama">
              <BFormInput v-model="nama" placeholder="Cari Nama" />
            </Label>
            <Label label="SKU">
              <BFormInput v-model="sku" placeholder="Cari SKU" />
            </Label>
            <Label label="Cabang">
              <BFormInput v-model="cabang" placeholder="Cari Cabang" />
            </Label>
            <Button
              :trigger="searchQuery"
              :loading="searchLoading"
              class="tw-w-40 tw-h-[37px] tw-ml-0 md:tw-ml-4"
              :icon="buttonText.icon">
              {{ buttonText.text }}
            </Button>
          </div>
        </template>
      </Card>
    </SlideRightX>
    <SlideRightX
      class="tw-w-full tw-flex tw-justify-end slide-container"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.2"
      :delay-out="0.1"
      :initial-x="-40"
      :x="40">
      <RouterButton
        class="tw-h-10"
        icon="mdi mdi-plus"
        to="/stock-transfer/add">
        Add Stock Transfer
      </RouterButton>
    </SlideRightX>
    <SlideRightX
      class="slide-container"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.3"
      :delay-out="0.1"
      :initial-x="-40"
      :x="40">
      <Card no-subheader>
        <template #header>List Stock</template>
        <template #content>
          <ServerTable
            v-if="isServerTable"
            :columns="listStockColumns"
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
            :total-data="count" />


          <Table
            v-else
            :columns="listStockColumns"
            :table-data="localStore || []"
          />

        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>
