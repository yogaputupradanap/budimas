<script setup>
import { computed, ref, watch, defineProps } from "vue";

const props = defineProps({
  table: { type: Object, required: true },
  totalData: { type: Number, required: true },
});

const currentPage = ref(props.table.getState().pagination.pageIndex + 1);
const totalPageCount = ref(props.table.getPageCount());

// Watch the table's state to keep currentPage and totalPageCount updated
watch(
  () => props.table.getState().pagination,
  (pagination) => {
    currentPage.value = pagination.pageIndex + 1;
    totalPageCount.value = props.table.getPageCount();
  },
  { immediate: true }
);

// Generate pages to display based on currentPage and totalPageCount
const visiblePages = computed(() => {
  const total = totalPageCount.value;
  if (total <= 5) return Array.from({ length: total }, (_, i) => i + 1);

  const pages = [];
  const startPage = Math.max(2, currentPage.value - 1);
  const endPage = Math.min(total - 1, currentPage.value + 1);

  if (currentPage.value > 3) pages.push("...");
  for (let i = startPage; i <= endPage; i++) pages.push(i);
  if (currentPage.value < total - 2) pages.push("...");

  return [1, ...pages, total];
});
</script>

<template>
  <div
    class="tw-w-full tw-flex lg:tw-flex-row tw-flex-col tw-gap-4 lg:tw-justify-between tw-justify-start lg:tw-items-center tw-items-start tw-mt-4 tw-pb-8">
    <!-- Information about the current page and total data -->
    <p class="tw-text-xs">
      Menampilkan {{ currentPage }} dari {{ totalPageCount }} halaman
      (tersaring dari {{ totalData }} total data)
    </p>

    <!-- Pagination buttons -->
    <div class="tw-flex tw-gap-1 tw-h-8">
      <button
        @click="props.table.previousPage"
        :disabled="!props.table.getCanPreviousPage()"
        class="table-page-button">
        <i class="mdi mdi-chevron-left tw-text-lg"></i>
      </button>

      <div class="tw-hidden lg:tw-flex tw-gap-1 ">
        <button
          v-for="page in visiblePages"
          :key="page"
          @click="() => page !== '...' && props.table.setPageIndex(page - 1)"
          :disabled="page === currentPage"
          class="table-page-button">
          {{ typeof page === 'number' ? page : '...' }}
        </button>
      </div>

      <button
        @click="props.table.nextPage"
        :disabled="!props.table.getCanNextPage()"
        class="table-page-button">
        <i class="mdi mdi-chevron-right tw-text-lg"></i>
      </button>
    </div>
  </div>
</template>