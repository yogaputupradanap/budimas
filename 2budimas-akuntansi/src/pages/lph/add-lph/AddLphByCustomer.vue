<script setup>
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import Table from "@/src/components/ui/table/Table.vue";
import {setoranService} from "@/src/services/setoran";
import {computed, ref, watch} from "vue";
import Label from "@/src/components/ui/Label.vue";
import Skeleton from "@/src/components/ui/Skeleton.vue";
import VueDatePicker from "@vuepic/vue-datepicker";
import Button from "@/src/components/ui/Button.vue";
import {useOthers} from "@/src/store/others";
import {useUser} from "@/src/store/user";
import { fetchWithAuth, formatCurrencyAuto, getTodayDate } from "@/src/lib/utils";
import SelectInput from "@/src/components/ui/formInput/SelectInput.vue";
import {addLphByCustomerColumns, addLphCustomerColModal} from "@/src/model/tableColumns/lph/add-lph/addLphByCustomerCol";
import {$swal} from "@/src/components/ui/SweetAlert.vue";
import {generateLphPdf} from "@/src/model/pdf/lphPdfTemplate";
import Modal from "@/src/components/ui/Modal.vue";
import { debounce } from "@/src/lib/debounce";

const {endpoints} = setoranService;
const others = useOthers();
const user = useUser();
const sales = ref(null);
const customer = ref(null);
const customerSearchQuery = ref('');
const customerLoading = ref(false);
const tanggal = ref(getTodayDate(1));
const dataTable = ref([]);
const dataTableModal = ref([]);
const loadingTableModal = ref(false);
const loadingTable = ref(false);
const hasSearched = ref(false);
const tableRef = ref(null);
const tableModalRef = ref(null);
const selectedCustomer = ref(null);
const id_cabang = user?.user?.value?.id_cabang;
const formTambahLph = ref(null);
const formSales = ref(null);

const getResource = async () => {
  if (!customer.value || !tanggal.value) {
    $swal.warning("Semua filter harus diisi");
    return;
  }

  try {
    loadingTable.value = true;
    const tanggalValue = tanggal.value;
    const response = await fetchWithAuth(
        "GET",
        `${endpoints.getAddLphByCustomer}?id_cabang=${id_cabang}&id_customer=${customer.value}&tanggal=${tanggalValue}`
    );
    dataTable.value = response || [];
    hasSearched.value = true;
  } catch (error) {
    console.error("Error fetching data:", error);
    dataTable.value = [];
  } finally {
    loadingTable.value = false;
  }
};

const totalTagihan = computed(() => {
  if (!tableRef.value) return 0;
  const selectedRows = tableRef.value.getSelectedRow();
  const selectedData = Object.keys(selectedRows).map(
      (index) => dataTable.value[parseInt(index)]
  );
  return selectedData.reduce(
      (sum, item) => sum + (item?.sisa_pembayaran || 0),
      0
  );
});

const totalRetur = computed(() => {
  if (!tableRef.value) return 0;
  const selectedRows = tableRef.value.getSelectedRow();
  const selectedData = Object.keys(selectedRows).map(
      (index) => dataTable.value[parseInt(index)]
  );
  return selectedData.reduce(
      (sum, item) => sum + (item?.nominal_retur || 0),
      0
  );
});

