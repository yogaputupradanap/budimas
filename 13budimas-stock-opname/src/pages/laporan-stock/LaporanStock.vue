<script setup>
import SelectInput from "@/src/components/ui/formInput/SelectInput.vue";
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Skeleton from "@/src/components/ui/Skeleton.vue";
import Card from "@/src/components/ui/Card.vue";
import Label from "@/src/components/ui/Label.vue";
import { BFormInput } from "bootstrap-vue-next";
import Table from "@/src/components/ui/table/Table.vue";
import { listStockColumns } from "@/src/model/tableColumns/laporan-stock/listStock";
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
import * as XLSX from "xlsx";
import { stockOpnameService } from "@/src/services/stockOpname";
import { saveAs } from "file-saver";

const others = useOthers();

const { principal, stockOpname, stockCabang } = storeToRefs(others);
const { onPaginationChange, pagination } = usePagination();
const { onColumnFilterChange, globalFilters } = useFiltering();
const { onSortingChange, sorting } = useSorting();

const { paginateStockOpnameUrl } = stockOpnameService;
const alert = useAlert();
const userStore = useUser();
const isServerTable = ref(false);

const perusahaan = ref(userStore.user.value.nama_perusahaan);
const cabang = ref(userStore.user.value.nama_cabang);
const cariData = ref(false);
const principalSelected = ref("");
const tanggal = ref("");
const listStockOpname = ref([]);
const id_cabang = userStore.user.value?.id_cabang;
const datePickerLocale = {
  locale: "id",
  format: "yyyy-MM-dd",
};

onMounted(() => {
  stockCabang.value.list = [];
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
  try {
    searchLoading.value = true;
    others.getStockCabangByPrincipal(principalSelected.value, id_cabang);
  } catch (error) {
    alert.setMessage(error, "danger");
  } finally {
    searchLoading.value = false;
  }
};

const exportExcel = () => {
  const dataMapping = stockCabang.value.list.map((val) => {
    return {
      Tanggal: val.tanggal_update,
      Perusahaan: perusahaan.value,
      Cabang: cabang.value,
      Principal: val.nama_principal,
      "Kode SKU": val.sku,
      Produk: val.nama_produk,
      "Stock Akhir": val.jumlah_gudang,
      "Jumlah Incoming": val.jumlah_incoming,
      Satuan: val.uom,
    };
  });

  const ws = XLSX.utils.json_to_sheet(dataMapping);
  const wb = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb, ws, "Sheet1");

  // Adjust column widths
  const autoWidth = (ws) => {
    const colWidths = dataMapping.map(
      (row) =>
        Object.values(row).map((val) => (val ? val.toString().length : 10)) // Default width if value is undefined
    );
    const maxColWidths = colWidths[0].map((_, i) =>
      Math.max(...colWidths.map((row) => row[i]))
    );
    ws["!cols"] = maxColWidths.map((w) => ({ wch: w + 10 }));
  };

  autoWidth(ws);

  const excelBuffer = XLSX.write(wb, { bookType: "xlsx", type: "array" });
  const data = new Blob([excelBuffer], { type: "application/octet-stream" });
  saveAs(
    data,
    `Stock Cabang-${cabang.value}-${perusahaan.value}-${
      dataMapping[0].Principal
    }-${new Date().toISOString().slice(0, 10)}.xlsx`
  );
};

const [data, count, loading, totalPage, key] = useFetchPaginate(
  `${paginateStockOpnameUrl}?id_cabang=${id_cabang}&`,
  {
    pagination,
    sorting,
    globalFilters,
    initialSortColumn: "tanggal_so",
    filterColum: "test",
  }
);

watch(
  stockOpname,
  () => {
    listStockOpname.value = stockOpname.value.list;
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
        <template #header>Form Cek Stock Cabang</template>
        <template #content>
          <div class="form-grid-card-4-menu tw-items-end">
            <Label label="Kode Stock Opname">
              <BFormInput
                disabled
                v-model="perusahaan"
                placeholder="Nama Perusahaan"
              />
            </Label>
            <Label label="Cabang" class="z-10">
              <BFormInput disabled v-model="cabang" placeholder="Nama Cabang" />
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
            <Button
              :trigger="searchQuery"
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
      class="slide-container tw-z-0"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.3"
      :delay-out="0.1"
      :initial-x="-40"
      :x="40"
    >
      <Card no-subheader>
        <template #header>Laporan Stock Cabang</template>
        <template #content>
          <div class="tw-flex tw-self-end tw-mb-4 tw-w-full tw-justify-end">
            <Button
              class="btn-c-success tw-text-base tw-py-2 tw-px-5"
              icon="mdi mdi-file-excel"
              v-if="stockCabang.list.length > 0"
              :loading="loadingSubmit"
              :trigger="exportExcel"
              >Excel</Button
            >
          </div>
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
            classic="true"
          />
          <Table
            v-else
            :key="localStore || []"
            :columns="listStockColumns(perusahaan, cabang)"
            :loading="stockCabang.loading"
            :classic="true"
            :table-data="stockCabang.list"
          />
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>
