<script setup>
import { computed, onMounted, ref, watch } from "vue";

const props = defineProps({
  table: Object,
  row: Number,
  column: String,
  initialValue: Number,
  // Data konversi
  konversi1: { type: Number, default: 1 }, // pieces
  konversi2: { type: Number, default: 1 }, // box
  konversi3: { type: Number, default: 1 }, // karton
  // Nilai awal
  totalKarton: { type: Number, default: 0 },
  totalBox: { type: Number, default: 0 },
  totalPieces: { type: Number, default: 0 },
});

// Input values
const uom1Value = ref(0); // Pieces
const uom2Value = ref(0); // Box
const uom3Value = ref(0); // Karton
const realisasiTotal = ref(0);

// Mengatur nilai input saat komponen dimuat
onMounted(() => {
  uom3Value.value = props.totalKarton || 0;
  uom2Value.value = props.totalBox || 0;
  uom1Value.value = props.totalPieces || 0;

  // Set nilai awal realisasi
  calculateTotal();
});

// Hitung total dalam pieces (realisasi)
const calculateTotal = () => {
  // Konversi ke pieces
  const piecesFromKarton = uom3Value.value * props.konversi3;
  const piecesFromBox = uom2Value.value * props.konversi2;
  const pieces = uom1Value.value * props.konversi1;

  // Total pieces
  realisasiTotal.value = piecesFromKarton + piecesFromBox + pieces;

  // Update nilai di tabel
  updateTableValue();
};

// Update nilai di tabel
const updateTableValue = () => {
  props.table.options.meta?.updateRow(
    realisasiTotal.value,
    props.row,
    props.column,
    "change"
  );
};

// Pantau perubahan pada input
watch([uom1Value, uom2Value, uom3Value], () => {
  calculateTotal();
});

// Format angka untuk tampilan
const formattedTotal = computed(() => {
  return realisasiTotal.value.toString();
});
</script>

<template>
  <div class="tw-w-full tw-px-2 tw-py-2">
    <!-- Layout sejajar -->
    <div class="tw-flex tw-items-center tw-gap-2">
      <!-- Input untuk Karton -->
      <div class="tw-flex tw-flex-col tw-items-center">
        <label class="tw-text-xs tw-text-gray-600 tw-font-medium tw-mb-1">Karton</label>
        <input
          v-model.number="uom3Value"
          type="number"
          min="0"
          class="[appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none tw-w-20 tw-h-8 tw-border tw-border-slate-400 tw-rounded-md focus:tw-outline-none focus:tw-border-2 focus:tw-border-indigo-500 tw-px-2 tw-text-center" />
      </div>

      <!-- Input untuk Box -->
      <div class="tw-flex tw-flex-col tw-items-center">
        <label class="tw-text-xs tw-text-gray-600 tw-font-medium tw-mb-1">Box</label>
        <input
          v-model.number="uom2Value"
          type="number"
          min="0"
          class="[appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none tw-w-20 tw-h-8 tw-border tw-border-slate-400 tw-rounded-md focus:tw-outline-none focus:tw-border-2 focus:tw-border-indigo-500 tw-px-2 tw-text-center" />
      </div>

      <!-- Input untuk Pieces -->
      <div class="tw-flex tw-flex-col tw-items-center">
        <label class="tw-text-xs tw-text-gray-600 tw-font-medium tw-mb-1">Pieces</label>
        <input
          v-model.number="uom1Value"
          type="number"
          min="0"
          class="[appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none tw-w-20 tw-h-8 tw-border tw-border-slate-400 tw-rounded-md focus:tw-outline-none focus:tw-border-2 focus:tw-border-indigo-500 tw-px-2 tw-text-center" />
      </div>

      <!-- Total Realisasi di sebelah kanan -->
      <div class="tw-flex tw-flex-col tw-items-start tw-ml-2">
        <label class="tw-text-xs tw-text-gray-600 tw-font-medium tw-mb-1">Total</label>
        <div class="tw-h-8 tw-flex tw-items-center tw-text-base tw-font-medium tw-text-blue-700">
          {{ formattedTotal }} <span class="tw-text-sm tw-text-gray-600 tw-ml-1">pcs</span>
        </div>
      </div>
    </div>
  </div>
</template>