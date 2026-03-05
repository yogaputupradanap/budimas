<?php

namespace App\Services;

use App\Models\Wilayah;
use App\Services\Service;  

/**
 * Service Class untuk Mengolah Data Wilayah.
 * 
 * Untuk mengetahui Fungsi yang Digunakan
 * dalam Memanipulasi Data.
 * @see Model App\Models.
 * 
 * Penyisipan Data Menggunakan Function.
 * @method setData().
 * @see Service App\Services.
 */
class OpsiWilayah extends Service
{
    /**
     * Mendapatkan Semua Data dari Tabel Wilayah1.
     * @return object (N) Banyak Baris dari Tabel Wilayah1.
     */
    function getProvinsi() {
        return (new Wilayah(1))->all();
    }

    /**
     * Mendapatkan Data dari Tabel Wilayah2 Berdasarkan Id.
     * @param id Id (Wilayah1).
     * @return object (1) Baris dari Tabel Wilayah2.
     */ 
    function getKabupatenKota($id) {
        return (new Wilayah(2))->where(["id_wilayah1", "=", $id])
               ->orderBy('id')->select()->get();
    }

    /**
     * Mendapatkan Data dari Tabel Wilayaha3 Berdasarkan Id.
     * @param id Id (Wilayaha2).
     * @return object (1) Baris dari Tabel Wilayaha3.
     */ 
    function getKecamatan($id) {
        return (new Wilayah(3))->where(["id_wilayah2", "=", $id])
               ->orderBy('id')->select()->get();
    }
    
    /**
     * Mendapatkan Data dari Tabel Wilayah4 Berdasarkan Id.
     * @param id Id (Wilayah3).
     * @return object (1) Baris dari Tabel Wilayah4.
     */ 
    function getKelurahan($id) {
        return (new Wilayah(4))->where(["id_wilayah3", "=", $id])
               ->orderBy('id')->select()->get();
    }
}