const submitLph = async () => {
  if (!tableRef.value) {
    $swal.warning("Tabel belum siap");
    return;
  }

  const selectedRows = tableRef.value.getSelectedRow();
  const selectedData = Object.keys(selectedRows).map(
      (index) => dataTable.value[parseInt(index)]
  );

  if (!sales.value) {
    $swal.warning("Pilih PJ (Sales) terlebih dahulu");
    return;
  }

  try {
    const isConfirmed = await $swal.confirmSubmit();
    if (!isConfirmed) return;
    loadingTable.value = true;

    const payload = {
      is_cp: null,
      id_cabang: id_cabang,
      id_sales: sales.value,
      tanggal: tanggal.value,
      id_user: user?.user?.value?.id,
      kode_perusahaan: dataTable.value[0]?.kode_perusahaan || "",
      nama_perusahaan: dataTable.value[0]?.nama_perusahaan || "",
      jumlah_ditagih: totalTagihan.value,
      data_tagihan: selectedData,
      total_retur: totalRetur.value,
    };

    console.log("LPH Payload:", payload);
    console.log("LPH Data Table:", dataTable.value);

    const response = await fetchWithAuth("POST", endpoints.addLph, payload);

    // Generate PDF using template
    const pdfDoc = generateLphPdf(response);

    // Download PDF
    const filename = `LPH-${
        response.data.kode_lph || "document"
    }-${new Date().getTime()}.pdf`;
    pdfDoc.save(filename);

    $swal.success("LPH berhasil dibuat dan diunduh");
    formSales.value.hide();
    reset();
  } catch (error) {
    console.error("Error submitting LPH:", error);
    $swal.error("Gagal menambahkan LPH");
  } finally {
    loadingTable.value = false;
  }
};

const submitAddLphModal = () => {
  if (!selectedCustomer.value) {
    $swal.warning("Pilih customer terlebih dahulu");
    return;
  }

  const selectedRows = tableModalRef.value.getSelectedRow();
  const selectedData = Object.keys(selectedRows).map(
      (index) => dataTableModal.value[parseInt(index)]
  );

  if (!selectedData.length) {
    $swal.warning("Pilih minimal satu tagihan untuk diunduh");
    return;
  }

  dataTable.value = [...dataTable.value, ...selectedData];
  closeModalTambahLph();
}

const showModalTambahLph = () => {
  if (formTambahLph.value) {
    formTambahLph.value.show();
    selectedCustomer.value = null;
    dataTableModal.value = [];
  }
};

const closeModalTambahLph = () => {
  if (formTambahLph.value) {
    formTambahLph.value.hide();
    dataTableModal.value = [];
    selectedCustomer.value = null;
  }
};

const reset = () => {
  customer.value = null;
  tanggal.value = getTodayDate();
  dataTable.value = [];
  hasSearched.value = false;
  others.resetCustomerSearch();
};

const showModalSales = () => {
  const selectedRows = tableRef.value.getSelectedRow();
  const selectedData = Object.keys(selectedRows).map(
      (index) => dataTable.value[parseInt(index)]
  );

  if (!selectedData.length) {
    $swal.warning("Pilih minimal satu tagihan untuk diunduh");
    return;
  }

  if (formSales.value) {
    formSales.value.show();
    sales.value = null;
  }
}

const getResourceModal = async () => {
  if (!selectedCustomer.value) return;

  try {
    loadingTableModal.value = true;
    const response = await fetchWithAuth(
        "GET",
        `${endpoints.getAddLphCustomerModal}?id_cabang=${id_cabang}&id_customer=${selectedCustomer.value}`
    );

    if (!response || !Array.isArray(response)) {
      dataTableModal.value = [];
      return;
    }

    dataTableModal.value = response;
  } catch (error) {
    console.error("Error fetching modal data:", error);
    dataTableModal.value = [];
  } finally {
    loadingTableModal.value = false;
  }
};

const searchCustomer = debounce(async (query) => {
  customerLoading.value = true;
  customerSearchQuery.value = query;
        
  if (!query || query.length < 2) {
    others.resetCustomerSearch();
    customerLoading.value = false;
    return;
  }

  await others.searchCustomer(query).catch((error) => {
    console.error("Error searching customers:", error);
  }).finally(() => {
    customerLoading.value = false;
  });
}, 300);

const handleCustomerSearch = (searchValue) => {searchCustomer(searchValue)};

watch(
    () => selectedCustomer.value,
    (newValue) => {
      if (newValue) {
        getResourceModal();
      } else {
        dataTableModal.value = [];
      }
    }
)

const customerModalOptions = computed(() => {
  const { isSearching, searchResults, displayData, list } = others.customer;
  const baseOptions = isSearching && searchResults.length
    ? searchResults : displayData.length 
    ? displayData : list;

  return baseOptions.map(cust => ({
    ...cust,
    displayText: `${cust.nama} (${cust.kode})`,
    searchText: `${cust.kode} ${cust.nama}`.toLowerCase()
  }));
});

