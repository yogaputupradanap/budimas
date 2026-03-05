<?php

namespace App\Services;

use App\Models\ProdukHarga;
use App\Models\Produk;
use App\Models\CustomerTipe;
use App\Services\Service;

/**
 * Service Class untuk Mengolah Data ProdukHarga.
 * Tabel ProdukHarga Memiliki Relasi dengan Tabel
 * CustomerTipe dan Produk.
 * 
 * Untuk mengetahui Fungsi yang Digunakan
 * dalam Memanipulasi Data.
 * @see Model App\Models.
 * 
 * Penyisipan Data Menggunakan Function.
 * @method setData().
 * @see Service App\Services.
 */
class OlahProdukHarga extends Service
{
    /**
     * Mendapatkan Semua Data dari Tabel ProdukHarga.
     * @return object (N) Banyak Baris dari Tabel ProdukHarga.
     */
    function getAll() {
        return (new ProdukHarga)->all();
    }

    /**
     * Mendapatkan Data dari Tabel ProdukHarga Berdasarkan Id.
     * @param id Id (ProdukHarga).
     * @return object (1) Baris dari Tabel ProdukHarga.
     */
    function getDataById($id) {
        return (new ProdukHarga)->retrieveById($id);
    }

    /**
     * Mendapatkan Semua Data dari Tabel Produk.
     * @return object (N) Banyak Baris dari Tabel Produk.
     */
    function getProdukList() {
        return (new Produk)->all();
    }

    /**
     * Mendapatkan Semua Data dari Tabel CustomerTipe.
     * @return object (N) Banyak Baris dari Tabel CustomerTipe.
     */
    function getCustomerTipeList() {
        return (new CustomerTipe)->all();
    }

    /**
     * Memasukkan Data Baru ke dalam Tabel ProdukHarga.
     * @param this->data Illuminate\Http\Request
     *        Data ProdukHarga Baru yang Akan Dimasukkan.
     * @return bool.
     */
    function insert() {
        return (new ProdukHarga)->insert([
            'id_produk'        => $this->data->idProduk,
            'id_customer_tipe' => $this->data->idCustomerTipe,
            'harga'            => $this->data->harga
        ])->check();
    }

    /**
     * Menyunting Data Berdasarkan Id dari Tabel ProdukHarga.
     * @param id Id (ProdukHarga).
     * @param this->data Illuminate\Http\Request
     *        Data ProdukHarga yang Akan Disunting.
     * @return bool.
     */
    function updateById($id) {
        return (new ProdukHarga)->id($id)->update([
            'id_produk'        => $this->data->idProduk,
            'id_customer_tipe' => $this->data->idCustomerTipe,
            'harga'            => $this->data->harga
        ])->check();
    }
    
    /**
     * Menghapus Data Berdasarkan Id dari Tabel ProdukHarga.
     * @param id Id (ProdukHarga).
     * @return bool.
     */
    function deleteById($id) {
        return (new ProdukHarga)->id($id)->delete()->check();
    }
}