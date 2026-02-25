import {createColumnHelper} from "@tanstack/vue-table";
import {h} from "vue";
import RouterButton from "@/src/components/ui/RouterButton.vue";
import Button from "@/src/components/ui/Button.vue";

const columnHelper = createColumnHelper();

export const listPreviewJurnalSetting = (handledelete) => [
    columnHelper.accessor((row) => row.row_num, {
        id: "no",
        header: "No",
        cell: (info) =>
            h("div", {
                class: "table-cell-lg",
                innerText: info.getValue(),
            }),
    }),
    columnHelper.accessor((row) => row.nama_mal, {
        id: "nama_mal",
        header: "Nama Jurnal Setting",
        cell: (info) => {
            return h("div", {
                class: "table-cell-lg ",
                innerText: info.getValue(),
            });
        },
    }),
    columnHelper.accessor((row) => row.action, {
        id: "action",
        header: "Action",
        cell: (info) => {
            return h(
                "div",
                {class: "tw-flex tw-gap-2"}, // flex biar rapi
                [
                    h(RouterButton, {
                        class: "tw-bg-blue-500 tw-text-white tw-px-3 tw-py-1 tw-rounded",
                        icon: "mdi mdi-pencil",
                        to: `/journal-setting/edit/${info.row.original.id_jurnal_mal}`,
                    }),
                    h(Button, {
                        class: "tw-bg-red-500 tw-text-white tw-px-3 tw-py-1 tw-rounded",
                        icon: "mdi mdi-trash-can-outline",
                        trigger: () => handledelete(info.row.original),
                    }),
                ]
            )
        },
    }),

];

export const listSumberData = [
    columnHelper.accessor((row) => row.no, {
        id: "no",
        header: "No",
        cell: (info) =>
            h("div", {
                class: "table-cell-lg",
                innerText: info.row.index + 1,
            }),
    }),
    columnHelper.accessor((row) => row.nama_kolom_view, {
        id: "nama_kolom_view",
        header: "Nama Kolom View",
        cell: (info) => {
            return h("div", {
                class: "table-cell-lg ",
                innerText: info.getValue(),
            });
        },
    }),
    columnHelper.accessor(row => row.nama_mal_list, {
        id: "nama_mal_list",
        header: "Jurnal Setting",
        cell: ({getValue}) => {
            const list = getValue();
            if (!Array.isArray(list) || list.length === 0) {
                return <span class="tw-text-gray-400 tw-italic">Tidak ada</span>;
            }

            return (
                <ul class="tw-list-disc tw-list-inside tw-space-y-1">
                    {list.map((item, i) => (
                        <li key={i} class="tw-text-gray-800 ">
                            {item}
                        </li>
                    ))}
                </ul>
            );
        },
    })
];