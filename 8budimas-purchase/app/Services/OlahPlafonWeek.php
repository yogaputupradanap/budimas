<?php

namespace App\Services;

use App\Models\PlafonWeek;
use App\Services\Service;

/**
 * Service Class untuk Mengolah Data PlafonWeek.
 * 
 * Untuk mengetahui Fungsi yang Digunakan
 * dalam Memanipulasi Data.
 * @see Model App\Models.
 * 
 * Penyisipan Data Menggunakan Function.
 * @method setData().
 * @see Service App\Services.
 */
class OlahPlafonWeek extends Service
{
    /**
     * Mendapatkan Semua Data dari Tabel PlafonWeek.
     * @return object (N) Banyak Baris dari Tabel PlafonWeek.
     */
    function getAll() {
        return (new PlafonWeek)->all();
    }

    /**
     * Mendapatkan Data dari Tabel PlafonWeek Berdasarkan Id.
     * @param id Id (PlafonWeek).
     * @return object (1) Baris dari Tabel PlafonWeek.
     */
    function getDataById($id) {
        return (new PlafonWeek)->retrieveById($id);
    }

    /**
     * Mendapatkan Data Current Week dari Tabel PlafonWeek.
     * @return object (1) Baris dari Tabel PlafonWeek (minggu).
     */
    function getCurrentWeek() {
        return (new PlafonWeek)->getCurrentWeek();
    }

    /**
     * Memasukkan Data Baru ke dalam Tabel PlafonWeek.
     * @param this->data Illuminate\Http\Request
     *        Data PlafonWeek Baru yang Akan Dimasukkan.
     * @return bool.
     */
    function insert() {
        return (new PlafonWeek)->insert([
            'tanggal' => $this->data->tanggal,
            'minggu'  => $this->data->minggu
        ])->check();
    }
    
    /**
     * Menghapus Data Berdasarkan Id dari Tabel PlafonWeek.
     * @param id Id (PlafonWeek).
     * @return bool.
     */
    function deleteById($id) {
        return (new PlafonWeek)->id($id)->delete()->check();
    }
}