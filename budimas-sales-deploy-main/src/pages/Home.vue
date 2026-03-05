<!-- eslint-disable vue/multi-word-component-names -->
<script setup>
import SlideRightX from "../components/animation/SlideRightX.vue";
import Card from "../components/ui/Card.vue";
import { useDashboard } from "../store/dashboard";
import { useSales } from "../store/sales";
import Skeleton from "../components/ui/Skeleton.vue";
import { parseCurrency, getMonthString } from "../lib/utils";
import { useChart, getMonthOptions } from "../lib/chartOmset";
import VueApexCharts from "vue3-apexcharts";
import { onMounted, ref } from "vue";
import SelectInput from "../components/ui/formInput/SelectInput.vue";
import Button from "../components/ui/Button.vue";
import VueDatePicker from "@vuepic/vue-datepicker";
import { sessionDisk } from "../lib/utils";
import Empty from "../components/ui/Empty.vue";
import { useAlert } from "../store/alert";
import Loader from "../components/ui/Loader.vue";

const monthOptions = getMonthOptions();
const dashboard = useDashboard();
const sales = useSales();
const alert = useAlert();
const selectedMonth = ref();
const selectedYear = ref(new Date().getFullYear());
const monthLoading = ref(false);
const user = sessionDisk.getSession("authUser");
const currentData = useChart();
const monthData = useChart();
const currentChartKey = ref(0);
const monthChartKey = ref(0);
const checkMonthSeries = ref([]);

const getMonthChart = async () => {
  try {
    if (!selectedMonth.value || !selectedYear.value)
      throw "ada field yang kosong";

    monthLoading.value = true;
    const omset = await dashboard.getChart(
      user.id_user,
      selectedYear.value,
      selectedMonth.value,
      true
    );
    monthData.transformSeries(omset.order, omset.realisasi, omset.retur);
    await dashboard.getDashboardInfoMonth(
      user.id_user,
      selectedYear.value,
      selectedMonth.value,
      monthData.options.value,
      monthData.series.value
    );
    checkMonthSeries.value = dashboard.dashboardInfoMonth.seriesData
      .map((val) => val.data)
      .flat();
  } catch (error) {
    alert.setMessage(error, "danger");
  } finally {
    monthChartKey.value++;
    monthLoading.value = false;
  }
};

onMounted(async () => {
  await dashboard.getCurrentChart(user.id_user);
  currentData.transformSeries(
    dashboard.chart.currentChart.order,
    dashboard.chart.currentChart.realisasi,
    dashboard.chart.currentChart.retur
  );
  checkMonthSeries.value = dashboard.dashboardInfoMonth.seriesData
    .map((val) => val.data)
    .flat();

  currentChartKey.value++;
});
</script>

<script>
export default {
  components: {
    apexchart: VueApexCharts,
  },
};
</script>

