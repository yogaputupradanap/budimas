<!-- eslint-disable vue/multi-word-component-names -->
<script setup>
import { useModal } from "bootstrap-vue-next";
import { ref, watch, defineProps, defineEmits, defineExpose } from "vue";

const props = defineProps(["id", "centered"]);
const programmaticModal = ref(false);
const emits = defineEmits(["modalClosed"]);

const { show, hide } = useModal(props.id);

defineExpose({
  show,
  hide,
});

watch(programmaticModal, () => {
  if (!programmaticModal.value) emits("modalClosed");
});
</script>

<template>
  <BModal hide-footer hide-header :centered="centered" :id="props.id" v-model="programmaticModal">
    <slot></slot>
  </BModal>
</template>
