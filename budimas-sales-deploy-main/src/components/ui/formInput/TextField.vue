<script setup>
import { parseCurrency } from "@/src/lib/utils";
import { defineProps, defineModel } from "vue";
import { parseNumberFromCurrency } from "../../../lib/utils";

const props = defineProps([
  "groupId",
  "labelFor",
  "configProps",
  "placeholder",
  "label",
  "type",
  "disable",
  "precision",
]);
const model = defineModel();

/**
 * format plain number value to currency value
 * @param {string} value
 * @returns {string}
 */
const formatNumber = (value) => {
  if (props.type == "currency" && typeof value === "string") {
    const toValueNumber = parseNumberFromCurrency(value, {
      precision: props.precision,
    });
    const currencyValue = parseCurrency(toValueNumber);
    return isNaN(toValueNumber) ? "" : currencyValue;
  }
};
</script>

<template>
  <BFormGroup
    :label-for="labelFor"
    :id="groupId"
    :label="label"
    class="tw-relative"
    v-bind="configProps">
    <BFormInput
      v-if="type === 'currency'"
      :formatter="formatNumber"
      inputmode="numeric"
      v-model="model"
      :placeholder="placeholder"
      :id="labelFor" />
    <input
      v-else
      :disabled="disable"
      v-model="model"
      :type="type"
      :id="labelFor"
      :placeholder="placeholder"
      :class="[
        'tw-w-full tw-h-11 tw-p-4 tw-border tw-border-gray-400 tw-rounded-md placeholder:tw-italic tw-outline-none focus:tw-outline-4 focus:tw-outline-blue-300 focus:tw-border-blue-200 placeholder:tw-text-gray-500 placeholder:tw-font-extralight',
        disable && 'tw-bg-gray-100',
      ]" />
  </BFormGroup>
</template>
