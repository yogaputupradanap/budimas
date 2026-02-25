<script setup>
import { onMounted, ref } from "vue";
import { defineProps } from "vue";

const props = defineProps([
  "column",
  "initialValue",
  "row",
  "table",
  "type",
  "placeholder",
]);
const textValue = ref("");

const onBlur = () => {
  props.table.options.meta?.updateRow(
    textValue.value,
    props.row,
    props.column,
    "change"
  );
};

onMounted(() => {
  textValue.value = props.initialValue || "";
});
</script>

<template>
  <input
    v-model="textValue"
    @blur="onBlur"
    :type="type ? type : 'text'"
    class="[appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none tw-w-32 tw-h-8 tw-border tw-border-slate-400 tw-rounded-md focus:tw-outline-none focus:tw-border-2 focus:tw-border-slate-500 tw-px-2"
    :placeholder="placeholder ? placeholder : ''" />
</template>
