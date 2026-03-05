<script setup>
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import Label from "@/src/components/ui/Label.vue";
import Button from "@/src/components/ui/Button.vue";
import Modal from "@/src/components/ui/Modal.vue";
import ServerTable from "@/src/components/ui/table/ServerTable.vue";
import Table from "@/src/components/ui/table/Table.vue";
import { useTableSearch } from "@/src/lib/useTableSearch";
import { useFetchPaginate } from "@/src/lib/useFetchPaginate";
import { ref, onMounted, computed, watch, nextTick, inject } from "vue";
import { detailCanvasRequestColumns } from "@/src/model/tableColumns/canvas-request/detail";
import { useSorting } from "@/src/lib/useSorting";
import { usePagination } from "@/src/lib/usePagination";
import { useFiltering } from "@/src/lib/useFiltering";
import { salesCanvasService } from "@/src/services/salesCanvas";
import { simpleDateNow, parseCurrency, breakdownToUOM } from "@/src/lib/utils";
import { useUser } from "@/src/store/user";
import { useRoute, useRouter } from "vue-router";
import { useOthers } from "@/src/store/others";

const $swal = inject("$swal");
const route = useRoute();
const router = useRouter();
const userStore = useUser();
const othersStore = useOthers();

const fetchUrl = ref("")
const formRef = ref({});
const modal = ref();
const totalPiecesInput = ref(0);
const userBranch = computed(() => userStore.user.value?.nama_cabang);
const salesCanvasData = computed(() => othersStore.salesCanvas.list);
const sisaPlafon = computed(() => salesCanvasData.value.sisa_plafon);
const plafonLimit = computed(() => salesCanvasData.value.plafon_limit);

const { id: id_canvas } = route.params;
const { tanggal_request } = route.query;

const { endpoints } = salesCanvasService;
const { onSortingChange, sorting } = useSorting();
const { onPaginationChange, pagination } = usePagination();
const { onColumnFilterChange, globalFilters } = useFiltering();

const [data, count, loading, totalPage, key] = useFetchPaginate(
  fetchUrl,
  {
    pagination,
    sorting,
    globalFilters,
    initialSortColumn: "nama_produk",
  }
);

const fieldPool = [];

const queryEntries = computed(() => {
  if (reset.value) return [];
  const entries = [
    ["nama_produk=", formRef.value.nama_produk],
  ];

  if (globalFilters.value?.text && globalFilters.value?.text.trim() !== "") {
    entries.push(["filters=", globalFilters.value?.text]);
  }
  return entries.filter(([_, v]) => v !== undefined && v !== null && v !== "");
});

const options = {
  initialColumnName: "nama_produk",
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
] = useTableSearch(fetchUrl, fieldPool, queryEntries, options);

const getTargetData = () => isServerTable.value ? data.value : clientData.value?.pages;

const findRowIndex = (targetData) => targetData?.findIndex(row => row.id === formRef.value.id) ?? -1;

const applyTableUpdate = (targetData, updatedRow, existIndex) => {
  const strategies = {
    server: () => {
      data.value[existIndex] = updatedRow;
      key.value = Date.now();
    },
    client: () => { clientData.value.pages[existIndex] = updatedRow }
  }
  const execution = isServerTable.value ? 'server' : 'client';
  strategies[execution]();
}

const showModalWithData = (rowData) => {
  if (rowData && typeof rowData === 'object' && !rowData.id && rowData.value) {
    rowData = rowData.value;
  }
  
  formRef.value = {
    id: rowData.id,
    nama_principal: rowData.nama_principal,
    nama_produk: rowData.nama_produk,
    stock_gudang: rowData.stock_gudang,
    qty_uom1: rowData.qty_uom1,
    qty_uom2: rowData.qty_uom2,
    qty_uom3: rowData.qty_uom3,
    uom1_nama: rowData.uom1_nama,
    uom2_nama: rowData.uom2_nama,
    uom3_nama: rowData.uom3_nama,
    uom1_factor: rowData.uom1_factor,
    uom2_factor: rowData.uom2_factor,
    uom3_factor: rowData.uom3_factor,
    harga_per_uom1: rowData.harga_per_uom1,
  }
  nextTick(() => { modal.value.show() });
}

const createUpdatedRowData = (originalRow, tempData) => ({
  ...originalRow,
  _isTemp: true,
  qty_uom1: tempData.qty_uom1,
  qty_uom2: tempData.qty_uom2,
  qty_uom3: tempData.qty_uom3,
  total_satuan: tempData.qty_request,
  harga_per_uom1: tempData.harga_per_pieces,
  total_permintaan: tempData.total_permintaan,
})

