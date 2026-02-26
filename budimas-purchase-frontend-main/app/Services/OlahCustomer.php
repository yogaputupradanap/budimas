<?php

namespace App\Services;

use App\Models\Customer;
use App\Models\Cabang;
use App\Models\CustomerTipe;
use App\Services\Service;

/**
 * Service Class untuk Mengolah Data Customer.
 * Tabel Customer Memiliki Relasi dengan Tabel
 * CustomerTipe dan Cabang.
 * 
 * Untuk mengetahui Fungsi yang Digunakan
 * dalam Memanipulasi Data.
 * @see Model App\Models.
 * 
 * Penyisipan Data Menggunakan Function.
 * @method setData().
 * @see Service App\Services.
 */
class OlahCustomer extends Service
{
    /**
     * Mendapatkan Semua Data dari Tabel Customer.
     * @return object (N) Banyak Baris dari Tabel Customer.
     */
    function getAll() {
        return (new Customer)->all();
    }

    /**
     * Mendapatkan Data dari Tabel Customer Berdasarkan Id.
     * @param id Id (Customer).
     * @return object (1) Baris dari Tabel Customer.
     */
    function getDataById($id) {
        return (new Customer)->retrieveById($id);
    }

    /**
     * Mendapatkan Daftar Data yang Sudah di Filter.
     * 
     * @param object|$this->data { 
     *      @key string `kode` Kode Customer. 
     *      @key string `nama` Nama Customer. 
     * }
     * @return bool.
     */
    function getFilteredList() {
        return (new Customer)->getFilteredList([
            'id_jabatan' => '4',
            'kode'       => $this->data->kode,
            'nama'       => $this->data->nama,
        ]);
    }

    /**
     * Mendapatkan Semua Data dari Tabel Cabang.
     * @return object (N) Banyak Baris dari Tabel Cabang.
     */
    function getCabangList() {
        return (new Cabang)->all();
    }

    /**
     * Mendapatkan Semua Data dari Tabel CustomerTipe.
     * @return object (N) Banyak Baris dari Tabel CustomerTipe.
     */
    function getTipeList() {
        return (new CustomerTipe)->all();
    }

    /**
     * Memasukkan Data Baru ke dalam Tabel Customer.
     * @param this->data Illuminate\Http\Request
     *        Data Customer Baru yang Akan Dimasukkan.
     * @return bool.
     */
    function insert() {
        return (new Customer)->insert([
            'nama'             => $this->data->nama,
            'alamat'           => $this->data->alamat,
            'telepon'          => $this->data->telepon,
            'npwp'             => $this->data->npwp,
            'id_wilayah1'      => $this->data->wilayah1,
            'id_wilayah2'      => $this->data->wilayah2,
            'id_wilayah3'      => $this->data->wilayah3,
            'id_wilayah4'      => $this->data->wilayah4,
            'id_tipe'          => $this->data->idTipe,
            'id_cabang'        => $this->data->idCabang,
            'no_rekening'      => $this->data->noRek,
            'pic'              => $this->data->pic,
            'longitude'        => $this->data->longitude,
            'latitude'         => $this->data->latitude
        ])->check();
    }

    /**
     * Menyunting Data Berdasarkan Id dari Tabel Customer.
     * @param id Id (Customer).
     * @param this->data Illuminate\Http\Request
     *        Data Customer yang Akan Disunting.
     * @return bool.
     */
    function updateById($id) {
        return (new Customer)->id($id)->update([
            'nama'             => $this->data->nama,
            'alamat'           => $this->data->alamat,
            'telepon'          => $this->data->telepon,
            'npwp'             => $this->data->npwp,
            'id_wilayah1'      => $this->data->wilayah1,
            'id_wilayah2'      => $this->data->wilayah2,
            'id_wilayah3'      => $this->data->wilayah3,
            'id_wilayah4'      => $this->data->wilayah4,
            'id_tipe'          => $this->data->idTipe,
            'id_cabang'        => $this->data->idCabang,
            'no_rekening'      => $this->data->noRek,
            'pic'              => $this->data->pic,
            'longitude'        => $this->data->longitude,
            'latitude'         => $this->data->latitude
        ])->check();
    }

    /**
     * Menghapus Data Berdasarkan Id dari Tabel Customer.
     * @param id Id (Customer).
     * @return bool.
     */
    function deleteById($id) {
        return (new Customer)->id($id)->delete()->check();
    }
}