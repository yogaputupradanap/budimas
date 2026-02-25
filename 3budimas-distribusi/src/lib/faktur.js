import QRCode from "qrcode";
import {calculateProductDiscounts, formatCurrencyAuto, getDateNow, numberToWords,} from "./utils";
import {jsPDF} from "jspdf";
import "jspdf-autotable";
import {svg2pdf} from "svg2pdf.js";

/**
 * Fungsi khusus untuk mengunduh faktur dengan jsPDF, tampilan mirip Faktur.vue
 * @param {Object} fakturInfo - Informasi faktur (data pelanggan, nomor faktur, dll)
 * @param {Array} detailFaktur - Detail produk dalam faktur (array produk)
 * @param {String} filename - Nama file yang akan diunduh (default: "faktur")
 * @param {Boolean} isRetur - Flag untuk menandakan apakah ini faktur retur (default: false)
 * @return {Promise} - Promise yang diselesaikan ketika PDF sudah diunduh
 */
export const downloadPdf2 = async (
  fakturInfo,
  detailFaktur,
  filename = "faktur",
  isRetur = false,
  existingDoc = null,
  skipSave = false,
  totalPagesForThisFaktur = 1,
  startPageNumber = 1,
  mode = "picked"
) => {
  try {
    // ======== INISIALISASI DOKUMEN ========
    const doc =
      existingDoc ||
      new jsPDF({
        orientation: "portrait",
        unit: "mm",
        format: "letter",
      });

    doc.setFont("courier");
    doc.setCharSpace(-0.3);

    // ======== KONSTANTA LAYOUT (JARAK DIPERKECIL) ========
    const LAYOUT = {
      margin: 4,
      pageWidth: doc.internal.pageSize.getWidth(),
      pageHeight: doc.internal.pageSize.getHeight(),
      lineHeight: 3,
      sectionSpacing: 4,
      signWidth: 30,
      signLineWidth: 30,
      maxContentHeight: 220,
      maxKodeChars: 11,
    };

    // Kolom utama
    const COLS = {
      left: LAYOUT.margin,
      middle: LAYOUT.pageWidth / 2,
      right: LAYOUT.pageWidth - LAYOUT.margin,
      // Kolom tabel produk
      kode: LAYOUT.margin,
      get nama() {
        return this.kode + 22;
      },
      get uom() {
        return this.nama + 47;
      },
      get harga() {
        return this.uom + 23;
      },
      get diskon() {
        return this.harga + 20;
      },
      get alasan() {
        return this.diskon + 48;
      },
      get totalDisc() {
        return isRetur ? this.alasan + 24 : this.diskon + 48;
      },
      get subtotal() {
        return this.totalDisc + 28;
      },
    };

    // ======== VARIABEL UNTUK TRACKING POSISI ========
    let y = 10;
    let currentPageOfThisFaktur = 1;
    let currentGlobalPage = startPageNumber;
    let startY = 0;

    // ======== PERHITUNGAN TOTAL ORDER DAN DISKON ========
    // Hitung total pesanan untuk perhitungan diskon
    const totalOrderSubtotal = detailFaktur.reduce((total, product) => {
      let kartonValue, boxValue, piecesValue;

      if (mode === "delivered") {
        kartonValue = product.karton_delivered || 0;
        boxValue = product.box_delivered || 0;
        piecesValue = product.pieces_delivered || 0;
      } else {
        kartonValue = product.karton_picked || 0;
        boxValue = product.box_picked || 0;
        piecesValue = product.pieces_picked || 0;
      }

      const kartonToUom1 = kartonValue * (product.konversi_level3 || 1);
      const boxToUom1 = boxValue * (product.konversi_level2 || 1);
      const totalPieces = kartonToUom1 + boxToUom1 + piecesValue;
      return total + totalPieces * (product.harga_jual || 0);
    }, 0);

    // Default voucherStatus untuk perhitungan diskon
    const voucherStatus = {
      v1r: true,
      v2r: true,
      v3r: true,
      v2p: true,
      v3p: true,
    };

    // Produk dengan perhitungan diskon
    const productsWithCalculations = detailFaktur.map((product) => ({
      ...product,
      calculations: calculateProductDiscounts(
        product,
        voucherStatus,
        totalOrderSubtotal,
        mode
      ),
    }));

    // Total keseluruhan dari faktur
    const grandTotal = productsWithCalculations.reduce(
      (total, product) => ({
        subtotal: total.subtotal + product.calculations.subtotal,
        totalDiskon: total.totalDiskon + product.calculations.totalDiskon,
        ppnValue: total.ppnValue + product.calculations.ppnValue,
      }),
      { subtotal: 0, totalDiskon: 0, ppnValue: 0 }
    );

    // Total akhir
    grandTotal.total =
      grandTotal.subtotal - grandTotal.totalDiskon + grandTotal.ppnValue;

    // ======== HELPER FUNCTIONS ========
    /**
     * Membagi teks menjadi beberapa baris berdasarkan lebar maksimum
     */
    function wrapText(text, maxWidth, fontSize) {
      const words = text.split(" ");
      const lines = [];
      let currentLine = "";

      words.forEach((word) => {
        const testLine = currentLine ? `${currentLine} ${word}` : word;
        const testWidth =
          (doc.getStringUnitWidth(testLine) * fontSize) /
          doc.internal.scaleFactor;

        if (testWidth > maxWidth) {
          lines.push(currentLine);
          currentLine = word;
        } else {
          currentLine = testLine;
        }
      });

      if (currentLine) lines.push(currentLine);
      return lines;
    }

    /**
     * Membuat garis pada dokumen
     */
    function drawLine(x1, y1, x2, y2, pattern = [0], width = 0.5) {
      doc.setDrawColor(0);
      doc.setLineDashPattern(pattern, 0);
      doc.setLineWidth(width);
      doc.line(x1, y1, x2, y2);
    }

    async function generateQRCodeSVG(text) {
      try {
        // Hitung panjang text untuk menentukan dimensi optimal
        const textLength = text.length;

        // Logika untuk menyesuaikan dimensi berdasarkan panjang text
        let size, margin;

        if (textLength <= 10) {
          // Text pendek
          size = 80;
          margin = 4;
        } else if (textLength <= 15) {
          // Text sedang
          size = 90;
          margin = 4;
        } else if (textLength <= 20) {
          // Text panjang (seperti NPBDMSL-2506000001)
          size = 100;
          margin = 4;
        } else {
          // Text sangat panjang
          size = 110;
          margin = 4;
        }

        // Generate QR code sebagai SVG string
        const qrSvgString = await QRCode.toString(text, {
          type: "svg",
          width: size,
          margin: margin,
          color: {
            dark: "#000000",
            light: "#ffffff",
          },
          errorCorrectionLevel: "M",
        });

        // Parse SVG string menjadi DOM element
        const parser = new DOMParser();
        const svgDoc = parser.parseFromString(qrSvgString, "image/svg+xml");
        const svgElement = svgDoc.documentElement;

        return svgElement;
      } catch (error) {
        console.error("Error generating QR code:", error);
        return null;
      }
    }
    /**
     * Menambahkan header utama pada halaman
     */
    function addHeaderUtama() {
      y = 10;

      // ---- BAGIAN KIRI HEADER ----
      doc.setFontSize(13);
      doc.setFont("courier", "bold");
      doc.text("PT. BUDIMAS MAKMUR MULIA", COLS.left, y);

      y += 5; // Diperkecil dari 7 ke 5
      doc.setFontSize(10);
      doc.setFont("courier", "normal");

      // Alamat dan informasi perusahaan
      const companyInfo = [
        "Jl. Serut RT 04/XII Mojosongo Solo",
        "Telp. / Fax. (0271) 856064",
        "Email : budimas.solo@yahoo.com",
      ];

      companyInfo.forEach((info) => {
        doc.text(info, COLS.left, y);
        y += LAYOUT.lineHeight; // Menggunakan lineHeight yang diperkecil
      });

      // Garis putus-putus di bawah nama perusahaan
      drawLine(COLS.left, y, COLS.left + 63, y, [2, 2], 0.1);

      y += LAYOUT.sectionSpacing; // Menggunakan sectionSpacing yang diperkecil
      doc.text(`Tanggal : ${fakturInfo?.tanggal_faktur_res || getDateNow()}`, COLS.left, y);

      // ---- BAGIAN TENGAH HEADER ----
      let centerY = 12;

      // Kode rute dan principal dalam kotak
      const kodeText = `${fakturInfo?.kode_rute || ""}#${
        fakturInfo?.kode_principal || ""
      }`;
      doc.setDrawColor(0);
      doc.setLineDashPattern([0], 0);
      doc.setLineWidth(0.5);
      doc.rect(COLS.middle - 30, centerY - 5, 60, 8);
      doc.setFont("courier", "bold");
      doc.setFontSize(18);
      doc.text(kodeText, COLS.middle, centerY + 0.5, { align: "center" });

      centerY += 8;
      doc.setFontSize(11);
      const fakturTitle = `FAKTUR ${isRetur ? "RETUR" : "PENJUALAN"}`;
      doc.text(fakturTitle, COLS.middle + 2, centerY, { align: "center" });

      // Garis bawah judul faktur
      const currentFontSize = doc.getFontSize();
      const titleWidth =
        (doc.getStringUnitWidth(fakturTitle) * currentFontSize) /
        doc.internal.scaleFactor;
      drawLine(
        COLS.middle - titleWidth / 2,
        centerY + 1,
        COLS.middle + titleWidth / 2,
        centerY + 1,
        [0, 0],
        0.1
      );

      // Nomor faktur
      doc.setFontSize(9);
      centerY += 5;
      doc.text(`No. ${isRetur ? "Retur" : "Faktur"} :`, COLS.middle, centerY, {
        align: "center",
      });

      doc.setFontSize(9);
      centerY += LAYOUT.lineHeight;
      doc.text(`${fakturInfo?.nomor_faktur || ""}`, COLS.middle + 3, centerY, {
        align: "center",
      });

      // ---- BAGIAN KANAN HEADER ----
      let rightY = 10;
      const customerColX = COLS.right - 60;

      doc.setFontSize(11);
      doc.setFont("courier");
      doc.text("Kepada Yth.", customerColX, rightY);

      // Data customer
      rightY += 5; // Diperkecil dari 7 ke 5
      doc.setFontSize(10);
      doc.setFont("courier", "normal");

      // Informasi customer
      const customerInfo = [
        `${fakturInfo?.nama_customer || ""} (${
          fakturInfo?.kode_customer || ""
        })`,
        `${fakturInfo?.alamat_customer || ""}`,
        `Telp : ${fakturInfo?.telepon_customer || ""}`,
      ];

      customerInfo.forEach((info) => {
        doc.text(info, customerColX, rightY);
        rightY += LAYOUT.lineHeight;
      });

      // Garis putus-putus di bawah informasi customer
      drawLine(customerColX, rightY, COLS.right, rightY, [2, 2], 0.1);

      // Tanggal jatuh tempo/pengajuan
      rightY += LAYOUT.sectionSpacing;
      const tanggalText = isRetur
        ? `Tanggal Pengajuan : ${getDateNow(
            new Date(fakturInfo?.tanggal_retur_pengajuan || new Date())
          )}`
        : `Jatuh Tempo : ${getDateNow(
            new Date(fakturInfo?.tanggal_jatuh_tempo || new Date())
          )}`;
      doc.text(tanggalText, customerColX, rightY);

      // ======== GARIS PEMBATAS HEADER ========
      const maxY = Math.max(y, centerY, rightY) + LAYOUT.lineHeight;
      drawLine(LAYOUT.margin, maxY, COLS.right, maxY, [0, 0], 0.1);

      // Menyetel y global ke maxY untuk lanjutan kode
      y = maxY;
      return y;
    }

    /**
     * Menambahkan header tabel produk
     */
    function addHeaderTabel() {
      y += LAYOUT.sectionSpacing;
      doc.setFontSize(10);
      doc.setFont("courier", "bold");

      // Header tabel dasar
      doc.text("Kode", COLS.kode, y + 1);
      doc.text("Nama", COLS.nama, y + 1);

      // Header UOM dengan subheader
      doc.text("Satuan", COLS.uom + 4, y - 0.5);
      doc.text("CT", COLS.uom, y + 3);
      doc.text("BX", COLS.uom + 8, y + 3);
      doc.text("PC", COLS.uom + 16, y + 3);

      doc.text("Harga", COLS.harga, y - 0.5);
      doc.text("Satuan", COLS.harga, y + 3);

      // Header Diskon dengan subheader
      doc.text("Diskon", COLS.diskon + 13, y - 0.5);
      doc.text("D1R", COLS.diskon, y + 3);
      doc.text("D2R", COLS.diskon + 8, y + 3);
      doc.text("D3R", COLS.diskon + 16, y + 3);
      doc.text("D2K", COLS.diskon + 24, y + 3);
      doc.text("D3K", COLS.diskon + 34, y + 3);

      if (isRetur) {
        doc.text("Alasan retur", COLS.alasan, y + 1);
      }

      doc.text("Total Disc", COLS.totalDisc, y + 1);
      doc.text("Sub Total", COLS.subtotal + 3, y + 1);

      // Garis pembatas setelah header
      y += 9; // Diperkecil dari 12 ke 9
      drawLine(LAYOUT.margin, y - 4, COLS.right, y - 4, [0, 0], 0.1); // Diperkecil spacing dari -5 ke -4
      doc.setFont("courier", "normal");

      // Setel posisi awal untuk data
      startY = y;
      return y;
    }

    /**
     * Menambahkan halaman baru
     */
    function addNewPage(withTableHeader = true) {
      doc.addPage();
      currentPageOfThisFaktur++;
      currentGlobalPage++;

      addHeaderUtama();

      if (withTableHeader) {
        addHeaderTabel();
      } else {
        y += LAYOUT.sectionSpacing;
      }
    }

    /**
     * Menambahkan kolom tanda tangan
     */
    function addSignatureColumn(posX, label, name = "") {
      doc.setFontSize(9);
      doc.text(label, posX, signY, { align: "center" });

      // Garis untuk tanda tangan
      drawLine(
        posX - LAYOUT.signLineWidth / 2,
        signY + 15,
        posX + LAYOUT.signLineWidth / 2,
        signY + 15,
        [0, 0],
        0.1
      );

      // Nama di bawah tanda tangan jika ada
      if (name) {
        doc.setFontSize(8);
        doc.text(name, posX, signY + 20, { align: "center" });
      }
    }

    // ======== TAMBAHKAN HEADER UTAMA DAN TABEL ========
    addHeaderUtama();
    addHeaderTabel();

    // ======== DATA TABEL PRODUK ========
    productsWithCalculations.forEach((product, index) => {
      // Cek apakah perlu halaman baru
      if (y > startY + LAYOUT.maxContentHeight) {
        addNewPage(true);
      }

      // ======== PERHITUNGAN NILAI PRODUK ========
      let kartonValue, boxValue, piecesValue;

      if (mode === "delivered") {
        kartonValue = product.karton_delivered || 0;
        boxValue = product.box_delivered || 0;
        piecesValue = product.pieces_delivered || 0;
      } else {
        kartonValue = product.karton_picked || 0;
        boxValue = product.box_picked || 0;
        piecesValue = product.pieces_picked || 0;
      }

      const kartonToUom1 = kartonValue * (product.konversi_level3 || 1);
      const boxToUom1 = boxValue * (product.konversi_level2 || 1);
      const totalPieces = kartonToUom1 + boxToUom1 + piecesValue;
      const subtotal = totalPieces * (product.harga_jual || 0);

      // ======== PERSIAPKAN TEXT UNTUK KODE DAN NAMA ========
      // Split kode SKU menjadi beberapa baris
      const kodeSku = product.kode_sku || "";
      const kodeLines = [];
      for (let i = 0; i < kodeSku.length; i += LAYOUT.maxKodeChars) {
        kodeLines.push(kodeSku.substring(i, i + LAYOUT.maxKodeChars));
      }

      // Split nama produk menjadi beberapa baris
      const namaProduk = product.nama_produk || "";
      const maxWidth = 40;
      const fontSize = 10;
      const namaLines = wrapText(namaProduk, maxWidth, fontSize);

      // Tentukan total baris yang dibutuhkan
      const totalLines = Math.max(kodeLines.length, namaLines.length);

      // ======== PERSIAPKAN TEXT UNTUK DISKON ========
      // Format diskon sebagai string
      const diskon = {
        d1r: String(
          product.calculations.diskon1r > 0 ? product.v1r_persen || "0" : "0"
        ),
        d2r: String(
          product.calculations.diskon2r > 0 ? product.v2r_persen || "0" : "0"
        ),
        d3r: String(
          product.calculations.diskon3r > 0 ? product.v3r_persen || "0" : "0"
        ),
        d2p: { nilai: "0", uom: "" },
        d3p: { nilai: "0", uom: "" },
      };

      // Diskon 2P (D2K)
      if (product.calculations.diskon2p > 0) {
        if (product.v2p_nominal_diskon) {
          diskon.d2p.nilai = String(product.v2p_nominal_diskon);
          diskon.d2p.uom = ``;
        } else {
          diskon.d2p.nilai = String(product.v2p_persen || "0");
        }
      }

      // Diskon 3P (D3K)
      if (product.calculations.diskon3p > 0) {
        if (product.v3p_nominal_diskon) {
          diskon.d3p.nilai = String(product.v3p_nominal_diskon);
          diskon.d3p.uom = ``;
        } else {
          diskon.d3p.nilai = String(product.v3p_persen || "0");
        }
      }

      // ======== PERSIAPKAN TEXT UNTUK TOTAL DISKON DAN SUBTOTAL ========
      const totalDiscText = formatCurrencyAuto(
        product.calculations.totalDiskon
      );
      const subtotalText = formatCurrencyAuto(subtotal);

      const totalDiscWidth =
        (doc.getStringUnitWidth(totalDiscText) * 9) / doc.internal.scaleFactor;
      const subtotalWidth =
        (doc.getStringUnitWidth(subtotalText) * 9) / doc.internal.scaleFactor;

      // ======== GAMBAR BARIS PERTAMA PRODUK ========
      doc.text(kodeLines[0] || "", COLS.kode, y);
      doc.text(namaLines[0] || "", COLS.nama, y);
      doc.text(String(kartonValue), COLS.uom, y);
      doc.text(String(boxValue), COLS.uom + 8, y);
      doc.text(String(piecesValue), COLS.uom + 16, y);
      doc.text(formatCurrencyAuto(product.harga_jual), COLS.harga, y);

      // Diskon untuk baris pertama
      doc.text(diskon.d1r, COLS.diskon, y);
      doc.text(diskon.d2r, COLS.diskon + 8, y);
      doc.text(diskon.d3r, COLS.diskon + 16, y);
      doc.text(diskon.d2p.nilai, COLS.diskon + 24, y);
      doc.text(diskon.d3p.nilai, COLS.diskon + 34, y);

      // Alasan retur jika diperlukan
      if (isRetur) {
        doc.text(product.keterangan_retur || "-", COLS.alasan, y);
      }

      // Total diskon dan subtotal dengan alignment kanan
      doc.text(totalDiscText, COLS.totalDisc + 19 - totalDiscWidth, y);
      doc.text(subtotalText, COLS.subtotal + 20 - subtotalWidth, y);

      // ======== GAMBAR BARIS TAMBAHAN JIKA DIPERLUKAN ========
      const hasDiskonUom = diskon.d2p.uom !== "" || diskon.d3p.uom !== "";

      if (totalLines > 1 || hasDiskonUom) {
        const effectiveTotalLines = Math.max(totalLines, hasDiskonUom ? 2 : 1);

        // Tambahkan baris-baris selanjutnya
        for (let i = 1; i < effectiveTotalLines; i++) {
          y += LAYOUT.lineHeight; // Menggunakan lineHeight yang diperkecil

          // Tampilkan kode dan nama produk untuk baris berikutnya jika tersedia
          if (i < kodeLines.length) {
            doc.text(kodeLines[i], COLS.kode, y);
          }

          if (i < namaLines.length) {
            doc.text(namaLines[i], COLS.nama, y);
          }

          // Tampilkan UOM di baris kedua
          if (i === 1) {
            if (diskon.d2p.uom !== "") {
              doc.text(diskon.d2p.uom, COLS.diskon + 24, y);
            }

            if (diskon.d3p.uom !== "") {
              doc.text(diskon.d3p.uom, COLS.diskon + 34, y);
            }
          }
        }

        // Tambah sedikit spacing setelah multi-baris (diperkecil)
        y += 0.5;
      }

      // Geser y untuk item berikutnya (diperkecil)
      y += 5;

      // Jika ini item terakhir dan membutuhkan halaman baru untuk footer
      if (
        index === productsWithCalculations.length - 1 &&
        y > LAYOUT.pageHeight - 70
      ) {
        addNewPage(false);
      }
    });

    // ======== GARIS PEMBATAS SETELAH TABEL ========
    y -= 2;
    drawLine(LAYOUT.margin, y, COLS.right, y, [0, 0], 0.1);

    // ======== CATATAN DAN RINGKASAN BIAYA ========
    y += 3;

    // ======== CATATAN DI KIRI BAWAH ========
    doc.setFontSize(9);
    let noteY = y;
    const noteItems = [
      "• Pembayaran dengan Cek/BG dianggap lunas setelah diuangkan",
      "• Barang diterima dengan baik dan benar, maksimal komplain 2X24 jam",
      "• Copy bukan untuk penghasilan",
      "• Penjualan KREDIT",
      "• Pembayaran melalui BG/Tranfer ditunjukan ke PT. Budimas Makmur Mulia",
      "  Dengan Nomor Rek: 783036499 Bank BCA Cabang Veteran",
    ];

    noteItems.forEach((item) => {
      // Cek jika item mengandung nomor rekening
      if (item.includes("783036499")) {
        // Split text untuk memisahkan bagian sebelum dan sesudah nomor rekening
        const parts = item.split("783036499");

        // Tulis bagian pertama dengan font normal
        doc.text(parts[0], LAYOUT.margin, noteY);

        // Hitung posisi x untuk nomor rekening
        const textWidth =
          (doc.getStringUnitWidth(parts[0]) * 9) / doc.internal.scaleFactor;

        // Set font bold dan tulis nomor rekening
        doc.setFont("courier", "bold");
        doc.text("783036499", LAYOUT.margin + textWidth, noteY);

        // Hitung posisi x untuk bagian terakhir
        const rekWidth =
          (doc.getStringUnitWidth("783036499") * 9) / doc.internal.scaleFactor;

        // Kembalikan ke font normal dan tulis bagian terakhir
        doc.setFont("courier", "normal");
        doc.text(parts[1], LAYOUT.margin + textWidth + rekWidth, noteY);
      } else {
        doc.text(item, LAYOUT.margin, noteY);
      }
      noteY += 3;
    });

    // ======== RINGKASAN BIAYA DI KANAN ========
    const summaryX = COLS.right - 80;
    const summaryLabelWidth = 30;

    // Ringkasan biaya
    const summaryItems = [
      {
        label: "Subtotal",
        value: formatCurrencyAuto(grandTotal.subtotal),
        prefix: "",
        yOffset: 0,
      },
      {
        label: "Discount Final",
        value: formatCurrencyAuto(grandTotal.totalDiskon),
        prefix: "- ",
        yOffset: 6, // Diperkecil dari 9 ke 6
      },
      {
        label: "PPN",
        value: formatCurrencyAuto(grandTotal.ppnValue),
        prefix: "+ ",
        yOffset: 6, // Diperkecil dari LAYOUT.sectionSpacing
      },
    ];

    doc.setFontSize(10);

    // Render ringkasan biaya
    let summaryY = y;
    summaryItems.forEach((item) => {
      summaryY += item.yOffset;
      doc.text(item.label, summaryX, summaryY);
      doc.text(":", summaryX + summaryLabelWidth, summaryY);
      doc.text(
        `${item.prefix}${item.value}`,
        COLS.right + (item.prefix ? 3 : 2),
        summaryY,
        {
          align: "right",
        }
      );
    });

    // Update y position
    y = summaryY;

    // ======== GARIS PEMBATAS SEBELUM TOTAL ========
    y += 7;
    drawLine(LAYOUT.margin, y - 3, COLS.right, y - 3, [0, 0], 0.1); // Diperkecil dari -5 ke -3

    // ======== TERBILANG DAN TOTAL ========
    // Terbilang
    doc.setFontSize(8);
    doc.setFont("courier", "italic");

    // Dapatkan teks terbilang
    const terbilangText = numberToWords(formatCurrencyAuto(grandTotal.total));
    const maxTerbilangWidth = summaryX - LAYOUT.margin - 10;

    // Bagi teks terbilang menjadi beberapa baris
    const terbilangLines = wrapText(`(${terbilangText})`, maxTerbilangWidth, 8);

    // Tampilkan teks terbilang
    let terbilangY = y;
    terbilangLines.forEach((line) => {
      doc.text(line, LAYOUT.margin, terbilangY);
      terbilangY += 3;
    });
    y += 1;
    // Total (posisi tidak berubah)
    doc.setFontSize(11);
    doc.setFont("courier", "bold");
    doc.text("Total", summaryX, y);
    doc.text(":", summaryX + summaryLabelWidth, y);
    doc.text(`Rp ${formatCurrencyAuto(grandTotal.total)}`, COLS.right + 3, y, {
      align: "right",
    });

    // ======== FOOTER DAN TANDA TANGAN ========
    y += 10;
    doc.setFontSize(8);
    doc.setFont("courier", "normal");

    // Footer info
    const footerItems = [
      `Jam : ${getDateNow(new Date(), true, true)}/${
        fakturInfo?.status_order_str || ""
      }/${fakturInfo?.nama_fakturist || "admin fakturist"}`,
      `Sales : ${fakturInfo?.nama_sales || ""}`,
      fakturInfo?.no_order || "",
    ];

    footerItems.forEach((item) => {
      doc.text(item, LAYOUT.margin, y);
      y += LAYOUT.lineHeight;
    });

    // ======== QR CODE DAN TEXT DISCLAIMER ========
    y += 6;

    const qrCodeText = fakturInfo?.nomor_faktur || "NO_FAKTUR";

    const addQRCodeAndDisclaimer = async () => {
      try {
        // Generate QR code
        const svgElement = await generateQRCodeSVG(qrCodeText);

        if (svgElement) {
          // Hitung dimensi PDF berdasarkan panjang text
          const textLength = qrCodeText.length;
          let pdfWidth, pdfHeight;

          if (textLength <= 10) {
            pdfWidth = 20;
            pdfHeight = 20;
          } else if (textLength <= 15) {
            pdfWidth = 22;
            pdfHeight = 22;
          } else if (textLength <= 20) {
            pdfWidth = 25;
            pdfHeight = 25;
          } else {
            pdfWidth = 28;
            pdfHeight = 28;
          }

          // Convert SVG to PDF using svg2pdf
          await svg2pdf(svgElement, doc, {
            x: LAYOUT.margin - 3,
            y: y - 8,
            width: pdfWidth,
            height: pdfHeight,
          });
          console.log("SVG QR Code added successfully");
        } else {
          console.log("QR Code generation failed, using fallback");
          // Fallback to text
          doc.setFontSize(10);
          doc.text(`QR Code: ${qrCodeText}`, LAYOUT.margin, y - 5);
        }

        // Text disclaimer
        doc.setFontSize(6);
        doc.setFont("courier", "normal");
        doc.text(
          "*Faktur ini sah dan diproses oleh komputer",
          LAYOUT.margin,
          y + 18
        );
      } catch (error) {
        console.error("Error adding QR code:", error);
        // Fallback to regular text
        doc.setFontSize(8);
        doc.text(`No: ${qrCodeText}`, LAYOUT.margin, y - 2);
        doc.setFontSize(6);
        doc.text(
          "*Faktur ini sah dan diproses oleh komputer",
          LAYOUT.margin,
          y + 2
        );
      }
    };
    // ======== TANDA TANGAN ========
    const signY = y - 8;

    // Posisi kolom tanda tangan
    const signX = COLS.right - 111;
    const signPositions = [
      signX,
      signX + LAYOUT.signWidth + 2,
      signX + (LAYOUT.signWidth + 2) * 2,
      signX + (LAYOUT.signWidth + 2) * 3,
    ];

    // Hormat Kami
    doc.setFontSize(10);
    doc.text("Hormat Kami,", COLS.right - 60, y - 15, { align: "center" });

    // Tambahkan kolom tanda tangan
    const signatureLabels = [
      {
        label: isRetur ? "Outlet" : "Penjualan",
        name: !isRetur ? fakturInfo?.nama_sales || "" : "",
      },
      {
        label: isRetur ? "Saleman" : "Driver",
        name: !isRetur ? fakturInfo?.nama_driver || "" : "",
      },
      { label: isRetur ? "Spv" : "Checker", name: "" },
      { label: isRetur ? "Delivery" : "Penerima", name: "" },
    ];

    signatureLabels.forEach((sig, i) => {
      addSignatureColumn(signPositions[i], sig.label, sig.name);
    });

    // ======== NOMOR HALAMAN (FOOTER ASLI - TIDAK DIUBAH) ========
    const actualTotalPages = currentPageOfThisFaktur;
    const pageNumberY = LAYOUT.pageHeight - 6;

    // Tambahkan nomor halaman dengan jumlah halaman yang sebenarnya
    for (let i = 1; i <= actualTotalPages; i++) {
      const pageIndex = startPageNumber + i - 1;
      doc.setPage(pageIndex);
      doc.setFontSize(8);
      doc.text(
        `Halaman ${i} dari ${actualTotalPages}`,
        LAYOUT.pageWidth / 2,
        pageNumberY,
        { align: "center" }
      );
    }

    // Execute QR code generation dan disclaimer
    await addQRCodeAndDisclaimer();

    // ======== SIMPAN PDF ========
    if (!existingDoc && !skipSave) {
      doc.save(`${filename}.pdf`);
    }

    return {
      doc: doc,
      totalPages: actualTotalPages,
      nextStartPage: currentGlobalPage + 1,
    };
  } catch (error) {
    console.error("Error generating PDF:", error);
    throw error;
  }
};
