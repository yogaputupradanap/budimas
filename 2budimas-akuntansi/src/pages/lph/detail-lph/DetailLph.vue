<script setup>
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import Table from "@/src/components/ui/table/Table.vue";
import {setoranService} from "@/src/services/setoran";
import {computed, onMounted, ref} from "vue";
import Label from "@/src/components/ui/Label.vue";
import Button from "@/src/components/ui/Button.vue";
import {fetchWithAuth, formatCurrencyAuto} from "@/src/lib/utils";
import {$swal} from "@/src/components/ui/SweetAlert.vue";
import {useRoute, useRouter} from "vue-router";
import {detailLphCol, detailLphCustomerCol} from "@/src/model/tableColumns/lph/detail-lph/detailLphCol";
import TextField from "@/src/components/ui/formInput/TextField.vue";
import generateLphPdf from "@/src/model/pdf/lphPdfTemplate";

const {endpoints} = setoranService;
const dataTable = ref([]);
const route = useRoute();
const router = useRouter();
const id_lph = route.params.id_lph;
const loadingTable = ref(false);

const getResource = async () => {
  loadingTable.value = true;
  try {
    const response = await fetchWithAuth(
        "GET",
        `${endpoints.getDetailLph}?id_lph=${id_lph}`
    );
    
    // PENTING: JSON Anda membungkus array dalam property 'result'
    dataTable.value = response?.result || [];
  } catch (error) {
    console.error("Error fetching data:", error);
    dataTable.value = [];
  } finally {
    loadingTable.value = false;
  }
};

const lphAnalysis = computed(() => {
  if (!dataTable.value.length) return { type: 'unknown', sales: [], customers: [] };
  
  const salesMap = new Map();
  const customerMap = new Map();
  
  dataTable.value.forEach(item => {
    if (item.id_sales) salesMap.set(item.id_sales, { id: item.id_sales, nama: item.nama_sales });
    if (item.id_customer) customerMap.set(item.id_customer, { 
      id: item.id_customer, nama: item.nama_customer, kode: item.kode_customer 
    });
  });
  
  const sales = Array.from(salesMap.values());
  const customers = Array.from(customerMap.values());
  
  return {
    type: sales.length > 1 ? 'by_customer' : 'by_sales',
    sales,
    customers,
    salesCount: sales.length,
    customerCount: customers.length
  };
});

const isByCustomer = computed(() => lphAnalysis.value.type === 'by_customer');
const tableColumns = computed(() => isByCustomer.value ? detailLphCustomerCol : detailLphCol);
const firstRecord = computed(() => dataTable.value[0] || {});

const displayInfo = computed(() => {
  const { sales, customers, type } = lphAnalysis.value;
  
  // PROTEKSI: Jika data belum ada, kembalikan objek default agar template tidak crash
  if (!dataTable.value.length) {
    return {
      primary: { label: 'Loading...', value: '-' },
      secondary: null,
      typeText: 'Loading...'
    };
  }
  
  if (type === 'by_customer') {
    return {
      primary: { 
        label: 'Customer', 
        value: customers.map(c => c.nama).join(', ') // Gunakan join agar jadi string
      },
      secondary: { 
        label: 'Nama PJ', 
        value: sales.map(s => s.nama).join(', ') 
      },
      typeText: 'By Customer'
    };
  }
  
  // Default untuk By Sales
  return {
    primary: { label: 'Sales', value: sales[0]?.nama || 'Unknown' },
    secondary: customers.length > 1 
      ? { 
          label: 'Customer', 
          value: customers.map(c => `${c.kode} - ${c.nama}`).join(', ') 
        } : null,
    typeText: 'By Sales'
  };
});

const submitLph = async () => {
  try {
    const isConfirmed = await $swal.confirmSubmit(
        "Apakah Anda yakin ingin mengunduh tagihan ini?"
    );
    if (!isConfirmed) return;

    // Ambil data dari tableData untuk payload
    const payload = {
      id_lph: Number(id_lph),
      batch_cetak: batchCetak.value,
      jumlah_ditagih: totalTagihan.value,
      data_tagihan: dataTable.value, // kirim semua data table
      nama_sales: dataTable.value[0]?.nama_sales || "",
      kode_lph: dataTable.value[0]?.kode_lph || "",
      tanggal_lph: dataTable.value[0]?.tanggal_lph || "",
      nama_perusahaan: dataTable.value[0]?.nama_perusahaan || "",
      alamat_perusahaan: dataTable.value[0]?.alamat_perusahaan || "",
    };

    const response = await fetchWithAuth(
        "POST",
        endpoints.cetakUlangLph,
        payload
    );

    // Generate PDF menggunakan template
    const pdfDoc = generateLphPdf({data: payload});
    const filename = `LPH_${
        payload.kode_lph || "document"
    }_${new Date().getTime()}.pdf`;
    pdfDoc.save(filename);

    $swal.success(response.message);
    router.back();
  } catch (error) {
    console.error("Error generating PDF:", error);
    $swal.error(error);
  }
};

const totalTagihan = computed(() => {
  return dataTable.value.reduce(
      (sum, item) => sum + (item?.sisa_pembayaran || 0),
      0
  );
});

const totalRetur = computed(() => {
  return dataTable.value.reduce(
      (sum, item) => sum + (item?.nominal_retur || 0),
      0
  );
});

const batchCetak = computed(() => {
  return dataTable.value.length > 0 ? dataTable.value[0].batch_cetak + 1 : "";
});

onMounted(() => {
  getResource();
});
</script>

<template>
<!-- <pre class="tw-text-xs tw-bg-gray-100">{{ dataTable }}</pre> -->

  <FlexBox full flex-col>
    <SlideRightX
    class="slide-container tw-z-10"
    :duration-enter="0.6"
    :duration-leave="0.6"
    :delay-in="0.1"
    :delay-out="0.1"
    :initial-x="-40"
    :x="40">
  <Card no-subheader>
    <template #header>
      Detail LPH {{ displayInfo?.typeText || '' }}
    </template>
    
    <template #content>
      <FlexBox v-if="dataTable && dataTable.length > 0" full>
        
        <Label label="Nomor LPH">
          <TextField :disable="true" :model-value="firstRecord.kode_lph"/>
        </Label>

        <Label :label="displayInfo?.primary?.label">
          <TextField
              :disable="true"
              :model-value="displayInfo?.primary?.value"/>
        </Label>

        <Label 
          v-if="displayInfo?.secondary" 
          :label="displayInfo?.secondary?.label"
        >
          <TextField
              :disable="true"
              :model-value="displayInfo?.secondary?.value"/>
        </Label>

        <Label label="Tanggal Ditagihkan">
          <TextField
              :disable="true"
              :model-value="firstRecord.tanggal_lph"/>
        </Label>

        <Label label="Batch Cetak ke">
          <TextField :disable="true" :model-value="batchCetak"/>
        </Label>

      </FlexBox>

      <FlexBox v-else full class="tw-justify-center tw-py-4">
        <span>Memuat data...</span>
      </FlexBox>
    </template>
  </Card>
</SlideRightX>
    <SlideRightX
        v-if="dataTable.length"
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
          <Table :columns="tableColumns" :table-data="dataTable"/>
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
            <div class="tw-mt-4 tw-flex tw-justify-end">
              <Button
                  :loading="loadingTable"
                  :trigger="submitLph"
                  :disabled="!dataTable.length"
                  icon="mdi mdi-download"
                  class="tw-h-[38px] tw-w-auto tw-px-6 tw-bg-green-500 hover:tw-bg-green-600">
                Unduh Tagihan
              </Button>
            </div>
          </FlexBox>
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>
