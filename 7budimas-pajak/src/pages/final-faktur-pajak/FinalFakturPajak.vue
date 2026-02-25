<script setup>
import SlideRightX from '@/src/components/animation/SlideRightX.vue';
import Card from '@/src/components/ui/Card.vue';
import FlexBox from '@/src/components/ui/FlexBox.vue';
import { onMounted, ref, watch } from 'vue';
import Button from "@/src/components/ui/Button.vue";
import Label from '@/src/components/ui/Label.vue';
import SelectInput from '@/src/components/ui/formInput/SelectInput.vue';
import { pajakService } from '@/src/services/pajak';
import { useOthers } from '@/src/store/others';
import { customerService } from '@/src/services/customer';
import { principalService } from '@/src/services/principal';
import Table from "@/src/components/ui/table/Table.vue";
import VueDatePicker from '@vuepic/vue-datepicker';
import { useAlert } from '@/src/store/alert';
import { parseFakturExcel } from '@/src/lib/ParseFakturExcel';
import { FinalFakturPajakColumn } from '@/src/model/tableColumns/final-faktur-pajak/final-faktur-pajak';
import { JoinIntoData } from '@/src/lib/utils';
import { computed } from 'vue';
import { CsvFinalFakturPajakColumns } from '@/src/model/tableColumns/final-faktur-pajak/csv-final-faktur-pajak/csv-final-faktur-pajak';
import { useAlertSwal } from '@/src/store/alertswal';
const loadingExport = ref(false);
const loadingForm = ref(false);
const loading = ref(false);
const perusahaan = ref(null);
const cabang = ref("");
const principal = ref("");
const customer = ref("");
const tanggal_faktur = ref([]);
const others = useOthers();
const principaldata = ref([]);
const customerdata = ref([]);
const finaldata = ref([]);
const tablekey = ref(0);
const tableRef = ref(null);
const removefilter = ref(false);
const inputfileref = ref(null);
const parsed_excel = ref([]);
const alert = useAlert();
const alertswal = useAlertSwal();

const GetData = async () => {
  try {
    const clauses = {
      id_perusahaan: perusahaan.value || null,
      id_cabang: cabang.value || null,
      id_principal: principal.value || null,
      id_customer: customer.value || null,
      tanggal_faktur_start: tanggal_faktur.value ? (tanggal_faktur.value[0] ? new Date(tanggal_faktur.value[0]).toISOString().split('T')[0] : null) : null,
      tanggal_faktur_end: tanggal_faktur.value ? (tanggal_faktur.value[1] ? new Date(tanggal_faktur.value[1]).toISOString().split('T')[0] : null) : null,
    };
    const response = await pajakService.getFinalFaktur(clauses);
    finaldata.value = response.data;
  } catch (error) {

  } finally {
    tablekey.value += 1;
    loadingForm.value = false;
  }
};

const ResetFilter = () => {
  perusahaan.value = null;
  cabang.value = null;
  principal.value = null;
  customer.value = null;
  tanggal_faktur.value = [];
};

const GetCust = async () => {
  try {
    const response = await customerService.getCustomer({
      id_cabang: cabang.value,
    });
    const temp = response.data;
    if (temp.length < 1) return;

    temp.forEach(item => {
      item.nama_kode = `${item.nama} - ${item.kode}`;
    });

    customerdata.value = temp;
  } catch (error) {
    throw error;
  } finally {
    loadingForm.value = false;
  }
};

const onFileChange = async (e) => {
  finaldata.value = [];
  const file = e.target.files?.[0];
  if (!file) return;
  const excel = await file.arrayBuffer();
  const { data, no_faktur_arr } = parseFakturExcel(excel);
  parsed_excel.value = data;
  if (data.length < 1) {
    alert.setMessage("Gagal memparsing file e-faktur", "danger");
    return;
  }

  try {
    const response = await pajakService.getFakturByFile(no_faktur_arr);
    if (response.success == false) {
      throw new Error("Tidak ada faktur yang sesuai di database");
    }

    tablekey.value += 1;
    removefilter.value = true;

    const body = data.map(item => ({
      nsfp: item['Nomor Faktur Pajak'],
      no_faktur: item['Referensi'],
      dpp_csv: item['DPP Nilai Lain/DPP'],
      hpp_csv: item['Harga Jual/Penggantian/DPP'],
      ppn_csv: item['PPN'],
      status_faktur: item['Status Faktur']
    }))

    const temp = JoinIntoData(response.data, body, 'no_faktur', ['nsfp', 'dpp_csv', 'hpp_csv', 'ppn_csv', 'status_faktur'], "-");
    console.log(temp);
    finaldata.value = temp;
  } catch (error) {
    // console.error(error);
    alert.setMessage(error.message || "Gagal mengunggah e-faktur", "danger");
    return;
  } finally {
    if (inputfileref.value) {
      inputfileref.value.value = null; // Reset the file input
    }
  };
}

