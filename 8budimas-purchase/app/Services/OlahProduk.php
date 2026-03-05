<?php

namespace App\Services;

use App\Models\Produk;
use App\Models\ProdukBrand;
use App\Models\ProdukKategori;
use App\Models\ProdukSatuan;
use App\Models\Principal;
use App\Services\Service;

/**
 * Service Class untuk Mengolah Data Produk.
 * Tabel Produk Memiliki Relasi dengan Tabel
 * ProdukBrand, ProdukKategori, ProdukSatuan, Principal.
 * 
 * Untuk mengetahui Fungsi yang Digunakan
 * dalam Memanipulasi Data.
 * @see Repository App\Models.
 * 
 * Penyisipan Data Menggunakan Function.
 * @method setData().
 * @see Service App\Services.
 */
class OlahProduk extends Service
{
    /**
     * Mendapatkan Semua Data dari Tabel Produk.
     * @return object (N) Banyak Baris dari Tabel Produk.
     */
    function getAll() {
        return (new Produk)->all();
    }

    /**
     * Mendapatkan Data dari Tabel Produk Berdasarkan Id.
     * @param id Id (Produk).
     * @return object (1) Baris dari Tabel Produk.
     */
    function getDataById($id) {
        return (new Produk)->find($id);
    }

    /**
     * Mendapatkan Semua Data dari Tabel ProdukBrand.
     * @return object (N) Banyak Baris dari Tabel ProdukBrand.
     */
    function getBrandList() {
        return (new ProdukBrand)->all();
    }

    /**
     * Mendapatkan Semua Data dari Tabel ProdukKategori.
     * @return object (N) Banyak Baris dari Tabel ProdukKategori.
     */
    function getKategoriList() {
        return (new ProdukKategori)->all();
    }

    /**
     * Mendapatkan Semua Data dari Tabel ProdukSatuan.
     * @return object (N) Banyak Baris dari Tabel ProdukSatuan.
     */
    function getSatuanList() {
        return (new ProdukSatuan)->all();
    }

    /**
     * Mendapatkan Semua Data dari Tabel Principal.
     * @return object (N) Banyak Baris dari Tabel Principal.
     */
    function getPrincipalList() {
        return (new Principal)->all();
    }

    /**
     * Memasukkan Data Baru ke dalam Tabel Produk.
     * @param this->data Illuminate\Http\Request
     *        Data Produk Baru yang Akan Dimasukkan.
     * @return bool.
     */
    function insert() {
        return (new Produk)->insert([
            'id_principal'    => $this->data->idPrincipal,
            'id_brand'        => $this->data->idBrand,
            'id_kategori'     => $this->data->idKategori,
            'id_status'       => $this->data->idStatus,
            'nama'            => $this->data->nama,
            'kode_sku'        => $this->data->kodeSku,
            'kode_ean'        => $this->data->kodeEan,
            'harga_beli'      => $this->data->hargaBeli,
            'id_satuan'       => $this->data->idSatuan,
            'isi_box'         => $this->data->isiBox,
            'kubikasi_satuan' => $this->data->kubikasiSatuan,
            'kubikasi_box'    => $this->data->kubikasiBox,
            'keterangan'      => $this->data->keterangan
        ])->check();
    }

    /**
     * Menyunting Data Berdasarkan Id dari Tabel Produk.
     * @param id Id (Produk).
     * @param this->data Illuminate\Http\Request
     *        Data Produk yang Akan Disunting.
     * @return bool.
     */
    function updateById($id) {
        return (new Produk)->id($id)->update([
            'id_principal'    => $this->data->idPrincipal,
            'id_brand'        => $this->data->idBrand,
            'id_kategori'     => $this->data->idKategori,
            'id_status'       => $this->data->idStatus,
            'nama'            => $this->data->nama,
            'kode_sku'        => $this->data->kodeSku,
            'kode_ean'        => $this->data->kodeEan,
            'harga_beli'      => $this->data->hargaBeli,
            'id_satuan'       => $this->data->idSatuan,
            'isi_box'         => $this->data->isiBox,
            'kubikasi_satuan' => $this->data->kubikasiSatuan,
            'kubikasi_box'    => $this->data->kubikasiBox,
            'keterangan'      => $this->data->keterangan
        ])->check();
    }

    /**
     * Menghapus Data Berdasarkan Id dari Tabel Produk.
     * @param id Id (Produk).
     * @return bool.
     */
    function deleteById($id) {
        return (new Produk)->id($id)->delete()->check();
    }

}