const updateTempTableData = async () => {
  if (!formRef.value.id) return;

  const payload = {
    id_produk: formRef.value.id,
    id_user: userStore.user.value?.id,
    qty_uom1: Number(formRef.value.qty_uom1) || 0,
    qty_uom2: Number(formRef.value.qty_uom2) || 0,
    qty_uom3: Number(formRef.value.qty_uom3) || 0,
  };

  try {
    const response = await salesCanvasService.updateCanvasRequestTemp(payload);
    if (!response?.pages?.[0]) { throw new Error('Response tidak valid!') }

    const tempData = response.pages[0];
    await nextTick(() => updateTableRowData(tempData));
    $swal.success('Request berhasil diupdate!');
    modal.value.hide();
  } catch (error) {
    console.error('Error updating temp canvas request:', error);
  }
};

const formEditConfirmation = async () => {
  if (!formRef.value.id) return;

  const payload = {
    canvas_request_id: id_canvas,
    id_produk: formRef.value.id,
    qty_uom1: Number(formRef.value.qty_uom1) || 0,
    qty_uom2: Number(formRef.value.qty_uom2) || 0,
    qty_uom3: Number(formRef.value.qty_uom3) || 0,
  };

  if (!payload.qty_uom1 && !payload.qty_uom2 && !payload.qty_uom3) {
    $swal.error('Jumlah request tidak boleh nol!');
    return;
  }

  try {
    await salesCanvasService.updateCanvasData(payload);
    router.push({ name: 'Canvas Request' });
    $swal.success('Edit request berhasil dikonfirmasi!');
  } catch (error) {
    console.error('Error creating canvas request:', error);
  }
}

const updateTableRowData = (tempData) => {
  const targetData = getTargetData();
  if (!Array.isArray(targetData)) return;
  
  const existingIndex = findRowIndex(targetData);
  if (existingIndex === -1) return;

  const updatedRow = createUpdatedRowData(targetData[existingIndex], tempData);
  applyTableUpdate(targetData, updatedRow, existingIndex);
};

const totalNominal = computed(() => {
  const tableData = isServerTable.value ? data.value : clientData.value?.pages || [];
  if (!Array.isArray(tableData)) return 0;
  
  return tableData.reduce((sum, row) => {
    return sum + (row.total_permintaan);
  }, 0);
});

const conditionalEditButtonShow = computed(() => {
  const pages = salesCanvasData.value?.pages || [];
  const findItem = pages.find(item => Number(item.id) === Number(id_canvas));
  return findItem.status === 3;
});

const tableMeta = { updateRow: (rowData, rowIndex, columnId, funcId) => {
    if (funcId === "openRowModal") { showModalWithData(rowData) }
  }
};

watch(() => userStore.user.value, (user) => {
  if (user?.id && id_canvas && tanggal_request) {
    const withParams = fetchUrl.value.includes('?') ? '&' : '?';
    const params = new URLSearchParams({ id_canvas, tanggal_request, id: user.id });
    fetchUrl.value = `${endpoints}/detail-canvas-request${withParams}${params.toString()}`;
  }
}, { immediate: true });

watch(() => totalPiecesInput.value, (newTotal) => {
  if (newTotal > 0 && formRef.value.uom1_factor) {
    const breakdown = breakdownToUOM(newTotal, {
      uom1_factor: formRef.value.uom1_factor,
      uom2_factor: formRef.value.uom2_factor,
      uom3_factor: formRef.value.uom3_factor
    });
    
    formRef.value.qty_uom1 = breakdown.uom1;
    formRef.value.qty_uom2 = breakdown.uom2;
    formRef.value.qty_uom3 = breakdown.uom3;
  }
});

