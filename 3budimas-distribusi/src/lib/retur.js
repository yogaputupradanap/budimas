import jsPDF from "jspdf";

const generateMinimalTablePDF = ({
                                     data,
                                     info
                                 }) => {
    const doc = new jsPDF();

    doc.setFont("courier");
    doc.setCharSpace(-0.3);

    // Judul
    doc.setFontSize(12);
    doc.text(info.nama_perusahaan, 105, 15, {align: "center"});

    // Subjudul
    doc.setFontSize(10);
    doc.text(info.alamat_perusahaan, 105, 20, {align: "center"});
    // doc.text("Telp./Fax. (0271) 856064 (Hunting) || Email: budimas.solo@udw.co.id", 105, 25, {align: "center"});
    doc.line(10, 28, 200, 28);

    doc.setFontSize(12);
    doc.text("PENGAJUAN RETUR PENJUALAN", 105, 35, {align: "center"});

    doc.setFontSize(10);
    doc.text(`No.     : ${info.kode_kpr}`, 14, 43);
    doc.text(`Tanggal : ${info.tanggal_request}`, 14, 48);

    doc.text("Kepada Yth.", 14, 56);
    doc.text(`${info.nama} (${info.kode})`, 14, 61);
    doc.text(`${info.alamat}`, 14, 66);

    // Table setup
    const startX = 14;
    const startY = 74;
    const rowHeight = 10;

    const colWidths = [10, 32, 65, 18, 18, 18, 25];
    const headers = ["No", "Kode Barang", "Nama Barang", "UOM 1", "UOM 2", "UOM 3", "Keterangan"];
    // data = [
    //     ["1", "40057479_BD", "STELLA AFR JAPANESE SAKURA 175ML RIV", "3 PC", "2 Box", "1 CT", "-"],
    //     ["2", "40019324 BD", "MITU BABY POWDER PINK 200G+75%", "0 PC", "1 Box", "0 CT", "-"],
    //     ["2", "40019324 BD", "MITU BABY POWDER PINK 200G+75%", "0 PC", "1 Box", "0 CT", "-"],
    //     ["2", "40019324 BD", "MITU BABY POWDER PINK 200G+75%", "0 PC", "1 Box", "0 CT", "-"],
    //     ["2", "40019324 BD", "MITU BABY POWDER PINK 200G+75%", "0 PC", "1 Box", "0 CT", "-"],
    //     ["2", "40019324 BD", "MITU BABY POWDER PINK 200G+75%", "0 PC", "1 Box", "0 CT", "-"],
    //     ["2", "40019324 BD", "MITU BABY POWDER PINK 200G+75%", "0 PC", "1 Box", "0 CT", "-"],
    //     ["2", "40019324 BD", "MITU BABY POWDER PINK 200G+75%", "0 PC", "1 Box", "0 CT", "-"],
    //     ["2", "40019324 BD", "MITU BABY POWDER PINK 200G+75%", "0 PC", "1 Box", "0 CT", "-"],
    //     ["2", "40019324 BD", "MITU BABY POWDER PINK 200G+75%", "0 PC", "1 Box", "0 CT", "-"],
    //     ["2", "40019324 BD", "MITU BABY POWDER PINK 200G+75%", "0 PC", "1 Box", "0 CT", "-"],
    //     ["2", "40019324 BD", "MITU BABY POWDER PINK 200G+75%", "0 PC", "1 Box", "0 CT", "-"],
    //     ["2", "40019324 BD", "MITU BABY POWDER PINK 200G+75%", "0 PC", "1 Box", "0 CT", "-"],
    //     ["2", "40019324 BD", "MITU BABY POWDER PINK 200G+75%", "0 PC", "1 Box", "0 CT", "-"],
    //     ["2", "40019324 BD", "MITU BABY POWDER PINK 200G+75%", "0 PC", "1 Box", "0 CT", "-"],
    //     ["2", "40019324 BD", "MITU BABY POWDER PINK 200G+75%", "0 PC", "1 Box", "0 CT", "-"],
    //     ["2", "40019324 BD", "MITU BABY POWDER PINK 200G+75%", "0 PC", "1 Box", "0 CT", "-"],
    //     ["2", "40019324 BD", "MITU BABY POWDER PINK 200G+75%", "0 PC", "1 Box", "0 CT", "-"],
    //     ["3", "40028285_BD", "MITU BABY COLOGNE F&C SWEET PINK 50ML", "1 PC", "0 Box", "2 CT", "-"]
    // ];

    let yPos = startY;

    // Draw top border of table
    doc.setLineWidth(0.5);
    doc.line(startX, yPos, startX + colWidths.reduce((a, b) => a + b, 0), yPos);

    // Header text
    let currentX = startX;
    headers.forEach((text, i) => {
        doc.text(text, currentX + 1.5, yPos + 7);
        currentX += colWidths[i];
    });

    // Bottom line of header
    yPos += rowHeight;
    doc.line(startX, yPos, startX + colWidths.reduce((a, b) => a + b, 0), yPos);

    const pageHeight = doc.internal.pageSize.height;
    const marginBottom = 20;

    data.forEach((row, rowIndex) => {
        let colX = startX;
        let maxLines = 1;

        const wrappedRow = row.map((text, i) => {
            const wrapped = doc.splitTextToSize(text, colWidths[i] - 2);
            if (wrapped.length > maxLines) maxLines = wrapped.length;
            return wrapped;
        });

        const rowHeightTotal = rowHeight * maxLines;

        // ⛔️ Cek apakah butuh halaman baru
        if (yPos + rowHeightTotal + marginBottom > pageHeight) {
            doc.addPage();
            yPos = 14; // Reset yPos untuk halaman baru

            // Garis atas table
            doc.line(startX, yPos, startX + colWidths.reduce((a, b) => a + b, 0), yPos);

            // Header table di halaman baru
            let currentX = startX;
            headers.forEach((text, i) => {
                doc.text(text, currentX + 1.5, yPos + 7);
                currentX += colWidths[i];
            });

            yPos += rowHeight;
            doc.line(startX, yPos, startX + colWidths.reduce((a, b) => a + b, 0), yPos);
        }

        // Tulis row datanya
        wrappedRow.forEach((wrapped, i) => {
            doc.text(wrapped, colX + 1, yPos + 6);
            colX += colWidths[i];
        });

        yPos += rowHeightTotal;

        // Garis bawah row
        doc.line(startX, yPos, startX + colWidths.reduce((a, b) => a + b, 0), yPos);
    });


    const leftText = `${info.nama} (${info.kode})`;
    const dropText = "(Dropping)";
    const rightText = "(Gudang)";

    // Footer
    doc.text("Hormat Kami", 14, yPos + 10);

    // Bagian kiri + Dropping (dengan jarak)
    doc.text(leftText, 14, yPos + 25);
    const leftWidth = doc.getTextWidth(leftText);
    doc.text(dropText, 14 + leftWidth + 30, yPos + 25); // +5 px jarak

    // Bagian kanan: rata kanan dokumen
    const pageWidth = doc.internal.pageSize.getWidth();
    const rightWidth = doc.getTextWidth(rightText);
    doc.text(rightText, pageWidth - rightWidth - 30, yPos + 25); // 14 px padding kanan

    doc.save("Retur Penjualan - " + info.kode_kpr + ".pdf");
};

export default generateMinimalTablePDF;
