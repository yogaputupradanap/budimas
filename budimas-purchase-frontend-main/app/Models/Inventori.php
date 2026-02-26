<?php

namespace App\Models;
use Illuminate\Support\Facades\Session;

class Inventori extends Model {
    /** 
     * Setting Up Intial API Endpoint. 
     */
    public function __construct(){
        parent::__construct();
        $this->endpoint = "/api/base/inventori";
    }

    /**
     * Insert Data Baru.
     * 
     * @method Override.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\Inventori Instance.
     */
    public function insert($data) {
        if (!is_object($data)) {
            $data = (object) $data;
        }
        return parent::insert([
            'id_transaksi'      => $data->idTransaksi     ?? '',
            'id_cabang'         => $data->idCabang        ?? '',
            'id_user'           => $data->idUser          ?? '',
            'id_tipe_transaksi' => $data->idTipeTransaksi ?? '',
            'id_tipe_stok'      => $data->idTipeStok      ?? '',
            'id_produk'         => $data->idProduk        ?? '',
            'id_produk_uom'     => $data->idProdukUom     ?? '',
            'nama_produk'       => $data->namaProduk      ?? '',
            'stok_awal'         => $data->stokAwal        ?? '',
            'stok_peralihan'    => $data->stokPeralihan   ?? '',
            'stok_akhir'        => $data->stokAkhir       ?? '',
            'valuasi'           => $data->valuasi         ?? '',
        ]);
    }

    /**
     * Insert Data Baru.
     * 
     * @method Override.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\Inventori Instance.
     */
    public function insertByProdukIndex($data, $i) {
        return parent::insert([
            'id_transaksi'      => $data->idTransaksi     ?? '',
            'id_cabang'         => $data->idCabang        ?? '',
            'id_user'           => $data->idUser          ?? '',
            'id_tipe_transaksi' => $data->idTipeTransaksi ?? '',
            'id_tipe_stok'      => $data->idTipeStok      ?? '',
            'id_produk'         => $data->idProduk[$i]    ?? '',
            'id_produk_uom'     => $data->idProdukUom     ?? '',
            'nama_produk'       => $data->namaProduk[$i]  ?? '',
            'stok_awal'         => $data->stokAwal        ?? '',
            'stok_peralihan'    => $data->stokPeralihan   ?? '',
            'stok_akhir'        => $data->stokAkhir       ?? '',
            'valuasi'           => $data->valuasi         ?? '',
            'tanggal'           => $data->tanggal         ?? '',
            'waktu'             => $data->waktu           ?? '',
        ]);
    }
}