onMounted(async () => { await othersStore.getOthers() });

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
        <template #header>Detail Sales Canvas</template>
        <template #content>
            <div class="form-grid-card tw-items-end">
            <Label label="Tanggal Request">
              <BFormInput
                size="md"
                readonly
                placeholder="yyyy-mm-dd"
                :class="'tw-bg-gray-200'"
                :model-value="simpleDateNow(tanggal_request)"
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
            <Label label="Limit Plafon">
              <BFormInput
                size="md"
                readonly
                placeholder="Rp. 0"
                :class="'tw-bg-gray-200'"
                :model-value="parseCurrency(plafonLimit)"
              />
            </Label>
            <Label label="Sisa Plafon">
              <BFormInput
                size="md"
                readonly
                placeholder="Rp. 0"
                :class="'tw-bg-gray-200'"
                :model-value="parseCurrency(sisaPlafon)"
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
            <template #header>List Produk</template>
            <template #content>
            <ServerTable
                v-if="isServerTable"
                table-width="tw-w-full"
                :columns="detailCanvasRequestColumns"
                :key="key"
                :table-data="data"
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
                :meta="tableMeta"
                @open-row-modal="(val) => showModalWithData(val)"
            >
              <template #footer>
                <tr class="tw-bg-gray-100 tw-border-t">
                  <td colspan="6" class="tw-p-2 tw-text-center tw-font-medium tw-text-sm tw-border-r">
                    Total Nominal Produk
                  </td>
                  <td class="tw-p-2 tw-text-center tw-font-semibold tw-text-sm">
                    {{ parseCurrency(totalNominal) }}
                  </td>
                </tr>
              </template>
            </ServerTable>
            <Table
                v-else
                :key="clientKey"
                :columns="detailCanvasRequestColumns"
                :table-data="clientData?.pages || []"
                :hideFooter="false"
                :meta="tableMeta"
                @open-row-modal="showModalWithData"
            >
              <template #footer>
                <tr class="tw-bg-gray-100 tw-border-t">
                  <td class="tw-p-2 tw-text-center tw-font-semibold tw-text-sm tw-border-l">
                    Total Nominal Produk:
                  </td>
                  <td class="tw-p-2 tw-text-center tw-font-medium tw-text-sm">
                    {{ parseCurrency(totalNominal) }}
                  </td>
                </tr>
              </template>
            </Table>
            <FlexBox full jusEnd>
              <Button
                v-if="conditionalEditButtonShow"
                :trigger="formEditConfirmation"
                icon="tw-mx-3 mdi mdi-check"
                class="tw-pr-6 tw-py-2 tw-text-sm tw-bg-indigo-500"
              >
                Konfirmasi Edit
              </Button>
            </FlexBox>
            <Modal
                ref="modal"
                id="modal"
                :centered="true"
              >
                <Card no-subheader>
                  <template class="tw-h-auto" #header>Edit Request</template>
                  <template #content>
                    <div class="tw-w-full tw-grid tw-grid-cols-1 tw-gap-4 lg:tw-grid-cols-1">
                    <Label label="Principal">
                      <BFormInput
                        readonly
                        class="tw-w-full"
                        :model-value="formRef.nama_principal"
                        :disabled="loading"
                        :class="'tw-bg-gray-200'"
                      />
                    </Label>
                    <Label label="Nama Produk">
                      <BFormInput
                        readonly
                        placeholder="Nama Produk"
                        :model-value="formRef.nama_produk"
                        :disabled="loading"
                        :class="'tw-bg-gray-200'"
                      />
                    </Label>
                    <Label label="Stok Gudang">
                      <BFormInput
                        readonly
                        placeholder="0 Pcs"
                        :model-value="formRef.stock_gudang + ` Pcs`"
                        :disabled="loading"
                        :class="'tw-bg-gray-200'"
                      />
                    </Label>
                    <Label label="Jumlah UOM 1 / Pieces">
                      <BFormInput
                        type="number"
                        placeholder="0"
                        v-model="formRef.qty_uom1"
                        :disabled="loading"
                      />
                    </Label>
                    <Label label="Jumlah UOM 2 / Box">
                      <BFormInput
                        type="number"                        
                        placeholder="0"
                        v-model="formRef.qty_uom2"
                        :disabled="loading"
                      />
                    </Label>
                    <Label label="Jumlah UOM 3 / Karton">
                      <BFormInput
                        type="number"                        
                        placeholder="0"
                        v-model="formRef.qty_uom3"
                        :disabled="loading"
                      />
                    </Label>
                    <div>
                    </div>
                    <FlexBox
                      full jus-center
                      class="tw-mt-4 lg:tw-justify-end lg:tw-flex-row tw-flex-wrap-reverse"
                    >
                      <Button 
                        :trigger="updateTempTableData"
                        class="tw-px-14 tw-py-2 tw-text-sm tw-bg-green-500"
                      >
                        Submit
                      </Button>
                    </FlexBox>
                    </div>
                  </template>
                </Card>
              </Modal>
          </template>
        </Card>
    </SlideRightX>
  </FlexBox>
</template>
