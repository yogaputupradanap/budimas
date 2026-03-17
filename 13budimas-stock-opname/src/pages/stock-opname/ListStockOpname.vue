<script setup>
import SelectInput from "@/src/components/ui/formInput/SelectInput.vue";
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Skeleton from "@/src/components/ui/Skeleton.vue";
import Card from "@/src/components/ui/Card.vue";
import Label from "@/src/components/ui/Label.vue";
import { BFormInput } from "bootstrap-vue-next";
import Table from "@/src/components/ui/table/Table.vue";
import { listStockColumns } from "@/src/model/tableColumns/stock-opname/listStock";
import RouterButton from "@/src/components/ui/RouterButton.vue";
import Button from "@/src/components/ui/Button.vue";
import { computed, onBeforeUnmount, onMounted, ref, watch } from "vue";
import { usePagination } from "@/src/lib/usePagination";
import { useFiltering } from "@/src/lib/useFiltering";
import { useSorting } from "@/src/lib/useSorting";
import { useFetchPaginate } from "@/src/lib/useFetchPaginate";
import ServerTable from "@/src/components/ui/table/ServerTable.vue";
import VueDatePicker from "@vuepic/vue-datepicker";
import { useAlert } from "@/src/store/alert";
import { useUser } from "@/src/store/user";
import { useOthers } from "@/src/store/others";
import { storeToRefs } from "pinia";
import { stockOpnameService } from "@/src/services/stockOpname";

const others = useOthers();

const { principal, stockOpname } = storeToRefs(others);
const { onPaginationChange, pagination } = usePagination();
const { onColumnFilterChange, globalFilters } = useFiltering();
const { onSortingChange, sorting } = useSorting();

const { paginateStockOpnameUrl } = stockOpnameService;
const alert = useAlert();
const userStore = useUser();
const isServerTable = ref(true);

const id_opname = ref("");
const cariData = ref(false);
const principalSelected = ref("");
const tanggal = ref("");
const listStockOpname = ref([]);
const id_cabang = computed(() => userStore.user.value?.id_cabang || 0);
const datePickerLocale = {
  locale: "id",
  format: "yyyy-MM-dd",
};

onMounted(() => {
  listStockOpname.value = stockOpname.value.list;
});
onBeforeUnmount(() => {
  if (cariData.value) {
    others.getAllStockOpname();
  }
});

const localStore = ref(null);
const searchLoading = ref(false);
const searchEntries = ref([]);
const buttonText = ref({
  text: "Cari Data",
  icon: "mdi mdi-magnify",
});

const buildClause = () => {
  searchEntries.value = [];
  if (principalSelected.value !== "") {
    searchEntries.value.push(["principal.id =", principalSelected.value]);
  }
  if (id_opname.value !== "") {
    searchEntries.value.push([
      "stock_opname.kode_so ILIKE",
      `'%${id_opname.value}%'`,
    ]);
  }

  if (tanggal.value !== "" && tanggal.value !== null) {
    const formattedDate = new Date(tanggal.value).toISOString().split("T")[0];
    searchEntries.value.push(["tanggal_so =", `'${formattedDate}'`]);
  }

  const searchObject = Object.fromEntries(searchEntries.value);
  const objectSearch = JSON.stringify(searchObject);
  return objectSearch;
};

const getButtonText = () => {
  buildClause();

  buttonText.value = {
    text: "Cari Data",
    icon: "mdi mdi-magnify",
  };
};

const searchQuery = async () => {
  const clause = buildClause();
  
  // Proteksi: Pastikan id_cabang ada sebelum fetch
  if (!id_cabang.value || id_cabang.value === 'undefined') {
      alert.setMessage("Sesi berakhir atau Cabang tidak diketahui. Silakan login ulang.", "danger");
      return;
  }
  cariData.value = true;
  try {
    searchLoading.value = true;
    others.getAllStockOpnameFilter(clause);

    if (clause === "{}") {
      isServerTable.value = true;
    } else {
      isServerTable.value = false;
    }
  } catch (error) {
    alert.setMessage(error, "danger");
  } finally {
    searchLoading.value = false;
    getButtonText();
  }
};

const [data, count, loading, totalPage, key] = useFetchPaginate(
  // Tambahkan .value di sini
  `${paginateStockOpnameUrl}?id_cabang=${id_cabang.value}&`, 
  {
    pagination,
    sorting,
    globalFilters,
    initialSortColumn: "tanggal_so",
    initialSortDirection: "desc",
    filterColum: "test",
  }
);

watch(
  // Gunakan fungsi getter agar Vue tetap bisa melacak referensinya meskipun awalnya null
  () => others.stockOpname, 
  (newValue) => {
    if (newValue && newValue.list) {
      listStockOpname.value = newValue.list;
    }
  },
  { deep: true }
);
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
        <template #header>Form Cari Stock Opname</template>
        <template #content>
          <div class="form-grid-card-4-menu tw-items-end">
            <Label label="Kode Stock Opname">
              <BFormInput
                v-model="id_opname"
                placeholder="Cari Kode Stock Opname"
              />
            </Label>
            <Label label="Principal" class="z-10">
              <Skeleton class="skeleton" v-if="principal.loading" />
              <SelectInput
                v-else
                v-model="principalSelected"
                placeholder="Pilih Principal"
                size="md"
                :search="true"
                class=""
                :options="principal.list"
                text-field="nama"
                value-field="id"
              />
            </Label>
            <Label label="Tanggal">
              <VueDatePicker
                v-model="tanggal"
                :enable-time-picker="false"
                placeholder="yyyy-mm-dd"
                :locale="datePickerLocale.locale"
                :format="datePickerLocale.format"
                :teleport="true"
                auto-apply
                hide-input-icon=""
              />
            </Label>
            <Button
              :trigger="searchQuery"
              :loading="searchLoading"
              class="tw-text-white tw-bg-blue-500 tw-rounded-lg tw-px-2 tw-py-2 tw-flex tw-justify-center tw-items-center hover:tw-bg-gray-500 hover:tw-text-white hover:tw-transition-all hover:tw-duration-300 hover:tw-ease-in-out"
              :icon="buttonText.icon"
            >
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
      :x="40"
    >
      <RouterButton
        class="tw-h-10"
        icon="mdi mdi-plus"
        to="/stock-opname/add-stock-opname"
      >
        Add Stock Opname
      </RouterButton>
    </SlideRightX>
    <SlideRightX
      class="slide-container tw-z-0"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.3"
      :delay-out="0.1"
      :initial-x="-40"
      :x="40"
    >
      <Card no-subheader>
        <template #header>List Stock Opname</template>
        <template #content>
          <ServerTable
            v-if="isServerTable"
            :columns="listStockColumns"
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
            :classic="true"
          />
          <Table
            v-else
            :key="localStore || []"
            :columns="listStockColumns"
            :loading="stockOpname.loading"
            :classic="true"
            :table-data="stockOpname.list"
          />
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>
