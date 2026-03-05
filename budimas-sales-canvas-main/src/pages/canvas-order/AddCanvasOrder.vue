<script setup>
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import Label from "@/src/components/ui/Label.vue";
import Button from "@/src/components/ui/Button.vue";
import Modal from "@/src/components/ui/Modal.vue";
import ServerTable from "@/src/components/ui/table/ServerTable.vue";
import Table from "@/src/components/ui/table/Table.vue";
import PaymentMethodToggle from "@/src/components/ui/PaymentMethodToggle.vue";
import SelectInput from "@/src/components/ui/formInput/SelectInput.vue";
import { useTableSearch } from "@/src/lib/useTableSearch";
import { useFetchPaginate } from "@/src/lib/useFetchPaginate";
import { ref, computed, watch, nextTick, inject, onMounted, reactive } from "vue";
import { listAddCanvasOrderColumn } from "@/src/model/tableColumns/canvas-order/tambah-order";
import { useSorting } from "@/src/lib/useSorting";
import { usePagination } from "@/src/lib/usePagination";
import { useFiltering } from "@/src/lib/useFiltering";
import { salesCanvasService } from "@/src/services/salesCanvas";
import { voucherService } from "@/src/services/vouchers";
import { simpleDateNow, checkNaN, formatNumber } from "@/src/lib/utils";
import { BFormInput, BFormGroup } from "bootstrap-vue-next";
import { useUser } from "@/src/store/user";
import { useVoucher } from "@/src/store/voucher";
import { pickVoucher } from "@/src/lib/utils";
import { useAlert } from "@/src/store/alert";
import { useRouter } from "vue-router";


const alert = useAlert();
const $swal = inject("$swal");
const router = useRouter()
const userStore = useUser();
const voucher = useVoucher();

// Modal section
const modal = ref();
const voucherRegulerModal = ref();

// Header Section
const user = userStore.user.value;
const tanggalRequest = ref(new Date());
const principalName = computed(() => user?.principal);
const userBranch = computed(() => userStore.user.value?.nama_cabang);

// Data Reference
const formRef = ref({});
const customerValue = ref("");
const voucherRegulerLoading = ref(false);
const selectedVoucherByPrincipal = ref({});
const selectedPrincipalId = ref(user?.id_principal)

// Payment Method
const paymentInfo = ref({
  isActive: false,
  totalAmount: 0,
  receivedAmount: 0,
  changeAmount: 0,
  isComplete: false
});

const onPaymentChange = (data) => {
  paymentInfo.value = data;
};

// Voucher Selection
const voucherData = ref({ voucher_2_produk: [], voucher_3_produk: [] })
const selectedVouchers = ref({ voucher2Product: null, voucher3Product: null });
const selectedVoucherReguler = ref({
  voucher1Regular: null,
  voucher2Regular: null,
  voucher3Regular: null
});


const { endpoints } = salesCanvasService;
const { onSortingChange, sorting } = useSorting();
const { onPaginationChange, pagination } = usePagination();
const { onColumnFilterChange, globalFilters } = useFiltering();

const fetchTableUrl = computed(() => {
  const user = userStore.user.value;
  return user?.id ? `${endpoints}/list-order-canvas?id=${user.id}` : null;
})

const [data, count, loading, totalPage, key] = useFetchPaginate(
  fetchTableUrl,
  {
    pagination,
    sorting,
    globalFilters,
    initialSortColumn: "nama_produk",
  }
);

const fieldPool = ["nama_produk"];

