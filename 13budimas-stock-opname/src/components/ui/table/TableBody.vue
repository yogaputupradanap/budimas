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
        'tw-cursor-pointer tw-duration-300 tw-ease-in-out tw-border-b tw-border-slate-300 tw-transition-colors hover:tw-bg-slate-500/20 data-[state=selected]:tw-bg-muted',
      ]"
      v-for="row in table.getRowModel().rows"
      :key="row.id"
    >
      <td
        :class="[
          'tw-p-4 tw-text-center tw-capitalize tw-relative tw-h-12  tw-align-middle tw-font-medium tw-text-muted-foreground [&:has([role=checkbox])]:tw-pr-0',
          classic && 'tw-border tw-border-[#8A8A8A]',
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
