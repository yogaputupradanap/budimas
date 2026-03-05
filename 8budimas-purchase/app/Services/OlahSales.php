<?php

namespace App\Services;

use App\Models\Sales;
use App\Models\Principal;
use App\Models\User;
use App\Models\SalesTipe;
use App\Services\Service;
use Illuminate\Support\Facades\Auth;

/**
 * Service Class untuk Mengolah Data Sales.
 * Tabel Sales Memiliki Relasi dengan Tabel
 * Principal, User dan SalesTipe.
 * 
 * Untuk mengetahui Fungsi yang Digunakan
 * dalam Memanipulasi Data.
 * @see Model App\Models.
 * 
 * Penyisipan Data Menggunakan Function.
 * @method setData().
 * @see Service App\Services.
 */
class OlahSales extends Service
{
    /**
     * Mendapatkan Semua Data dari Tabel Sales.
     * @return object (N) Banyak Baris dari Tabel Sales.
     */
    function getAll() {
        return (new Sales)->all();
    }
    
    /**
     * Mendapatkan Data dari Tabel Sales Berdasarkan Id.
     * @param id Id (Sales).
     * @return object (1) Baris dari Tabel Sales.
     */
    function getDataById($id) {
        return (new Sales)->retrieveById($id);
    }

    /**
     * Mendapatkan Data dari Tabel Sales Berdasarkan Id.
     * @param id Id (Sales).
     * @return object (1) Baris dari Tabel Sales.
     */
    function getDataById2($id) {
        return (new User)->getDataJabatanSalesById($id);
    }

    /**
     * Mendapatkan Daftar Data yang Sudah di Filter.
     * 
     * @param object|$this->data { 
     *      @key string `nik` Nomer Induk User. 
     *      @key string `nama` Nama User. 
     * }
     * @return bool.
     */
    function getFilteredList() {
        return (new User)->getFilteredList([
            'id_jabatan' => '4',
            'nik'        => $this->data->nik,
            'nama'       => $this->data->nama,
        ]);
    }

    /**
     * Mendapatkan Semua Data dari Tabel Principal.
     * @return object (N) Banyak Baris dari Tabel Principal.
     */
    function getPrincipalList() {
        return (new Principal)->all();
    }

    /**
     * Mendapatkan Semua Data dari Tabel User.
     * @return object (N) Banyak Baris dari Tabel User.
     */
    function getUserList() {
        return (new User)->getJabatanSales();
    }

    /**
     * Mendapatkan Semua Data dari Tabel SalesTipe.
     * @return object (N) Banyak Baris dari Tabel SalesTipe.
     */
    function getTipeList() {
        return (new SalesTipe)->all();
    }

    /**
     * Memasukkan Data Baru ke dalam Tabel Sales.
     * @param this->data Illuminate\Http\Request
     *        Data Sales Baru yang Akan Dimasukkan.
     * @return bool.
     */
    function insert() {
        return (new Sales)->insert([
            'id_user'      => $this->data->idUser,
            'id_principal' => $this->data->idPrincipal,
            'id_wilayah1'  => $this->data->wilayah1,
            'id_wilayah2'  => $this->data->wilayah2,
            'id_tipe'      => $this->data->idTipe
        ])->check();
    }

    /**
     * Menyunting Data Berdasarkan Id dari Tabel Sales.
     * @param id Id (Sales).
     * @param this->data Illuminate\Http\Request
     *        Data Sales yang Akan Disunting.
     * @return bool.
     */
    function updateById($id) {
        return (new Sales)->id($id)->update([
            'id_user'      => $this->data->idUser,
            'id_principal' => $this->data->idPrincipal,
            'id_wilayah1'  => $this->data->wilayah1,
            'id_wilayah2'  => $this->data->wilayah2,
            'id_tipe'      => $this->data->idTipe
        ])->check();
    }

    /**
     * Menghapus Data Berdasarkan Id dari Tabel Sales.
     * @param id Id (Sales).
     * @return bool.
     */
    function deleteById($id) {
        return (new Sales)->id($id)->delete()->check();
    }

}