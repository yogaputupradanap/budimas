<script setup>
import { FlexRender } from "@tanstack/vue-table";
import { defineProps } from "vue";

defineProps({ table: null, classic: null });
</script>

<template>
  <thead class="[&_tr]:tw-border tw-border-slate-300 tw-text-xs">
    <tr
      class="tw-shadow-sm tw-bg-slate-100"
      v-for="headerGroup in table?.getHeaderGroups()"
      :key="headerGroup?.id"
    >
      <th
        v-for="header in headerGroup?.headers"
        :key="header?.id"
        :colSpan="header?.colSpan"
        :class="[
          'tw-capitalize tw-py-3 tw-relative tw-text-center',
          header?.column?.getCanSort()
            ? 'tw-cursor-pointer tw-select-none'
            : '',
          classic && 'tw-text-bold tw-border-slate-300  tw-bg-[#8A8A8A] ',
        ]"
        @click="header?.column?.getToggleSortingHandler()?.($event)"
      >
        <template v-if="!header?.isPlaceholder">
          <div
            class="tw-w-full tw-flex tw-justify-center tw-items-center tw-gap-4"
          >
            <FlexRender
              :render="header?.column?.columnDef?.header"
              :props="header?.getContext()"
            />
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
