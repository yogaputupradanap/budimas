<script setup>
import { FlexRender } from "@tanstack/vue-table";
import { defineProps } from "vue";
defineProps({ table: null, classic: null});
</script>

<template>
  <tbody
    :class="[
      'tw-text-[0.775rem]',
      !classic && '[&_tr:last-child]:tw-border-0',
    ]">
    <tr
      :class="[
        'tw-cursor-pointer tw-duration-300 tw-ease-in-out tw-border-b tw-border-slate-300 tw-transition-colors hover:tw-bg-slate-500/20 data-[state=selected]:tw-bg-muted',
      ]"
      v-for="row in table.getRowModel().rows"
      :key="row.id">
      <td
        :class="[
          'tw-py-4 tw-capitalize tw-relative tw-h-12 tw-text-left tw-align-middle tw-font-medium tw-text-muted-foreground [&:has([role=checkbox])]:tw-pr-0',
          classic && 'tw-border-x tw-border-slate-300',
        ]"
        v-for="cell in row.getVisibleCells()"
        :key="cell.id">
        <FlexRender
          :render="cell.column.columnDef.cell"
          :props="cell.getContext()" />
      </td>
    </tr>
  </tbody>
</template>
