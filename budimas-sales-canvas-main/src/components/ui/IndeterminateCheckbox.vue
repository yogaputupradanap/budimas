<script setup>
import { toRefs, ref } from "vue";

const props = defineProps({
  indeterminate: Boolean
});

const inputRef = ref(null)
const { indeterminate } = toRefs(props)
</script>

<template>
  <input
    type="checkbox"
    ref="inputRef"
    class="tw-cursor-pointer tw-w-4 tw-h-4 tw-bg-sky-100"
    :indeterminate="indeterminate"
    v-bind="$attrs"
    />
</template>
