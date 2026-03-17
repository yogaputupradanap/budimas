<script setup>
import Skeleton from "./Skeleton.vue";

const props = defineProps({
  label: String,
  loading: Boolean,
  value: String,
});
</script>

<template>
  <div class="tw-w-[25%]">
    <div>
      <p>{{ props?.label }}</p>
      <div
        class="tw-h-10 tw-w-full tw-font-medium tw-text-sm tw-bg-slate-300 tw-rounded-md tw-mt-2 tw-flex tw-items-center">
        <p v-if="!props.loading" :title="props.value" class="tw-ml-4">
          {{
            props?.value?.length > 25
              ? props?.value?.substring(0, 25) + " ...."
              : props?.value
          }}
        </p>
        <Skeleton v-else class="tw-w-full tw-h-10" />
      </div>
    </div>
  </div>
</template>
