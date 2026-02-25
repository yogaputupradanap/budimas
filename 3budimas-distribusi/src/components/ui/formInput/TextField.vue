<script setup>
import { parseCurrency } from "@/src/lib/utils";
import { defineProps, defineModel } from "vue";
import { parseNumberFromCurrency } from "../../../lib/utils";
import { BFormInput } from "bootstrap-vue-next";

const props = defineProps([
  "groupId",
  "labelFor",
  "configProps",
  "placeholder",
  "label",
  "type",
  "disable",
]);
const model = defineModel();

/**
 * format plain number value to currency value
 * @param {string} value
 * @returns {string}
 */
const formatNumber = (value) => {
  if (props.type == "currency" && typeof value === "string") {
    const toValueNumber = parseNumberFromCurrency(value);
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
    class="tw-relative tw-w-full"
    v-bind="configProps">
    <BFormInput
      v-if="type === 'currency'"
      :formatter="formatNumber"
      inputmode="numeric"
      v-model="model"
      :placeholder="placeholder"
      :id="labelFor" />
    <BFormInput
      v-else
      :disabled="disable"
      v-model="model"
      :type="type"
      :id="labelFor"
      :placeholder="placeholder"
      :class="[disable && 'tw-bg-gray-100']" />
  </BFormGroup>
</template>