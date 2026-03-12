<script setup>
import { FlexRender } from "@tanstack/vue-table";
import { defineProps } from "vue";
import Loader from "../Loader.vue";

defineProps({ table: null, classic: null, server: Boolean, loading: Boolean });
</script>

<template>
  <tbody
    :class="[
      'tw-text-[0.775rem]',
      !classic && '[&_tr:last-child]:tw-border-0',
      server && loading && 'tw-relative',
    ]"
  >
    <tr
      :class="[
        'even:tw-bg-stone-100 tw-cursor-pointer tw-duration-300 tw-ease-in-out tw-border-b tw-border-slate-200 tw-transition-colors hover:tw-bg-sky-500/5 data-[state=selected]:tw-bg-muted',
      ]"
      v-for="row in table.getRowModel().rows"
      :key="row.id"
    >
      <td
        :class="[
          'tw-py-2 tw-capitalize tw-relative tw-text-left tw-align-middle tw-font-medium tw-text-muted-foreground [&:has([role=checkbox])]:tw-pr-0',
          classic && 'tw-border-x tw-border-slate-300',
        ]"
        v-for="cell in row.getVisibleCells()"
        :key="cell.id"
      >
        <FlexRender
          :render="cell.column.columnDef.cell"
          :props="cell.getContext()"
        />
      </td>
    </tr>
    <div
      v-if="server && loading"
      class="tw-w-full tw-h-full tw-absolute tw-top-0 tw-bg-white/80 tw-flex tw-justify-center tw-items-center tw-z-40"
    >
      <Loader />
    </div>
  </tbody>
</template>
