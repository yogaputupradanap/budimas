<script setup>
import SlideRightX from "../components/animation/SlideRightX.vue";
import Card from "../components/ui/Card.vue";
import StatusBar from "../components/ui/StatusBar.vue";
import {getDateNow} from "../lib/utils";
import {useKepalaCabang} from "../store/kepalaCabang";
import {ref, computed, watch} from "vue";
import {useHistory} from "../store/history";
import ServerTableV2 from "@/src/components/ui/table/ServerTableV2.vue";
import {tabelDistribusiHistory} from "@/src/model/tableColumns/tabelDistribusiHistory";
import {useFetchPaginate} from "@/src/lib/useFetchPaginate";
import {usePagination} from "@/src/lib/usePagination";
import {useFiltering} from "@/src/lib/useFiltering";
import {useSorting} from "@/src/lib/useSorting";

const user = useKepalaCabang();
const history = useHistory();
const {onPaginationChange, pagination} = usePagination();
const {onColumnFilterChange, globalFilters} = useFiltering();
const {onSortingChange, sorting} = useSorting();
const tableKey = ref(0);
const idCabang = user.kepalaCabangUser.id_cabang;


/*
  Nama cabang (aman dari undefined)
*/
const namaCabang = computed(() => {
  return (
    user.kepalaCabangUser?.kepalaCabang?.nama_cabang ||
    user.kepalaCabangUser?.nama_cabang ||
    "-"
  );
});

const getResource = async () => {
  await history.getRuteList(idCabang);
  tableKey.value++;
};
const [data, count, loading, totalPage, key] = useFetchPaginate(
    `${process.env.VUE_APP_API_URL}/api/distribusi/get-list-history-distribusi?id_cabang=${idCabang}&`,
    {
      pagination,
      sorting,
      globalFilters,
      initialSortColumn: "tanggal_terkirim",
      initialSortDirection: "desc",
    }
);
// watch(data, (val) => {
//     console.log("DATA HISTORY:", val);
//   console.log("ARRAY:", val?.result);

// });
</script>

<template>
  <div class="tw-flex tw-flex-col tw-gap-4 tw-min-h-[80vh]">
    <SlideRightX
        :duration-enter="0.6"
        :duration-leave="0.6"
        :delay-out="0.1"
        :delay-in="0.1"
        :initial-x="-40"
        :x="40">
      <Card :no-subheader="true">
        <template #header>History Distribusi</template>
        <template #content>
          <div class="status-field-container-2-col">
            <StatusBar
                label="Cabang :"
                :value="namaCabang"/>
            <StatusBar
                label="Tanggal Distribusi:"
                :value="getDateNow(new Date(), false)"/>
          </div>
        </template>
      </Card>
    </SlideRightX>
    <SlideRightX
        :duration-enter="0.6"
        :duration-leave="0.6"
        :delay-out="0.2"
        :delay-in="0.2"
        :initial-x="-40"
        :x="40">
      <Card :no-subheader="true" class="tw-pb-10">
        <template #header>List Faktur</template>
        <template #content>
          <!--          <Table-->
          <!--              :key="tableKey"-->
          <!--              :loading="history.listRuteHistory.loading"-->
          <!--              :table-data="history.listRuteHistory.listRute"-->
          <!--              :columns="tabelDistribusiHistory"/>-->
          <ServerTableV2
            :columns="tabelDistribusiHistory"
            :key="key"
            :loading="loading"
            :table-data="data?.result || []"
            :on-pagination-change="onPaginationChange"
            :on-global-filters-change="onColumnFilterChange"
            :on-sorting-change="onSortingChange"
            :pagination="pagination"
            :sorting="sorting"
            :filter="globalFilters"
            :page-count="totalPage"
            :total-data="count"
          />
        </template>
      </Card>
    </SlideRightX>
  </div>
</template>
