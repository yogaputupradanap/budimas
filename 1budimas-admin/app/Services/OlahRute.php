<?php

namespace App\Services;

use App\Models\Rute;
use App\Models\Cabang;
use App\Services\Service;

/**
 * Service Class untuk Mengolah Data Rute.
 * Tabel Rute Memiliki Relasi dengan Tabel
 * Cabang.
 * 
 * Untuk mengetahui Fungsi yang Digunakan
 * dalam Memanipulasi Data.
 * @see Model App\Models.
 * 
 * Penyisipan Data Menggunakan Function.
 * @method setData().
 * @see Service App\Services.
 */
class OlahRute extends Service
{
    /**
     * Mendapatkan Semua Data dari Tabel Rute.
     * @return object (N) Banyak Baris dari Tabel Rute.
     */
    function getAll() {
        return (new Rute)->all();
    }

    /**
     * Mendapatkan Data dari Tabel Rute Berdasarkan Id.
     * @param id Id (Rute).
     * @return object (1) Baris dari Tabel Rute.
     */
    function getDataById($id) {
        return (new Rute)->retrieveById($id);
    }

    /**
     * Mendapatkan Semua Data dari Tabel Cabang.
     * @return object (N) Banyak Baris dari Tabel Cabang.
     */
    function getCabangList() {
        return (new Cabang)->all();
    }

     /**
     * Memasukkan Data Baru ke dalam Tabel Rute.
     * @param this->data Illuminate\Http\Request
     *        Data Rute Baru yang Akan Dimasukkan.
     * @return bool.
     */
    function insert() {
        return (new Rute)->insert([
            'id_cabang'    => $this->data->idCabang,
            'kode'         => $this->data->kode,
            'prioritas'    => $this->data->prioritas
        ])->check();
    }

    /**
     * Menyunting Data Berdasarkan Id dari Tabel Rute.
     * @param id Id (Rute).
     * @param this->data Illuminate\Http\Request
     *        Data Rute yang Akan Disunting.
     * @return bool.
     */
    function updateById($id) {
        return (new Rute)->id($id)->update([
            'id_cabang'    => $this->data->idCabang,
            'kode'         => $this->data->kode,
            'prioritas'    => $this->data->prioritas
        ])->check();
    }

    /**
     * Menghapus Data Berdasarkan Id dari Tabel Rute.
     * @param id Id (Rute).
     * @return bool.
     */
    function deleteById($id) {
        return (new Rute)->id($id)->delete()->check();
    }

}