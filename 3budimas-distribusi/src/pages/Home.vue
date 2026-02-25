<script setup>
import SlideRightX from "../components/animation/SlideRightX.vue";
import Card from "../components/ui/Card.vue";
import { useDashboard } from "../store/dashboard";
import Skeleton from "../components/ui/Skeleton.vue";
import { ref, onMounted } from "vue";
import VueDatePicker from "@vuepic/vue-datepicker";
import "@vuepic/vue-datepicker/dist/main.css";
import { useKepalaCabang } from "../store/kepalaCabang";

const kepalaCabang = useKepalaCabang();
const date = ref();
const fromDate = ref();
const toDate = ref();

const getResource = async () => {
  const startDate = new Date();
  const endDate = new Date(new Date().setDate(startDate.getDate() + 7));
  date.value = [startDate, endDate];
}

onMounted(() => {
  getResource()
});
</script>

<template>
  <div class="tw-flex tw-flex-col tw-gap-4 lg:tw-px-4 tw-px-0 tw-min-h-screen">
    <SlideRightX
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.2"
      :delay-out="0.2"
      :initial-x="-40"
      :x="40">
      <Card :no-subheader="true">
        <template #header>Summary Report</template>
        <template #content>
          <span
            class="tw-w-full tw-text-m tw-flex tw-flex-row tw-gap-4 tw-mb-3 tw-mt-[-10px]">
            Last Update :
            <Skeleton
              class="tw-w-48 tw-h-6"
              v-if="
                kepalaCabang?.loading && !kepalaCabang?.kepalaCabangUser
              " />
            <p v-else>
              {{ kepalaCabang?.kepalaCabangUser?.kepalaCabang?.last_update }}
            </p>
          </span>
          <div class="tw-w-full md:tw-w-1/2 tw-grid tw-grid-cols-1 md:tw-grid-cols-2 tw-gap-4 tw-pb-10">
            <div class="tw-flex tw-flex-col tw-gap-2">
              <span>Tanggal Dari :</span>
              <VueDatePicker
                v-model="fromDate"
                :enable-time-picker="false"
                placeholder="mm/dd/yyyy"
                :teleport="true"
                auto-apply />
            </div>
            <div class="tw-flex tw-flex-col tw-gap-2">
              <span>Tanggal Sampai :</span>
              <VueDatePicker
                v-model="toDate"
                :enable-time-picker="false"
                placeholder="mm/dd/yyyy"
                :teleport="true"
                auto-apply />
            </div>
          </div>
        </template>
      </Card>
    </SlideRightX>
  </div>
</template>
