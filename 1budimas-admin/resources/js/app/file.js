/*
 |--------------------------------------------------------------------------
 | File Handler.
 |--------------------------------------------------------------------------
 |
 | Global File Handler Functions & Configurations Collection.
 |
 */
/**
 * CSV Handler (CSV to JSON)
 * CSV Downloader (Otomatis Mengunduh Resource/File)
 *
 * @param data `json` dengan konten {header:<val>, data:<val>, filename:<val>}
 * @param data `data.header` baris pertama dari data yang berisi nama kolom.
 * @param data `data.data` baris lainnya dari data yang berisi nilai untuk tiap kolom.
 * @param data `data.file_name` nama dari file csv yang akan dibuat.
*/
function csvDownload(data) {
    // Baris Pertama dari Data Berisi Nama Kolom.
    let header = data.header

    // Baris Lainnya Berisi Nilai/Value dari Tiap Kolom.
    let items = data.data.map((item) => { return Object.values(item).toString() });

    // Join Header dan Items ke Dalam satu Array.
    let rows = [header, ...items].join('\n');

    // Membuat Objek Blob (File) dengan Konten Csv.
    let blob = new Blob([rows], { type : 'application/csv' });

    // Membuat Temporary Storage untuk File Csv.
    let url  = URL.createObjectURL(blob);

    // Membuat Perintah Download Otomatis dengan Menggunakan Tag Anchor
    let a           = document.createElement('a');
    a.href          = url; // Lokasi (Temporary Storage) dari File.
    a.download      = data.file_name;
    a.style.display = 'none';

    document.body.appendChild(a);
    a.click();
    a.remove();

    // Menghapus File dari Temporary Storage.
    URL.revokeObjectURL(url);
}
