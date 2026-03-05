<?php

namespace App\Services;

use App\Models\Cabang;
use App\Services\Service;

/**
 * Service Class untuk Mengolah Data Cabang.
 * 
 * Untuk mengetahui Fungsi yang Digunakan
 * dalam Memanipulasi Data.
 * @see Model App\Models.
 * 
 * Penyisipan Data Menggunakan Function.
 * @method setData().
 * @see Service App\Services.
 */
class OlahCabang extends Service
{
    /**
     * Mendapatkan Semua Data dari Tabel Cabang.
     * @return object (N) Banyak Baris dari Tabel Cabang.
     */
    function getAll() {
        return (new Cabang)->all();
    }

    /**
     * Mendapatkan Data dari Tabel Cabang Berdasarkan Id.
     * @param id Id (Cabang).
     * @return object (1) Baris dari Tabel Cabang.
     */
    function getDataById($id) {
        return (new Cabang)->retrieveById($id);
    }

    /**
     * Memasukkan Data Baru ke dalam Tabel Cabang.
     * @param this->data Illuminate\Http\Request
     *        Data Cabang Baru yang Akan Dimasukkan.
     * @return bool.
     */
    function insert() {
        return (new Cabang)->insert([
            'nama'        => $this->data->nama,
            'alamat'      => $this->data->alamat,
            'telepon'     => $this->data->telepon,
            'npwp'        => $this->data->npwp,
            'id_wilayah1' => $this->data->wilayah1,
            'id_wilayah2' => $this->data->wilayah2,
            'id_wilayah3' => $this->data->wilayah3,
            'id_wilayah4' => $this->data->wilayah4
        ])->check();
    }

    /**
     * Menyunting Data Berdasarkan Id dari Tabel Cabang.
     * @param id Id (Cabang).
     * @param this->data Illuminate\Http\Request
     *        Data Cabang yang Akan Disunting.
     * @return bool.
     */
    function updateById($id) {
        return (new Cabang)->id($id)->update([
            'nama'        => $this->data->nama,
            'alamat'      => $this->data->alamat,
            'telepon'     => $this->data->telepon,
            'npwp'        => $this->data->npwp,
            'id_wilayah1' => $this->data->wilayah1,
            'id_wilayah2' => $this->data->wilayah2,
            'id_wilayah3' => $this->data->wilayah3,
            'id_wilayah4' => $this->data->wilayah4
        ])->check();
    }

    /**
     * Menghapus Data Berdasarkan Id dari Tabel Cabang.
     * @param id Id (Cabang).
     * @return bool.
     */
    function deleteById($id) {
        return (new Cabang)->id($id)->delete()->check();
    }

}