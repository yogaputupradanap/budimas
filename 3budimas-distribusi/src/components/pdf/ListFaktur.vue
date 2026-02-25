<script setup>
import { getMonthString } from "../../lib/utils";
import { getDateNow, parseCurrency, getDayString } from "../../lib/utils";

const props = defineProps({
  list: {
    type: Array,
    default() {
      return [];
    },
  },
  info: {
    type: Object,
    default() {
      return {};
    },
  },
});

const dateWord = () => {
  const nowDateArr = getDateNow().split("/");
  const getMonthWord = getMonthString(nowDateArr[1]);
  nowDateArr[1] = getMonthWord;
  return nowDateArr.join(" ");
};
const slashDate = getDateNow(new Date(), false);
const getDay = () => getDayString(new Date().getDay());
</script>

<template>
  <div
    id="list-faktur"
    class="tw-w-full tw-flex tw-flex-col tw-p-8 tw-text-[8px] tw-items-center tw-gap-6">
    <h1
      class="tw-uppercase tw-font-bold tw-pb-2 tw-border-b tw-border-black tw-text-[12px]">
      draft by nota
    </h1>
    <div class="tw-w-[90%] tw-flex tw-justify-between">
      <div class="tw-flex tw-flex-col tw-gap-4">
        <span class="tw-uppercase tw-text-[12px]">pt budimas makmur mulia</span>
        <div class="tw-flex tw-flex-col tw-hap-2">
          <span class="tw-font-bold">{{ dateWord() }}</span>
          <span class="tw-font-bold">DR824050018</span>
          <span class="tw-uppercase">
            {{ props.info.nama }} / {{ getDay() }} / {{ dateWord() }} / g1
          </span>
        </div>
      </div>
      <div class="tw-w-32 tw-flex tw-flex-col tw-text-[9px]">
        <span class="tw-uppercase">{{ props?.info?.nama }}</span>
        <span>{{ slashDate }} {{ getDateNow(new Date(), true, true) }}</span>
        <span>Page 1 of 1</span>
      </div>
    </div>
    <div class="tw-w-full tw-flex tw-flex-col tw-gap-2">
      <div
        class="tw-w-full tw-flex tw-justify-between tw-items-center tw-px-2 tw-border-b tw-border-black tw-font-bold tw-text-[6px]">
        <span class="tw-w-6 tw-h-6 tw-text-start">No</span>
        <span class="tw-w-20 tw-h-6 tw-text-start">Tanggal</span>
        <span class="tw-w-32 tw-h-6 tw-text-start">Faktur</span>
        <span class="tw-w-24 tw-h-6 tw-text-start tw-pl-2">Area</span>
        <span class="tw-w-96 tw-h-6 tw-text-start">Outlet</span>
        <span class="tw-w-20 tw-h-6 tw-text-start">Route</span>
        <span class="tw-w-16 tw-h-6 tw-text-start">Terms</span>
        <span class="tw-w-24 tw-h-6 tw-text-start">Jumlah Harga</span>
      </div>
      <div
        class="tw-w-full tw-flex tw-flex-col tw-gap-0 tw-h-auto tw-border-b tw-border-black tw-text-[6px] tw-px-2 [&_div:last-child]:tw-border-none">
        <div
          v-for="(list, idx) in props.list"
          :key="list"
          class="tw-w-full tw-flex tw-justify-between tw-pb-3 tw-border-b tw-border-gray-800 tw-border-dashed">
          <span class="tw-w-6 tw-text-start">
            {{ idx + 1 }}
          </span>
          <span class="tw-w-20 tw-text-start">
            {{ list.tanggal_order }}
          </span>
          <span class="tw-w-32 tw-text-start">
            {{ list.no_faktur }}
          </span>
          <span class="tw-w-24 tw-text-start tw-pl-2">{{ list.area }}</span>
          <span class="tw-w-96 tw-text-start tw-uppercase">
            {{ list.kode_customer }} {{ list.nama_customer }} "{{
              list.no_order
            }}
          </span>
          <span class="tw-w-20 tw-text-start">
            {{ list.kode_rute }}
          </span>
          <span class="tw-w-16 tw-text-start">
            {{ list.terms }}
          </span>
          <span class="tw-w-24 tw-text-start">
            Rp. {{ parseCurrency(list.total_penjualan) }}
          </span>
        </div>
      </div>
      <div class="tw-w-full tw-flex tw-justify-end tw-relative">
        <div
          class="tw-w-40 tw-font-bold tw-text-[12px] tw-pb-3 tw-pr-2 tw-text-end tw-border-b-[0.2px] tw-border-black">
          Rp {{ parseCurrency(props.info.total_penjualan) }}
        </div>
        <div
          class="tw-absolute tw-right-0 tw-w-40 tw-top-1 tw-h-[29px] tw-border-b-[0.2px] tw-border-black" />
      </div>
    </div>
    <div class="tw-w-full tw-flex tw-justify-center">
      <div class="tw-w-[70%] tw-flex tw-justify-between">
        <div
          class="tw-w-32 tw-h-16 tw-flex tw-flex-col tw-items-center tw-justify-between">
          <span>Droping</span>
          <span>(..................................................)</span>
        </div>
        <div
          class="tw-w-32 tw-h-16 tw-flex tw-flex-col tw-items-center tw-justify-between">
          <span>Checker</span>
          <span>(..................................................)</span>
        </div>
        <div
          class="tw-w-32 tw-h-16 tw-flex tw-flex-col tw-items-center tw-justify-between">
          <span>Admin</span>
          <span>(..................................................)</span>
        </div>
      </div>
    </div>
  </div>
</template>
