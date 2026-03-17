import RouterButton from "@/src/components/ui/RouterButton.vue";
import { formatRupiah } from "@/src/lib/utils";
import { createColumnHelper } from "@tanstack/vue-table";
import { h, ref } from "vue";
import printJS from "print-js";
import pdfMake from "pdfmake/build/pdfmake";
import pdfFonts from "pdfmake/build/vfs_fonts";
import { stockOpnameService } from "@/src/services/stockOpname";
import { prepareReportData } from "@/src/model/data/StockOpnamePdfData";
import { definition } from "@/src/model/pdf/stockDetailDefinition";

const printingStates = ref({});

pdfMake.vfs = pdfFonts.pdfMake ? pdfFonts.pdfMake.vfs : pdfFonts.vfs;

const previewPrint = async (row) => {
    try {
        printingStates.value[row.id_stock_opname] = true;
        const productData = await fetchStockOpnameData(row.id_stock_opname);
        if (!productData) return;

        const reportData = prepareReportData(row, productData);
        generateAndShowPdf(reportData);
    } catch (error) {
        console.error("Error Message:", error);
    } finally {
        printingStates.value[row.id_stock_opname] = false;
    }
};

const fetchStockOpnameData = async (stockOpnameId) => {
    const response = await stockOpnameService.getOneStockOpnameDetail(stockOpnameId);
    if (!response) {
        console.error("No data available for PDF generation");
        return null;
    }
    return response;
};

const generateAndShowPdf = (data) => {
    try {
        const docDefinition = definition(data);
        const pdfDoc = pdfMake.createPdf(docDefinition);
    
        pdfDoc.getBlob((blob) => {
            const url = URL.createObjectURL(blob);
    
            printJS({
                printable: url,
                type: 'pdf',
                showModal: false,
                onLoadingEnd: () => {
                    setTimeout(() => URL.revokeObjectURL(url), 2000);
                }
            });
        });
    } catch (error) {
        console.error('PDF Generation Error:', error)
    }
};

const columnHelper = createColumnHelper();
export const listStockColumns = [
    columnHelper.accessor((row) => "no", {
        id: "no",
        header: h("div", {
            class: "tw-w-20 md:tw-w-auto",
            innerText: "No",
        }),
        cell: (info) => h("div", { class: "tw-w-auto", innerText: info.row.index + 1 }),
    }),
    columnHelper.accessor((row) => row.kode_so, {
        id: "summarized_data.kode_so",
        header: "Kode SO",
        cell: (info) =>
            h("div", { class: "tw-w-52 md:tw-w-auto", innerText: info.getValue() }),
    }),
    columnHelper.accessor((row) => row.tanggal_so, {
        id: "summarized_data.tanggal_so",
        header: "Tanggal",
        cell: (info) => h("div", { class: "tw-w-20 md:tw-w-auto", innerText: info.getValue() }),
    }),
    columnHelper.accessor((row) => row.nama_principal, {
        id: "nama_principal",
        header: "Principal",
        cell: (info) => h("div", { class: "tw-w-20 md:tw-w-auto", innerText: info.getValue() }),
    }),
    columnHelper.accessor((row) => row.produk_count, {
        id: "not incl1",
        header: "Jml. Produk",
        cell: (info) => h("div", { class: "tw-w-44 md:tw-w-auto", innerText: info.getValue() }),
    }),
    columnHelper.accessor((row) => row.total, {
        id: "summarized_data.total",
        header: "Total Harga",
        cell: (info) => h("div", { class: "tw-w-44 md:tw-w-auto", innerText: formatRupiah(info.getValue()) }),
    }),
    columnHelper.accessor((row) => row.ket_so, {
        id: "summarized_data.ket_so",
        header: "Keterangan",
        cell: (info) => h("div", { class: "tw-w-44 md:tw-w-auto", innerText: info.getValue() }),
    }),
    columnHelper.accessor((row) => row.status_so, {
        id: "summarized_data.status_so",
        header: "Status",
        cell: (info) => h("div", { class: "tw-w-44 md:tw-w-auto", innerText: info.getValue() }),
    }),
    columnHelper.accessor((row) => "action", {
        id: "not incl2",
        header: "Action",
        cell: (info) => {
            const isPrinting = printingStates.value[info.row.original.id_stock_opname];

            return h('div', { class: 'tw-flex tw-items-center' }, [
                h(RouterButton, {
                    class: "tw-h-10 tw-mx-1 tw-px-3",
                      to: `/stock-opname/detail-stock-opname/${info.row.original.id_stock_opname}`,
                    innerHTML: 'Detail'
                }),
                h("button", {
                    class: `tw-h-10 tw-mx-1 tw-px-3 tw-rounded-lg 
                      tw-text-white tw-transition-colors tw-duration-300
                      ${isPrinting ? 'tw-bg-gray-600' : 'tw-bg-gray-500 hover:tw-bg-gray-700'
                    }`,
                    onClick: () => previewPrint(info.row.original),
                    disabled: isPrinting,
                    innerHTML: isPrinting ? `
                    <div class="tw-flex tw-items-center">
                        <span class="tw-inline-block tw-w-4 tw-h-4 tw-rounded-full tw-border-2 
                                    tw-border-white tw-border-t-transparent tw-animate-spin tw-mr-2">
                        </span>
                        Loading
                    </div>` : 'Cetak'
                })
            ])
        }
    }),
];
