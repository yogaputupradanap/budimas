<script setup>
import { defineProps, defineModel } from "vue";

defineProps([
  "groupId",
  "labelFor",
  "configProps",
  "placeholder",
  "label",
  "type",
  "disable",
]);
const model = defineModel();
</script>

<template>
  <BFormGroup
    :label-for="labelFor"
    :id="groupId"
    :label="label"
    class="tw-relative"
    v-bind="configProps"
  >
    <input
      :disabled="disable"
      v-model="model"
      :type="type"
      :id="labelFor"
      :placeholder="placeholder"
      :class="[
        'tw-w-full tw-h-11 tw-p-4 tw-border tw-border-gray-400 tw-rounded-md placeholder:tw-italic tw-outline-none focus:tw-outline-4 focus:tw-outline-blue-300 focus:tw-border-blue-200 placeholder:tw-text-gray-500 placeholder:tw-font-extralight',
        disable && 'tw-bg-gray-100',
      ]"
    />
  </BFormGroup>
</template>
