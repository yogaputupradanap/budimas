<?php

namespace App\Services;

use App\Models\Perusahaan;
use App\Services\Service;

/**
 * Service Class untuk Mengolah Data Perusahaan.
 * 
 * Untuk mengetahui Fungsi yang Digunakan
 * dalam Memanipulasi Data.
 * @see Model App\Models.
 * 
 * Penyisipan Data Menggunakan Function.
 * @method setData().
 * @see Service App\Services.
 */
class OlahPerusahaan extends Service
{
    /**
     * Mendapatkan Semua Data dari Tabel Perusahaan.
     * @return object (N) Banyak Baris dari Tabel Perusahaan.
     */
    function getAll() {
        return (new Perusahaan)->all();
    }

    /**
     * Mendapatkan Data dari Tabel Perusahaan Berdasarkan Id.
     * @param id Id (Perusahaan).
     * @return object (1) Baris dari Tabel Perusahaan.
     */
    function getDataById($id) {
        return (new Perusahaan)->retrieveById($id);
    }

    /**
     * Memasukkan Data Baru ke dalam Tabel Perusahaan.
     * @param this->data Illuminate\Http\Request
     *        Data Perusahaan Baru yang Akan Dimasukkan.
     * @return bool.
     */
    function insert() {
        return (new Perusahaan)->insert([
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
     * Menyunting Data Berdasarkan Id dari Tabel Perusahaan.
     * @param id Id (Perusahaan).
     * @param this->data Illuminate\Http\Request
     *        Data Perusahaan yang Akan Disunting.
     * @return bool.
     */
    function updateById($id) {
        return (new Perusahaan)->id($id)->update([
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
     * Menghapus Data Berdasarkan Id dari Tabel Perusahaan.
     * @param id Id (Perusahaan).
     * @return bool.
     */
    function deleteById($id) {
        return (new Perusahaan)->id($id)->delete()->check();
    }

}