<?php

namespace App\Services;

use App\Models\Plafon;
use App\Models\Customer;
use App\Models\Principal;
use App\Models\ProdukTipeHarga;
use App\Models\Sales;
use App\Models\User;
use App\Services\Service;

/**
 * Service Class untuk Mengolah Data Plafon.
 * Tabel Plafon Memiliki Relasi dengan Tabel
 * Customer, Principal, dan Sales.
 * 
 * Untuk mengetahui Fungsi yang Digunakan
 * dalam Memanipulasi Data.
 * @see Model App\Models.
 * 
 * Penyisipan Data Menggunakan Function.
 * @method setData().
 * @see Service App\Services.
 */
class OlahPlafon extends Service
{
    /**
     * Mendapatkan Semua Data dari Tabel Plafon.
     * @return object (N) Banyak Baris dari Tabel Plafon.
     */
    function getAll() {
        return (new Plafon)->all();
    }

    /**
     * Mendapatkan Data dari Tabel Plafon Berdasarkan Id.
     * @param id Id (Plafon).
     * @return object (1) Baris dari Tabel Plafon.
     */
    function getDataById($id) {
        return (new Plafon)->retrieveById($id);
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
        return (new Plafon)->getFilteredList([
            'kode'         => $this->data->kode,
            'id_user'      => $this->data->idUser,
            'id_customer'  => $this->data->idCustomer,
            'id_principal' => $this->data->idPrincipal,
        ]);
    }

    /**
     * Mendapatkan Semua Data dari Tabel Customer.
     * @return object (N) Banyak Baris dari Tabel Customer.
     */
    function getCustomerList() {
        return (new Customer)->all();
    }

    /**
     * Mendapatkan Semua Data dari Tabel Principal.
     * @return object (N) Banyak Baris dari Tabel Principal.
     */
    function getPrincipalList() {
        return (new Principal)->all();
    }

    /**
     * Mendapatkan Semua Data dari Tabel Sales.
     * (unused, Mungkin nanti akan digunakan kembali)
     * @return object (N) Banyak Baris dari Tabel Sales.
     */
    function getSalesList() {
        return (new Sales)->all();
    }
    
    /**
     * Mendapatkan Semua Data dari Tabel User.
     * @return object (N) Banyak Baris dari Tabel User.
     */
    function getUserList() {
        return (new User)->getJabatanSales();
    }

    /**
     * Mendapatkan Semua Data dari Tabel ProdukTipeHarga.
     * @return object (N) Banyak Baris dari Tabel User.
     */
    function getProdukTipeHargaList() {
        return (new ProdukTipeHarga)->all();
    }

    /**
     * Memasukkan Data Baru ke dalam Tabel Plafon.
     * @param this->data Illuminate\Http\Request
     *        Data Plafon Baru yang Akan Dimasukkan.
     * @return bool.
     */
    function insert() {
        return (new Plafon)->insert([
            'id_customer'   =>  $this->data->idCustomer,
            'id_principal'  =>  $this->data->idPrincipal,
            'id_user'       =>  $this->data->idUser,
            'limit_bon'     =>  $this->data->limit,
            'kode'          =>  $this->data->kode,
            'top'           =>  $this->data->top,
            'lock_order'    =>  $this->data->lockOrder,
            'id_tipe_harga' =>  $this->data->idTipeHarga
        ])->check();
    }

    /**
     * Menyunting Data Berdasarkan Id dari Tabel Plafon.
     * @param id Id (Plafon).
     * @param this->data Illuminate\Http\Request
     *        Data Plafon yang Akan Disunting.
     * @return bool.
     */
    function updateById($id) {
        return (new Plafon)->id($id)->update([
            'id_customer'   =>  $this->data->idCustomer,
            'id_principal'  =>  $this->data->idPrincipal,
            'id_user'       =>  $this->data->idUser,
            'limit_bon'     =>  $this->data->limit,
            'kode'          =>  $this->data->kode,
            'top'           =>  $this->data->top,
            'lock_order'    =>  $this->data->lockOrder,
            'id_tipe_harga' =>  $this->data->idTipeHarga
        ])->check();
    }

    /**
     * Menghapus Data Berdasarkan Id dari Tabel Plafon.
     * @param id Id (Plafon).
     * @return bool.
     */
    function deleteById($id) {
        return (new Plafon)->id($id)->delete()->check();
    }
}