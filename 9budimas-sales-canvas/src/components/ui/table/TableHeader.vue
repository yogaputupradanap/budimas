<script setup>
import { FlexRender } from "@tanstack/vue-table";
import { defineProps } from "vue";

defineProps({ table: null, classic: null });
</script>

<template>
  <thead class="tw-text-xs tw-sticky tw-top-0 tw-z-10 tw-bg-white">
    <tr
      class="tw-shadow-md tw-shadow-black/5"
      v-for="headerGroup in table?.getHeaderGroups()"
      :key="headerGroup?.id">
      <th
        v-for="header in headerGroup?.headers"
        :key="header?.id"
        :colSpan="header?.colSpan"
        :class="[
          'tw-capitalize tw-py-4 tw-relative tw-text-center ',
          header?.column?.getCanSort() ? 'tw-cursor-pointer tw-select-none' : '',
          classic && 'tw-border-r tw-border-slate-300',
        ]"
        @click="header?.column?.getToggleSortingHandler()?.($event)">
        <template v-if="!header?.isPlaceholder">
          <div class="tw-w-full tw-flex tw-justify-start tw-items-center tw-gap-4">
            <FlexRender
              :render="header?.column?.columnDef?.header"
              :props="header?.getContext()" />
            <span v-if="header?.column?.getIsSorted() == 'desc'">
              <i class="mdi mdi-arrow-down tw-text-[1rem]"></i>
            </span>
            <span v-if="header?.column?.getIsSorted() == 'asc'" class="">
              <i class="mdi mdi-arrow-up tw-text-[1rem]"></i>
            </span>
          </div>
        </template>
      </th>
    </tr>
  </thead>
</template>
