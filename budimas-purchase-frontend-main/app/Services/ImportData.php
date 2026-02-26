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
    function insert() {
        $file        = $this->data->file('file');
        $fileName    = $file->getClientOriginalName();
        $fileContent = fopen($file->path(), "r");
        
        switch ($this->data->opsi) {
            case 1: $table = 'cabang';              break;
            case 2: $table = 'perusahaan';          break;
            case 3: $table = 'principal';           break;
            case 4: $table = 'customer_tipe';       break;
            case 5: $table = 'customer';            break;
            case 6: $table = 'produk_brand';        break;
            case 7: $table = 'produk_kategori';     break;
            case 8: $table = 'produk_satuan';       break;
            case 9: $table = 'produk';              break;
        }

        return (new Import($table))->attach($fileName, $fileContent)->check();
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
    function getNamaKolomList() {
        return (new Import())->getNamaKolom($this->data->opsi);
    }
}