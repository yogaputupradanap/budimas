<?php

namespace App\Services;

use App\Models\Budget;
use App\Models\Departemen;
use App\Models\Principal;
use App\Services\Service;

/**
 * Service Class untuk Mengolah Data Budget.
 * Tabel Budget Memiliki Relasi dengan Tabel
 * Departemen dan Principal.
 * 
 * Untuk mengetahui Fungsi yang Digunakan
 * dalam Memanipulasi Data.
 * @see Model App\Models.
 * 
 * Penyisipan Data Menggunakan Function.
 * @method setData().
 * @see Service App\Services.
 */
class OlahBudget extends Service
{
    /**
     * Mendapatkan Semua Data dari Tabel Budget.
     * @return object (N) Banyak Baris dari Tabel Budget.
     */
    function getAll() {
        return (new Budget)->all();
    }

    /**
     * Mendapatkan Data dari Tabel Budget Berdasarkan Id.
     * @param id Id (Budget).
     * @return object (1) Baris dari Tabel Budget.
     */
    function getDataById($id) {
        return (new Budget)->retrieveById($id);
    }

    /**
     * Mendapatkan Semua Data dari Tabel Departemen.
     * @return object (N) Banyak Baris dari Tabel Departemen.
     */
    function getDepartemenList() {
        return (new Departemen)->all();
    }

    /**
     * Mendapatkan Semua Data dari Tabel Principal.
     * @return object (N) Banyak Baris dari Tabel Principal.
     */
    function getPrincipalList() {
        return (new Principal)->all();
    }

     /**
     * Memasukkan Data Baru ke dalam Tabel Budget.
     * @param this->data Illuminate\Http\Request
     *        Data Budget Baru yang Akan Dimasukkan.
     * @return bool.
     */
    function insert() {
        return (new Budget)->insert([
            'id_principal'  => $this->data->idPrincipal,
            'id_departemen' => $this->data->idDepartemen,
            'bulan'         => $this->data->bulan,
            'tahun'         => $this->data->tahun,
            'nominal'       => $this->data->nominal,
            'limit'         => $this->data->limit,
            'kode'          => $this->data->kode,
            'keterangan'    => $this->data->keterangan
        ])->check();
    }

    /**
     * Menyunting Data Berdasarkan Id dari Tabel Budget.
     * @param id Id (Budget).
     * @param this->data Illuminate\Http\Request
     *        Data Budget yang Akan Disunting.
     * @return bool.
     */
    function updateById($id) {
        return (new Budget)->id($id)->update([
            'id_principal'  => $this->data->idPrincipal,
            'id_departemen' => $this->data->idDepartemen,
            'bulan'         => $this->data->bulan,
            'tahun'         => $this->data->tahun,
            'nominal'       => $this->data->nominal,
            'limit'         => $this->data->limit,
            'kode'          => $this->data->kode,
            'keterangan'    => $this->data->keterangan
        ])->check();
    }

    /**
     * Menghapus Data Berdasarkan Id dari Tabel Budget.
     * @param id Id (Budget).
     * @return bool.
     */
    function deleteById($id) {
        return (new Budget)->id($id)->delete()->check();
    }
}