<script setup>
import { ref } from "vue";
import { defineProps, defineEmits } from "vue";
defineProps([
  "groupId",
  "labelFor",
  "modelValue",
  "configProps",
  "placeholder",
]);

const model = defineModel()
const showPassword = ref(false);
</script>

<template>
  <BFormGroup
    :id="groupId"
    label="Password*"
    :label-for="labelFor"
    v-bind="configProps"
  >
    <div class="tw-w-full tw-relative">
      <i
        @click="showPassword = false"
        v-if="showPassword"
        class="mdi mdi-eye tw-text-2xl tw-absolute tw-top-2 tw-right-3 tw-z-50 tw-cursor-pointer"
      ></i>
      <i
        @click="showPassword = true"
        v-if="!showPassword"
        class="mdi mdi-eye-off tw-text-2xl tw-absolute tw-top-2 tw-right-3 tw-z-50 tw-cursor-pointer"
      ></i>
      <input
        :type="showPassword ? 'text' : 'password'"
        :id="labelFor"
        :placeholder="placeholder"
        :value="modelValue"
        class="tw-w-full tw-h-12 tw-p-4 tw-border tw-border-gray-400 tw-rounded-md placeholder:tw-italic tw-outline-none focus:tw-outline-4 focus:tw-outline-blue-300 focus:tw-border-blue-200 placeholder:tw-text-gray-500 placeholder:tw-font-extralight"
        v-model="model"
      />
    </div>
  </BFormGroup>
</template>