<template>
  <div class="tw-flex tw-flex-col tw-gap-4 lg:tw-px-0 tw-px-0 tw-min-h-[700px]">
    <SlideRightX
      class=""
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-out="0.1"
      :delay-in="0.1"
      :initial-x="-40"
      :x="40">
      <Card :no-header="true" :no-subheader="true">
        <template #content>
          <div
            class="tw-w-full tw-flex lg:tw-flex-row tw-flex-col lg:tw-justify-between tw-justify-start lg:tw-items-center tw-items-start tw-py-5 tw-gap-2">
            <span
              class="responsive-text tw-flex tw-flex-row tw-gap-2 tw-justify-center tw-items-center">
              Sales:
              <Skeleton
                class="tw-w-32 tw-h-6"
                v-if="sales.loading && !sales.salesUser" />
              <p v-else>
                {{ sales.salesUser?.nama }}
              </p>
            </span>
            <span class="responsive-text tw-flex tw-flex-row tw-gap-4">
              Last Update :
              <Skeleton
                class="tw-w-48 tw-h-6"
                v-if="
                  dashboard.loading && !dashboard.dashboardInfo?.updateTerakhir
                " />
              <p v-else>
                {{ dashboard.dashboardInfo?.updateTerakhir.split(".")[0] }}
              </p>
            </span>
          </div>
        </template>
      </Card>
    </SlideRightX>
    <SlideRightX
      class=""
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.2"
      :delay-out="0.2"
      :initial-x="-40"
      :x="40">
      <Card :no-subheader="true">
        <template #header>Report Harian</template>
      </Card>
    </SlideRightX>
    <SlideRightX
      class="tw-w-full tw-flex tw-justify-between tw-items-center tw-gap-4 tw-flex-wrap lg:tw-flex-nowrap"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.3"
      :delay-out="0.3"
      :initial-x="-40"
      :x="40">
      <div
        class="tw-w-full tw-h-[130px] tw-p-6 tw-flex tw-flex-col tw-justify-start tw-items-start tw-gap-2 tw-bg-white tw-drop-shadow-xl tw-rounded-lg -tw-z-50 hover:tw-scale-105 tw-duration-300 tw-ease-out">
        <span class="tw-font-bold tw-text-sm tw-text-gray-700">Order</span>
        <div class="tw-flex tw-gap-2 tw-text-gray-700">
          <i class="mdi mdi-clipboard-text responsive-text"></i>
          <Skeleton class="tw-w-32 tw-h-8" v-if="dashboard.loading" />
          <span class="tw-font-bold responsive-text" v-else>
            {{ dashboard.dashboardInfo?.totalOrder }} Order
          </span>
        </div>
      </div>
      <div
        class="tw-w-full tw-h-[130px] tw-p-6 tw-flex tw-flex-col tw-justify-start tw-items-start hover:tw-scale-105 tw-duration-300 tw-ease-out tw-gap-2 tw-bg-white tw-drop-shadow-xl tw-rounded-lg">
        <span class="tw-font-bold tw-text-sm tw-text-gray-700">
          Customer Order
        </span>
        <div class="tw-flex tw-items-center tw-gap-2 tw-text-gray-700">
          <i class="mdi mdi-account-multiple responsive-text"></i>
          <Skeleton class="tw-w-32 tw-h-8" v-if="dashboard.loading" />
          <span class="tw-font-bold responsive-text" v-else>
            {{ dashboard.dashboardInfo?.totalCustomerOrder }} Customer
          </span>
        </div>
      </div>
      <div
        class="tw-w-full tw-h-[130px] tw-p-6 tw-flex tw-flex-col tw-justify-start tw-items-start hover:tw-scale-105 tw-duration-300 tw-ease-out tw-gap-2 tw-bg-white tw-drop-shadow-xl tw-rounded-lg">
        <span class="tw-font-bold tw-text-sm tw-text-gray-700">Kunjungan</span>
        <div class="tw-flex tw-gap-2 tw-text-gray-700">
          <i class="mdi mdi-calendar-check responsive-text"></i>
          <Skeleton class="tw-w-32 tw-h-8" v-if="dashboard.loading" />
          <span class="tw-font-bold responsive-text" v-else>
            {{ dashboard.dashboardInfo?.sudahBerkunjung }}/{{
              dashboard.dashboardInfo?.belumKunjungan
            }}
            Kunjungan
          </span>
        </div>
      </div>
      <div
        class="tw-w-full tw-h-[130px] tw-p-6 tw-flex tw-flex-col tw-justify-start tw-items-start hover:tw-scale-105 tw-duration-300 tw-ease-out tw-gap-2 tw-bg-white tw-drop-shadow-xl tw-rounded-lg">
        <span class="tw-font-bold tw-text-sm tw-text-gray-700">
          Total Order
        </span>
        <div class="tw-flex tw-gap-2 tw-text-gray-700">
          <i class="mdi mdi-currency-usd responsive-text"></i>
          <Skeleton class="tw-w-32 tw-h-8" v-if="dashboard.loading" />
          <span class="tw-font-bold responsive-text" v-else>
            Rp. {{ parseCurrency(dashboard.dashboardInfo?.totalTransaksi) }}
          </span>
        </div>
      </div>
      <div
        class="tw-w-full tw-h-[130px] tw-p-6 tw-flex tw-flex-col tw-justify-start tw-items-start hover:tw-scale-105 tw-duration-300 tw-ease-out tw-gap-2 tw-bg-white tw-drop-shadow-xl tw-rounded-lg">
        <span class="tw-font-bold tw-text-sm tw-text-gray-700">
          Target Pencapaian
        </span>
        <div class="tw-flex tw-gap-2 tw-text-gray-700">
          <i class="mdi mdi-currency-usd responsive-text"></i>
          <Skeleton class="tw-w-32 tw-h-8" v-if="dashboard.loading" />
          <span class="tw-font-bold responsive-text" v-else>Rp. 0</span>
        </div>
      </div>
    </SlideRightX>
    <SlideRightX
      class="tw-w-full tw-flex tw-justify-between tw-items-center tw-gap-4 tw-flex-wrap lg:tw-flex-nowrap"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.4"
      :delay-out="0.4"
      :initial-x="-40"
      :x="40">
      <Card :no-subheader="true">
        <template #header>Grafik Harian</template>
        <template #content>
          <div id="chart" class="tw-w-full tw-py-8">
            <div
              class="tw-w-full tw-h-80 tw-flex tw-justify-center tw-items-center"
              v-if="dashboard.chart.loading">
              <Loader />
            </div>
            <apexchart
              v-else
              height="450"
              :key="currentChartKey"
              :options="currentData.options.value"
              :series="currentData.series.value" />
          </div>
        </template>
      </Card>
    </SlideRightX>
    <Card :no-subheader="true">
      <template #header>Report Bulanan</template>
      <template #content>
        <div
          class="tw-w-full tw-flex tw-flex-col tw-justify-center tw-items-center tw-pb-8 tw-gap-6">
          <div
            class="tw-flex tw-flex-row tw-w-full tw-items-center tw-justify-center tw-px-2 tw-gap-2 tw-flex-wrap">
            <div
              class="tw-w-full md:tw-w-[300px] tw-h-20 tw-flex tw-flex-col tw-gap-2">
              <span class="tw-font-bold">Bulan :</span>
              <div class="tw-w-full">
                <SelectInput
                  v-model="selectedMonth"
                  :options="monthOptions"
                  placeholder="Select Month"
                  size="sm"
                  class="tw-h-[38px]" />
              </div>
            </div>
            <div
              class="tw-w-full md:tw-w-[300px] tw-h-20 tw-flex tw-flex-col tw-gap-2">
              <span class="tw-font-bold">Tahun :</span>
              <div class="tw-w-full">
                <VueDatePicker
                  v-model="selectedYear"
                  year-picker
                  auto-apply
                  placeholder="Select Year" />
              </div>
            </div>
            <Button
              class="tw-w-full md:tw-w-32 tw-h-10 tw-mt-6"
              :trigger="getMonthChart">
              <i class="mdi mdi-magnify tw-text-lg tw-mr-1"></i>
              Cari Data
            </Button>
          </div>
          <div v-if="dashboard.dashboardInfoMonth.month" class="tw-text-sm">
            <span>Bulan Terpilih :</span>
            <strong>
              {{ getMonthString(dashboard.dashboardInfoMonth.month) }}
              {{ dashboard.dashboardInfoMonth.year }}
            </strong>
          </div>
        </div>
      </template>
    </Card>
    <SlideRightX
      class="tw-w-full tw-flex tw-justify-between tw-items-center tw-gap-4 tw-flex-wrap lg:tw-flex-nowrap"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.3"
      :delay-out="0.3"
      :initial-x="-40"
      :x="40">
      <div
        class="tw-w-full tw-h-[130px] tw-p-6 tw-flex tw-flex-col tw-justify-start tw-items-start tw-gap-2 tw-bg-white tw-drop-shadow-xl tw-rounded-lg -z-50 hover:tw-scale-105 tw-duration-300 tw-ease-out">
        <span class="tw-font-bold tw-text-sm tw-text-gray-700">Nota Order</span>
        <div class="tw-flex tw-gap-2 tw-text-gray-700">
          <i class="mdi mdi-clipboard-text responsive-text"></i>
          <Skeleton
            class="tw-w-32 tw-h-8"
            v-if="dashboard.dashboardInfoMonth.loading" />
          <span class="tw-font-bold responsive-text" v-else>
            {{ dashboard.dashboardInfoMonth.dashboardInfo?.totalOrder }} Nota
            Order
          </span>
        </div>
      </div>
      <div
        class="tw-w-full tw-h-[130px] tw-p-6 tw-flex tw-flex-col tw-justify-start tw-items-start hover:tw-scale-105 tw-duration-300 tw-ease-out tw-gap-2 tw-bg-white tw-drop-shadow-xl tw-rounded-lg">
        <span class="tw-font-bold tw-text-sm tw-text-gray-700">
          Active Outlet
        </span>
        <div class="tw-flex tw-items-center tw-gap-2 tw-text-gray-700">
          <i class="mdi mdi-account-multiple responsive-text"></i>
          <Skeleton
            class="tw-w-32 tw-h-8"
            v-if="dashboard.dashboardInfoMonth.loading" />
          <span class="tw-font-bold responsive-text" v-else>
            {{ dashboard.dashboardInfoMonth.dashboardInfo?.totalCustomerOrder }}
            Active Outlet
          </span>
        </div>
      </div>
      <div
        class="tw-w-full tw-h-[130px] tw-p-6 tw-flex tw-flex-col tw-justify-start tw-items-start hover:tw-scale-105 tw-duration-300 tw-ease-out tw-gap-2 tw-bg-white tw-drop-shadow-xl tw-rounded-lg">
        <span class="tw-font-bold tw-text-sm tw-text-gray-700">
          Actual Call
        </span>
        <div class="tw-flex tw-gap-2 tw-text-gray-700">
          <i class="mdi mdi-calendar-check responsive-text"></i>
          <Skeleton
            class="tw-w-32 tw-h-8"
            v-if="dashboard.dashboardInfoMonth.loading" />
          <span class="tw-font-bold responsive-text" v-else>
            {{ dashboard.dashboardInfoMonth.dashboardInfo?.sudahBerkunjung }}
            Actual Call
          </span>
        </div>
      </div>
      <div
        class="tw-w-full tw-h-[130px] tw-p-6 tw-flex tw-flex-col tw-justify-start tw-items-start hover:tw-scale-105 tw-duration-300 tw-ease-out tw-gap-2 tw-bg-white tw-drop-shadow-xl tw-rounded-lg">
        <span class="tw-font-bold tw-text-sm tw-text-gray-700">
          Total Order
        </span>
        <div class="tw-flex tw-gap-2 tw-text-gray-700">
          <i class="mdi mdi-currency-usd responsive-text"></i>
          <Skeleton
            class="tw-w-32 tw-h-8"
            v-if="dashboard.dashboardInfoMonth.loading" />
          <span class="tw-font-bold responsive-text" v-else>
            Rp.
            {{
              parseCurrency(
                dashboard.dashboardInfoMonth.dashboardInfo?.totalTransaksi
              )
            }}
          </span>
        </div>
      </div>
      <div
        class="tw-w-full tw-h-[130px] tw-p-6 tw-flex tw-flex-col tw-justify-start tw-items-start hover:tw-scale-105 tw-duration-300 tw-ease-out tw-gap-2 tw-bg-white tw-drop-shadow-xl tw-rounded-lg">
        <span class="tw-font-bold tw-text-sm tw-text-gray-700">
          Target Pencapaian
        </span>
        <div class="tw-flex tw-gap-2 tw-text-gray-700">
          <i class="mdi mdi-currency-usd responsive-text"></i>
          <Skeleton
            class="tw-w-32 tw-h-8"
            v-if="dashboard.dashboardInfoMonth.loading" />
          <span class="tw-font-bold responsive-text" v-else>Rp. 0</span>
        </div>
      </div>
      <div
        class="tw-w-full tw-h-[130px] tw-p-6 tw-flex tw-flex-col tw-justify-start tw-items-start hover:tw-scale-105 tw-duration-300 tw-ease-out tw-gap-2 tw-bg-white tw-drop-shadow-xl tw-rounded-lg">
        <span class="tw-font-bold tw-text-sm tw-text-gray-700">Call Plan</span>
        <div class="tw-flex tw-gap-2 tw-text-gray-700">
          <i class="mdi mdi-calendar-check responsive-text"></i>
          <Skeleton
            class="tw-w-32 tw-h-8"
            v-if="dashboard.dashboardInfoMonth.loading" />
          <span class="tw-font-bold responsive-text" v-else>
            {{ dashboard.dashboardInfoMonth.dashboardInfo?.totalCallPlan || 0 }}
            Call Plan
          </span>
        </div>
      </div>
    </SlideRightX>
    <Card :no-subheader="true">
      <template #header>Grafik Bulanan</template>
      <template #content>
        <div id="chart" class="tw-w-full tw-py-16">
          <Empty
            v-if="!checkMonthSeries.length && !monthLoading"
            text="Tidak ada data" />
          <div
            class="tw-w-full tw-h-80 tw-flex tw-justify-center tw-items-center"
            v-else-if="monthLoading">
            <Loader />
          </div>
          <apexchart
            v-else
            height="450"
            :key="monthChartKey"
            :options="dashboard.dashboardInfoMonth.optionsdata"
            :series="dashboard.dashboardInfoMonth.seriesData" />
        </div>
      </template>
    </Card>
  </div>
