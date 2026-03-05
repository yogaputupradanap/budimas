<script setup>
import { onMounted, ref, watch } from "vue";
import { defineProps } from "vue";

const props = defineProps([
  "column",
  "initialValue",
  "row",
  "table",
  "type",
  "placeholder",
  "id",
]);

const textValue = ref("");

// Fungsi untuk mendapatkan nilai dari data baris saat ini
const getCurrentValue = () => {
  // Pastikan table dan row tersedia
  if (!props.table || props.row === undefined) return props.initialValue || "";

  try {
    // Cari data asli dari baris saat ini
    const allRows = props.table.getPrePaginationRowModel().rows;
    if (!allRows || !allRows[props.row]) return props.initialValue || "";

    const rowData = allRows[props.row].original;
    // Jika nilai sudah ada di data baris, gunakan itu
    return rowData[props.column] !== undefined
      ? rowData[props.column]
      : props.initialValue || "";
  } catch (error) {
    console.error("Error getting current value:", error);
    return props.initialValue || "";
  }
};

const onBlur = () => {
  props.table.options.meta?.updateRow(
    textValue.value,
    props.row,
    props.column,
    "change"
  );
};

// Inisialisasi nilai saat komponen di-mount
onMounted(() => {
  textValue.value = getCurrentValue();
});

// Memantau perubahan pada props.row atau props.table untuk memperbarui nilai
watch([() => props.row, () => props.table], () => {
  const currentValue = getCurrentValue();
  if (currentValue !== textValue.value) {
    textValue.value = currentValue;
  }
});
</script>

<template>
  <input
    :id="id"
    v-model="textValue"
    @blur="onBlur"
    :type="type ? type : 'text'"
    class="[appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none tw-w-32 tw-h-8 tw-border tw-border-slate-400 tw-rounded-md focus:tw-outline-none focus:tw-border-2 focus:tw-border-slate-500 tw-px-2"
    :placeholder="placeholder ? placeholder : ''" />
</template>
