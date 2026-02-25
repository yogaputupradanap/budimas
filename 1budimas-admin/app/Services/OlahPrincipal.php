<?php

namespace App\Services;

use App\Models\Principal;
use App\Models\Perusahaan;
use App\Services\Service;

/**
 * Service Class untuk Mengolah Data Principal.
 * Tabel Principal Memiliki Relasi dengan Tabel
 * Perusahaan.
 *
 * Untuk mengetahui Fungsi yang Digunakan
 * dalam Memanipulasi Data.
 * @see Model App\Models.
 *
 * Penyisipan Data Menggunakan Function.
 * @method setData().
 * @see Service App\Services.
 */
class OlahPrincipal extends Service
{
    /**
     * Mendapatkan Semua Data dari Tabel Principal.
     * @return object (N) Banyak Baris dari Tabel Principal.
     */
    function getAll() {
        return (new Principal)->all();
    }

    /**
     * Mendapatkan Data dari Tabel Principal Berdasarkan Id.
     * @param id Id (Principal).
     * @return object (1) Baris dari Tabel Principal.
     */
    function getDataById($id) {
        return (new Principal)->retrieveById($id);
    }

    /**
     * Mendapatkan Daftar Data yang Sudah di Filter.
     *
     * @param object|$this->data {
     *      @key string `nama` Nama Principal.
     * }
     * @return bool.
     */
    function getFilteredList() {
        return (new Principal)->getFilteredList([
            'nama' => $this->data->nama,
        ]);
    }

    /**
     * Mendapatkan Semua Data dari Tabel Perusahaan.
     * @return object (N) Banyak Baris dari Tabel Perusahaan.
     */
    function getPerusahaanList() {
        return (new Perusahaan)->all();
    }

    /**
     * Memasukkan Data Baru ke dalam Tabel Principal.
     * @param this->data Illuminate\Http\Request
     *        Data Principal Baru yang Akan Dimasukkan.
     * @return bool.
     */
    function insert() {
        return (new Principal)->insert([
            'nama'          => $this->data->nama,
            'alamat'        => $this->data->alamat,
            'telepon'       => $this->data->telepon,
            'npwp'          => $this->data->npwp,
            'id_wilayah1'   => $this->data->wilayah1,
            'id_wilayah2'   => $this->data->wilayah2,
            'id_wilayah3'   => $this->data->wilayah3,
            'id_wilayah4'   => $this->data->wilayah4,
            'no_rekening'   => $this->data->noRek,
            'pic'           => $this->data->pic,
            'id_perusahaan' => $this->data->idPerusahaan,
            'kode'         => $this->data->kode
        ])->check();
    }

    /**
     * Menyunting Data Berdasarkan Id dari Tabel Principal.
     * @param id Id (Principal).
     * @param this->data Illuminate\Http\Request
     *        Data Principal yang Akan Disunting.
     * @return bool.
     */
    function updateById($id) {
        return (new Principal)->id($id)->update([
            'nama'          => $this->data->nama,
            'alamat'        => $this->data->alamat,
            'telepon'       => $this->data->telepon,
            'npwp'          => $this->data->npwp,
            'id_wilayah1'   => $this->data->wilayah1,
            'id_wilayah2'   => $this->data->wilayah2,
            'id_wilayah3'   => $this->data->wilayah3,
            'id_wilayah4'   => $this->data->wilayah4,
            'no_rekening'   => $this->data->noRek,
            'pic'           => $this->data->pic,
            'id_perusahaan' => $this->data->idPerusahaan,
            'kode'          => $this->data->kode
        ])->check();
    }

    /**
     * Menghapus Data Berdasarkan Id dari Tabel Principal.
     * @param id Id (Principal).
     * @return bool.
     */
    function deleteById($id) {
        return (new Principal)->id($id)->delete()->check();
    }

}
