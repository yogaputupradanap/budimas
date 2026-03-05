<?php

namespace App\Models;
use Illuminate\Support\Facades\Session;

class Stok extends Model {
    /**
     * Setting Up Intial API Endpoint.
     */
    public function __construct(){
        parent::__construct();
        $this->endpoint = "/api/base/stok";
    }

    /**
     * Getting Stok Data Based on Product and Cabang Id.
     * @param  Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return Illuminate\Http\JsonResponse Rows of Purchase Request Detail.
     */
    public function getDataByIdProdukCabang($idProduk, $idCabang) {
        return $this->where(['id_produk', '=', $idProduk])
                    ->where(['id_cabang', '=', $idCabang])
                    ->select()->first();
    }

    /**
     * Insert Data Baru.
     * 
     * @method Override.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\Stok Instance.
     */
    public function insert($data) {
        if (!is_object($data)) {
            $data = (object) $data;
        }
        
        return parent::insert([
            'id_cabang'      => $data->idCabang      ?? '',
            'id_produk'      => $data->idProduk      ?? '',
            'stok_ready'     => $data->stokReady     ?? '',
            'stok_booked'    => $data->stokBooked    ?? '',
            'stok_delivery'  => $data->stokDelivery  ?? '',
            'stok_bad'       => $data->stokBad       ?? '',
            'stok_canvas'    => $data->stokCanvas    ?? '',
            'stok_incoming'  => $data->stokIncoming  ?? '',
            'tanggal_update' => $data->tanggal       ?? '',
            'waktu_update'   => $data->waktu         ?? '',
        ]);
    }

    /**
     * Insert Data Baru.
     * 
     * @method Override.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\Stok Instance.
     */
    public function insertByProdukIndex($data, $i) {
        return parent::insert([
            'id_cabang'      => $data->idCabang      ?? '',
            'id_produk'      => $data->idProduk[$i]  ?? '',
            'stok_ready'     => $data->stokReady     ?? '',
            'stok_booked'    => $data->stokBooked    ?? '',
            'stok_delivery'  => $data->stokDelivery  ?? '',
            'stok_bad'       => $data->stokBad       ?? '',
            'stok_canvas'    => $data->stokCanvas    ?? '',
            'stok_incoming'  => $data->stokIncoming  ?? '',
            'tanggal_update' => $data->tanggal       ?? '',
            'waktu_update'   => $data->waktu         ?? '',
        ]);
    }

    /**
     * Update Data Berdasarkan Id.
     * 
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\Stok Instance.
     */
    public function updateById($data) {
        return $this->id($data->id)->update([
            'id_cabang'      => $data->idCabang      ?? '',
            'id_produk'      => $data->idProduk      ?? '',
            'stok_ready'     => $data->stokReady     ?? '',
            'stok_booked'    => $data->stokBooked    ?? '',
            'stok_delivery'  => $data->stokDelivery  ?? '',
            'stok_bad'       => $data->stokBad       ?? '',
            'stok_canvas'    => $data->stokCanvas    ?? '',
            'stok_incoming'  => $data->stokIncoming  ?? '',
            'tanggal_update' => $data->tanggal       ?? '',
            'waktu_update'   => $data->waktu         ?? '',
        ]);
    }

    /**
     * Updating the Ready Stock from a Certain Data Based on Id.
     * @param  Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\PurchaseRequest Instance.
     */
    public function updateStokReadyById($id, $data) {
        $this->id($id)->update([
            'stok_ready'     => $data->stokReady,
            'tanggal_update' => $data->tanggal,
            'waktu_update'   => $data->waktu,
        ]);
    }
}