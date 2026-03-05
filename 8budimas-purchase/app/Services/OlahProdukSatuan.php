<?php

namespace App\Services;

use App\Models\ProdukSatuan;
use App\Services\Service;

/**
 * Service Class untuk Mengolah Data ProdukSatuan.
 * 
 * Untuk mengetahui Fungsi yang Digunakan
 * dalam Memanipulasi Data.
 * @see Model App\Models.
 * 
 * Penyisipan Data Menggunakan Function.
 * @method setData().
 * @see Service App\Services.
 */
class OlahProdukSatuan extends Service
{
    /**
     * Mendapatkan Semua Data dari Tabel ProdukSatuan.
     * @return object (N) Banyak Baris dari Tabel ProdukSatuan.
     */
    function getAll() {
        return (new ProdukSatuan)->all();
    }

    /**
     * Mendapatkan Data dari Tabel ProdukSatuan Berdasarkan Id.
     * @param id Id (ProdukSatuan).
     * @return object (1) Baris dari Tabel ProdukSatuan.
     */
    function getDataById($id) {
        return (new ProdukSatuan)->retrieveById($id);
    }

    /**
     * Memasukkan Data Baru ke dalam Tabel ProdukSatuan.
     * @param this->data Illuminate\Http\Request
     *        Data ProdukSatuan Baru yang Akan Dimasukkan.
     * @return bool.
     */
    function insert() {
        return (new ProdukSatuan)->insert([
            'nama' => $this->data->nama
        ])->check();
    }

    /**
     * Menyunting Data Berdasarkan Id dari Tabel ProdukSatuan.
     * @param id Id (ProdukSatuan).
     * @param this->data Illuminate\Http\Request
     *        Data ProdukSatuan yang Akan Disunting.
     * @return bool.
     */
    function updateById($id) {
        return (new ProdukSatuan)->id($id)->update([
            'nama' => $this->data->nama
        ])->check();
    }
    
    /**
     * Menghapus Data Berdasarkan Id dari Tabel ProdukSatuan.
     * @param id Id (ProdukSatuan).
     * @return bool.
     */
    function deleteById($id) {
        return (new ProdukSatuan)->id($id)->delete()->check();
    }
}