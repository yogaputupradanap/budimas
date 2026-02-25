<?php

namespace App\Services;

use App\Models\ProdukBrand;
use App\Services\Service;

/**
 * Service Class untuk Mengolah Data ProdukBrand.
 * 
 * Untuk mengetahui Fungsi yang Digunakan
 * dalam Memanipulasi Data.
 * @see Model App\Models.
 * 
 * Penyisipan Data Menggunakan Function.
 * @method setData().
 * @see Service App\Services.
 */
class OlahProdukBrand extends Service
{
    /**
     * Mendapatkan Semua Data dari Tabel ProdukBrand.
     * @return object (N) Banyak Baris dari Tabel ProdukBrand.
     */
    function getAll() {
        return (new ProdukBrand)->all();
    }

    /**
     * Mendapatkan Data dari Tabel ProdukBrand Berdasarkan Id.
     * @param id Id (ProdukBrand).
     * @return object (1) Baris dari Tabel ProdukBrand.
     */
    function getDataById($id) {
        return (new ProdukBrand)->retrieveById($id);
    }

    /**
     * Memasukkan Data Baru ke dalam Tabel ProdukBrand.
     * @param this->data Illuminate\Http\Request
     *        Data ProdukBrand Baru yang Akan Dimasukkan.
     * @return bool.
     */
    function insert() {
        return (new ProdukBrand)->insert([
            'nama' => $this->data->nama
        ])->check();
    }

    /**
     * Menyunting Data Berdasarkan Id dari Tabel ProdukBrand.
     * @param id Id (ProdukBrand).
     * @param this->data Illuminate\Http\Request
     *        Data ProdukBrand yang Akan Disunting.
     * @return bool.
     */
    function updateById($id) {
        return (new ProdukBrand)->id($id)->update([
            'nama' => $this->data->nama
        ])->check();
    }
    
    /**
     * Menghapus Data Berdasarkan Id dari Tabel ProdukBrand.
     * @param id Id (ProdukBrand).
     * @return bool.
     */
    function deleteById($id) {
        return (new ProdukBrand)->id($id)->delete()->check();
    }
}