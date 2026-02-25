import {jsPDF} from "jspdf";
import autoTable from "jspdf-autotable";
import {formatCurrencyAuto} from "@/src/lib/utils";

const generateLphPdf = (responseData) => {
    const {data} = responseData;

    // Create new PDF document in landscape mode
    const doc = new jsPDF({
        orientation: "landscape",
        unit: "mm",
        format: "a4",
    });

    // Set font
    doc.setFont("helvetica");

    // Set font
    const pageWidth = doc.internal.pageSize.getWidth();

// Judul utama perusahaan (tengah)
    doc.setFontSize(12);
    doc.setFont("helvetica", "bold");
    doc.text(data.nama_perusahaan, pageWidth / 2, 12, {align: "center"});

// Alamat perusahaan (tengah)
    doc.setFontSize(10);
    doc.setFont("helvetica", "normal");
    doc.text(data.alamat_perusahaan, pageWidth / 2, 17, {align: "center"});

// Garis pembatas
    doc.line(10, 26, pageWidth - 10, 26);

    const labelX = 15;
    const colonX = 45;
    const valueX = 50;
    const startY = 30;
    const lineHeight = 6;

    const labels = ["Sales", "No LPH", "Tanggal"];
    const values = [
        data.nama_sales || "-",
        data.kode_lph || "-",
        data.tanggal_lph || "-"
    ];

    doc.setFont("helvetica", "normal");
    doc.setFontSize(10);

    labels.forEach((label, i) => {
        const y = startY + i * lineHeight;

        doc.text(label, labelX, y);     // Label (e.g., Sales)
        doc.text(":", colonX, y);       // Titik dua (:) selalu sejajar
        doc.text(values[i], valueX, y); // Value (e.g., abidbe)
    });


    if (data.batch_cetak > 1) {
        const y = startY + labels.length * lineHeight; // Tepat di bawah 'Tanggal'
        doc.setFontSize(10);
        doc.text("Batch Cetak", labelX, y);
        doc.text(":", colonX, y);
        doc.text(data.batch_cetak.toString(), valueX, y);
    }

    // Prepare table data
    const tableData = data.data_tagihan.map((item, index) => [
        index + 1, // No
        item.nama_customer || "-", // Nama Outlet
        item.kode_customer || "-", // Kode Outlet
        item.tanggal_faktur || "-", // Tgl
        item.no_faktur || "-", // Nomor
        formatCurrencyAuto(item.sisa_pembayaran || 0), // Rp
        item.tanggal_jatuh_tempo || "-", // Tanggal JT
        item.kode_cn || "-", // Tanggal JT
        formatCurrencyAuto(item.nominal_retur || 0), // Nilai Retur
    ]);
    // const dummyTagihan = Array.from({ length: 12 }).map((_, index) => ({
    //   nama_customer: `Customer ${index + 1}`,
    //   kode_customer: `CUST${index + 1}`,
    //   tanggal_faktur: "2025-08-01",
    //   no_faktur: `INV/${index + 100}`,
    //   sisa_pembayaran: 10000 + index * 1000,
    //   tanggal_jatuh_tempo: "2025-08-15",
    //   nota_retur: "",
    //   nilai_retur: 0,
    // }));
    // const tableData = dummyTagihan.map((item, index) => [
    //   index + 1,
    //   item.nama_customer,
    //   item.kode_customer,
    //   item.tanggal_faktur,
    //   item.no_faktur,
    //   formatCurrencyAuto(item.sisa_pembayaran),
    //   item.tanggal_jatuh_tempo,
    //   item.nota_retur,
    //   formatCurrencyAuto(item.nilai_retur),
    // ]);


    // Calculate total
    const total = data.data_tagihan.reduce(
        (sum, item) => sum + (item.sisa_pembayaran || 0),
        0
    );
    const totalRetur = data.data_tagihan.reduce(
        (sum, item) => sum + (item.nominal_retur || 0),
        0
    );

    // Add total row
    tableData.push([
        "", "", "", "", "TOTAL", formatCurrencyAuto(total), "", "", formatCurrencyAuto(totalRetur)
    ]);

    // Create table using autoTable
    autoTable(doc, {
        startY: 52,
        head: [
            [
                {content: "No", rowSpan: 2},
                {content: "Nama Outlet", rowSpan: 2},
                {content: "Kode Outlet", rowSpan: 2},
                {content: "Faktur", colSpan: 3, styles: {halign: 'center'}},
                {content: "Tanggal Jatuh Tempo", rowSpan: 2},
                {content: "Nota Retur", rowSpan: 2},
                {content: "Nilai Retur", rowSpan: 2},
            ],
            ["Tgl", "Nomor", "Rp"]
        ],
        body: tableData,
        margin: {left: 8, right: 8}, // ✅ lebih kecil dari 10
        tableWidth: "wrap",            // ✅ rapet sesuai konten
        theme: "grid",
        headStyles: {
            fillColor: [240, 240, 240],
            textColor: [0, 0, 0],
            fontStyle: "bold",
            fontSize: 10,
        },
        bodyStyles: {
            fontSize: 9,
        },
        columnStyles: {
            0: {halign: "center", cellWidth: 10},   // No
            1: {halign: "left", cellWidth: 45},     // Nama Outlet (dikurangin)
            2: {halign: "center", cellWidth: 25},   // Kode Outlet
            3: {halign: "center", cellWidth: 25},   // Tgl
            4: {halign: "left", cellWidth: 40},     // Nomor
            5: {halign: "right", cellWidth: 32},    // Rp
            6: {halign: "center", cellWidth: 30},   // Tanggal JT
            7: {halign: "left", cellWidth: 32},    // Nilai Retur
            8: {
                halign: "right",
                cellWidth: 42,          // ✅ fix, ga wrap berlebihan
                overflow: "linebreak",  // ✅ pecah baris kalau panjang
            }, // Nota Retur
        },
        didParseCell: function (data) {
            // Make total row bold
            if (data.row.index === tableData.length - 1) {
                data.cell.styles.fontStyle = "bold";
                data.cell.styles.fillColor = [245, 245, 245];
            }
        },
        // ✅ Draw header/footer for each page
        didDrawPage: function (data) {
            const pageWidth = doc.internal.pageSize.getWidth();

            // // Re-draw header
            // doc.setFont("helvetica", "bold");
            // doc.setFontSize(12);
            // doc.text(data.nama_perusahaan, pageWidth / 2, 12, { align: "center" });
            //
            // doc.setFontSize(10);
            // doc.setFont("helvetica", "normal");
            // doc.text("Jl. Serut RT 04/XII Mojosongo Solo", pageWidth / 2, 17, { align: "center" });
            // doc.text("Telp./Fax. (0271) 856064 (Hunting) | Email: budimas.solo@udw.co.id", pageWidth / 2, 22, { align: "center" });
            // doc.line(10, 26, pageWidth - 10, 26);
            //
            // const labelX = 15;
            // const colonX = 45;
            // const valueX = 50;
            // const startY = 30;
            // const lineHeight = 6;
            //
            // const labels = ["Sales", "No LPH", "Tanggal"];
            // const values = [
            //   data.nama_sales || "-",
            //   data.kode_lph || "-",
            //   data.tanggal_lph || "-"
            // ];
            //
            // doc.setFont("helvetica", "normal");
            // doc.setFontSize(10);
            // labels.forEach((label, i) => {
            //   const y = startY + i * lineHeight;
            //   doc.text(label, labelX, y);
            //   doc.text(":", colonX, y);
            //   doc.text(values[i], valueX, y);
            // });
            //
            // if (data.batch_cetak > 1) {
            //   doc.setFontSize(11);
            //   doc.text(`Batch Cetak : ${data.batch_cetak || "-"}`, 15, 36);
            // }

            // Footer: page + timestamp
            const marginLeft = 15;
            const now = new Date();
            const formattedDate = now.toLocaleDateString("id-ID");
            const formattedTime = now.toTimeString().substring(0, 5);
            const pageHeight = doc.internal.pageSize.getHeight();

            doc.setFont("helvetica", "normal");
            doc.setFontSize(9);
            doc.text(`Page ${doc.internal.getNumberOfPages()}`, marginLeft, pageHeight - 10);
            doc.text(formattedDate, marginLeft + 30, pageHeight - 10);
            doc.text(formattedTime, marginLeft + 60, pageHeight - 10);
        },
    });

    const totalPages = doc.internal.getNumberOfPages();
    const currentPage = doc.internal.getCurrentPageInfo().pageNumber;

    if (currentPage === totalPages) {
        // Tambahkan halaman baru jika ruang tidak cukup
        const pageHeight = doc.internal.pageSize.getHeight();
        const spaceNeeded = 40;
        const currentY = doc.lastAutoTable.finalY;

        if (currentY + spaceNeeded > pageHeight - 5) {
            doc.addPage();
        }

        const finalY = (doc.lastAutoTable.finalY + 25 <= pageHeight - 20)
            ? doc.lastAutoTable.finalY + 25
            : 30;

        const marginLeft = 15;
        const colWidth = 60; // space between each signature
        const lineText = "( ............................ )";

        // Positions
        const sig1X = marginLeft + 20;
        const sig2X = sig1X + colWidth + 30;
        const sig3X = sig2X + colWidth + 30;

        doc.setFontSize(10);
        doc.setFont("helvetica", "normal");

        // Draw (............................)
        doc.text(lineText, sig1X, finalY);
        doc.text(lineText, sig2X, finalY);
        doc.text(lineText, sig3X, finalY);

        // Labels under lines
        doc.setFont("helvetica", "bold");
        doc.text("Penagih", sig1X + 10, finalY + 7);
        doc.text("Penerima", sig2X + 9, finalY + 7);
        doc.text("Kasir", sig3X + 14, finalY + 7);
    }


    return doc;
};

export default generateLphPdf;
export {generateLphPdf};
