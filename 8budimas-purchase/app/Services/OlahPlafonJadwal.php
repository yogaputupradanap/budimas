<?php

namespace App\Services;

use App\Models\PlafonJadwal;
use App\Models\Plafon;
use App\Services\Service;

/**
 * Service Class untuk Mengolah Data PlafonJadwal.
 * Tabel PlafonJadwal Memiliki Relasi dengan Tabel
 * Plafon.
 * 
 * Untuk mengetahui Fungsi yang Digunakan
 * dalam Memanipulasi Data.
 * @see Model App\Models.
 * 
 * Penyisipan Data Menggunakan Function.
 * @method setData().
 * @see Service App\Services.
 */
class OlahPlafonJadwal extends Service
{
     /**
     * Mendapatkan Semua Data dari Tabel PlafonJadwal.
     * @return object (N) Banyak Baris dari Tabel PlafonJadwal.
     */
    function getAll() {
        return (new PlafonJadwal)->all();
    }

    /**
     * Mendapatkan Data dari Tabel PlafonJadwal Berdasarkan Id.
     * @param id Id (PlafonJadwal).
     * @return object (1) Baris dari Tabel PlafonJadwal.
     */
    function getDataById($id) {
        return (new PlafonJadwal)->retrieveById($id);
    }

     /**
     * Mendapatkan Semua Data dari Tabel Plafon.
     * @return object (N) Banyak Baris dari Tabel Plafon.
     */
    function getPlafonList() {
        return (new Plafon)->all();
    }

    /**
     * Memasukkan Data Baru ke dalam Tabel PlafonJadwal.
     * @param this->data Illuminate\Http\Request
     *        Data PlafonJadwal Baru yang Akan Dimasukkan.
     * @return bool.
     */
    function insert() {
        return (new PlafonJadwal)->insert([
            'id_plafon'          => $this->data->idPlafon,
            'id_tipe_kunjungan'  => $this->data->idTipeKunjungan,
            'id_hari'            => $this->data->idHari,
            'id_minggu'          => $this->data->idMinggu,
            'id_status'          => $this->data->idStatus
        ])->check();
    }

    /**
     * Menyunting Data Berdasarkan Id dari Tabel PlafonJadwal.
     * @param id Id (PlafonJadwal).
     * @param this->data Illuminate\Http\Request
     *        Data PlafonJadwal yang Akan Disunting.
     * @return bool.
     */
    function updateById($id) {
        return (new PlafonJadwal)->id($id)->update([
            'id_plafon'          => $this->data->idPlafon,
            'id_tipe_kunjungan'  => $this->data->idTipeKunjungan,
            'id_hari'            => $this->data->idHari,
            'id_minggu'          => $this->data->idMinggu,
            'id_status'          => $this->data->idStatus
        ])->check();
    }

    /**
     * Menghapus Data Berdasarkan Id dari Tabel PlafonJadwal.
     * @param id Id (PlafonJadwal).
     * @return bool.
     */
    function deleteById($id) {
        return (new PlafonJadwal)->id($id)->delete()->check();
    }

}