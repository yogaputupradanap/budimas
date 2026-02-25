<script setup>
import SlideRightX from "../components/animation/SlideRightX.vue";
import Card from "../components/ui/Card.vue";
import Button from "../components/ui/Button.vue";
import Table from "../components/ui/table/Table.vue";
import RouterButton from "../components/ui/RouterButton.vue";
import VueDatePicker from "@vuepic/vue-datepicker";
import { onMounted } from "vue";
import { useDriver } from "../store/driver";
import { listDriver } from "../model/tableColumns/listDriver";
import { ref, computed } from "vue";
import { apiUrl, fetchWithAuth, simpleDateNow } from "../lib/utils";
import { useAlert } from "../store/alert";
import { $swal } from "@/src/components/ui/SweetAlert.vue";

const tableKey = ref(0);
const driver = ref("");
const isReload = computed(getIsReload);
const driverStore = useDriver();
const selTanggal = ref(null);
const alert = useAlert();

const search = async () => {
  try {
    if (!driver.value.length && !selTanggal.value) {
      driverStore.listPengeluaran.list = [];
      getResource();
    } else {
      const namaDriver = `nama_driver=${driver.value}`;
      const formatTanggal = simpleDateNow(selTanggal.value);
      const tanggal = `tanggal=${formatTanggal}`;

      const result = await fetchWithAuth(
        "GET",
        `${apiUrl}/api/distribusi/search-driver?${namaDriver}&${tanggal}`
      );

      driverStore.listPengeluaran.list = result;
    }

    tableKey.value++;
  } catch (error) {
    $swal.error(error);
    console.log(error);
  }
};

const getResource = async () => {
  if (!driverStore.listPengeluaran.list.length) {
    await driverStore.getListDriver();
    tableKey.value++;
  }
};

function getIsReload() {
  const checkDriverAndTanggal = selTanggal.value || driver.value.length;
  return checkDriverAndTanggal;
}

onMounted(() => getResource());
</script>

<template>
  <div class="tw-flex tw-flex-col tw-gap-4 lg:tw-px-4 tw-px-0 tw-min-h-[700px]">
    <SlideRightX
      class=""
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-out="0.1"
      :delay-in="0.1"
      :initial-x="-40"
      :x="40">
      <Card no-subheader no-header class="tw-mb-6">
        <template #content>
          <div
            class="tw-w-full tw-flex tw-flex-col tw-gap-4 tw-py-8 tw-px-2 tw-items-start">
            <div class="tw-w-full tw-flex tw-justify-between">
              <span class="tw-text-xl tw-font-bold">List Pengeluaran</span>
              <RouterButton
                icon="mdi mdi-plus"
                to="/driver/add-pengeluaran-driver"
                class="tw-w-28">
                Add
              </RouterButton>
            </div>
            <div
              class="tw-grid tw-grid-cols-1 md:tw-grid-cols-3 tw-gap-4 tw-w-full md:tw-w-[80%] tw-mb-12 tw-mt-8">
              <VueDatePicker
                @keyup.enter="search"
                v-model="selTanggal"
                :enable-time-picker="false"
                placeholder="Tanggal"
                :teleport="true"
                auto-apply />
              <BFormInput
                @keyup.enter="search"
                type="text"
                v-model="driver"
                placeholder="Driver" />
              <Button
                :trigger="search"
                class="tw-bg-blue-500 tw-px-6 tw-w-full md:tw-w-28"
                loading-mode="icon">
                <i
                  :class="[
                    'mdi tw-text-xl',
                    isReload ? 'mdi-magnify' : 'mdi-reload',
                  ]" />
              </Button>
            </div>
            <Table
              :key="tableKey"
              :loading="driverStore.listPengeluaran.loading"
              :columns="listDriver"
              :table-data="driverStore.listPengeluaran.list" />
          </div>
        </template>
      </Card>
    </SlideRightX>
  </div>
</template>
