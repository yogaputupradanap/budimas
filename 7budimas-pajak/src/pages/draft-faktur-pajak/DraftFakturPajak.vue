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
import { DraftFakturPajakColumn } from '@/src/model/tableColumns/draft-faktur-pajak/draft-faktur-pajak';
import { useAlert } from '@/src/store/alert';
import { GetLengthObject } from '@/src/lib/utils';
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
const draftdata = ref([]);
const tablekey = ref(0);
const tableRef = ref(null);
const alert = useAlert();
const perusahaandata = ref(others.perusahaan.list);
const cabangdata = ref(others.cabang.list);

const ExportXmlEfaktur = async () => {
  try {
    const selectedRows = tableRef.value.getSelectedRow();
    const length = GetLengthObject(selectedRows);
    if (length < 1) throw new Error("Pilih data yang akan di export");
    const response = await pajakService.exportXmlDraftPajak(selectedRows)
    
    let blob;
    if(typeof response === "string") {
      blob = new Blob([response], { type: 'application/xml' });
    }else {
      throw new Error("Unexpected response type for XML download");
    }

    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "export_pajak.xml";
    a.click();
    GetData();
    window.URL.revokeObjectURL(url);
  } catch (error) {
    alert.setMessage(error.message, "danger");
  } finally {
    loadingExport.value = false;
  }
};

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
    const response = await pajakService.getDraftFaktur(clauses);
    draftdata.value = response.data;
  } catch (error) {
    // Handle error logic here

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
      item.nama_kode = `${item.nama} - (${item.kode})`;
    });

    customerdata.value = temp;
  } catch (error) {
    throw error;
  } finally {
    loadingForm.value = false;
  }
};

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
</script>

<template>
  <FlexBox flex-col>
    <SlideRightX class="slide-container tw-z-10" :duration-enter="0.6" :duration-leave="0.6" :delay-in="0.1"
      :delay-out="0.1" :initial-x="-40" :x="40">

      <Card no-subheader dense>
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
              <Button class="tw-bg-blue-800 tw-px-4 tw-h-[40px] tw-w-[160px] tw-ml-auto" :loading="loadingForm"
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
            <Table ref="tableRef" :loading="loading" :key="tablekey" :columns="DraftFakturPajakColumn"
              :table-data="draftdata || []" />
            <Button :trigger="ExportXmlEfaktur" icon="mdi mdi-plus"
              class="tw-bg-green-500 tw-px-4 tw-h-[40px] tw-ml-auto" :loading="loadingExport">
              Export E-Faktur
            </Button>
          </FlexBox>
        </template>
      </Card>


    </SlideRightX>
  </FlexBox>
</template>