<script setup>
import { BButton } from "bootstrap-vue-next";
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
    class="tw-w-full tw-flex lg:tw-flex-row tw-flex-col tw-gap-4 lg:tw-justify-between tw-justify-start lg:tw-items-center tw-items-start tw-mt-4 tw-pb-8">
    <div
      class="tw-flex lg:tw-gap-2 tw-gap-1 tw-select-none tw-text-xs tw-break-all lg:tw-flex-row tw-flex-col">
      <span>Menampilkan</span>
      <span>
        {{ table.getState().pagination.pageIndex + 1 }} dari
        {{ table.getPageCount() }}
      </span>
      <span>halaman</span>
      <span>{{ `( tersaring dari ${totalData} total data )` }}</span>
    </div>
    <div class="tw-flex tw-gap-4 tw-h-8">
      <BButton
        squared
        @click="() => table.previousPage()"
        :disabled="!table.getCanPreviousPage()"
        class="tw-bg-blue-500 tw-w-10 tw-border-none tw-text-xl"
        variant="primary">
        &lsaquo;
      </BButton>
      <div class="tw-flex tw-gap-2">
        <BButton
          squared
          class="tw-bg-blue-500 tw-text-white tw-w-10"
          v-for="firstPg in firstPage"
          :key="firstPg"
          @click="table.setPageIndex(firstPg - 1)"
          :disabled="firstPg === table.getState().pagination.pageIndex + 1">
          {{ firstPg }}
        </BButton>
        <div
          v-if="totalPage.total.length > 5 && currentPage > 3"
          class="tw-text-blue-600 tw-text-2xl">
          ...
        </div>
        <BButton
          size="sm"
          squared
          v-for="page in middlePage"
          :key="page"
          class="tw-bg-blue-500 tw-text-white tw-w-10 tw-text-xs"
          :disabled="page === table.getState().pagination.pageIndex + 1"
          @click="table.setPageIndex(page - 1)">
          {{ page }}
        </BButton>
        <div
          v-if="totalPage.total.length > 5"
          class="tw-text-blue-600 tw-text-2xl">
          ...
        </div>
        <BButton
          squared
          class="tw-bg-blue-500 tw-text-white tw-w-10"
          v-for="last in lastPage"
          :key="last"
          @click="table.setPageIndex(last - 1)"
          :disabled="last === table.getState().pagination.pageIndex + 1">
          {{ last }}
        </BButton>
      </div>
      <BButton
        squared
        @click="() => table.nextPage()"
        :disabled="!table.getCanNextPage()"
        class="tw-bg-blue-500 tw-w-10 tw-border-none tw-text-xl"
        variant="primary">
        &rsaquo;
      </BButton>
    </div>
  </div>
</template>
