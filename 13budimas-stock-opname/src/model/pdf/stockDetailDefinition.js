import { parseCurrency } from "@/src/lib/utils";
import { format } from "date-fns";
import { id } from "date-fns/locale";

const TABLE_WIDTHS = ["9%", "10%", "6%", "6%", "6%", "8%", "8%", "8%", "10%", "10%", "12%", "10%"];
const TABLE_HEADERS = [
    "SKU", "Nama Produk", "UOM 3", "UOM 2", "UOM 1",
    "Stock", "Selisih", "Stock System", "Harga", "Subtotal Selisih",
    "Subtotal", "Ket."
];

/**
 * Creates a table for stock opname details
 * @param {Object} stockOpname - Stock opname data
 * @returns {Object} PDFMake table object
 */
function createStockOpnameTable(stockOpname) {
    const products = stockOpname.produks;

    const subtotal = products.reduce((acc, cur) => acc + cur.subtotal, 0);
    const subtotalSelisih = products.reduce((acc, cur) => acc + cur.subtotal_selisih, 0);

    // Create Table Body Rows
    const tableHeaders = TABLE_HEADERS.map(header => ({
        text: header,
        style: "tableHeader",
    }));

    const dataRows = [];
    for (const product of products) {
        dataRows.push([
            { text: product.sku, style: "tableBodySubheader" },
            { 
                text: product.nama_produk, 
                style: "tableBodySubheader", 
                alignment: "left" 
            },
            { text: product.uom3, style: "tableBodySubheader" },
            { text: product.uom2, style: "tableBodySubheader" },
            { text: product.uom1, style: "tableBodySubheader" },
            { text: product.stock, style: "tableBodySubheader" },
            { text: product.selisih, style: "tableBodySubheader" },
            { text: product.stock_system, style: "tableBodySubheader" },
            { 
                text: parseCurrency(product.harga), 
                style: "tableBodySubheader", 
                alignment: "left" 
            },
            { 
                text: parseCurrency(product.subtotal_selisih), 
                style: "tableBodySubheader",
                alignment: "left" 
            },
            { 
                text: parseCurrency(product.subtotal), 
                style: "tableBodySubheader", 
                alignment: "left" 
            },
            { 
                text: product.keterangan, 
                style: "tableBodySubheader", 
                alignment: "left"
            },
        ]);
    }

    const emptyCells = Array(11).fill('');
    const totalSeparatorRow = [
        ...emptyCells,
        { text: "", alignment: "right" }
    ]

    const totalRow = [
        ...emptyCells,
        {
            text: [
                { text: "Total Selisih:\n", fontSize: 6, bold: true },
                { text: parseCurrency(subtotalSelisih), fontSize: 6, bold: true },
                { text: "\n\n", fontSize: 6 },
                { text: "Total:\n", fontSize: 6, bold: true },
                { text: parseCurrency(subtotal), fontSize: 6, bold: true }
            ],
            alignment: "right",
            margin: [0, 10, 0, 0]
        }
    ]

    // Build Table Structure
    const tableBody = [
        tableHeaders,
        ...dataRows,
        totalSeparatorRow,
        totalRow,
    ];

    return {
        // Styling UI Print Table
        layout: {
            hLineWidth: (i, node) => {
                if (i === 0 || i === 1) return 1;
                if (i === node.table.body.length - 1) return 1
                return 0;
            },
            vLineWidth: () => 0,
            hLineColor: () => '#aaa',
            paddingLeft: () => 4,
            paddingRight: () => 4,
            paddingTop: () => 2,
            paddingBottom: () => 2
        },
        margin: [0, 10, 0, 0],
        table: {
            widths: TABLE_WIDTHS,
            body: tableBody,
        },
    }
}

/**
 * Creates a PDF definition for stock opname report
 * @param {Object} data - Report data
 * @returns {Object} PDFMake document definition
 */
export const definition = (data) => {
    if (!data?.stockOpnameDetail?.length) {
        console.error("Missing required data for PDF generation");
        return { content: [{ text: "Error: Missing data" }] };
    }

    const stockOpnameDetail = data.stockOpnameDetail[0];
    const tables = data.stockOpnameDetail.map(createStockOpnameTable);

    const currentDate = format(new Date(), "dd/MM/yyyy");
    const currentTime = format(new Date(), "p", { locale: id });
    const formattedDateTime = `${currentDate}, ${currentTime}`;

    return {
        pageMargins: [20, 20, 20, 20],
        footer: (currentPage, pageSize) => ({
            text: `Page ${currentPage} of ${pageSize}`,
            fontSize: 6,
            alignment: "right",
            margin: [0, 0, 20, 0],
        }),
        content: [
            // Title section
            {
                width: "auto",
                text: "LAPORAN STOCK OPNAME",
                alignment: "center",
            },
            {
                canvas: [
                    {
                        type: "line",
                        x1: 205,
                        y1: 3,
                        x2: 350,
                        y2: 3,
                        lineWidth: 1,
                    },
                ],
            },
            {
                width: "auto",
                text: `(${stockOpnameDetail.nama_principal} - ${stockOpnameDetail.kode_so})`,
                alignment: "center",
                fontSize: 10,
                italics: true,
                margin: [0, 5, 0, 0],
            },
            // Header information
            {
                margin: [0, 10, 0, 0],
                columns: [
                    {
                        text: `${data.user.nama_perusahaan}\nCabang: ${data.user.nama_cabang}\nTanggal SO: ${stockOpnameDetail.tanggal_so}`,
                        style: "subheader",
                    },
                    {
                        text: `${data.user.nama}\n${formattedDateTime}`,
                        style: "subheader",
                        alignment: "right",
                    },
                ],
            },
            // Stock-Opname tables
            ...tables,
        ],

        styles: {
            header: {
                fontSize: 16,
                bold: true,
                margin: [0, 0, 0, 10],
            },
            subheader: {
                fontSize: 10,
                margin: [0, 10, 0, 5],
            },
            tableHeader: {
                bold: true,
                fontSize: 7,
                fillColor: "#eeeeee",
                alignment: "left",
            },
            tableBodyHeader: {
                fontSize: 7,
                bold: true,
                fillColor: "#eeeeee",
            },
            tableBodySubheader: {
                fontSize: 6,
                margin: [0, 2, 0, 0],
            },
        },
        defaultStyle: {
            alignment: "justify",
        },
    }
}
