<script setup>
import SlideRightX from '@/src/components/animation/SlideRightX.vue';
import Card from '@/src/components/ui/Card.vue';
import FlexBox from '@/src/components/ui/FlexBox.vue';
import Label from '@/src/components/ui/Label.vue';
import Button from "@/src/components/ui/Button.vue";
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router'
import Table from "@/src/components/ui/table/Table.vue";
import { DraftDetailFakturPajakColumns } from '@/src/model/tableColumns/draft-faktur-pajak/detail-daftar-faktur-pajak/detail-daftar-faktur-pajak';
import { pajakService } from '@/src/services/pajak';
import { useAlert } from '@/src/store/alert';

const no_faktur = ref("");
const tanggal_faktur = ref("");
const customer = ref("");
const principal = ref("");
const npwp = ref("");
const tablekey = ref(0);
const route = useRoute()
const detaildraftdata = ref([]);
const loading = ref(false);
const loadingExport = ref(false);
const tableRef = ref(null);
const alert = useAlert();
const ExportXmlEfaktur = async () => {
  try {
    const id = route.params.id;
    const response = await pajakService.exportXmlDraftPajak({[id]: true})
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
    loading.value = true;
    const response = await pajakService.GetDetailDraftFaktur(route.params.id);
    console.log("Get Response data detail", response);
    detaildraftdata.value = response.data.tabledata;
    const temp = response.data.filterdata[0];
    no_faktur.value = temp.no_faktur;
    tanggal_faktur.value = new Date(temp.tanggal_faktur).toLocaleDateString('id-ID', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    }).replace(/\//g, '-');
    customer.value = `${temp.nama_customer} - (${temp.kode_customer})`;
    principal.value = temp.nama_principal;
    npwp.value = temp.npwp;
  } catch (error) {
  } finally {
    loading.value = false;
    tablekey.value += 1;
  }
};

onMounted(() => {
  GetData()
});

</script>

<template>
  <SlideRightX class="slide-container tw-z-10" :duration-enter="0.6" :duration-leave="0.6" :delay-in="0.1"
    :delay-out="0.1" :initial-x="-40" :x="40">
    <Card no-subheader dense>
      <template #header>Filter Faktur Pajak</template>
      <template #content>
        <FlexBox full gap="" no-left-padding flex-col>
          <FlexBox full no-left-padding class="tw-flex-wrap md:tw-flex-nowrap">

            <Label label="No Faktur :">
              <BFormInput type="text" v-model="no_faktur" placeholder="Input Nomor Prefix" size="sm" class="tw-w-full disabled:tw-cursor-not-allowed"
                 disabled/>
            </Label>

            <Label label="Tanggal faktur :">
              <BFormInput type="text" v-model="tanggal_faktur" placeholder="Input Nomor Prefix" size="sm" class="tw-w-full disabled:tw-cursor-not-allowed"
                disabled />
            </Label>

            <Label label="Customer :">
              <BFormInput type="text" v-model="customer" placeholder="Input Nomor Prefix" size="sm" class="tw-w-full disabled:tw-cursor-not-allowed"
                disabled />
            </Label>

            <Label label="Principal :">
              <BFormInput type="text" v-model="principal" placeholder="Input Nomor Prefix" size="sm" class="tw-w-full disabled:tw-cursor-not-allowed"
                disabled />
            </Label>

          </FlexBox>

          <FlexBox full no-left-padding it-end>
            <Label label="NPWP">
              <BFormInput type="text" v-model="npwp" placeholder="Input Nomor Prefix" size="sm"
                class="tw-w-full tw-cursor-not-allowed tw-max-w-[278px]" disabled />
            </Label>

          </FlexBox>
        </FlexBox>
      </template>
    </Card>
    <Card no-subheader dense>
      <template #header>Detail Faktur Pajak</template>
      <template #content>
        <FlexBox full jus-end flex-col no-left-padding>
          <Table ref="tableRef" hide-toolbar :loading="loading" :key="tablekey" :columns="DraftDetailFakturPajakColumns"
              :table-data="detaildraftdata || []" />
          <Button :trigger="ExportXmlEfaktur" icon="mdi mdi-plus" class="tw-bg-green-500 tw-px-4 tw-h-[40px] tw-ml-auto"
            :loading="loadingExport">
            Export E-Faktur
          </Button>
        </FlexBox>
      </template>
    </Card>
  </SlideRightX>
</template>