</template>

<style lang="scss" scoped>
.dp__theme_light {
  --dp-background-color: #fff;
  --dp-text-color: #212121;
  --dp-hover-color: #f3f3f3;
  --dp-hover-text-color: #212121;
  --dp-hover-icon-color: #959595;
  --dp-primary-color: #1976d2;
  --dp-primary-disabled-color: #6bacea;
  --dp-primary-text-color: #f8f5f5;
  --dp-secondary-color: #c0c4cc;
  --dp-border-color: #7e7e7e;
  --dp-menu-border-color: #ddd;
  --dp-border-color-hover: #aaaeb7;
  --dp-border-color-focus: #aaaeb7;
  --dp-disabled-color: #f6f6f6;
  --dp-scroll-bar-background: #f3f3f3;
  --dp-scroll-bar-color: #959595;
  --dp-success-color: #76d275;
  --dp-success-color-disabled: #a3d9b1;
  --dp-icon-color: #535353;
  --dp-danger-color: #ff6f60;
  --dp-marker-color: #ff6f60;
  --dp-tooltip-color: #fafafa;
  --dp-disabled-color-text: #8e8e8e;
  --dp-highlight-color: rgb(25 118 210 / 10%);
  --dp-range-between-dates-background-color: var(--dp-hover-color, #f3f3f3);
  --dp-range-between-dates-text-color: var(--dp-hover-text-color, #212121);
  --dp-range-between-border-color: var(--dp-hover-color, #f3f3f3);
}
.make-z-hight {
  z-index: -99 !important;
}
</style>
