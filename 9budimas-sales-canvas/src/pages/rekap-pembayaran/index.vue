<script setup>
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import Label from "@/src/components/ui/Label.vue";
import Button from "@/src/components/ui/Button.vue";
import FIleInput from "@/src/components/ui/formInput/FIleInput.vue";
import ServerTable from "@/src/components/ui/table/ServerTable.vue";
import SelectInput from "@/src/components/ui/formInput/SelectInput.vue";
import Table from "@/src/components/ui/table/Table.vue";
import { useTableSearch } from "@/src/lib/useTableSearch";
import { useFetchPaginate } from "@/src/lib/useFetchPaginate";
import { ref, onMounted, computed } from "vue";
import { listRekapPembayaran } from "@/src/model/tableColumns/rekap-pembayaran";
import { useSorting } from "@/src/lib/useSorting";
import { usePagination } from "@/src/lib/usePagination";
import { useFiltering } from "@/src/lib/useFiltering";
import { salesCanvasService } from "@/src/services/salesCanvas";
import { simpleDateNow } from "@/src/lib/utils";
import { useUser } from "@/src/store/user";
import { useRouter } from "vue-router";

// Define stores and router
const router = useRouter();
const userStore = useUser();

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

const redirectToAddItems = () => { router.push({ name: "Add Canvas Order" }) };

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
        <template #header>Rekap Pembayaran Sales Canvas</template>
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
            <Label label="Cabang">
              <BFormInput
                size="md"
                readonly
                placeholder="Pilih Data"
                :class="'tw-bg-gray-200'"
                :model-value="userBranch"
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
          <template #header>Rekap Pembayaran</template>
          <template #content>
          <ServerTable
              v-if="isServerTable"
              table-width="tw-w-full"
              :columns="listRekapPembayaran"
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
              :columns="listRekapPembayaran"
              :table-data="Array.isArray(clientData) ? clientData : (clientData?.pages || [])"
              :hideFooter="true"
          />
          <FlexBox full flex-col>
            <div class="tw-grid tw-grid-cols-1 md:tw-grid-cols-3 tw-w-full tw-px-16 tw-gap-3">
                <Label label="Jumlah Setoran Tunai" class="tw-text-sm tw-w-full">
                    <BFormInput
                    size="md"
                    readonly
                    placeholder="Total Nominal"
                    class="tw-bg-gray-200 tw-text-start tw-w-full"
                    :model-value="`Rp. 1.500.000`"
                    />
                </Label>
                <Label label="Jumlah Setoran Non Tunai" class="tw-text-sm tw-w-full">
                    <BFormInput
                    size="md"
                    readonly
                    placeholder="Total Nominal"
                    class="tw-bg-gray-200 tw-text-start tw-w-full"
                    :model-value="`Rp. 1.500.000`"
                    />
                </Label>
                <Label label="Total Setoran" class="tw-text-sm tw-w-full">
                    <BFormInput
                    size="md"
                    readonly
                    placeholder="Total Nominal"
                    class="tw-bg-gray-200 tw-text-start tw-w-full"
                    :model-value="`Rp. 3.000.000`"
                    />
                </Label>
            </div>
            <div class="tw-grid tw-grid-cols-1 tw-w-full tw-px-16">
                <FlexBox full>
                    <FIleInput
                        class="tw-w-full"
                        accept="image/*"
                        group-id="file-1"
                        label="Upload Bukti Transfer"
                        label-for="input-file-1" 
                    />
                </FlexBox>
            </div>
            <FlexBox full jusEnd>
                <Button
                    class="tw-mt-4 tw-w-full md:tw-w-1/3"
                    variant="primary"
                    @click="redirectToAddItems"
                >
                    Submit
                </Button>
            </FlexBox>
        </FlexBox>
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>
