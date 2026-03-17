<script setup>
import SelectInput from "../formInput/SelectInput.vue";
import { defineProps, defineEmits, ref, onMounted } from "vue";
import { debounce } from "../../../lib/debounce";

const props = defineProps({
  table: null,
  server: Boolean,
  filter: null,
});

defineEmits(["update:modelValue"]);
const textinput = ref(null);

const pageSizes = [
  { text: "5", value: 5 },
  { text: "10", value: 10 },
  { text: "20", value: 20 },
  { text: "30", value: 30 },
];

const handlePageSizeChange = (e) => {
  props.table.setPageSize(e);
};

const setFilterValue = debounce((e) => {
  const allColumns = props.table.getAllColumns();
  const columns = allColumns.map((col) => `"${col.id}"`).slice(1);
  const text = e.target.value;

  const filterValue = { text, columns };
  props.table.setGlobalFilter(filterValue);
  props.table.resetPageIndex();
}, 1000);

onMounted(() => {
  if (props.server) {
    const textLength =
      props.filter.value.text.length || !props.filter.value.text.length;
    textLength && props.filter.state === "typing" && textinput.value.focus();
  }
});
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
    <div class="lg:tw-w-auto tw-w-full tw-flex tw-items-center">
      <span
        :class="[
          'lg:tw-font-bold tw-font-normal tw-text-m tw-w-24'
        ]"
      >
        search
      </span>
      <input
        v-if="server"
        class="filter-table-input"
        ref="textinput"
        :value="filter.value.text"
        placeholder="Cari ..."
        @keydown.esc="textinput.blur()"
        @input="(event) => setFilterValue(event)"
      />
      <BFormInput
        v-else
        :model-value="filter"
        @input="$emit('update:modelValue', $event)"
        placeholder="Cari ..."
        size="sm"
      />
    </div>
  </div>
</template>
