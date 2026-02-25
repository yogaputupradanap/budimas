import { createColumnHelper } from "@tanstack/vue-table";
import { h, ref } from "vue";
import RouterButton from "@/src/components/ui/RouterButton.vue";


const columnHelper = createColumnHelper();

const selectedRows = ref([]);

export const ListPajakColumn = [
    columnHelper.display({
        id: 'no',
        header: () => h('div', { class: 'tw-pl-3', innerText: 'No' }),
        cell: (info) => h('input', {
            type: 'checkbox',
            class: 'form-checkbox ms-2 ',
            checked: selectedRows.value.includes(info.row.index),
            onChange: (event) => {
                const index = info.row.index;
                if (event.target.checked) {
                    selectedRows.value.push(index);
                } else {
                    selectedRows.value = selectedRows.value.filter(i => i !== index);
                }
            }
        }),
    }),
    columnHelper.accessor((row) => row.nomor_faktur, {
        id: "nomor_faktur",
        header: "No Faktur",
        cell: (info) => h("div", {
            class: "table-cell-medium",
            innerText: info.getValue(),
        }),
    }),
    columnHelper.accessor((row) => row.principal, {
        id: "principal",
        header: "Principal",
        cell: (info) => h("div", {
            class: "table-cell-lg",
            innerText: info.getValue(),
        }),
    }),
    columnHelper.accessor((row) => row.tanggal, {
        id: "tanggal",
        header: "Tanggal Order",
        cell: (info) => h("div", {
            class: "table-cell-medium",
            innerText: info.getValue(),
        }),
    }),
    columnHelper.accessor((row) => row.customer, {
        id: "customer",
        header: "Customer",
        cell: (info) => h("div", {
            class: "table-cell-medium",
            innerText: info.getValue(),
        }),
    }),
    columnHelper.accessor((row) => row.npwp, {
        id: "npwp",
        header: "NPWP",
        cell: (info) => h("div", {
            class: "table-cell-medium",
            innerText: info.getValue(),
        }),
    }),
    columnHelper.accessor((row) => row.nilai_faktur, {
        id: "nilai_faktur",
        header: "Nilai Faktur",
        cell: (info) => h("div", {
            class: "table-cell-medium",
            innerText: info.getValue(),
        }),
    }),
    columnHelper.display({
        id: "actions",
        header: "Action",
        cell: (info) => {
            const id = info.row.original.nomor_faktur
            return h(
                RouterButton,
                {
                    to: `/list-pajak/detail-list-pajak`,
                    class: "tw-text-white tw-w-24 tw-py-2",
                },
                () => "Detail"
            );
        },
    }),
];
