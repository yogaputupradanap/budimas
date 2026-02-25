<script setup>
import SelectInput from "../formInput/SelectInput.vue";
import { defineProps, defineEmits } from "vue";

const props = defineProps(["table", "filter"]);
defineEmits(["update:modelValue"]);

const pageSizes = [
  { text: "5", value: 5 },
  { text: "10", value: 10 },
  { text: "20", value: 20 },
  { text: "30", value: 30 },
];
const handlePageSizeChange = (e) => {
  props.table.setPageSize(e);
};
</script>

<template>
  <div
    class="tw-w-full tw-flex lg:tw-flex-row tw-flex-col lg:tw-justify-between tw-justify-start lg:tw-items-center tw-items-start tw-gap-4"
  >
    <div class="tw-w-48 tw-h-8 tw-flex tw-gap-4 tw-items-center">
      <span>Show</span>
      <SelectInput
        :options="pageSizes"
        @change="handlePageSizeChange"
        :model-value="table.getState().pagination.pageSize"
      />
      <span>Entries</span>
    </div>
    <div class="lg:tw-w-96 tw-w-full tw-flex tw-items-center">
      <span class="tw-w-24 lg:tw-font-bold tw-font-normal tw-text-md">
        search
      </span>
      <BFormInput
        :model-value="filter"
        @input="$emit('update:modelValue', $event)"
        placeholder="Cari ..."
        size="sm"
      />
    </div>
  </div>
</template>
