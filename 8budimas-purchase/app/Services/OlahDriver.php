<?php

namespace App\Services;

use App\Models\Driver;
use App\Models\Armada;
use App\Models\User;
use App\Services\Service;

/**
 * Service Class untuk Mengolah Data Driver.
 * Tabel Driver Memiliki Relasi dengan Tabel
 * Armada dan User.
 * 
 * Untuk mengetahui Fungsi yang Digunakan
 * dalam Memanipulasi Data.
 * @see Model App\Models.
 * 
 * Penyisipan Data Menggunakan Function.
 * @method setData().
 * @see Service App\Services.
 */
class OlahDriver extends Service
{
    /**
     * Mendapatkan Semua Data dari Tabel Driver.
     * @return object (N) Banyak Baris dari Tabel Driver.
     */
    function getAll() {
        return (new Driver)->all();
    }

    /**
     * Mendapatkan Data dari Tabel Driver Berdasarkan Id.
     * @param id Id (Driver).
     * @return object (1) Baris dari Tabel Driver.
     */
    function getDataById($id) {
        return (new Driver)->retrieveById($id);
    }

    /**
     * Mendapatkan Semua Data dari Tabel Armada.
     * @return object (N) Banyak Baris dari Tabel Armada.
     */
    function getArmadaList() {
        return (new Armada)->all();
    }

    /**
     * Mendapatkan Semua Data dari Tabel User.
     * @return object (N) Banyak Baris dari Tabel User.
     */
    function getUserList() {
        return (new User)->getJabatanDriver();
    }

    /**
     * Memasukkan Data Baru ke dalam Tabel Driver.
     * @param this->data Illuminate\Http\Request
     *        Data Driver Baru yang Akan Dimasukkan.
     * @return bool.
     */
    function insert() {
        return (new Driver)->insert([
            'id_user'     => $this->data->idUser,
            'id_armada'   => $this->data->idArmada,
            'id_wilayah1' => $this->data->wilayah1,
            'id_wilayah2' => $this->data->wilayah2
        ])->check();
    }

    /**
     * Menyunting Data Berdasarkan Id dari Tabel Driver.
     * @param id Id (Driver).
     * @param this->data Illuminate\Http\Request
     *        Data Driver yang Akan Disunting.
     * @return bool.
     */
    function updateById($id) {
        return (new Driver)->id($id)->update([
            'id_user'      => $this->data->idUser,
            'id_armada'    => $this->data->idArmada,
            'id_wilayah1'  => $this->data->wilayah1,
            'id_wilayah2'  => $this->data->wilayah2
        ])->check();
    }

    /**
     * Menghapus Data Berdasarkan Id dari Tabel Driver.
     * @param id Id (Driver).
     * @return bool.
     */
    function deleteById($id) {
        return (new Driver)->id($id)->delete()->check();
    }

}