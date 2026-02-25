<script setup>
import { defineProps } from "vue";

defineProps(["informations"]);
</script>

<template>
  <div
    class="tw-w-full tw-flex tw-flex-col tw-gap-4 tw-p-8 tw-text-xs lg:tw-text-base"
  >
    <h4>Keterangan Warna pada tombol :</h4>
    <div class="tw-flex tw-flex-col tw-justify-center tw-gap-4">
      <div
        v-for="inform in informations"
        :key="inform.information"
        class="tw-flex tw-items-center lg:tw-gap-6 tw-gap-2"
      >
        <span
          :class="[
            'lg:tw-w-36 tw-w-16 tw-pt-[0.28rem] tw-pb-[0.28rem] tw-rounded-md tw-text-center lg:tw-text-sm tw-text-[0.6rem]',
            inform.buttonColor,
            inform?.buttonTextColor || 'tw-text-black',
          ]"
        >
          {{ inform.buttonText }}
        </span>
        <span>=</span>
        <span>
          {{ inform.information }}
        </span>
      </div>
    </div>
  </div>
</template>
