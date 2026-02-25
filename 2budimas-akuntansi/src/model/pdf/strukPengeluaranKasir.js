import jsPDF from "jspdf";

/**
 * Cetak struk pengeluaran kasir
 * @param {Object} pengeluaran - Data pengeluaran dari response submitKonfirmasi
 */
export function cetakStrukPengeluaranKasir(pengeluaran, namaKasir = "") {
  const doc = new jsPDF({
    unit: "mm",
    format: [80, 120], // ukuran struk kecil (lebar x tinggi)
  });

  // Format tanggal dan jam
  const tanggal_diberikan = pengeluaran.tanggal_diberikan
    ? pengeluaran.tanggal_diberikan.split(" ")[0].split("-").reverse().join("-")
    : "";

  const jam_diberikan = pengeluaran.tanggal_diberikan
    ? pengeluaran.tanggal_diberikan.split(" ")[1].slice(0, 5)
    : "";

    const tanggal_diajukan = pengeluaran.tanggal_pengajuan
    ? pengeluaran.tanggal_pengajuan.split(" ")[0].split("-").reverse().join("-")
    : "";
    const jam_diajukan = pengeluaran.tanggal_pengajuan
    ? pengeluaran.tanggal_pengajuan.split(" ")[1].slice(0, 5)
    : "";

  // Format jumlah
  const jumlah = pengeluaran.jumlah_acc || pengeluaran.jumlah_pengeluaran || 0;
  const jumlahStr = jumlah.toLocaleString("id-ID");

  // Isi struk
  let y = 10;
  doc.setFontSize(10);
  doc.setFont("courier", "bold");
  doc.text(pengeluaran.nama_perusahaan, 40, y, { align: "center" });
  y += 5;
  doc.text("========================================", 40, y, {
    align: "center",
  });
  y += 6;
  doc.text("BUKTI PENGELUARAN KASIR", 40, y, { align: "center" });
  y += 5;
  doc.setFontSize(15);
  doc.text("----------------------------------------", 40, y, {
    align: "center",
  });
  y += 6;
  doc.setFontSize(8);
  doc.text(`TANGGAL DIAJUKAN : ${tanggal_diajukan}   JAM: ${jam_diajukan}`, 5, y);
  y += 5;
  doc.text(`TANGGAL DIBERIKAN: ${tanggal_diberikan}   JAM: ${jam_diberikan}`, 5, y);
    y += 5;
  doc.text(`NO. PENGELUARAN : ${pengeluaran.no_pengeluaran}`, 5, y);
  y += 5;
  doc.text(`KASIR    : ${namaKasir}`, 5, y);
  y += 5;
  doc.text(`PIC      : ${pengeluaran.pic}`, 5, y);
  y += 5;
  doc.text(`KETERANGAN: ${pengeluaran.keterangan_pengeluaran}`, 5, y);
  y += 5;
  doc.setFontSize(15);
  doc.text("----------------------------------------", 40, y, {
    align: "center",
  });
  doc.setFontSize(8);
  y += 6;
  doc.text(`JUMLAH PENGELUARAN:      ${jumlahStr}`, 5, y);
  y += 7;
  doc.setFontSize(10);
  doc.text("========================================", 40, y, {
    align: "center",
  });
  doc.setFontSize(8);
  y += 6;
  doc.text(`STATUS         : Diberikan`, 5, y);
  y += 5;
  doc.setFontSize(15);
  doc.text("----------------------------------------", 40, y, {
    align: "center",
  });
  doc.setFontSize(8);
  y += 7;
  doc.text("TTD KASIR: _____________", 5, y);
  y += 7;
  doc.text("APPROVAL : _________", 5, y);

  doc.autoPrint();
  window.open(doc.output("bloburl"), "_blank");
}
