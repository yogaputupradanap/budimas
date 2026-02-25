<script setup>
import { computed, reactive, ref, watch, watchEffect, defineProps } from "vue";

const props = defineProps({ table: null, totalData: null });
const currentPage = ref(props.table.getState().pagination.pageIndex + 1);
const totalPage = reactive({
  total: [...Array(props.table.getPageCount())].map(
    (_page, index) => index + 1
  ),
});

watch(props.table.getState(), () => {
  currentPage.value = props.table.getState().pagination.pageIndex + 1;
});

watchEffect(() => {
  totalPage.total = [...Array(props.table.getPageCount())].map(
    (_page, index) => index + 1
  );
});

const firstPage = computed(() => {
  const first = totalPage.total.length > 5 ? [...totalPage.total][0] : [];
  return first;
});

const middlePage = computed(() => {
  const middlePageArray = [...totalPage.total];
  middlePageArray.pop();
  const midddle =
    totalPage.total.length > 5
      ? middlePageArray.splice(
          currentPage.value > 4 ? currentPage.value - 2 : 1,
          4
        )
      : totalPage.total;
  return midddle;
});

const lastPage = computed(() => {
  const last = totalPage.total.length > 5 ? [...totalPage.total].slice(-1) : [];
  return last;
});
</script>

<template>
  <div
    class="tw-w-full tw-flex lg:tw-flex-row tw-flex-col tw-gap-4 lg:tw-justify-between tw-justify-start lg:tw-items-center tw-items-start tw-mt-4 tw-pb-8"
  >
    <div
      class="tw-flex lg:tw-gap-2 tw-gap-1 tw-select-none tw-text-xs tw-break-all lg:tw-flex-row tw-flex-col"
    >
      <span>Showing</span>
      <span>
        {{ table.getState().pagination.pageIndex + 1 }} to
        {{ table.getPageCount() }}
      </span>
      <span>of {{ table.getPageCount() }} entries</span>
      <span>{{ `( fiitered from ${totalData} total entries )` }}</span>
    </div>
    <div class="tw-flex tw-h-8">
      <button
        @click="() => table.previousPage()"
        :disabled="!table.getCanPreviousPage()"
        :class="
          !table.getCanPreviousPage()
            ? 'tw-text-gray-400 tw-border tw-border-gray-300 tw-px-2 tw-text-center'
            : 'tw-border tw-border-gray-300 tw-px-2 tw-text-center'
        "
      >
        Prev
      </button>
      <!-- <div class="tw-flex tw-gap-1">
        <button
          class="table-page-button"
          v-for="firstPg in firstPage"
          :key="firstPg"
          @click="table.setPageIndex(firstPg - 1)"
          :disabled="firstPg === table.getState().pagination.pageIndex + 1"
        >
          {{ firstPg }}
        </button>
        <button
          v-if="totalPage.total.length > 5 && currentPage > 3"
          class="table-page-button"
        >
          ...
        </button>
        <button
          v-for="page in middlePage"
          :key="page"
          class="table-page-button"
          :disabled="page === table.getState().pagination.pageIndex + 1"
          @click="table.setPageIndex(page - 1)"
        >
          {{ page }}
        </button>
        <button v-if="totalPage.total.length > 5" class="table-page-button">
          ...
        </button>
        <button
          class="table-page-button"
          v-for="last in lastPage"
          :key="last"
          @click="table.setPageIndex(last - 1)"
          :disabled="last === table.getState().pagination.pageIndex + 1"
        >
          {{ last }}
        </button>
      </div> -->
      <button
        @click="() => table.nextPage()"
        :disabled="!table.getCanNextPage()"
        :class="
          !table.getCanNextPage()
            ? 'tw-text-gray-400 tw-border tw-border-gray-300 tw-px-2 tw-text-center'
            : 'tw-border tw-border-gray-300 tw-px-2 tw-text-center'
        "
      >
        Next
      </button>
    </div>
  </div>
</template>
