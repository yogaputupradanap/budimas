<script setup>
import { FlexRender } from "@tanstack/vue-table";
import { defineProps, computed } from "vue";
import Loader from "../Loader.vue";

const props = defineProps({ table: null, classic: null, server: Boolean, loading: Boolean });

const hasFooterContent = computed(() => {
  if (!props.table) return false;
  return props.table.getFooterGroups().some(group => 
    group.headers.some(header => header.column.columnDef.footer)
  );
});

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
  <tfoot v-if="hasFooterContent" class="tw-bg-gray-100 tw-font-medium">
    <tr
      v-for="footerGroup in table.getFooterGroups()"
      :key="footerGroup.id"
      class="tw-border-t tw-border-slate-300"
    >
      <th
        v-for="header in footerGroup.headers"
        :key="header.id"
        :colSpan="header.colSpan"
        class="tw-pt-1.5 tw-pb-1"
      >
        <FlexRender
          v-if="!header.isPlaceholder"
          :render="header.column.columnDef.footer"
          :props="header.getContext()"
        />
      </th>
    </tr>
  </tfoot>
</template>
