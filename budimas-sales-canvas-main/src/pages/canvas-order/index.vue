<script setup>
import VueDatePicker from "@vuepic/vue-datepicker";
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import Label from "@/src/components/ui/Label.vue";
import Button from "@/src/components/ui/Button.vue";
import ServerTable from "@/src/components/ui/table/ServerTable.vue";
import RouterButton from "@/src/components/ui/RouterButton.vue";
import SelectInput from "@/src/components/ui/formInput/SelectInput.vue";
import Table from "@/src/components/ui/table/Table.vue";
import { useTableSearch } from "@/src/lib/useTableSearch";
import { useFetchPaginate } from "@/src/lib/useFetchPaginate";
import { ref, onMounted, computed } from "vue";
import { listCanvasOrderColumn } from "@/src/model/tableColumns/canvas-order";
import { useSorting } from "@/src/lib/useSorting";
import { usePagination } from "@/src/lib/usePagination";
import { useFiltering } from "@/src/lib/useFiltering";
import { salesCanvasService } from "@/src/services/salesCanvas";
import { parseCanvasStatus, simpleDateNow } from "@/src/lib/utils";
import { useUser } from "@/src/store/user";
import { useRouter } from "vue-router";
import { useOthers } from "@/src/store/others";

// Define stores and router
const router = useRouter();
const userStore = useUser();
const othersStore = useOthers();

// Initial data
const selectedStatus = ref(null);
const selectedOrderDate = ref(null);
const tanggal_order = ref(new Date())
const user = userStore.user.value;
const userBranch = computed(() => user?.nama_cabang);
const principalName = computed(() => user?.principal)

const { endpoints } = salesCanvasService;
const { onSortingChange, sorting } = useSorting();
const { onPaginationChange, pagination } = usePagination();
const { onColumnFilterChange, globalFilters } = useFiltering();

const fetchUrl = computed(() => {
  const user = userStore.user.value;
  return user?.id ? `${endpoints}/all-canvas-order?id=${user.id}` : null;
});

const [data, count, loading, totalPage, key] = useFetchPaginate(
  fetchUrl,
  {
    pagination,
    sorting,
    globalFilters,
    initialSortColumn: "nama_produk",
  }
);

const fieldPool = ["nama_produk", "status_order", "tanggal_order"];

const queryEntries = computed(() => {
  if (reset.value) return [];
  const entries = [
    ["tanggal_order=", selectedOrderDate.value ? simpleDateNow(selectedOrderDate.value) : undefined],
    ["status_order=", selectedStatus.value ? selectedStatus.value : undefined],
  ];

  if (globalFilters.value?.text && globalFilters.value?.text.trim() !== "") {
    entries.push(["filters=", globalFilters.value?.text]);
  }
  return entries.filter(([_, v]) => v !== undefined && v !== null && v !== "");
});

const options = {
  initialColumnName: "canvas_order",
  checkFieldFilterFunc: (val) => val[1] === undefined || val[1] === null,
  filterFunction: (val) => val[1] !== undefined && val[1] !== null,
  asArgument: true,
};

const [
    clientData,  
    buttonText,
    ,    
    isServerTable,     
    clientKey,        
    searchQuery,       
    reset 
] = useTableSearch(fetchUrl.value, fieldPool, queryEntries, options);

const canvasStatusOptions = [
  { id: 1, nama: parseCanvasStatus(1) },
  { id: 2, nama: parseCanvasStatus(2) },
  { id: 3, nama: parseCanvasStatus(3) }
]

const redirectToAddItems = () => { router.push({ name: "Add Canvas Order" }) };

onMounted(async () => { 
  console.log('User data:', userStore.user.value);
  console.log('Data Value:', data);
  await othersStore.getOthers();
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
        <template #header>Informasi Sales Canvas</template>
        <template #content>
            <div class="form-grid-card tw-grid-cols-3 tw-items-end">
            <Label label="Tanggal">
              <BFormInput
                size="md"
                readonly
                placeholder="yyyy-mm-dd"
                :class="'tw-bg-gray-200'"
                :model-value="simpleDateNow(tanggal_order)"
              />
            </Label>
            <Label label="Principal">
              <BFormInput
                size="md"
                readonly
                placeholder="Principal"
                :model-value="principalName"
                :class="'tw-bg-gray-200'"
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
          </div>
          <div class="form-grid-card tw-grid-cols-4 tw-items-end tw-gap-4">
            <Label label="Status Pembayaran">
              <SelectInput
                placeholder="Pilih Status Pembayaran"
                size="md"
                :search="false"
                text-field="nama"
                value-field="id"
                v-model="selectedStatus"
                :options="canvasStatusOptions"
              />
            </Label>
            <Label label="Tanggal Order">
              <VueDatePicker
                format="yyyy-MM-dd"
                placeholder="Pilih Tanggal"
                size="md"
                v-model="selectedOrderDate"
              />
            </Label>
            <div class="tw-col-span-2 tw-flex tw-justify-end">
              <Button
                :loading="loading"
                :trigger="searchQuery"
                icon="mdi mdi-magnify tw-mr-1"
                class="tw-h-[40px] tw-w-full xl:tw-w-36"
              >
                Cari Data
              </Button>
            </div>
          </div>
          <div class="form-grid-card tw-grid-cols-4 tw-items-end">
            <RouterButton
                to="/canvas-order/list-vouchers"
                icon="mdi mdi-ticket-percent tw-mr-2"
                class="tw-bg-indigo-600 hover:tw-bg-indigo-700 tw-py-2 tw-px-4 tw-w-full xl:tw-w-36"
            >
                Voucher
            </RouterButton>
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
          <template #header>List Order</template>
          <template #content>
          <FlexBox full jusEnd class="tw-px-4">
            <Button
              :trigger="redirectToAddItems"
              icon="mdi mdi-plus tw-mr-2"
              class="tw-py-2 tw-px-4"
            >
              Tambah
            </Button>
          </FlexBox>
          <ServerTable
              v-if="isServerTable"
              table-width="tw-w-full"
              :columns="listCanvasOrderColumn"
              :key="key"
              :table-data="Array.isArray(data) ? data : []"
              :loading="loading"
              :on-pagination-change="onPaginationChange"
              :on-global-filters-change="onColumnFilterChange"
              :on-sorting-change="onSortingChange"
              :pagination="pagination"
              :sorting="sorting"
              :filter="globalFilters"
              :page-count="totalPage"
              :total-data="count"
              :hideFooter="false"
          />
          <Table
              v-else
              :key="clientKey"
              :columns="listCanvasOrderColumn"
              :table-data="Array.isArray(clientData) ? clientData : (clientData?.pages || [])"
              :hideFooter="false"
          />
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>
