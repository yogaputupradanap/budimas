<script setup>
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import Table from "@/src/components/ui/table/Table.vue";
import Label from "@/src/components/ui/Label.vue";
import SelectInput from "@/src/components/ui/formInput/SelectInput.vue";
import VueDatePicker from "@vuepic/vue-datepicker";
import Button from "@/src/components/ui/Button.vue";
import { buatSuratTagihanSalesColumn } from "@/src/model/tableColumns/surat-tagihan-sales/buat-surat-tagihan-sales/buatSuratTagihanSales";
import { useOthers } from "@/src/store/others";
import Skeleton from "@/src/components/ui/Skeleton.vue";
import { computed, ref } from "vue";
import { useTableSearch } from "@/src/lib/useTableSearch";
import { piutangService } from "@/src/services/piutang";
import { getSelectedRow } from "@/src/lib/utils";
import { useAlert } from "@/src/store/alert";

const alert = useAlert();
const others = useOthers();
const { tagihanSales } = piutangService;

const tableRef = ref();
const selectedRow = computed(() => tableRef.value?.getSelectedRow());
const loadingSubmit = ref(false);

const customer = ref(null);
const principal = ref(null);
const mulaiJatuhtempo = ref(null);
const selesaiJatuhTempo = ref(null);

const fieldPool = [customer, principal, mulaiJatuhtempo, selesaiJatuhTempo];
const queryEntries = computed(() => [
  ["customer=", customer.value],
  ["principal=", principal.value],
  ["mulai_jatuh_tempo=", mulaiJatuhtempo.value],
  ["selesai_jatuh_tempo=", selesaiJatuhTempo.value],
]);

const options = {
  initialColumnName: "nomor_faktur",
  checkFieldFilterFunc: (val) => val[1] === null,
  filterFunction: (val) => val[1] !== null,
  asArgument: true,
};

const [data, , , , key, search, reset] = useTableSearch(
  tagihanSales,
  fieldPool,
  queryEntries,
  options
);

const submitTagihan = async () => {
  const selectedData = getSelectedRow(selectedRow, data.value);
  const id_sales_order = selectedData.map((val) => val.id_sales_order);

  try {
    loadingSubmit.value = true;
    const result = await piutangService.postTagihan({ id_sales_order });
    alert.setMessage(result, "success");
    reset();
  } catch (error) {
    alert.setMessage(error, "danger");
  } finally {
    loadingSubmit.value = false;
  }
};
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
      :x="40">
      <Card no-subheader>
        <template #header>Form Buat Surat Tagihan Sales</template>
        <template #content>
          <div class="form-grid-card-container-4-col">
            <Label label="Customer">
              <Skeleton
                v-if="others.customer.loading"
                class="skeleton" />
              <SelectInput
                v-model="customer"
                v-else
                placeholder="Pilih Data"
                size="md"
                :search="true"
                :options="others.customer.list"
                text-field="nama"
                value-field="id"
                :virtual-scroll="true" />
            </Label>
            <Label label="Principal ">
              <Skeleton
                v-if="others.principal.loading"
                class="skeleton" />
              <SelectInput
                v-model="principal"
                v-else
                placeholder="Pilih Data"
                size="md"
                :search="true"
                :options="others.principal.list"
                text-field="nama"
                value-field="id" />
            </Label>
            <Label label="Mulai Jatuh Tempo">
              <VueDatePicker
                v-model="mulaiJatuhtempo"
                format="yyyy-MM-dd"
                model-type="yyyy-MM-dd"
                :enable-time-picker="false"
                placeholder="yyyy/mm/dd"
                :teleport="true"
                auto-apply />
            </Label>
            <Label label="Selesai Jatuh Tempo">
              <VueDatePicker
                v-model="selesaiJatuhTempo"
                format="yyyy-MM-dd"
                model-type="yyyy-MM-dd"
                :enable-time-picker="false"
                placeholder="yyyy/mm/dd"
                :teleport="true"
                auto-apply />
            </Label>
          </div>
          <div class="tw-w-full tw-flex tw-gap-2">
            <Button
              :trigger="reset"
              icon="mdi mdi-reload"
              class="tw-h-[38px] tw-w-full xl:tw-w-32 tw-bg-red-500">
              reset
            </Button>
            <Button
              :trigger="search"
              icon="mdi mdi-magnify"
              class="tw-h-[38px] tw-w-full xl:tw-w-32">
              Cari Data
            </Button>
          </div>
        </template>
      </Card>
    </SlideRightX>
    <SlideRightX
      class="slide-container"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.1"
      :delay-out="0.1"
      :initial-x="-40"
      :x="40">
      <Card no-subheader>
        <template #header>List Tagihan</template>
        <template #content>
          <Table
            ref="tableRef"
            :key="key"
            :columns="buatSuratTagihanSalesColumn"
            :table-data="data || []" />
          <FlexBox full jus-end>
            <Button
              :trigger="submitTagihan"
              :loading="loadingSubmit"
              icon="mdi mdi-check"
              class="tw-bg-green-500 tw-px-4 tw-h-[34px]">
              Submit
            </Button>
          </FlexBox>
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>
