<script setup>
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import Label from "@/src/components/ui/Label.vue";
import SelectInput from "@/src/components/ui/formInput/SelectInput.vue";
import Button from "@/src/components/ui/Button.vue";
import {onMounted, ref} from "vue";
import Skeleton from "@/src/components/ui/Skeleton.vue";
import ServerTable from "@/src/components/ui/table/ServerTable.vue";
import {usePagination} from "@/src/lib/usePagination";
import {useFiltering} from "@/src/lib/useFiltering";
import {useSorting} from "@/src/lib/useSorting";
import {useFetchPaginateV2} from "@/src/lib/useFetchPaginateV2";
import {useOthers} from "@/src/store/others";
import {$swal} from "@/src/components/ui/SweetAlert.vue";
import {
  listPreviewJurnalSetting,
  listSumberData
} from "@/src/model/tableColumns/jurnal-setting/listPreviewJurnalSetting";
import RouterButton from "@/src/components/ui/RouterButton.vue";
import axios from "axios";
import {fetchWithAuth, sessionDisk} from "@/src/lib/utils";
import Modal from "@/src/components/ui/Modal.vue";
import Table from "@/src/components/ui/table/Table.vue";

const selectedPerusahaanFilter = ref(null);
const selectedPerusahaanModal = ref(null);
const dataSourceModul = ref([]);

const others = useOthers()
const tipeModal = ref(1); // 1 tambah, 2 update
const triggerFetch = ref(0);
const laodingSubmit = ref(false);
const advancedFilters = ref([]);
const {onPaginationChange, pagination} = usePagination();
const {onColumnFilterChange, globalFilters} = useFiltering();
const {onSortingChange, sorting} = useSorting();
const modalJurnalSetting = ref(null);

const handleFilter = () => {
  advancedFilters.value = [];
  const dataFilter = []
  if (selectedPerusahaanFilter.value) {
    dataFilter.push(
        {
          column: "id_perusahaan",
          value: selectedPerusahaanFilter.value,
        }
    )
  }
  advancedFilters.value = dataFilter;
}

const getSourceData = async () => {
  try {
    const res = await fetchWithAuth("GET", "/api/akuntansi/get-source-modul-use-jurnal-setting")
    dataSourceModul.value = res
  } catch (error) {
    console.log("Error fetching source data:", error);
    $swal.error("Gagal mengambil data sumber modul: " + error);
  }
}


const handleDelete = async (row) => {
  const isConfirm = await $swal.confirm(
      "Apakah Anda yakin ingin menghapus data jurnal setting ini?",
  );
  if (!isConfirm) {
    return;
  }

  laodingSubmit.value = true;
  try {
    const clause = {
      "id_jurnal_mal = ": `'${row.id_jurnal_mal}'`
    }
    const body = {
      "is_deleted  ": true,
      "deleted_at  ": new Date().toISOString(),
    }
    await axios.put(
        `${process.env.VUE_APP_API_URL}/api/base/jurnal_mal?where=` + encodeURIComponent(JSON.stringify(clause)),
        body,
        {
          headers: {
            Authorization: `Bearer ${sessionDisk.getSession("authUser").token}`,
            "Content-Type": "multipart/form-data"
          }
        }
    )
    $swal.success("Berhasil menghapus data jurnal setting.");
    // refresh table
    triggerFetch.value += 1;
  } catch (error) {
    console.log("Error deleting coa:", error);
    $swal.error("Gagal menghapus data jurnal setting: " + error);
  } finally {
    laodingSubmit.value = false;
  }
};

const [data, count, loading, totalPage, key] = useFetchPaginateV2(
    `/api/akuntansi/get-jurnal-mal-list?`,
    {
      pagination,
      sorting,
      globalFilters,
      initialSortColumn: "id_jurnal_mal",
      advancedFilters: advancedFilters,
      initialSortDirection: "desc",
      isRunOnMounted: true,
      triggerFetch
    }
);

onMounted(
    async () => {
      await getSourceData();
    }
)

</script>

<template>
  <Modal ref="modalJurnalSetting" id="modalJurnalSetting" size="xl">
    <SlideRightX
        :duration-enter="0.3"
        :duration-leave="0.3"
        :delay-in="0.1"
        :delay-out="0.1"
        :initial-x="-20"
        :x="20">
      <Card no-subheader>
        <template #header>List Source Data</template>
        <template #content>
          <div class="tw-space-y-4 tw-w-full">
            <Table
                :table-data="dataSourceModul"
                :columns="listSumberData"
            />
            <div class="tw-flex tw-gap-2 tw-justify-end">
              <Button
                  :trigger="() => { modalJurnalSetting.hide() }"
                  icon="mdi mdi-close"
                  class="tw-h-[38px] tw-w-full xl:tw-w-44"
              >
                Close
              </Button>
            </div>
          </div>
        </template>
      </Card>
    </SlideRightX>
  </Modal>
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
        <template #header>Filter MAL</template>
        <template #content>
          <div class="form-grid-card-5-col tw-items-end">
            <Label label="Perusahaan">
              <Skeleton
                  class="tw-w-full tw-h-[34px]"
                  v-if="others.perusahaan.loading"
              />
              <SelectInput
                  v-else
                  v-model="selectedPerusahaanFilter"
                  placeholder="Pilih Data"
                  size="md"
                  :search="true"
                  :options="others.perusahaan.list"
                  text-field="nama"
                  value-field="id"
              />
            </Label>
            <div class="tw-flex tw-gap-2">
              <Button
                  :trigger="handleFilter"
                  icon="mdi mdi-magnify"
                  class="tw-h-[38px] tw-w-full xl:tw-w-44"
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
        <template #header>List Jurnal Setting</template>
        <template #content>
          <FlexBox full jusEnd class="tw-mb-4">
            <RouterButton
                to="/journal-setting/add"
                icon="mdi mdi-plus"
                class="tw-h-[38px] tw-w-full xl:tw-w-44"
            >
              Tambah
            </RouterButton>
            <Button
                :trigger="() => { modalJurnalSetting.show() }"
                icon="mdi mdi-information-outline"
                class="tw-h-[38px] tw-w-full xl:tw-w-44 tw
                tw-ml-2"
            >
              List Sumber Data
            </Button>
          </FlexBox>
          <ServerTable
              :columns="listPreviewJurnalSetting( handleDelete)"
              :key="key"
              :table-data="data?.pages?.result || data?.result || []"
              :loading="loading"
              :on-pagination-change="onPaginationChange"
              :on-global-filters-change="onColumnFilterChange"
              :on-sorting-change="onSortingChange"
              :pagination="pagination"
              :sorting="sorting"
              :filter="globalFilters"
              :page-count="totalPage"
              :total-data="count"/>
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>