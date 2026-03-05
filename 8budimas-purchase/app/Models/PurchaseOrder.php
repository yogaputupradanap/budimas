<?php

namespace App\Models;
use Illuminate\Support\Facades\Session;

class PurchaseOrder extends Model {
    
    public function __construct() {
        /**
         * Set Endpoint Awal (Base) untuk Requesting API.
         */

        parent::__construct();
        $this->endpoint = "/api/base/purchase_order";
    }

    public function generateKode() {
        /**
         * MEMBUAT KODE UNTUK ORDER.
         * KOMBINASI :
         * 1. [CHARS]    SINGKATAN DARI PURCHASE ORDER "PO".
         * 2. [TANGGAL]  FORMAT "YMD".
         * 3. [NUMBERS]  ID CABANG DARI USER YANG LOGIN.
         * 4. [CHARS]    KARAKTER ACAK TIGA HURUF.
         * 
         * DISAMBUNGKAN DENGAN HYPHEN "-".
         * 
         */
        return "PO" . date('Ymd') . user()->id_cabang . rand(100,1000);
    }

    public function all() {
        /**
         * Mendapatkan `rows data` dari Join Tabel
         * Main, Proses Log, User, Cabang, dan Principal.
         * 
         * @return Illuminate\Http\JsonResponse.
         * 
         */

        return $this->select('/api/extra/purchase-order/all')->get();
    }

    public function getDataProsesRequestByIdOrder($id) {
        /**
         * Mendapatkan `rows data` dari Join Tabel
         * Main, Proses Log, User, Cabang, dan Principal.
         * 
         * @return Illuminate\Http\JsonResponse.
         */

        return  $this->where([
                    ['purchase_order.id', '=', $id],
                    ['purchase_order_proses_log.id_proses_diselesaikan', '=', '1']
                ])
                ->select('/api/extra/purchase-order/all')
                ->first();
    }

    /**
     * Getting Purchase Request List Where The Process is Just Drafted.
     * @return Illuminate\Http\JsonResponse Rows of Purchase Request.
     */
    public function getListProsesKonfirmasi() {
        // return  $this->where([
        //             ['purchase_order.proses_id_berjalan', '=', '2'],
        //             // ['purchase_order_proses_log.id_proses_diselesaikan', '=', '1'],
        //         ])
        //         // ->select('/api/extra/purchase-order/all')
                return  $this->select()
                ->get();
    }

    /**
     * Getting Purchase Request List Where The Process is Just Drafted.
     * @return Illuminate\Http\JsonResponse Rows of Purchase Request.
     */
    public function getListProsesPurchasing() {
        return  $this->where([
                    // ['purchase_order.proses_id_berjalan', '=', '3'],
                    // ['purchase_order_proses_log.id_proses_diselesaikan', '=', '1'],
                ])
                ->select('/api/extra/purchase-order/all')
                ->get();
    }

    /**
     * Inserting New Data Into Purchase Order Table and Returning the Id
     * from The Inserted Data.
     * @param  Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return int|$id.
     */
    public function insertReturningId($data) {
        return $this->returning('id')->insert([
            'cabang_id'          => $data->idCabang          ?? '',
            'principal_id'       => $data->idPrincipal       ?? '',
            'proses_id_berjalan' => $data->idProsesBerjalan  ?? '',
            'kode'               => $data->kodeOrder         ?? '',
            'keterangan'         => $data->keterangan        ?? '',
            'batch_pengiriman'   => $data->batchPengiriman   ?? '',
        ])->first()->id;
    }

    /**
     * Inserting New Data Into Purchase Order Table and Returning the Id
     * from The Inserted Data.
     * @param  Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return int|$id.
     */
    public function updateById($data, $id) {
        return $this->id($id)->update([
            'id_cabang'          => $data->idCabang          ?? '',
            'id_principal'       => $data->idPrincipal       ?? '',
            'id_proses_berjalan' => $data->idProsesBerjalan  ?? '',
            'kode'               => $data->kodeOrder         ?? '',
            'keterangan'         => $data->keterangan        ?? '',
            'batch_pengiriman'   => $data->batchPengiriman   ?? '',
        ]);
    }


    /**
     * @param  int|$id.
     * @return App\Models\PurchaseOrder Instance.
     */
    public function updateProsesOnPurchase($id) {
        return parent::id($id)->update(['id_proses_berjalan' => '3'])->response();
    }

    /**
     * @param  int|$id.
     * @return App\Models\PurchaseOrder Instance.
     */
    public function updateProsesClosed($id) {
        $data = $this->find($id);
        return parent::id($data->idOrder)->update(['id_proses_berjalan' => '4'])->response();
    }

    /**
     * Deleting a Certain Data Based on Id.
     * @param  int|$id
     * @return App\Models\PurchaseOrder Instance.
     */
    public function deleteById($id) {
        return $this->id($id)->delete();
    }
}