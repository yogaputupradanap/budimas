<script setup>
import { ref, defineProps, defineEmits } from "vue";
import FlexBox from "../FlexBox.vue";
import Card from "../Card.vue";
import Button from "../Button.vue";
import Modal from "../Modal.vue";
import Image from "../Image.vue";

const props = defineProps([
  "groupId",
  "labelFor",
  "modelValue",
  "configProps",
  "label",
  "imageViewer",
  "webUrl",
  "webFilename",
]);

const updatModelValue = defineEmits(["update:modelValue"]);

const fileRef = ref(null);
const filename = ref(props.webFilename || "");
const modalRef = ref();
const imageUrl = ref(props.webUrl || "");

const clickFile = () => (fileRef?.value).click();
const onChangeFile = (event) => {
  const fileEl = event.target;

  if (!fileEl.files) return;

  const file = fileEl.files[0];
  const blobUrl = URL.createObjectURL(file);

  filename.value = file.name;
  imageUrl.value = blobUrl;

  updatModelValue("update:modelValue", file);
};

const open = () => modalRef.value.show();
const close = () => modalRef.value.hide();
</script>

<template>
  <BFormGroup
    class="tw-w-full tw-flex tw-flex-col tw-gap-2"
    :id="groupId"
    :label-for="labelFor"
    :label="label"
    v-bind="configProps">
    <input
      ref="fileRef"
      :id="labelFor"
      class="tw-hidden"
      type="file"
      @change="onChangeFile" />
    <div
      @click="clickFile"
      class="tw-w-full tw-h-10 focus:tw-outline focus:tw-outline-blue-500 tw-pl-0 tw-pr-4 tw-py-0 tw-justify-start tw-items-center tw-gap-4 tw-rounded-lg tw-border-2 tw-border-slate-400 tw-flex tw-cursor-pointer tw-group tw-transition-all tw-duration-300 tw-overflow-hidden">
      <div
        class="tw-bg-blue-500 tw-h-full tw-text-white tw-italic tw-transition-all tw-duration-300 tw-flex tw-px-8 tw-py-1 tw-justify-center tw-items-center group-hover:tw-bg-blue-700">
        Pilih
      </div>
      <span
        class="tw-text-gray-400 tw-italic group-hover:tw-text-gray-600 tw-transition-all tw-duration-300 tw-font-semibold tw-truncate">
        {{ filename || "Tolong Pilih File" }}
      </span>
    </div>
  </BFormGroup>
  <Button
    v-if="imageViewer && filename"
    variant="outline-primary"
    class="tw-px-6"
    :trigger="open">
    Lihat File
  </Button>
  <Modal
    v-if="imageViewer"
    ref="modalRef"
    id="modalRef"
    centered
    @modal-closed="">
    <FlexBox full flex-col no-left-padding>
      <FlexBox no-left-padding full class="tw-text-xl tw-font-bold">
        {{ filename }}
      </FlexBox>
      <Image :src="imageUrl" object-fit="contain" class="tw-w-full tw-h-full" />
      <FlexBox full jus-end no-left-padding>
        <Button variant="danger" :trigger="close" class="tw-px-6">Close</Button>
      </FlexBox>
    </FlexBox>
  </Modal>
</template>
