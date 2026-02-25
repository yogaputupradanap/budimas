<script setup>
import { getDateNow } from "@/src/lib/utils";
import budimasImage from "../../assets/images/logo-budimas-black.png";

const props = defineProps({
  info: {
    type: Object,
    default() {
      return {};
    },
  },
  list: {
    type: Array,
    default() {
      return [];
    },
  },
});

const fieldCol = [
  "Customer",
  "No. Faktur",
  "Parkir",
  "Bongkar",
  "Biaya Lainnya",
  "keterangan",
  "Sub Total",
  "Terms"
];
const dateNow = getDateNow();
</script>

<template>
  <div
    id="laporan-driver"
    class="tw-w-full tw-h-full tw-flex tw-flex-col tw-p-2 tw-text-xs">
    <div
      class="tw-w-full tw-flex tw-flex-col tw-min-h-[740px] tw-h-auto tw-justify-between tw-text-[8px]">
      <div class="tw-w-full tw-flex tw-flex-col">
        <div
          class="tw-w-full tw-flex tw-flex-col tw-gap-1 tw-border-b tw-border-black tw-justify-center tw-items-center tw-p-4 tw-relative tw-pb-6">
          <div
            class="tw-p-2 tw-h-10 tw-border-2 tw-border-black tw-text-[14px] tw-font-extrabold tw-rounded-lg tw-leading-[0px]">
            {{ props.info?.kode_rute }}
          </div>
          <h1 class="tw-font-extrabold tw-text-base">SK RUTE</h1>
          <p class="tw-text-center">
            Alamat : FRM+F28, JL, Gn.Slamet IV, Mojosongo, Kec. Jebres, Kota
            Surakarta, Jawa Tengah 67136
          </p>
          <h4 class="tw-font-medium tw-text-[10px]">Phone : (0271) 856064</h4>
          <img
            :src="budimasImage"
            alt="logo-budimas"
            class="tw-w-28 tw-absolute tw-right-8 tw-top-4" />
        </div>
        <div
          class="tw-w-full tw-flex tw-flex-row tw-justify-between tw-px-8 tw-font-semibold tw-border-b tw-border-black tw-pb-4 tw-text-[10px]">
          <table class="tw-w-[270px]">
            <tr>
              <td>Berangkat</td>
              <td class="tw-w-10 tw-text-center">:</td>
              <td>{{ dateNow }}</td>
            </tr>
            <tr>
              <td>No. Polisi</td>
              <td class="tw-w-16 tw-text-center">:</td>
              <td>{{ props.info?.no_pelat }}</td>
            </tr>
            <tr>
              <td>Driver</td>
              <td class="tw-w-16 tw-text-center">:</td>
              <td>{{ props.info?.nama }}</td>
            </tr>
            <tr>
              <td>Helper</td>
              <td class="tw-w-16 tw-text-center">:</td>
              <td></td>
            </tr>
            <tr>
              <td>Faktur</td>
              <td class="tw-w-16 tw-text-center">:</td>
              <td>{{ props.list.length }}</td>
            </tr>
          </table>
          <table class="tw-w-[400px]">
            <tr>
              <td class="tw-text-end">KM Berangkat</td>
              <td class="tw-w-10 tw-text-center">:</td>
              <td><div class="tw-w-52 tw-h-2"></div></td>
            </tr>
            <tr>
              <td class="tw-text-end">KM Pulang</td>
              <td class="tw-w-16 tw-text-center">:</td>
              <td></td>
            </tr>
            <tr>
              <td class="tw-text-end">KM Isi BBM</td>
              <td class="tw-w-16 tw-text-center">:</td>
              <td></td>
            </tr>
            <tr>
              <td class="tw-text-end">Isi BBM/Liter</td>
              <td class="tw-w-16 tw-text-center">:</td>
              <td></td>
            </tr>
            <tr>
              <td class="tw-text-end">Isi BBM/Liter</td>
              <td class="tw-w-16 tw-text-center">:</td>
              <td></td>
            </tr>
          </table>
        </div>
        <div
          class="tw-w-full tw-border-b tw-border-black tw-flex tw-justify-between tw-px-2">
          <span
            v-for="(col, index) in fieldCol"
            :key="col"
            :class="[
              'tw-w-24 tw-text-center tw-h-6 tw-font-bold',
              index == 0 || index == 1
                ? 'tw-pl-4'
                : index == 7
                ? 'tw-pr-4'
                : index == 6 && 'tw-pr-2',
            ]">
            {{ col }}
          </span>
        </div>
        <div
          class="tw-w-full tw-border-b tw-border-black tw-flex tw-flex-col tw-py-2 tw-gap-2">
          <div
            v-for="a in Array.from({ length: 10 }, (_, i) => i)"
            :key="a"
            class="tw-w-full tw-flex tw-justify-between tw-px-2">
            <span
              class="tw-w-28 tw-border tw-border-black tw-min-h-[20px] tw-rounded-sm tw-px-2 tw-h-auto tw-text-[0.60rem]">
              <!-- {{ a.nama_customer }} -->
            </span>
            <span
              class="tw-w-28 tw-border tw-border-black tw-min-h-[20px] tw-rounded-sm tw-px-2 tw-pb-4 tw-h-auto tw-text-[0.60rem]">
              <!-- {{ a.no_faktur }} -->
            </span>
            <span
              class="tw-w-28 tw-border tw-border-black tw-h-[20px] tw-rounded-sm"></span>
            <span
              class="tw-w-28 tw-border tw-border-black tw-h-[20px] tw-rounded-sm"></span>
            <span
              class="tw-w-28 tw-border tw-border-black tw-h-[20px] tw-rounded-sm"></span>
            <span
              class="tw-w-28 tw-border tw-border-black tw-h-[20px] tw-rounded-sm"></span>
            <span
              class="tw-w-28 tw-border tw-border-black tw-h-[20px] tw-rounded-sm"></span>
              <span
              class="tw-w-28 tw-border tw-border-black tw-h-[20px] tw-rounded-sm"></span>
          </div>
        </div>
        <div class="tw-w-full tw-flex tw-justify-end tw-text-[10px]">
          <table class="tw-w-[400px]">
            <tr>
              <td>Kasbon Harian</td>
              <td class="tw-w-10 tw-text-center">:</td>
              <td><div class="tw-w-44" /></td>
            </tr>
            <tr>
              <td>Sisa Kasbon</td>
              <td class="tw-w-10 tw-text-center">:</td>
              <td><div class="tw-w-44" /></td>
            </tr>
          </table>
        </div>
      </div>
      <div class="tw-w-full tw-flex tw-gap-6 tw-pl-12 tw-text-[12px]">
        <div
          class="tw-w-[200px] tw-flex tw-flex-col tw-gap-2 tw-justify-center tw-items-center">
          <div class="tw-w-full tw-border-b tw-border-black tw-h-1" />
          <span>Driver</span>
        </div>
        <div
          class="tw-w-[200px] tw-flex tw-flex-col tw-gap-2 tw-justify-center tw-items-center">
          <div class="tw-w-full tw-border-b tw-border-black tw-h-1" />
          <span>Helper</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
table > tr:last-child {
  width: 200px;
}
</style>
