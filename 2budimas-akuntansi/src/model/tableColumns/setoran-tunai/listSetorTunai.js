import { createColumnHelper } from "@tanstack/vue-table";
import { h } from "vue";
import RouterButton from "@/src/components/ui/RouterButton.vue";
import T from "@/src/components/ui/table/T.vue";
import TableInput from "@/src/components/ui/table/TableInput.vue";

const columnHelper = createColumnHelper();

export const listSetorTunaiColumn = [
  columnHelper.display({
    id: "no",
    header: h("div", { class: "tw-pl-3", innerText: 'No' }),
    cell: (info) => h(T, { innerText: info.row.index + 1 }),
  }),
  columnHelper.accessor((row) => row.no_faktur, {
    id: "no_faktur",
    header: h("div", { class: "tw-pl-4", innerText: "No. Faktur" }),
    cell: (info) =>
      h("div", {
        class: "table-cell-lg",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.accessor((row) => row.jatuh_tempo, {
    id: "jatuh_tempo",
    header: "Jatuh Tempo",
    cell: (info) =>
      h("div", {
        class: "table-cell-medium",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.accessor((row) => row.sales, {
    id: "sales",
    header: "Sales",
    cell: (info) =>
      h("div", {
        class: "table-cell-medium",
        innerText: info.getValue(),
      }),
  }),
  columnHelper.accessor((row) => row.tagihan, {
    id: "tagihan",
    header: "Tagihan",
    cell: (info) =>
      h("div", {
        class: "table-cell-medium",
        innerText: info.getValue(),
      }),
  }),
columnHelper.accessor("status_tagihan", {
    id: "setoran",
    header: () => h('div', { class: 'tw-pl-3', innerText: "Setoran" }),
    cell: (info) => {
        // Cek apakah data baris tersedia
        const rowData = info.row.original;
        if (!rowData) return h('div', "-");

        return h(T, () =>
            h(TableInput, {
                table: info.table,
                column: info.column.id,
                row: info.row.index,
                type: "number",
                // Tambahkan modelValue jika TableInput membutuhkannya agar tidak undefined
                modelValue: rowData.setoran_piutang ?? 0 
            })
        );
    },
}),
];
