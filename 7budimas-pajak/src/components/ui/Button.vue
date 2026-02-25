<script setup>
import { ref, defineProps } from "vue";
import { useRouter } from "vue-router";
import { useAlert } from "@/src/store/alert";

const props = defineProps({
  loading: Boolean,
  disabled: Boolean,
  fallbackUrl: String,
  trigger: Function,
  loadingMode: String,
  icon: String
});
const buttonLoading = ref(props.loading || false);

const router = useRouter();
const alert = useAlert();

const change = async () => {
  try {
    buttonLoading.value = true;
    await props.trigger();
    if (props.fallbackUrl) router.push(props.fallbackUrl);
  } catch (error) {
    alert.setMessage(error.message, "danger");
  } finally {
    buttonLoading.value = false;
  }
};
</script>

<template>
  <BButton
    size="sm"
    @click="change"
    :disabled="disabled"
    :class="['tw-flex tw-border-none tw-rounded-sm te-text-white tw-capitalize', icon && 'tw-gap-1']">
    <i :class="[icon]" v-if="icon && !buttonLoading"></i>
    <slot v-if="!buttonLoading"></slot>
    <div
      v-if="buttonLoading"
      class="tw-flex tw-items-center tw-justify-center tw-gap-2">
      <BSpinner small />
      <span v-if="loadingMode !== 'icon'">loading</span>
    </div>
  </BButton>
</template>
