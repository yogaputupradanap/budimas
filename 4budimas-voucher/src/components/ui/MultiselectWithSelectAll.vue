<script setup>
import { computed, watchEffect } from "vue";
import Multiselect from "vue-multiselect";

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => [],
  },
  options: {
    type: Array,
    default: () => [],
  },
  label: {
    type: String,
    default: "nama",
  },
  trackBy: {
    type: String,
    default: "id",
  },
  placeholder: {
    type: String,
    default: "Pilih Data",
  },
  loading: {
    type: Boolean,
    default: false,
  },
  preselectFirst: {
    type: Boolean,
    default: true,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["update:modelValue"]);

// Pastikan nilai default untuk value adalah array kosong agar tidak undefined
const value = computed({
  get: () => props.modelValue || [],
  set: (val) => emit("update:modelValue", val),
});

function selectAll() {
  // Pastikan options tidak undefined sebelum menjalankan operasi
  if (!props.options || !Array.isArray(props.options)) return;

  if (allSelected.value) {
    // Jika semua sudah dipilih, kosongkan semua
    emit("update:modelValue", []);
  } else {
    // Jika belum semua dipilih, pilih semua
    emit("update:modelValue", [...props.options]);
  }
}

const allSelected = computed(() => {
  // Pastikan options dan modelValue bukan undefined
  const options = props.options || [];
  const modelValue = props.modelValue || [];

  return options.length > 0 && modelValue.length === options.length;
});

const buttonText = computed(() => {
  return allSelected.value ? "Batal Pilih Semua" : "Pilih Semua";
});

// Untuk debugging
watchEffect(() => {
  console.log("Options length:", props.options?.length || 0);
  console.log("Model value length:", props.modelValue?.length || 0);
});
</script>

<template>
  <Multiselect
    v-model="value"
    :options="options || []"
    :multiple="true"
    :close-on-select="false"
    :clear-on-select="false"
    :preserve-search="true"
    :placeholder="placeholder"
    :label="label"
    :track-by="trackBy"
    :preselect-first="preselectFirst"
    :loading="loading"
    :disabled="disabled">
    <template #selection="{ values, search, isOpen }">
      <span
        class="multiselect__single"
        v-if="values && values.length"
        v-show="!isOpen">
        {{ values.length }} opsi dipilih
      </span>
    </template>
    <template #beforeList>
      <div
        class="multiselect__option tw-cursor-pointer tw-font-medium tw-bg-gray-100 tw-py-2"
        @click="selectAll">
        {{ buttonText }}
      </div>
    </template>
  </Multiselect>
</template>