const customerOptionsCount = computed(() => {
  const { isSearching, searchResults, fullDataLoaded, totalItems } = others.customer;
  const statusMap = [
    { condition: isSearching && searchResults.length > 0, value: `${searchResults.length} hasil pencarian` },
    { condition: fullDataLoaded, value: `${totalItems.toLocaleString()} customers tersedia` },
  ];
  const found = statusMap.find(item => item.condition);
  return found ? found.value : "Loading data...";
});

</script>

<template>
  <FlexBox full flex-col>
    <!-- Add Pengeluaran Modal -->
    <Modal ref="formTambahLph" id="formTambahLph" size="xl" :centered="true">
      <SlideRightX
          :duration-enter="0.3"
          :duration-leave="0.3"
          :delay-in="0.1"
          :delay-out="0.1"
          :initial-x="-20"
          :x="20">
        <Card no-subheader>
          <template #header>
            <div class="tw-flex tw-justify-between tw-items-center">
              <span>Form Tambah LPH</span>
            </div>
          </template>
          <template #content>
            <div class="tw-space-y-4 tw-w-full">
              <Label label="Customer">
                <SelectInput
                  v-model="selectedCustomer"
                  placeholder="Pilih Customer (Nama/Kode)"
                  size="md"
                  :search="true"
                  :server-search="true"
                  :options="customerModalOptions"
                  :virtual-scroll="true"
                  text-field="displayText"
                  value-field="id"
                  @search="handleCustomerSearch"
                />
              </Label>
              <h3 class="tw-text-lg tw-font-semibold tw-text-gray-800">
                List Faktur
              </h3>
              <Table
                ref="tableModalRef"
                :columns="addLphCustomerColModal"
                :table-data="dataTableModal"
                :loading="loadingTableModal"
              />
              <div class="tw-mt-4 tw-flex tw-gap-4 tw-justify-end">
                <Button
                    :loading="loadingTable"
                    :trigger="closeModalTambahLph"
                    icon="mdi mdi-close"
                    class="tw-h-[38px] tw-w-auto tw-px-6 tw-bg-red-500 hover:tw-bg-red-600">
                  Cancel
                </Button>
                <Button
                    :loading="loadingTable"
                    :trigger="submitAddLphModal"
                    :disabled="!dataTableModal.length"
                    icon="mdi mdi-check"
                    class="tw-h-[38px] tw-w-auto tw-px-6 tw-bg-green-500 hover:tw-bg-green-600">
                  Submit
                </Button>
              </div>
            </div>
          </template>
        </Card>
      </SlideRightX>
    </Modal>
    <Modal ref="formSales" id="formSales" size="md" :centered="true">
      <SlideRightX
          :duration-enter="0.3"
          :duration-leave="0.3"
          :delay-in="0.1"
          :delay-out="0.1"
          :initial-x="-20"
          :x="20">
        <Card no-subheader>
          <template #header>
            <div class="tw-flex tw-justify-between tw-items-center">
              <span>Form Pilih PJ</span>
            </div>
          </template>
          <template #content>
            <div class="tw-space-y-4 tw-w-full">
              <Label label="Cari Sales (PJ)">
                <SelectInput
                  v-model="sales"
                  placeholder="Pilih PJ"
                  size="md"
                  :search="true"
                  :options="others.sales.list"
                  :virtual-scroll="true"
                  text-field="nama"
                  value-field="id"
                />
              </Label>
            </div>
            <FlexBox full flexCol itEnd>
             <Button
                :trigger="submitLph"
                icon="mdi mdi-check tw-mr-2"
                class="tw-h-[38px] tw-w-auto tw-px-6 tw-bg-blue-500 hover:tw-bg-blue-600"
              >
                Submit
              </Button>
            </FlexBox>
          </template>
        </Card>
      </SlideRightX>
    </Modal>
    <SlideRightX
        class="slide-container tw-z-10"
        :duration-enter="0.6"
        :duration-leave="0.6"
        :delay-in="0.1"
        :delay-out="0.1"
        :initial-x="-40"
        :x="40">
      <Card no-subheader>
        <template #header>Cari Tagihan</template>
        <template #content>
          <FlexBox full flexCol itEnd class="md:tw-flex-row">
            <FlexBox full class="tw-flex-col tw-mb-4 md:tw-flex-row tw-gap-4">
              <Label full label="Cari Customer">
                <Skeleton class="skeleton" v-if="others.customer.loading"/>
                <SelectInput
                    v-else
                    v-model="customer"
                    :placeholder="others.customer.fullDataLoaded ? 'Pilih Customer' : 'Mencari data...'"
                    size="md"
                    :search="true"
                    :server-search="true"
                    :options="others.customerOptions"
                    :virtual-scroll="false"
                    text-field="nama"
                    value-field="id"
                    @search="handleCustomerSearch"
                />
                <div 
                  class="tw-text-xs tw-mt-1" 
                  v-on:reset="reset"
                  :class="others.customer.fullDataLoaded ? 'tw-text-green-600' : 'tw-text-orange-600'"
                >
                  {{ customerOptionsCount }}
                </div>
              </Label>
              <Label full label="Tanggal">
                <VueDatePicker
                    v-model="tanggal"
                    model-type="yyyy-MM-dd"
                    format="yyyy-MM-dd"
                    :clearable="false"
                    :enable-time-picker="false"
                    placeholder="yyyy-MM-dd"
                    auto-apply
                    :week-start="0"/>
              </Label>
            </FlexBox>
            <FlexBox full jusEnd>
              <FlexBox full jusEnd>
                <Button
                    :trigger="reset"
                    icon="mdi mdi-reload"
                    class="tw-h-[38px] tw-w-full xl:tw-w-32 tw-bg-red-500">
                  Reset
                </Button>
                <Button
                    :loading="loadingTable"
                    :trigger="getResource"
                    icon="mdi mdi-magnify"
                    class="tw-h-[38px] tw-w-full xl:tw-w-32">
                  Cari Data
                </Button>
              </FlexBox>
            </FlexBox>
          </FlexBox>
        </template>
      </Card>
    </SlideRightX>
    <SlideRightX
        v-if="hasSearched"
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
            <span>List Setoran Customer</span>
          </div>
        </template>
        <template #content>
          <Table
              ref="tableRef"
              :columns="addLphByCustomerColumns"
              :table-data="dataTable"
              :loading="loadingTable"/>
          <FlexBox full flexCol itEnd class="tw-px-4">
            <div class="tw-mt-4 tw-p-3 tw-bg-gray-50 tw-rounded-lg tw-border">
              <div class="tw-flex tw-justify-between tw-items-center">
                <span class="tw-font-semibold tw-text-gray-700 tw-mr-2">
                  Total Retur:
                </span>
                <span class="tw-font-bold tw-text-lg tw-text-blue-600">
                  {{ formatCurrencyAuto(totalRetur) }}
                </span>
              </div>
              <div class="tw-flex tw-justify-between tw-items-center">
                <span class="tw-font-semibold tw-text-gray-700 tw-mr-2">
                  Total Tagihan:
                </span>
                <span class="tw-font-bold tw-text-lg tw-text-blue-600">
                  {{ formatCurrencyAuto(totalTagihan) }}
                </span>
              </div>
            </div>

            <!-- Button Unduh Tagihan -->
            <div class="tw-mt-4 tw-flex tw-gap-4 tw-justify-end">
              <Button
                  :loading="loadingTable"
                  :trigger="showModalTambahLph"
                  class="tw-h-[38px] tw-w-auto tw-px-6 tw-bg-blue-500 hover:tw-bg-blue-600">
                Tambah LPH
              </Button>
              <Button
                  :loading="loadingTable"
                  :trigger="showModalSales"
                  :disabled="!dataTable.length"
                  icon="mdi mdi-download"
                  class="tw-h-[38px] tw-w-auto tw-px-6 tw-bg-green-500 hover:tw-bg-green-600">
                Unduh Tagihan
              </Button>
            </div>
          </FlexBox>

          <!-- Total Tagihan -->
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>
