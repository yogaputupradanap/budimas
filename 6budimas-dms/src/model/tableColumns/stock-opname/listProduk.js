import { createColumnHelper } from "@tanstack/vue-table";
import { BFormInput } from "bootstrap-vue-next";
import { h, ref, watch } from "vue";

const columnHelper = createColumnHelper();
export const listProdukColumns = (data) => [
    columnHelper.accessor((row) => "no", {
        id: "no",
        header: h("div", {
            class: "tw-pl-4 tw-w-20 md:tw-w-auto",
            innerText: "No",
        }),
        cell: (info) => h("div", { class: "tw-text-base", innerText: info.row.index + 1 }),
    }),
    columnHelper.accessor((row) => row.nama_produk, {
        id: "produkas",
        header: "Produk",
        cell: (info) =>
            h("div", { class: "tw-w-52 tw-text-base md:tw-w-auto", innerText: info.getValue() }),
    }),
    columnHelper.display({
        id: "Jml. UOM 3as",
        header: "Jml. UOM 3",
        cell: (info) => {
            const uom3 = ref(0);
            watch(uom3,
                (newValue) => {
                    if (newValue == '') {
                        uom3.value = 0;
                    }
                    if (newValue >= 0) {
                        data[info.row.index].jumlah_uom_3 = Number(newValue);
                        data[info.row.index].stock = Number(data[info.row.index].jumlah_uom_1) * info.row.original.konversi_uom_1 + Number(data[info.row.index].jumlah_uom_2) * info.row.original.konversi_uom_2 + Number(data[info.row.index].jumlah_uom_3) * info.row.original.konversi_uom_3;
                        data[info.row.index].total = Number(data[info.row.index].stock) * info.row.original.harga_produk;
                    }

                })
            return <div class="tw-flex tw-text-center tw-justify-center">
                <label class="tw-text-center tw-text-[#01579B]" >
                    {info.row.original.label_uom_3}
                    <BFormInput class="tw-text-center" type="number" placeholder="" v-model={uom3.value} />
                </label></div>
        },
    }),
    columnHelper.display({
        id: "jml. UOM 2as",
        header: "Jml UOM 2",
        cell: (info) => {
            const uom2 = ref(0);
            watch(uom2,
                (newValue) => {
                    if (newValue >= 0) {
                        data[info.row.index].jumlah_uom_2 = Number(newValue);
                        data[info.row.index].stock = Number(data[info.row.index].jumlah_uom_1) * info.row.original.konversi_uom_1 + Number(data[info.row.index].jumlah_uom_2) * info.row.original.konversi_uom_2 + Number(data[info.row.index].jumlah_uom_3) * info.row.original.konversi_uom_3;
                        data[info.row.index].total = Number(data[info.row.index].stock) * info.row.original.harga_produk;
                    }
                })
            return <div class="tw-flex tw-text-[center!important] tw-items-[center!important] tw-justify-center">
                <label class="tw-text-center tw-text-[#01579B]">
                    {info.row.original.label_uom_2}

                    <BFormInput class="tw-text-center" type="number" v-model={uom2.value} placeholder="" />
                </label>
            </div>
        },
    }),
    columnHelper.display({
        id: "jml_UOM_1sa",
        header: "Jml. UOM 1",
        cell: (info) => {
            const uom1 = ref(0);
            watch(uom1,
                (newValue) => {
                    if (newValue >= 0) {
                        data[info.row.index].jumlah_uom_1 = Number(newValue);
                        data[info.row.index].stock = Number(data[info.row.index].jumlah_uom_1) * info.row.original.konversi_uom_1 + Number(data[info.row.index].jumlah_uom_2) * info.row.original.konversi_uom_2 + Number(data[info.row.index].jumlah_uom_3) * info.row.original.konversi_uom_3;
                        data[info.row.index].total = Number(data[info.row.index].stock) * info.row.original.harga_produk;
                    }
                })
            return <div class="tw-flex tw-justify-center">
                <label class="tw-text-center tw-text-[#01579B]">
                    {info.row.original.label_uom_1}
                    <BFormInput class="tw-text-center" type="number" placeholder="" v-model={uom1.value} />
                </label></div>
        },
    }),
    columnHelper.display({
        id: "Stock",
        header: "Stock",
        cell: (info) =>
            <p class="tw-w-52 tw-text-base md:tw-w-auto">{data[info.row.index].stock}</p>

    }),
    columnHelper.display({
        id: "BAD",
        header: "Bad",
        cell: (info) => {
            const bad = ref(0);
            watch(bad,
                (newValue) => {
                    if (newValue >= 0) {
                        data[info.row.index].bad_stock = Number(newValue);
                    }
                })
            return <div class="tw-flex tw-justify-center">
                <label class="tw-text-center tw-text-[#01579B]">
                    PIECES
                    <BFormInput class="tw-text-center" type="number" placeholder="" v-model={bad.value} />
                </label></div>
        },
    }),
    columnHelper.display({
        id: "keterangana",
        header: "Keterangan",
        cell: (info) => <BFormInput v-model={data[info.row.index].keterangan} placeholder="" />
        ,
    }),
];
