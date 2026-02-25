<?php

namespace App\Services;

use App\Models\ArmadaTipe;
use App\Services\Service;

/**
 * Service Class untuk Mengolah Data ArmadaTipe.
 * 
 * Untuk mengetahui Fungsi yang Digunakan
 * dalam Memanipulasi Data.
 * @see Model App\Models.
 * 
 * Penyisipan Data Menggunakan Function.
 * @method setData().
 * @see Service App\Services.
 */
class OlahArmadaTipe extends Service
{
    /**
     * Mendapatkan Semua Data dari Tabel ArmadaTipe.
     * @return object (N) Banyak Baris dari Tabel ArmadaTipe.
     */
    function getAll() {
        return (new ArmadaTipe)->all();
    }

    /**
     * Mendapatkan Data dari Tabel ArmadaTipe Berdasarkan Id.
     * @param id Id (ArmadaTipe).
     * @return object (1) Baris dari Tabel ArmadaTipe.
     */
    function getDataById($id) {
        return (new ArmadaTipe)->retrieveById($id);
    }

    /**
     * Memasukkan Data Baru ke dalam Tabel ArmadaTipe.
     * @param this->data Illuminate\Http\Request
     *        Data ArmadaTipe Baru yang Akan Dimasukkan.
     * @return bool.
     */
    function insert() {
        return (new ArmadaTipe)->insert([
            'nama' => $this->data->nama
        ])->check();
    }

    /**
     * Menyunting Data Berdasarkan Id dari Tabel ArmadaTipe.
     * @param id Id (ArmadaTipe).
     * @param this->data Illuminate\Http\Request
     *        Data ArmadaTipe yang Akan Disunting.
     * @return bool.
     */
    function updateById($id) {
        return (new ArmadaTipe)->id($id)->update([
            'nama' => $this->data->nama
        ])->check();
    }
    
    /**
     * Menghapus Data Berdasarkan Id dari Tabel ArmadaTipe.
     * @param id Id (ArmadaTipe).
     * @return bool.
     */
    function deleteById($id) {
        return (new ArmadaTipe)->id($id)->delete()->check();
    }
}