const queryEntries = computed(() => {
  if (reset.value) return [];
  const entries = [[]];

  if (globalFilters.value?.value?.text && globalFilters.value.value.text.trim() !== "") {
    entries.push(["filters=", globalFilters.value?.text]);
    entries.push(["columns=", JSON.stringify(["nama_produk"])]);
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
] = useTableSearch(fetchTableUrl, fieldPool, queryEntries, options);

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

const loadRegularVouchers = async () => {
  voucherRegulerLoading.value = true;
  try {
    const [voucher1Regular, voucher2Regular, voucher3Regular] = await Promise.all([
      voucherService.getVoucherV1Regular(),
      voucherService.getVoucherV2Regular(),
      voucherService.getVoucherV3Regular()
    ]);

    voucher.voucher1RegularList = voucher1Regular || [];
    voucher.voucher2RegularList = voucher2Regular || [];
    voucher.voucher3RegularList = voucher3Regular || [];
  } catch (error) {
    console.error("Error loading regular vouchers:", error);
    voucher.voucher1RegularList = [];
    voucher.voucher2RegularList = [];
    voucher.voucher3RegularList = [];
  } finally {
    voucherRegulerLoading.value = false;
  }
};

const submitVoucherReguler = async () => {
  voucherRegulerLoading.value = true;

  try {
    // 1. Ambil objek voucher dari ID yang dipilih
    const selectedVoucherObjects = {
      voucher1Regular: selectedVoucherReguler.value.voucher1Regular
        ? voucher.voucher2RegularList.find(v => Number(v.id) === Number(selectedVoucherReguler.value.voucher2Regular))
        : null,
      voucher2Regular: selectedVoucherReguler.value.voucher2Regular
        ? voucher.voucher2RegularList.find(v => v.id === selectedVoucherReguler.value.voucher2Regular)
        : null,
      voucher3Regular: selectedVoucherReguler.value.voucher3Regular
        ? voucher.voucher3RegularList.find(v => v.id === selectedVoucherReguler.value.voucher3Regular)
        : null
    };

    // 2. Simpan voucher reguler yang dipilih ke store
    voucher.setSelectedRegularVouchers(selectedVoucherObjects);

    // 3. Update tracking per principal
    selectedVoucherByPrincipal.value = {
      ...selectedVoucherByPrincipal.value,
      [selectedPrincipalId.value]: {
        voucher1Regular: selectedVoucherObjects.voucher1Regular,
        voucher2Regular: selectedVoucherObjects.voucher2Regular,
        voucher3Regular: selectedVoucherObjects.voucher3Regular
      }
    };

    // 4. Terapkan ke semua produk di table
    const targetData = getTargetData();
    if (Array.isArray(targetData)) {
      targetData.forEach(row => {
        row.v1r = selectedVoucherObjects.voucher1Regular?.persentase_diskon_1 || 0;
        row.v2r = selectedVoucherObjects.voucher2Regular?.persentase_diskon_2 || 0;
        row.v3r = selectedVoucherObjects.voucher3Regular?.persentase_diskon_3 || 0;
        row.id_voucher_2 = selectedVoucherObjects.voucher2Regular?.id ?? row.id_voucher_2 ?? null;
        row.id_voucher_3 = selectedVoucherObjects.voucher3Regular?.id ?? row.id_voucher_3 ?? null;
      });
      updateRowCalculations();
    }

    // 5. Show success message
    const msg = selectedVoucherObjects.voucher1Regular ||
                selectedVoucherObjects.voucher2Regular ||
                selectedVoucherObjects.voucher3Regular
      ? "Voucher reguler telah diterapkan ke semua produk"
      : "Semua voucher reguler telah dihapus";

    alert.setMessage(msg, "success");

  } catch (error) {
    console.error("Error applying regular vouchers:", error);
    alert.setMessage(`Terjadi kesalahan: ${error.message}`, "danger");
  } finally {
    voucherRegulerLoading.value = false;
    closeVoucherRegulerModal();
  }
};

const fetchVoucherProduk = async () => {
  const totalQty = (formRef.value.qty_uom1 || 0) + (formRef.value.qty_uom2 || 0) + (formRef.value.qty_uom3 || 0);
  
  if (totalQty <= 0) {
    voucherData.value = {};
    return;
  }

  try {
    const branchId = userStore.user.value?.id_cabang;
    if (!branchId) {
      console.error('Branch ID tidak ditemukan');
      return;
    }

    const [voucher2Response, voucher3Response] = await Promise.all([
      voucherService.getVoucherV2Product(formRef.value.id, { id_cabang: branchId }),
      voucherService.getVoucherV3Product(formRef.value.id, { id_cabang: branchId }),
    ]);
    
    voucherData.value = {
      voucher_2_produk: voucher2Response || [],
      voucher_3_produk: voucher3Response || []
    };
  } catch (error) {
    console.error('Error loading voucher produk:', error);
    voucherData.value = {};
  }
};

const calculateRowTotals = (row) => {
  if (!row) return { subtotal: 0, total_diskon: 0, jumlah_harga: 0, ppn: row?.ppn || 0 };

  const u1f = Number(row.uom1_factor) || 1;
  const u2f = Number(row.uom2_factor) || 1;
  const u3f = Number(row.uom3_factor) || 1;
  
  const qty_total_pieces =
    (Number(row.qty_uom1) || 0) * u1f +
    (Number(row.qty_uom2) || 0) * u2f +
    (Number(row.qty_uom3) || 0) * u3f;

  const harga_per_uom1 = Number(row.harga_per_uom1) || 0;
  const subtotal = qty_total_pieces * harga_per_uom1;

  const diskonPersenTotal =
    (Number(row.v1r) || 0) +
    (Number(row.v2r) || 0) +
    (Number(row.v3r) || 0);

  const diskonPersenValue = subtotal * (diskonPersenTotal / 100);
  const diskonNominalValue = (Number(row.v2p) || 0) + (Number(row.v3p) || 0);

  const total_diskon = diskonPersenValue + diskonNominalValue;
  const jumlah_harga = Math.max(subtotal - total_diskon, 0);
  const ppnRate = Number(row.ppn) || 0;
  const pajak_row = jumlah_harga * (ppnRate / 100);
  const total_row = jumlah_harga + pajak_row;

  return {
    subtotal, total_diskon,
    jumlah_harga, pajak_row,
    total_row, ppn: ppnRate
  };
};

const updateRowCalculations = () => {
  const targetData = getTargetData();
  if (!Array.isArray(targetData)) return;
  
  targetData.forEach(row => {
    const calculations = calculateRowTotals(row);
    row.subtotal = calculations.subtotal;
    row.total_diskon = calculations.total_diskon;
    row.jumlah_harga = calculations.jumlah_harga;
    row._pajak_row = calculations.pajak_row;
    row._total_row = calculations.total_row;
  });
  
  if (isServerTable.value) {
    key.value = Date.now();
  } else {
    clientKey.value = Date.now();
  }
};

const openVoucherRegulerModal = async () => {
  await loadRegularVouchers();

  const currentRegularVouchers = voucher.getSelectedRegularVouchers();
  selectedVoucherReguler.value = {
    voucher1Regular: currentRegularVouchers.voucher1Regular?.id || null,
    voucher2Regular: currentRegularVouchers.voucher2Regular?.id || null,
    voucher3Regular: currentRegularVouchers.voucher3Regular?.id || null
  };
  voucherRegulerModal.value.show();
};

const closeVoucherRegulerModal = () => { voucherRegulerModal.value.hide() };

const showModalWithData = async (rowData) => {
  if (rowData && typeof rowData === 'object' && !rowData.id && rowData.value) {
    rowData = rowData.value;
  }
  
  formRef.value = {
    id: rowData.id,
    v1r: rowData.v1r,
    v2r: rowData.v2r,
    v3r: rowData.v3r,
    v2p: rowData.v2p,
    v3p: rowData.v3p,
    nama_principal: rowData.nama_principal,
    nama_produk: rowData.nama_produk,
    stock_canvas: rowData.stock_canvas,
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

  voucherData.value = {
    voucher_2_produk: [],
    voucher_3_produk: []
  };

  selectedVouchers.value = {
    voucher2Product: rowData.voucher2Product ?? null,
    voucher3Product: rowData.voucher3Product ?? null
  };

  await fetchVoucherProduk(rowData.id)
  
  if (!rowData.voucher2Product) selectedVouchers.value.voucher2Product = null;
  if (!rowData.voucher3Product) selectedVouchers.value.voucher3Product = null;

  nextTick(() => { modal.value.show() });
}

const createUpdatedRowData = (originalRow, tempData) => ({
  ...originalRow,
  _isTemp: true,
  qty_uom1: tempData.qty_uom1,
  qty_uom2: tempData.qty_uom2,
  qty_uom3: tempData.qty_uom3,
  v2p: tempData.v2p,
  v3p: tempData.v3p,
  total_satuan: tempData.qty_request,
  harga_per_uom1: tempData.harga_per_pieces,
  total_permintaan: tempData.total_permintaan,
  ppn: tempData.ppn ?? originalRow.ppn ?? 0,
  id_voucher_2: tempData.id_voucher_2 ?? selectedVouchers.value.voucher2Product ?? selectedVoucherReguler.value.voucher2Regular ?? null,
  id_voucher_3: tempData.id_voucher_3 ?? selectedVouchers.value.voucher3Product ?? selectedVoucherReguler.value.voucher3Regular ?? null,
  voucher2Product: selectedVouchers.value.voucher2Product,
  voucher3Product: selectedVouchers.value.voucher3Product,
})

const updateTempTableData = async () => {
  if (!formRef.value.id) return;

  const selectedV2ProductId = selectedVouchers.value?.voucher2Product ? Number(selectedVouchers.value.voucher2Product) : null;
  const selectedV3ProductId = selectedVouchers.value?.voucher3Product ? Number(selectedVouchers.value.voucher3Product) : null;
  const selectedV2RegularId = selectedVoucherReguler.value?.voucher2Regular ? Number(selectedVoucherReguler.value.voucher2Regular) : null;
  const selectedV3RegularId = selectedVoucherReguler.value?.voucher3Regular ? Number(selectedVoucherReguler.value.voucher3Regular) : null;

  const v2Product = selectedV2ProductId !== null
    ? (voucherData.value.voucher_2_produk || []).find(v => Number(v.id) === selectedV2ProductId)
    : null;

  const v3Product = selectedV3ProductId !== null
    ? (voucherData.value.voucher_3_produk || []).find(v => Number(v.id) === selectedV3ProductId)
    : null;

  const v2Regular = selectedV2RegularId !== null
    ? (voucher.voucher2RegularList || []).find(v => Number(v.id) === selectedV2RegularId)
    : null;

  const v3Regular = selectedV3RegularId !== null
    ? (voucher.voucher3RegularList || []).find(v => Number(v.id) === selectedV3RegularId)
    : null;

  const finalVoucher2 = pickVoucher(v2Product, v2Regular);
  const finalVoucher3 = pickVoucher(v3Product, v3Regular);

  const payload = {
    id_produk: formRef.value.id,
    id_voucher_2: finalVoucher2?.id,
    id_voucher_3: finalVoucher3?.id,
    id_user: userStore.user.value?.id,
    v2p: v2Product?.persentase_diskon_2 || 0,
    v3p: v3Product?.persentase_diskon_3 || 0,
    qty_uom1: Number(formRef.value.qty_uom1) || 0,
    qty_uom2: Number(formRef.value.qty_uom2) || 0,
    qty_uom3: Number(formRef.value.qty_uom3) || 0,
  };

  try {
    const response = await salesCanvasService.updateCanvasRequestTemp(payload);
    if (!response?.pages?.[0]) { throw new Error('Response tidak valid!') }

    const tempData = response.pages[0];
    const mergedTemp = {
      ...tempData,
      id_voucher_2: tempData.id_voucher_2 ?? selectedV2ProductId ?? selectedV2RegularId ?? null,
      id_voucher_3: tempData.id_voucher_3 ?? selectedV3ProductId ?? selectedV3RegularId ?? null,
    }
    await nextTick(() => {
      updateTableRowData(mergedTemp);
      updateRowCalculations();
    });
    $swal.success('Request berhasil diupdate!');
    modal.value.hide();
  } catch (error) {
    console.error('Error updating temp canvas request:', error);
  }
};

const updateTableRowData = (tempData) => {
  const targetData = getTargetData();
  if (!Array.isArray(targetData)) return;
  
  const existingIndex = findRowIndex(targetData);
  if (existingIndex === -1) return;

  const updatedRow = createUpdatedRowData(targetData[existingIndex], tempData);
  applyTableUpdate(targetData, updatedRow, existingIndex);
};

const onVoucherChange = () => {
  const v2 = voucherData.value.voucher_2_produk?.find(v => v.id === selectedVouchers.value.voucher2Product);
  const v3 = voucherData.value.voucher_3_produk?.find(v => v.id === selectedVouchers.value.voucher3Product);
  formRef.value.v2p = v2?.persentase_diskon_2 || v2?.nominal_diskon || 0;
  formRef.value.v3p = v3?.persentase_diskon_3 || v3?.nominal_diskon || 0;
  updateRowCalculations();
};

const submitCanvasOrderData = async () => {
  if (!formRef.value.id) return $swal.error('ID produk tidak ditemukan.');
  
  if (!customerValue.value || customerValue.value.trim() === '') {
    return $swal.error('Nama customer tidak boleh kosong.');
  }

  const filteredItems = getTargetData().filter(row =>
    (
      Number(row.qty_uom1) > 0 || 
      Number(row.qty_uom2) > 0 || 
      Number(row.qty_uom3) > 0
    ) && Number(row.jumlah_harga) > 0
  );

  if (filteredItems.length === 0) {
    return $swal.warning('Tidak ada item dengan jumlah yang valid untuk disubmit.');
  } 

  const payload = {
    id_user: userStore.user.value?.id,
    nama_customer: customerValue.value,
    ppn: pajak.value,
    total: total.value,
    subtotal: subTotal.value,
    list_items: getTargetData().map(row => ({
      id_produk: row.id,
      id_voucher_2: row.id_voucher_2,
      id_voucher_3: row.id_voucher_3,
      harga_per_uom1: row.harga_per_uom1,
      qty_uom1: row.qty_uom1,
      qty_uom2: row.qty_uom2,
      qty_uom3: row.qty_uom3,
      v1r: row.v1r,
      v2r: row.v2r,
      v3r: row.v3r,
      v2p: row.v2p,
      v3p: row.v3p,
      total_diskon: row.total_diskon,
      jumlah_harga: row.jumlah_harga,
    })),
    is_direct_payment: paymentInfo.value.isActive,
    jumlah_setoran: paymentInfo.value.isActive ? paymentInfo.value.receivedAmount : null
  };

  if (payload.qty_uom1 <= 0 && payload.qty_uom2 <= 0 && payload.qty_uom3 <= 0) {
    return $swal.warning('Quantity tidak boleh kosong semua.');
  }

  console.log("Submitting payload:", payload);

  try {
    await salesCanvasService.createCanvasOrder(payload);
    router.push({ name: 'Canvas Order' });
    $swal.success('Canvas request berhasil dibuat!');
    resetFormModal();
  } catch (error) {
    console.error('Error creating canvas Order:', error);
  }
}

const resetFormModal = () => {
  formRef.value = {};
  customerValue.value = "";
  selectedVouchers.value = {
    voucher2Product: null,
    voucher3Product: null
  };
  selectedVoucherReguler.value = {
    voucher1Regular: null,
    voucher2Regular: null,
    voucher3Regular: null
  };
  voucher.setSelectedRegularVouchers({});
  updateRowCalculations();
}

const checkCurrencyMinus = (value) => {
  return value < 1 ? 0 : value;
};

const subTotalBeforeDiscount = computed(() => {
  const targetData = getTargetData();
  if (!Array.isArray(targetData)) return 0;
  
  return checkNaN(
    targetData.reduce((total, row) => {
      return total + (Number(row.subtotal) || 0);
    }, 0)
  );
});

const subTotal = computed(() => {
  const targetData = getTargetData();
  if (!Array.isArray(targetData)) return 0;
  
  return checkNaN(
    targetData.reduce((total, row) => {
      return total + (Number(row.jumlah_harga) || 0);
    }, 0)
  );
});

const totalDiskon = computed(() => {
  const targetData = getTargetData();
  if (!Array.isArray(targetData)) return 0;

  return checkNaN(
    targetData.reduce((total, row) => {
      return total + (Number(row.total_diskon) || 0);
    }, 0)
  );
});

const pajak = computed(() => {
  const targetData = getTargetData();
  if (!Array.isArray(targetData)) return 0;

  return checkNaN(
    targetData.reduce((total, row) => {
      return total + (Number(row._pajak_row) || 0);
    }, 0)
  );
});

const total = computed(() => {
  const finalTotal = parseFloat(subTotal.value) + parseFloat(pajak.value);
  return checkNaN(finalTotal);
});

const initialReceivedAmount = computed(() => total.value);

const tableMeta = { updateRow: (rowData, rowIndex, columnId, funcId) => {
    if (funcId === "openRowModal") { showModalWithData(rowData) }
  }
};

watch(
  () => [formRef.value.qty_uom1, formRef.value.qty_uom2, formRef.value.qty_uom3],
  () => {
    if (formRef.value.id) {
      fetchVoucherProduk();
    }
    updateRowCalculations();
  },
  { deep: true }
);

onMounted(() => { loadRegularVouchers() });

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
            <Label label="Tanggal Request">
              <BFormInput
                size="md"
                readonly
                placeholder="yyyy-mm-dd"
                :class="'tw-bg-gray-200'"
                :model-value="simpleDateNow(tanggalRequest)"
              />
            </Label>
             <Label label="Principal">
              <BFormInput
                size="md"
                readonly
                placeholder="Rp. 0"
                :class="'tw-bg-gray-200'"
                :model-value="principalName"
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
            <Label label="Customer">
              <BFormInput
                size="md"
                type="text"
                placeholder="Input Customer..."
                v-model="customerValue"
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
            <template #header>Form Canvas Request</template>
            <template #content>
              <div class="tw-w-full tw-pb-10">
                <ServerTable
                  v-if="isServerTable"
                  table-width="tw-w-full"
                  :columns="listAddCanvasOrderColumn"
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
                />
                <Table
                  v-else
                  :key="clientKey"
                  :columns="listAddCanvasOrderColumn"
                  :table-data="clientData?.pages || []"
                  :hideFooter="false"
                  :meta="tableMeta"
                  @open-row-modal="showModalWithData"
                />
                <div class="tw-w-fit tw-flex tw-mx-3">
                  <Button
                    :trigger="openVoucherRegulerModal"
                    icon="mdi mdi-ticket-percent tw-mr-2"
                    class="tw-mt-4 tw-px-5 tw-py-2 tw-bg-indigo-500 hover:tw-bg-indigo-600"
                  >
                    Voucher Reguler
                  </Button>
                </div>
                <div class="tw-grid tw-grid-cols-2 tw-gap-4">
                  <div>
                    <PaymentMethodToggle 
                      :initial-payment-active="false"
                      :total-amount="total"
                      :initial-received-amount="initialReceivedAmount"
                      total-amount-label="Total Pembayaran"
                      received-amount-label="Jumlah Diterima"
                      currency-symbol="Rp"
                      @payment-change="onPaymentChange"
                    />
                  </div>

                  <div>
                    <FlexBox gap="small" flex-col full class="tw-px-4 tw-mt-6">
                      <div
                        class="tw-w-full md:tw-w-96 tw-ml-auto tw-bg-gray-50 tw-rounded-lg tw-p-4 tw-shadow-sm">
                        <h3
                          class="tw-font-semibold tw-text-gray-700 tw-mb-3 tw-text-base">
                          Rincian Pembayaran
                        </h3>

                        <div class="tw-flex tw-justify-between tw-py-2">
                          <span class="tw-text-gray-600">Sub Total (Sebelum Diskon)</span>
                          <span class="tw-font-medium">
                            Rp. {{ formatNumber(checkCurrencyMinus(subTotalBeforeDiscount)) }}
                          </span>
                        </div>

                        <div
                          class="tw-flex tw-justify-between tw-py-2 tw-border-b tw-border-gray-400">
                          <span class="tw-text-gray-600">Total Diskon</span>
                          <span class="tw-font-medium tw-text-red-500">
                            - Rp. {{ formatNumber(checkCurrencyMinus(totalDiskon)) }}
                          </span>
                        </div>

                        <div class="tw-flex tw-justify-between tw-py-2">
                          <span class="tw-text-gray-600">Sub Total</span>
                          <span class="tw-font-medium">
                            Rp. {{ formatNumber(checkCurrencyMinus(subTotal)) }}
                          </span>
                        </div>

                        <div
                          class="tw-flex tw-justify-between tw-py-2 tw-border-b tw-border-gray-400">
                          <span class="tw-text-gray-600">PPN</span>
                          <span class="tw-font-medium">
                            + Rp. {{ formatNumber(checkCurrencyMinus(pajak)) }}
                          </span>
                        </div>

                        <div
                          class="tw-flex tw-justify-between tw-py-3 tw-mt-2 tw-bg-blue-50 tw-rounded-md tw-px-3">
                          <span class="tw-font-bold tw-text-gray-800">Total</span>
                          <span class="tw-font-bold tw-text-lg tw-text-blue-700">
                            Rp. {{ formatNumber(checkCurrencyMinus(total)) }}
                          </span>
                        </div>
                      </div>

                      <FlexBox full jus-end class="tw-mt-4">
                        <Button
                          :trigger="submitCanvasOrderData"
                          class="tw-bg-green-500 hover:tw-bg-green-600 tw-border-none tw-w-40 tw-h-10 tw-text-white tw-rounded-md tw-font-medium">
                          <i class="mdi mdi-check tw-mr-2"></i>
                          Submit Order
                        </Button>
                      </FlexBox>
                    </FlexBox>
                  </div>
                </div>
              </div>

              <Modal
                ref="voucherRegulerModal"
                id="voucherRegulerModal"
                :centered="true"
              >
                <Card no-subheader>
                  <template class="tw-h-auto" #header>Pilih Voucher Reguler</template>
                  <template #content>
                    <div class="tw-w-full tw-grid tw-grid-cols-1 tw-gap-4 lg:tw-grid-cols-1">
                      <Label label="Voucher Reguler 1">
                        <SelectInput
                          size="md"
                          class="tw-w-full"
                          text-field="nama_voucher"
                          value-field="id"
                          placeholder="Pilih Voucher Reguler 1"
                          :clearable="true"
                          :search="true"
                          :options="voucher.voucher1RegularList"
                          v-model="selectedVoucherReguler.voucher1Regular"
                          :loading="voucherRegulerLoading"
                        />
                      </Label>
                      <Label label="Voucher Reguler 2">
                        <SelectInput
                          size="md"
                          class="tw-w-full"
                          text-field="nama_voucher"
                          value-field="id"
                          placeholder="Pilih Voucher Reguler 2"
                          :clearable="true"
                          :search="true"
                          :options="voucher.voucher2RegularList"
                          v-model="selectedVoucherReguler.voucher2Regular"
                          :loading="voucherRegulerLoading"
                        />
                      </Label>
                      <Label label="Voucher Reguler 3">
                        <SelectInput
                          size="md"
                          class="tw-w-full"
                          text-field="nama_voucher"
                          value-field="id"
                          placeholder="Pilih Voucher Reguler 3"
                          :clearable="true"
                          :search="true"
                          :options="voucher.voucher3RegularList"
                          v-model="selectedVoucherReguler.voucher3Regular"
                          :loading="voucherRegulerLoading"
                        />
                      </Label>
                    <div>
                    </div>
                    <FlexBox
                      full jus-center
                      class="tw-mt-4 lg:tw-justify-end lg:tw-flex-row tw-flex-wrap-reverse"
                    >
                      <Button 
                        :trigger="submitVoucherReguler"
                        class="tw-px-14 tw-py-2 tw-text-sm tw-bg-green-500"
                      >
                        Submit
                      </Button>
                    </FlexBox>
                    </div>
                  </template>
                </Card>
              </Modal>

              <Modal
                ref="modal"
                id="modal"
                :centered="true"
              >
                <Card no-subheader>
                  <template class="tw-h-auto" #header>Edit Order</template>
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
                        :model-value="formRef.stock_canvas + ` Pcs`"
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
                    <BFormGroup label="Voucher 2 Produk:">
                      <SelectInput
                        id="voucher2-product-select"
                        placeholder="Pilih Voucher 2 Produk"
                        text-field="nama_voucher"
                        :clearable="true"
                        :search="true"
                        value-field="id"
                        size="md"
                        :options="voucherData.voucher_2_produk || []"
                        v-model="selectedVouchers.voucher2Product"
                        @update:model-value="onVoucherChange"
                      />
                    </BFormGroup>
                    <BFormGroup label="Voucher 3 Produk:">
                      <SelectInput
                        id="voucher3-product-select"
                        placeholder="Pilih Voucher 3 Produk"
                        text-field="nama_voucher"
                        :search="true"
                        :clearable="true"
                        value-field="id"
                        size="md"
                        :options="voucherData.voucher_3_produk || []"
                        v-model="selectedVouchers.voucher3Product"
                        @update:model-value="onVoucherChange"
                      />
                    </BFormGroup>
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
