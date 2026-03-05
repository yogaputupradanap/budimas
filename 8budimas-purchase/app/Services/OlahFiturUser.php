<?php

namespace App\Services;

use App\Models\UserAkses;
use App\Models\Fitur;
use App\Models\User;
use App\Services\Service;

/**
 * Service Class untuk Mengolah Data UserAkses.
 * Tabel UserAkses Memiliki Relasi dengan Tabel
 * Fitur dan User.
 * 
 * Untuk mengetahui Fungsi yang Digunakan
 * dalam Memanipulasi Data.
 * @see Model App\Models.
 * 
 * Penyisipan Data Menggunakan Function.
 * @method setData().
 * @see Service App\Services.
 */
class OlahFiturUser extends Service
{
    /**
     * Mendapatkan Semua Data dari Tabel UserAkses.
     * @return object (N) Banyak Baris dari Tabel UserAkses.
     */
    function getAll() {
        return (new UserAkses)->getUserDistinctList();
    }

    /**
     * Mendapatkan Data dari Tabel UserAkses Berdasarkan Id.
     * @param id Id (UserAkses).
     * @return object (1) Baris dari Tabel UserAkses.
     */
    function getListByIdUser($id) {
        return (new UserAkses)->getListByIdUser($id);
    }

    /**
     * Mendapatkan Data dari Tabel Fitur Berdasarkan Id.
     * @param id Id (Fitur).
     * @return object (1) Baris dari Tabel Fitur.
     */
    function getListTersedia($id) {
        return (new Fitur)->getFiturUserTersedia($id);
    }

    /**
     * Mendapatkan Data dari Tabel User Berdasarkan Id.
     * @param id Id (User).
     * @return object (1) Baris dari Tabel User.
     */
    function getUserDataById($id) {
        return (new User)->retrieveById($id);
    }

    /**
     * Memasukkan Data Baru ke dalam Tabel UserAkses.
     * @param this->data Illuminate\Http\Request
     *        Data UserAkses Baru yang Akan Dimasukkan.
     * @return bool.
     */
    function insert() {
        return (new UserAkses)->insert([
            'id_user'  => $this->data->idUser,
            'id_fitur' => $this->data->idFitur,
        ])->check();
    }

    /**
     * Menghapus Data Berdasarkan Id dari Tabel UserAkses.
     * @param id Id (UserAkses).
     * @return bool.
     */
    function deleteById($id) {
        return (new UserAkses)->id($id)->delete()->check();
    }

}