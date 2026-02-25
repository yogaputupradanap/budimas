<?php

namespace App\Services;

use App\Models\Import;
use App\Services\Service;

/**
 * Service Class untuk Melakukan Import Data.
 *
 * Untuk mengetahui Fungsi yang Digunakan
 * dalam Memanipulasi Data.
 * @see App\Models\Model.
 *
 * Penyisipan Data Menggunakan Function.
 * @method setData().
 * @see App\Services\Service.
 */
class ImportData extends Service
{
    /**
     * Bulk Insert Data ke Table (Berdasarkan Opsi).
     * Note: Gunakan Multipart Request Agar File bisa
     *       Diterima.
     *
     * @param object|$this->data {
     *      @key int `opsi` dari Table yang Dipilih.
     *      @key blob `file` Berisi Data yang Akan Dimasukkan.
     *                       Format dari File adalah CSV.
     * }.
     *
     * @return bool.
     */
    function insert()
    {
        $file = $this->data->file('file');
        $fileName = $file->getClientOriginalName();
        $fileContent = fopen($file->path(), 'r');

        $table = $this->getTableFromOpsi($this->data->opsi);

        $import = new Import($table);
        $import->attach($fileName, $fileContent);

        if ($this->validateFileName($fileName, $this->data->opsi) && $this->validateHeaderColumns($fileContent, $this->data->opsi)) {
            try {
                $result = $import->upload();
                // \Log::info('Import successful: ' . json_encode($result));
                return $result;  // request baru dikirim di sini
            } catch (\Exception $e) {
                // \Log::error("Import failed: " . $e->getMessage());
                throw new \Exception($e->getMessage());
            }
        }
    }

    /**
     * Mendapatkan Daftar Keterangan dari Format Kolom dari Table.
     *
     * @param object|$this->data {
     *      @key int `opsi` dari Table yang Dipilih.
     * }
     *
     * @return array.
     */
    function getNamaKolomList()
    {
        $opsi = $this->data->opsi;
        $table = $this->getTableFromOpsi($opsi);  // Implement this method to map opsi to table names
        return (new Import($table))->getNamaKolom($opsi);
    }

    /**
     * Get table name from opsi.
     *
     * @param int $opsi
     * @return string
     */
    function getTableFromOpsi($opsi)
    {
        switch ($opsi) {
            case 1:
                return 'cabang';
            case 2:
                return 'perusahaan';
            case 3:
                return 'principal';
            case 4:
                return 'customer_tipe';
            case 5:
                return 'customer';
            case 6:
                return 'produk_brand';
            case 7:
                return 'produk_kategori';
            case 8:
                return 'produk';
            case 9:
                return 'armada';
            case 10:
                return 'plafon';
            case 11:
                return 'sales';
            case 12:
                return 'user';
            default:
                throw new \InvalidArgumentException("Invalid opsi: $opsi");
        }
    }

    function validateHeaderColumns($fileContent, $opsi)
    {

        $csv = fgetcsv($fileContent);
        if ($csv === false || count($csv) < 2) {
            throw new \Exception("error : File CSV tidak valid atau kosong.");
        }

        $header = $this->getCsvHeader($fileContent);

        $table = self::getTableFromOpsi($opsi);
        $expectedColumns = (new Import($table))->getNamaKolom($opsi);

        // Normalizer: ambil nama kolom, trim, hapus BOM, spasi->underscore, lowercase
        $normalize = function ($name) {
            // Bila item expected berupa array seperti [$nama, $keterangan], ambil indeks 0
            if (is_array($name)) {
                $name = $name[0] ?? '';
            }
            $name = (string) $name;
            $name = ltrim($name, "\xEF\xBB\xBF");             // strip BOM jika ada
            $name = trim($name);
            $name = preg_replace('/\s+/', '_', $name);         // spasi -> underscore
            $name = strtolower($name);                         // case-insensitive
            return $name;
        };

        $expected = array_map($normalize, $expectedColumns);
        $actual   = array_map($normalize, $header);

        // Samakan jadi set unik
        $expectedSet = array_values(array_unique($expected));
        $actualSet   = array_values(array_unique($actual));

        // Cek kolom yang hilang dan yang tak terduga
        $missing    = array_diff($expectedSet, $actualSet);
        $unexpected = array_diff($actualSet, $expectedSet);

        // Jika ada kolom hilang atau ekstra yang tak dikenali → invalid
        if (!empty($missing) || !empty($unexpected)) {
            // Opsional: logging detail untuk debugging
            // \Log::warning('Import header mismatch', compact('missing','unexpected','expectedSet','actualSet'));
            throw new \Exception("Kolom berikut tidak ada atau tidak sesuai " .
                (!empty($missing) ? 'Hilang: ' . implode(', ', $missing) . '. ' : '') .
                (!empty($unexpected) ? 'Tak terduga: ' . implode(', ', $unexpected) . '.' : '')
            );
        }

        return true;
    }

    function validateFileName($fileName, $opsi)
    {

        try {
            $fileName = explode('-', $fileName);
            $fileName = $fileName[1];
            $expectedName = $this->getTableFromOpsi($opsi);

            if (strpos($fileName, $expectedName) === false) {
                throw new \Exception("Data tidak sesuai");
            }

            return true;
        } catch (\Exception $e) {
            throw new \Exception("Data tidak sesuai");
        }
    }


    private function getCsvHeader($fileContent, string $delimiter = ','): array
    {
        if (!is_resource($fileContent)) {
            throw new \InvalidArgumentException('fileContent harus resource stream');
        }

        $pos = ftell($fileContent);      // simpan posisi sekarang
        rewind($fileContent);            // baca dari awal

        $header = fgetcsv($fileContent, 0, $delimiter);
        if ($header === false) {
            throw new \Exception("File CSV tidak valid atau kosong.");
        }

        // hapus BOM dan trim masing-masing kolom header
        if (isset($header[0])) {
            $header[0] = preg_replace('/^\xEF\xBB\xBF/', '', (string)$header[0]);
        }
        $header = array_map(static function ($h) {
            return trim((string)$h);
        }, $header);

        fseek($fileContent, $pos);       // kembalikan pointer ke posisi semula
        return $header;
    }
}
