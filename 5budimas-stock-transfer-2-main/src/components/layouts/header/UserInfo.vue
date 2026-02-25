<script setup>
import Skeleton from "../../ui/Skeleton.vue";

const props = defineProps({
  loading: Boolean,
  icon: String,
  userInfo: String,
});
</script>

<template>
  <div class="tw-flex tw-items-center tw-gap-2 tw-capitalize">
    <i :class="['mdi', icon]"></i>
    <Skeleton v-if="loading" class="tw-w-16 tw-h-4" />
    <span v-else>{{ userInfo }}</span>
  </div>
</template>
