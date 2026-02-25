<script setup>
import { ref, defineProps, defineEmits } from "vue";

defineProps(["groupId", "labelFor", "modelValue", "configProps", "label"]);

const updatModelValue = defineEmits(["update:modelValue"]);

const fileRef = ref(null);
const filename = ref("");

const clickFile = () => (fileRef?.value).click();
const onChangeFile = (event) => {
  const fileEl = event.target;

  if (!fileEl.files) return;

  const file = fileEl.files[0];
  filename.value = file.name;
  updatModelValue("update:modelValue", file);
};
</script>

<template>
  <BFormGroup
    :id="groupId"
    :label-for="labelFor"
    :label="label"
    v-bind="configProps"
  >
    <input
      ref="fileRef"
      :id="labelFor"
      class="tw-hidden"
      type="file"
      @change="onChangeFile"
    />
    <div
      @click="clickFile"
      class="tw-w-full tw-h-10 focus:tw-outline focus:tw-outline-blue-500 tw-pl-0 tw-pr-4 tw-py-0 tw-justify-start tw-items-center tw-gap-4 tw-rounded-lg tw-border-2 tw-border-slate-400 tw-flex tw-cursor-pointer tw-group tw-transition-all tw-duration-300 tw-overflow-hidden"
    >
      <div
        class="tw-bg-blue-500 tw-h-full tw-text-white tw-italic tw-transition-all tw-duration-300 tw-flex tw-px-8 tw-py-1 tw-justify-center tw-items-center group-hover:tw-bg-blue-700"
      >
        Pilih
      </div>
      <span
        class="tw-text-gray-400 tw-italic group-hover:tw-text-gray-600 tw-transition-all tw-duration-300 tw-font-semibold"
      >
        {{ !filename.length ? "Tolong Pilih File" : filename.length > 32 ? filename.substring(0,32) + ' ......' : filename }}
      </span>
    </div>
  </BFormGroup>
</template>
