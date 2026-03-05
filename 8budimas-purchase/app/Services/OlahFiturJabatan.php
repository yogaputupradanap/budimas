<?php

namespace App\Services;

use App\Models\JabatanAkses;
use App\Models\Fitur;
use App\Models\Jabatan;
use App\Services\Service;

/**
 * Service Class untuk Mengolah Data JabatanAkses.
 * Tabel JabatanAkses Memiliki Relasi dengan Tabel
 * Fitur dan Jabatan.
 * 
 * Untuk mengetahui Fungsi yang Digunakan
 * dalam Memanipulasi Data.
 * @see Model App\Models.
 * 
 * Penyisipan Data Menggunakan Function.
 * @method setData().
 * @see Service App\Services.
 */
class OlahFiturJabatan extends Service
{
    /**
     * Mendapatkan Semua Data dari Tabel Jabatan.
     * @return object (N) Banyak Baris dari Tabel Jabatan.
     */
    function getAll() {
        return (new Jabatan)->all();
    }

    /**
     * Mendapatkan Data dari Tabel Jabatan Berdasarkan Id.
     * @param id Id (Jabatan).
     * @return object (1) Baris dari Tabel Jabatan.
     */
    function getJabatanDataById($id) {
        return (new Jabatan)->retrieveById($id);
    }

    /**
     * Mendapatkan Data dari Tabel JabatanAkses Berdasarkan Id.
     * @param id Id (JabatanAkses).
     * @return object (1) Baris dari Tabel JabatanAkses.
     */
    function getListByIdJabatan($id) {
        return (new JabatanAkses)->getListByIdJabatan($id);
    }

    /**
     * Mendapatkan Data dari Tabel Fitur Berdasarkan Id.
     * @param id Id (Fitur).
     * @return object (1) Baris dari Tabel Fitur.
     */
    function getListTersedia($id) {
        return (new Fitur)->getFiturJabatanTersedia($id);
    }

    /**
     * Memasukkan Data Baru ke dalam Tabel JabatanAkses.
     * @param this->data Illuminate\Http\Request
     *        Data JabatanAkses Baru yang Akan Dimasukkan.
     * @return bool.
     */
    function insert() {
        return (new JabatanAkses)->insert([
            'id_jabatan' => $this->data->idJabatan,
            'id_fitur'   => $this->data->idFitur,
        ])->check();
    }

    /**
     * Menghapus Data Berdasarkan Id dari Tabel JabatanAkses.
     * @param id Id (JabatanAkses).
     * @return bool.
     */
    function deleteById($id) {
        return (new JabatanAkses)->id($id)->delete()->check();
    }

}