const SubmitFormFaktur = async () => {
  try {
    loadingExport.value = true;
    const body = parsed_excel.value
      .reduce((acc, item) => {
        const no_faktur = item['Referensi']?.trim();
        if (no_faktur) {
          acc.push({
            nsfp: item['Nomor Faktur Pajak'],
            no_faktur,
            dpp: item['DPP Nilai Lain/DPP'],
            subtotal_penjualan: item['Harga Jual/Penggantian/DPP'],
            pajak: item['PPN'],
            status_faktur_pajak: item['Status Faktur']
          });
        }
        return acc;
      }, []);

    // finaldata.value.forEach(item => {
    //   if ( item.dpp != item.dpp_csv ) throw new Error(`Pada faktur nomor ${item.no_faktur}, nilai DPP tidak sesuai antara data CSV dan data di sistem.`);
    // })

    // throw new Error("Fitur ini masih dalam pengembangan");

    if (finaldata.value.length < 1) {
      throw new Error("Tidak ada data faktur untuk disubmit");
    }

    const response = await pajakService.AddFakturPajak(body);
    if (response.success == true) {
      console.log(response);
      const amandedCount = response.data.amanded || 0;
      const canceledCount = response.data.canceled || 0;
      
      alertswal.setMessage(`Terdapat ${amandedCount} faktur yang di-amandemen dan ${canceledCount} faktur yang dibatalkan.`);
    } else {
      throw new Error(response.message || "Gagal menambahkan data faktur");
    }
  } catch (error) {
    alert.setMessage(error.message || "Gagal mengunggah e-faktur", "danger");
  } finally {
    removefilter.value = false;
    if (inputfileref.value) {
      inputfileref.value.value = null; // Reset the file input
    }
    GetData();
  }
}

const GetPrincipal = async () => {
  try {
    const response = await principalService.getPrincipal({
      id_perusahaan: perusahaan.value,
    });
    principaldata.value = response.data;
  } catch (error) {
    throw error;
  } finally {
    loadingForm.value = false;
  }
};

const OnTrigger = () => {
  // removefilter.value = !removefilter.value;
  if (inputfileref.value) {
    inputfileref.value.click();
  }
};

onMounted(() => {
  GetData();
  const startDate = "";
  const endDate = "";
  tanggal_faktur.value = [startDate, endDate];
});

watch([perusahaan, cabang], () => {
  if (perusahaan.value) {
    principal.value = null;
    GetPrincipal();
  }
  if (cabang.value) {
    customer.value = null;
    GetCust();
  }
});

watch([principal, customer, tanggal_faktur, perusahaan, cabang], () => {
  // You can add any additional logic here if needed when these values change
  GetData();
});

const activeColumns = computed(() =>
  removefilter.value ? CsvFinalFakturPajakColumns : FinalFakturPajakColumn
);
</script>

<template>
  <FlexBox flex-col>
    <SlideRightX class="slide-container tw-z-10" :duration-enter="0.6" :duration-leave="0.6" :delay-in="0.1"
      :delay-out="0.1" :initial-x="-40" :x="40">

      <Card no-subheader dense v-if="!removefilter">
        <template #header>Filter Faktur Pajak</template>
        <template #content>
          <FlexBox full gap="" no-left-padding wrap={false} flex-col>
            <FlexBox full no-left-padding class="tw-flex-wrap md:tw-flex-nowrap">

              <Label label="Perusahaan :">
                <SelectInput v-model="perusahaan" placeholder="Pilih Data" size="md" :search="true"
                  :options="others.perusahaan.list" text-field="nama" value-field="id" />
              </Label>

              <Label label="Cabang :">
                <SelectInput v-model="cabang" placeholder="Pilih Data" size="md" :search="true"
                  :options="others.cabang.list" text-field="nama" value-field="id" />
              </Label>

              <Label label="Principal :">
                <SelectInput v-model="principal" placeholder="Pilih Data" size="md" :search="true"
                  :options="principaldata" text-field="nama" value-field="id" :virtual-scroll="true" />
              </Label>

              <Label label="Customer :">
                <SelectInput v-model="customer" placeholder="Pilih Data" size="md" :search="true"
                  :options="customerdata" text-field="nama_kode" value-field="id" :virtual-scroll="true" />
              </Label>

            </FlexBox>

            <FlexBox full no-left-padding it-end>
              <Label label="Tanggal Faktur">
                <VueDatePicker v-model="tanggal_faktur"
                  class=" tw-max-w-[278px] tw-border-gray-200 hover:tw-border-gray-400 hover:tw-bg-gray-50 focus:tw-outline-none focus:tw-ring-4 focus:tw-ring-blue-200 tw-rounded-md"
                  model-type="yyyy-MM-dd" format="yyyy-MM-dd" placeholder="yyyy-MM-dd" :monday-first="true"
                  :auto-apply="true" range />
              </Label>
              <Button class="tw-bg-red-600 tw-px-4 tw-h-[40px] tw-w-[160px] tw-ml-auto" :loading="loadingForm"
                :trigger="ResetFilter">
                Hapus
              </Button>
              <Button class="tw-bg-blue-800 tw-px-4 tw-h-[40px] tw-w-[160px]" :loading="loadingForm"
                :trigger="GetData">
                Cari
              </Button>
            </FlexBox>
          </FlexBox>
        </template>
      </Card>

      <Card no-subheader dense>
        <template #header>List Faktur Pajak</template>
        <template #content>
          <FlexBox full jus-end flex-col no-left-padding>
            <input ref="inputfileref" type="file" class="tw-hidden" accept=".xlsx" @change="onFileChange" />
            <Button :trigger="OnTrigger" v-if="!removefilter" icon="mdi mdi-plus"
              class="tw-bg-green-500 tw-px-4 tw-h-[40px] tw-ml-auto">
              Unggah E-Faktur
            </Button>
            <Table ref="tableRef" :loading="loading" :key="tablekey" :columns="activeColumns"
              :table-data="finaldata || []" hide-toolbar />

            <Button v-if="removefilter" :trigger="SubmitFormFaktur" icon="mdi arrow-up"
              class="tw-bg-green-500 tw-px-4 tw-h-[40px] tw-ml-auto">
              Submit
            </Button>
          </FlexBox>
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>