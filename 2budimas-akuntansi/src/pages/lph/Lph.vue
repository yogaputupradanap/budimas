<script setup>
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import Modal from "@/src/components/ui/Modal.vue";
import ServerTable from "@/src/components/ui/table/ServerTable.vue";
import Button from "@/src/components/ui/Button.vue";
import { lphColumns } from "@/src/model/tableColumns/lph/lphCol";
import { usePagination } from "@/src/lib/usePagination";
import { useFiltering } from "@/src/lib/useFiltering";
import { useSorting } from "@/src/lib/useSorting";
import { useFetchPaginate } from "@/src/lib/useFetchPaginate";
import { ref } from "vue";
import { useUser } from "@/src/store/user";
import { useRouter } from "vue-router";

const user = useUser();
const router = useRouter();
const modalLphOption = ref(null);

const { onPaginationChange, pagination } = usePagination();
const { onColumnFilterChange, globalFilters } = useFiltering();
const { onSortingChange, sorting } = useSorting();

// Gunakan endpoint string literal atau fallback
const lphEndpoint = "/api/akuntansi/get-lph";

const [data, count, loading, totalPage, key] = useFetchPaginate(lphEndpoint, {
  pagination,
  sorting,
  globalFilters,
  initialSortColumn: "tanggal_lph",
  additionalParams: {
    id_cabang: user?.user?.value?.id_cabang,
  }
});

const showModalLph = () => modalLphOption.value?.show();

const selectByCustomer = async () => {
  modalLphOption.value?.hide();
  await router.push({ path: '/lph/add-lph-customer' });
}

const selectBySales = async () => {
  modalLphOption.value?.hide();
  await router.push({ path: '/lph/add-lph' });
}

</script>

<template>
  <FlexBox full flex-col>
    <Modal 
      ref="modalLphOption" 
      id="modalLphOption" 
      size="md"
      :centered="true"
    >
      <Card no-subheader>
        <template #header>
          <span>Tambah LPH</span>
        </template>
        <template #content>
          <div class="tw-space-y-3 tw-w-full">
            <div class="tw-w-full">
              <Button
                :trigger="selectByCustomer"
                icon="mdi mdi-account-group"
                class="tw-w-full tw-h-12 tw-bg-blue-500 hover:tw-bg-blue-600 tw-text-white tw-font-semibold"
              >
                Berdasarkan Customer
              </Button>
            </div>
            <div class="tw-w-full">
              <Button
                :trigger="selectBySales"
                icon="mdi mdi-account-tie"
                class="tw-w-full tw-h-12 tw-bg-green-500 hover:tw-bg-green-600 tw-text-white tw-font-semibold"
              >
                 Berdasarkan Sales
              </Button>
            </div>
          </div>
        </template>
      </Card>
    </Modal>
    <SlideRightX
      class="slide-container"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.2"
      :delay-out="0.2"
      :initial-x="-40"
      :x="40">
      <Card no-subheader>
        <template #header>
          <div class="tw-flex tw-justify-between tw-items-center">
            <span>List Penagihan Hutang</span>
          </div>
        </template>
        <template #content>
          <FlexBox full jusEnd class="tw-px-4">
            <Button
              :trigger="showModalLph"
              class="tw-px-4 tw-py-2"
              variant="primary"
              icon="mdi mdi-plus"
              size="sm"
            >
              Tambah LPH
            </Button>
          </FlexBox>
          <ServerTable
    :columns="lphColumns"
    :key="key"
    :table-data="data?.result || []"  :loading="loading"
    :page-count="totalPage"
    :total-data="count"
    :pagination="pagination"
    :sorting="sorting"
    :filter="globalFilters"
    @on-pagination-change="onPaginationChange"
    @on-global-filters-change="onColumnFilterChange"
    @on-sorting-change="onSortingChange"
/>
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>
