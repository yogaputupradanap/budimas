<script setup>
import SlideRightX from "../components/animation/SlideRightX.vue";
import FlexBox from "../components/ui/FlexBox.vue";
import Card from "../components/ui/Card.vue";
import Table from "../components/ui/table/Table.vue";
import {
  HistoryOrderColumns,
  HistoryReturColumns,
} from "../model/tableColumns";
import SelectInput from "../components/ui/formInput/SelectInput.vue";
import VueDatePicker from "@vuepic/vue-datepicker";
import { ref, watchEffect } from "vue";
import Button from "../components/ui/Button.vue";
import { useSales } from "../store/sales";
import { apiUrl, fetchWithAuth, sessionDisk } from "../lib/utils";
import Skeleton from "../components/ui/Skeleton.vue";
import { useAlert } from "../store/alert";

const user = sessionDisk.getSession("authUser")
const sales = useSales();
const alert = useAlert();

const customerName = ref("");
const fromDate = ref();
const toDate = ref();

const listOrderHistory = ref([]);
const listReturHistory = ref([]);

const listCustomer = ref([]);
const tableKey = ref(0);

const cariHistory = async () => {
  try {
    if (!customerName.value || !fromDate.value || !toDate.value) {
      throw `Ada field yang kosong`;
    }
    const from_date = new Date(fromDate.value);
    const to_date = new Date(toDate.value);

    const fromDateIso = from_date.toISOString().slice(0, 10);
    const toDateIso = to_date.toISOString().slice(0, 10);

    const id_user = user.id_user;

    const history = await fetchWithAuth(
      "GET",
      `${apiUrl}/api/customer/history-customer?id_customer=${customerName.value}&from_date=${fromDateIso}&to_date=${toDateIso}&id_user=${id_user}`
    );

    console.log("history ", history)
    if (!history.sales_order.length && !history.sales_retur.length) {
      return alert.setMessage("Hasil Pencarian Kosong", "warning");
    }

    listOrderHistory.value = history.sales_order;
    listReturHistory.value = history.sales_retur;

    tableKey.value++;
    
  } catch (error) {
    alert.setMessage(error, "danger");
  }
};

const getCustomerList = async () => {
  const id_user = user.id_user;

  listCustomer.value = await fetchWithAuth(
    "GET",
    `${apiUrl}/api/customer/list-sales-customer/${id_user}`
  );
};

watchEffect(() => {
  getCustomerList();
});
</script>

<template>
  <FlexBox full flex-col class="lg:tw-pl-6 tw-pl-2">
    <SlideRightX
      class="tw-w-full tw-z-10"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.1"
      :delay-out="0.1"
      :initial-x="-40"
      :x="40"
    >
      <Card no-subheader>
        <template #header>Form Pencarian History</template>
        <template #content>
          <FlexBox full class="tw-pb-10">
            <BForm
              novalidate
              class="tw-w-full tw-h-full tw-flex lg:tw-flex-row tw-flex-col tw-gap-4 tw-justify-center tw-items-end"
            >
              <div
                class="lg:tw-w-[270px] tw-w-full tw-flex tw-flex-col tw-gap-2"
              >
                <span>Nama Customer</span>
                <Skeleton
                  class="lg:tw-w-64 tw-w-full tw-h-10 tw-rounded-lg"
                  v-if="!listCustomer.length"
                />
                <SelectInput
                  v-else
                  v-model="customerName"
                  :style="[{ height: '38px' }]"
                  :disabled="isEdit"
                  :search="true"
                  placeholder="Pilih Customer"
                  :options="listCustomer"
                  text-field="nama"
                  value-field="id"
                />
              </div>
              <div
                class="lg:tw-w-[270px] tw-w-full tw-flex tw-flex-col tw-gap-2"
              >
                <span>Mulai dari</span>
                <VueDatePicker
                  v-model="fromDate"
                  :enable-time-picker="false"
                  placeholder="mm/dd/yyyy"
                  :teleport="true"
                  auto-apply
                />
              </div>
              <div
                class="lg:tw-w-[270px] tw-w-full tw-flex tw-flex-col tw-gap-2"
              >
                <span>Sampai</span>
                <VueDatePicker
                  v-model="toDate"
                  :enable-time-picker="false"
                  placeholder="mm/dd/yyyy"
                  :teleport="true"
                  auto-apply
                />
              </div>
              <Button
                :trigger="cariHistory"
                class="tw-bg-blue-500 tw-w-28 tw-h-10 tw-text-lg"
                @click="searchNota"
              >
                <i class="mdi mdi-magnify tw-mr-2"></i>
                Cari
              </Button>
            </BForm>
          </FlexBox>
        </template>
      </Card>
    </SlideRightX>
    <SlideRightX
      class="tw-w-full"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.2"
      :delay-out="0.2"
      :initial-x="-40"
      :x="40"
    >
      <Card no-subheader class="tw-pb-16 tw-px-4">
        <template #header>List Order</template>
        <template #content>
          <Table
            :key="tableKey"
            :columns="HistoryOrderColumns"
            :table-data="listOrderHistory"
            table-width="tw-w-[100vw]"
          />
        </template>
      </Card>
    </SlideRightX>
    <SlideRightX
      class="tw-w-full"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.3"
      :delay-out="0.3"
      :initial-x="-40"
      :x="40"
    >
      <Card no-subheader class="tw-pb-16 tw-px-4">
        <template #header>List Retur</template>
        <template #content>
          <Table
            :key="tableKey"
            :columns="HistoryReturColumns"
            :table-data="listReturHistory"
          />
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>
