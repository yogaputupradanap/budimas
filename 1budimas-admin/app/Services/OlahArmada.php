<?php

namespace App\Services;

use App\Models\Armada;
use App\Models\ArmadaTipe;
use App\Models\Cabang;
use App\Services\Service;

/**
 * Service Class untuk Mengolah Data Armada.
 * Tabel Armada Memiliki Relasi dengan Tabel
 * ArmadaTipe dan Cabang.
 * 
 * Untuk mengetahui Fungsi yang Digunakan
 * dalam Memanipulasi Data.
 * @see Model App\Models.
 * 
 * Penyisipan Data Menggunakan Function.
 * @method setData().
 * @see Service App\Services.
 */
class OlahArmada extends Service
{
    /**
     * Mendapatkan Semua Data dari Tabel Armada.
     * @return object (N) Banyak Baris dari Tabel Armada.
     */
    function getAll() {
        return (new Armada)->all();
    }

    /**
     * Mendapatkan Data dari Tabel Armada Berdasarkan Id.
     * @param id Id (Armada).
     * @return object (1) Baris dari Tabel Armada.
     */
    function getDataById($id) {
        return (new Armada)->retrieveById($id);
    }

    /**
     * Mendapatkan Semua Data dari Tabel Cabang.
     * @return object (N) Banyak Baris dari Tabel Cabang.
     */
    function getCabangList() {
        return (new Cabang)->all();
    }

    /**
     * Mendapatkan Semua Data dari Tabel ArmadaTipe.
     * @return object (N) Banyak Baris dari Tabel ArmadaTipe.
     */
    function getTipeList() {
        return (new ArmadaTipe)->all();
    }

    /**
     * Memasukkan Data Baru ke dalam Tabel Armada.
     * @param this->data Illuminate\Http\Request
     *        Data Armada Baru yang Akan Dimasukkan.
     * @return bool.
     */
    function insert() {
        return (new Armada)->insert([
            'id_cabang'    => $this->data->idCabang,
            'id_tipe'      => $this->data->idTipe,
            'id_status'    => $this->data->idStatus,
            'nama'         => $this->data->nama,
            'no_pelat'     => $this->data->noPelat,
            'kubikasi'     => $this->data->kubikasi,
            'tanggal_stnk' => $this->data->tanggalStnk,
            'tanggal_uji'  => $this->data->tanggalUji,
            'keterangan'   => $this->data->keterangan
        ])->check();
    }

    /**
     * Menyunting Data Berdasarkan Id dari Tabel Armada.
     * @param id Id (Armada).
     * @param this->data Illuminate\Http\Request
     *        Data Armada yang Akan Disunting.
     * @return bool.
     */
    function updateById($id) {
        return (new Armada)->id($id)->update([
            'id_cabang'    => $this->data->idCabang,
            'id_tipe'      => $this->data->idTipe,
            'id_status'    => $this->data->idStatus,
            'nama'         => $this->data->nama,
            'no_pelat'     => $this->data->noPelat,
            'kubikasi'     => $this->data->kubikasi,
            'tanggal_stnk' => $this->data->tanggalStnk,
            'tanggal_uji'  => $this->data->tanggalUji,
            'keterangan'   => $this->data->keterangan
        ])->check();
    }

    /**
     * Menghapus Data Berdasarkan Id dari Tabel Armada.
     * @param id Id (Armada).
     * @return bool.
     */
    function deleteById($id) {
        return (new Armada)->id($id)->delete()->check();
    }
}