<script setup>
import { parseCurrency, simpleDateNow } from "@/src/lib/utils";

const props = defineProps({
  info: {
    type: Object,
    default() {
      return {}
    }
  },
  list: {
    type: Array,
    default() {
      return []
    }
  }
})

const calcSubTotal = (object) => {
  const subtotal =
    object.nominal_parkir + object.nominal_bongkar + object.nominal_lainnya;
  return subtotal;
};

const fieldCol = [
  "Parkir",
  "Bongkar",
  "Biaya Lainnya",
  "keterangan",
  "Sub Total",
];
</script>

<template>
  <div
    id="pengeluaran-driver"
    class="tw-w-full tw-flex tw-flex-col tw-p-2 tw-text-xs">
    <div
      v-for="(i, idx) in list"
      :key="idx"
      :class="[
        'tw-w-full tw-flex tw-flex-col tw-h-[510px] tw-justify-between tw-text-[8px]',
        idx % 2 == 0
          ? 'tw-border-b tw-border-gray-600 tw-border-dashed'
          : 'tw-mt-8',
      ]">
      <div class="tw-w-full tw-flex tw-flex-col">
        <div
          class="tw-w-full tw-flex tw-flex-col tw-border-b tw-border-black tw-justify-center tw-items-center tw-p-4 tw-relative tw-pb-6">
          <div
            class="tw-p-2 tw-h-10 tw-border-2 tw-border-black tw-text-[14px] tw-font-extrabold tw-rounded-lg tw-leading-[0px]">
            {{ i.kode_rute }}
          </div>
          <h1 class="tw-font-extrabold tw-text-base">FAKTUR RUTE</h1>
          <p>No. Faktur : {{ i.nomor_faktur }}</p>
          <p class="tw-text-center">
            Alamat : FRM+F28, JL, Gn.Slamet IV, Mojosongo, Kec. Jebres, Kota
            Surakarta, Jawa Tengah 67136
          </p>
          <h4 class="tw-font-medium tw-text-[10px]">Phone : (0271) 856064</h4>
          <h4
            class="tw-font-medium tw-text-[8px] tw-absolute tw-top-4 tw-right-4">
            {{ simpleDateNow() }}
          </h4>
          <img
            :src="budimasImage"
            alt="logo-budimas"
            class="tw-w-28 tw-absolute tw-right-8 tw-top-4" />
        </div>
        <div
          class="tw-w-full tw-flex tw-flex-row tw-justify-between tw-px-8 tw-font-semibold tw-border-b tw-border-black tw-pb-4 tw-text-[10px]">
          <table class="tw-w-[200px]">
            <tr>
              <td>Berangkat</td>
              <td class="tw-w-10 tw-text-center">:</td>
              <td>{{ simpleDateNow(info.tanggal) }}</td>
            </tr>
            <tr>
              <td>Driver</td>
              <td class="tw-w-16 tw-text-center">:</td>
              <td>{{ info.namaDriver }}</td>
            </tr>
            <tr>
              <td>Helper</td>
              <td class="tw-w-16 tw-text-center">:</td>
              <td>{{ info.helper }}</td>
            </tr>
            <tr>
              <td>Tujuan</td>
              <td class="tw-w-10 tw-text-center">:</td>
              <td>{{ info.tujuan }}</td>
            </tr>
          </table>
          <table class="tw-w-[200px]">
            <tr>
              <td>KM Berangkat</td>
              <td class="tw-w-10 tw-text-center">:</td>
              <td>{{ info.km_berangkat }}</td>
            </tr>
            <tr>
              <td>KM Pulang</td>
              <td class="tw-w-16 tw-text-center">:</td>
              <td>{{ info.km_pulang }}</td>
            </tr>
            <tr>
              <td>KM Isi BBM</td>
              <td class="tw-w-16 tw-text-center">:</td>
              <td>{{ info.km_isi_bbm }}</td>
            </tr>
            <tr>
              <td>Isi BBM/Liter</td>
              <td class="tw-w-16 tw-text-center">:</td>
              <td>{{ info.isi_bbm_liter }}</td>
            </tr>
          </table>
        </div>
        <div
          class="tw-w-full tw-border-b tw-border-black tw-flex tw-justify-between tw-px-2">
          <span
            v-for="col in fieldCol"
            :key="col"
            :class="['tw-w-28 tw-h-6 tw-font-bold', index === 0 && 'tw-pl-2']">
            {{ col }}
          </span>
        </div>
        <div
          class="tw-w-full tw-border-b tw-border-black tw-flex tw-flex-col tw-h-32 tw-py-2 tw-gap-2">
          <div class="tw-w-full tw-flex tw-justify-between tw-px-2">
            <span class="tw-w-28 tw-h-[20px] tw-rounded-sm">
              Rp. {{ parseCurrency(i.nominal_parkir) }}
            </span>
            <span class="tw-w-28 tw-h-[20px] tw-rounded-sm">
              Rp. {{ parseCurrency(i.nominal_bongkar) }}
            </span>
            <span class="tw-w-28 tw-h-[20px] tw-rounded-sm">
              Rp. {{ parseCurrency(i.nominal_lainnya) }}
            </span>
            <span class="tw-w-28 tw-h-[20px] tw-rounded-sm">
              {{ i.keterangan }}
            </span>
            <span class="tw-w-28 tw-h-[20px] tw-rounded-sm">
              Rp.
              {{ parseCurrency(calcSubTotal(i)) }}
            </span>
          </div>
        </div>
        <div class="tw-w-full tw-flex tw-justify-end tw-text-[10px]">
          <table class="tw-w-[270px]">
            <tr>
              <td>Kasbon Harian</td>
              <td class="tw-w-4 tw-text-center">:</td>
              <td class="tw-w-44"></td>
            </tr>
            <tr>
              <td>Sisa Kasbon</td>
              <td class="tw-w-4 tw-text-center">:</td>
              <td class="tw-w-44"></td>
            </tr>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>
