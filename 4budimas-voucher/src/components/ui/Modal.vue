<script setup>
import { useModal } from "bootstrap-vue-next";
import { ref, watch, defineProps, defineEmits, defineExpose } from "vue";

// Define props and destructure them
const props = defineProps(["id", "centered"]);
const { id, centered } = props;

const programmaticModal = ref(false);
const emits = defineEmits(["modalClosed"]);

// UseModal hooks
const { show, hide } = useModal(id);

defineExpose({
  show,
  hide,
});

// Watch for changes to programmaticModal
watch(programmaticModal, (newValue) => {
  if (!newValue) {
    emits("modalClosed");
  }
});
</script>

<template>
  <BModal 
    hide-footer 
    hide-header 
    :centered="centered" 
    :id="id" 
    v-model="programmaticModal"
  >
    <slot></slot>
  </BModal>
</template>
