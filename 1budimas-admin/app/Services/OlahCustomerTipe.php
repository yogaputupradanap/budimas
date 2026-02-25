<?php

namespace App\Services;

use App\Models\CustomerTipe;
use App\Services\Service;

/**
 * Service Class untuk Mengolah Data CustomerTipe.
 * 
 * Untuk mengetahui Fungsi yang Digunakan
 * dalam Memanipulasi Data.
 * @see Model App\Models.
 * 
 * Penyisipan Data Menggunakan Function.
 * @method setData().
 * @see Service App\Services.
 */
class OlahCustomerTipe extends Service
{
    /**
     * Mendapatkan Semua Data dari Tabel CustomerTipe.
     * @return object (N) Banyak Baris dari Tabel CustomerTipe.
     */
    function getAll() {
        return (new CustomerTipe)->all();
    }

    /**
     * Mendapatkan Data dari Tabel CustomerTipe Berdasarkan Id.
     * @param id Id (CustomerTipe).
     * @return object (1) Baris dari Tabel CustomerTipe.
     */
    function getDataById($id) {
        return (new CustomerTipe)->retrieveById($id);
    }

    /**
     * Memasukkan Data Baru ke dalam Tabel CustomerTipe.
     * @param this->data Illuminate\Http\Request
     *        Data CustomerTipe Baru yang Akan Dimasukkan.
     * @return bool.
     */
    function insert() {
        return (new CustomerTipe)->insert([
            'nama' => $this->data->nama
        ])->check();
    }

    /**
     * Menyunting Data Berdasarkan Id dari Tabel CustomerTipe.
     * @param id Id (CustomerTipe).
     * @param this->data Illuminate\Http\Request
     *        Data CustomerTipe yang Akan Disunting.
     * @return bool.
     */
    function updateById($id) {
        return (new CustomerTipe)->id($id)->update([
            'nama' => $this->data->nama
        ])->check();
    }

    /**
     * Menghapus Data Berdasarkan Id dari Tabel CustomerTipe.
     * @param id Id (CustomerTipe).
     * @return bool.
     */
    function deleteById($id) {
        return (new CustomerTipe)->id($id)->delete()->check();
    }

}