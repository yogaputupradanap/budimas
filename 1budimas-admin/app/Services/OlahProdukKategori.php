<?php

namespace App\Services;

use App\Models\ProdukKategori;
use App\Services\Service;

/**
 * Service Class untuk Mengolah Data ProdukKategori.
 * 
 * Untuk mengetahui Fungsi yang Digunakan
 * dalam Memanipulasi Data.
 * @see Model App\Models.
 * 
 * Penyisipan Data Menggunakan Function.
 * @method setData().
 * @see Service App\Services.
 */
class OlahProdukKategori extends Service
{
    /**
     * Mendapatkan Semua Data dari Tabel ProdukKategori.
     * @return object (N) Banyak Baris dari Tabel ProdukKategori.
     */
    function getAll() {
        return (new ProdukKategori)->all();
    }

    /**
     * Mendapatkan Data dari Tabel ProdukKategori Berdasarkan Id.
     * @param id Id (ProdukKategori).
     * @return object (1) Baris dari Tabel ProdukKategori.
     */
    function getDataById($id) {
        return (new ProdukKategori)->retrieveById($id);
    }

    /**
     * Memasukkan Data Baru ke dalam Tabel ProdukKategori.
     * @param this->data Illuminate\Http\Request
     *        Data ProdukKategori Baru yang Akan Dimasukkan.
     * @return bool.
     */
    function insert() {
        return (new ProdukKategori)->insert([
            'nama' => $this->data->nama
        ])->check();
    }

    /**
     * Menyunting Data Berdasarkan Id dari Tabel ProdukKategori.
     * @param id Id (ProdukKategori).
     * @param this->data Illuminate\Http\Request
     *        Data ProdukKategori yang Akan Disunting.
     * @return bool.
     */
    function updateById($id) {
        return (new ProdukKategori)->id($id)->update([
            'nama' => $this->data->nama
        ])->check();
    }

    /**
     * Menghapus Data Berdasarkan Id dari Tabel ProdukKategori.
     * @param id Id (ProdukKategori).
     * @return bool.
     */
    function deleteById($id) {
        return (new ProdukKategori)->id($id)->delete()->check();
    }
}