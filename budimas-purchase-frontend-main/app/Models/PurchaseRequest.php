<?php

namespace App\Models;
use Illuminate\Support\Facades\Session;

class PurchaseRequest extends Model {
    /** 
     * Setting Up Initial API Endpoint and Additional Resources. 
     */
    public function __construct() {
        parent::__construct();
        $this->endpoint = "/api/base/purchase_request";
    }

    /**
     * Getting Purchase Request List Where The Process is Just Drafted.
     * @return Illuminate\Http\JsonResponse Rows of Purchase Request.
     */
    public function getListKonfirmasi() {
        return $this->where(['purchase_request.id_proses', '=', '1'])
                    ->select('/api/extra/getPurchaseRequest')
                    ->get();
    }
    
    /**
     * Getting Purchase Request List Where The Process is Just Drafted.
     * @return Illuminate\Http\JsonResponse Rows of Purchase Request.
     */
    public function getListPenerimaanBarang() {
        return $this->where(['id_proses', '=', '3'])
                    ->where(['purchase_request.id_cabang', '=', user()->id_cabang])
                    ->select('/api/extra/getPurchaseRequest')
                    ->get();
    }

    /**
     * Getting Purchase Request List Where The Process Has Been Confirmed.
     * @return Illuminate\Http\JsonResponse Rows of Purchase Request.
     */
    public function getListDisetujui() {
        return $this->where(['id_proses', '=', '5'])
                    ->select('/api/extra/getPurchaseRequest')
                    ->get();
    }

    /**
     * Getting Purchase Request List Where The Process Has Been Closed.
     * @return Illuminate\Http\JsonResponse Rows of Purchase Request.
     */
    public function getListClosed() {
        return $this->where(['id_proses', '=', '9'])
                    ->select('/api/extra/getPurchaseRequest')
                    ->get();
    }

    /**
     * Inserting New Data Into Purchase Request Table and Returning the Id
     * from The Inserted Data.
     * @param  Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return int|$id.
     */
    public function insertReturningId($data) {
        return $this->returning('id')->insert([
            'id_cabang'            => $data->idCabang            ?? '',
            'id_principal'         => $data->idPrincipal         ?? '',
            'id_user1'             => $data->idUser1             ?? '',
            'id_user2'             => $data->idUser2             ?? '',
            'id_proses'            => $data->idProses            ?? '',
            'kode'                 => $data->kodeRequest         ?? '',
            'keterangan'           => $data->keterangan          ?? '',
            'no_batch'             => $data->noBatch             ?? '',
            'tanggal_dibuat'       => $data->tanggalDibuat       ?? '',
            'tanggal_dikonfirmasi' => $data->tanggalDikonfirmasi ?? '',
            'waktu_dibuat'         => $data->waktuDibuat         ?? '',
            'waktu_dikonfirmasi'   => $data->waktuDikonfirmasi   ?? '',
        ])->first()->id;
    }

    /**
     * Updating a Certain Data Based on Id.
     * @param  int|$id
     * @param  Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\Produk Instance.
     */
    public function updateById($data, $id) {
        return $this->id($id)->update([
            'id_cabang'            => $data->idCabang            ?? '',
            'id_principal'         => $data->idPrincipal         ?? '',
            'id_user1'             => $data->idUser1             ?? '',
            'id_user2'             => $data->idUser2             ?? '',
            'id_proses'            => $data->idProses            ?? '',
            'kode'                 => $data->kodeRequest         ?? '',
            'keterangan'           => $data->keterangan          ?? '',
            'no_batch'             => $data->noBatch             ?? '',
            'tanggal_dibuat'       => $data->tanggalDibuat       ?? '',
            'tanggal_dikonfirmasi' => $data->tanggalDikonfirmasi ?? '',
            'waktu_dibuat'         => $data->waktuDibuat         ?? '',
            'waktu_dikonfirmasi'   => $data->waktuDikonfirmasi   ?? '',
        ]);
    }

    /**
     * Updating the Process to be Confirmed from a Certain Data Based on Id.
     * @param  int|$id.
     * @return App\Models\PurchaseRequest Instance.
     */
    public function updateDisetujui($data) {
        return $this->id($data->id)->update([
            'id_proses'            => '3',
            'id_user2'             => $data->idUser2             ?? '',
            'tanggal_dikonfirmasi' => $data->tanggalDikonfirmasi ?? '',
            'waktu_dikonfirmasi'   => $data->waktuDikonfirmasi   ?? '',
        ])->response();
    }

    /**
     * Updating the Process to be Closed from a Certain Data Based on Id.
     * @param  int|$id
     * @return App\Models\PurchaseRequest Instance.
     */
    public function updateClosed($data) {
        return $this->id($data->id)->update([
            'id_proses'            => '2',
            'id_user2'             => $data->idUser2             ?? '',
            'tanggal_dikonfirmasi' => $data->tanggalDikonfirmasi ?? '',
            'waktu_dikonfirmasi'   => $data->waktuDikonfirmasi   ?? '',
        ])->response();
    }

    /**
     * Updating the Order Batch Number from a Certain Data Based on Id.
     * @param  Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\PurchaseRequest Instance.
     */
    public function updateBatchNumber($data) {
        return $this->id($data->idRequest)->update(['order_batch' => $data->orderNumber])->response();
    }

    /**
     * Deleting a Certain Data Based on Id.
     * @param  int|$id
     * @return App\Models\PurchaseRequest Instance.
     */
    public function deleteById($id) {
        return $this->id($id)->delete();
    }
}