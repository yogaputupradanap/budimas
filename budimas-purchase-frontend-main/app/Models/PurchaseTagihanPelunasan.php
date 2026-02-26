<?php

namespace App\Models;
use Illuminate\Support\Facades\Session;

class PurchaseTagihanPelunasan extends Model {
    /** 
     * Setting Up Initial API Endpoint and Additional Resources. 
     */
    public function __construct() {
        parent::__construct();
        $this->endpoint = "/api/base/purchase_tagihan_pelunasan";
    }

    /**
     * Getting Purchase Request List Where The Process is Just Drafted.
     * @return Illuminate\Http\JsonResponse Rows of Purchase Request.
     */
    public function getListByIdOrder($id) {
        return $this->where(['id_order', '=', $id])->orderBy('id')
                    ->select('/api/extra/getPurchaseTagihanPelunasan')
                    ->get();
    }

    /**
     * Getting Purchase Request List Where The Process is Just Drafted.
     * @return Illuminate\Http\JsonResponse Rows of Purchase Request.
     */
    public function getDataTerakhirByIdOrder($id) {
        return $this->where(['id_order', '=', $id])
                    ->orderBy('id DESC')->limit(1)
                    ->select('/api/extra/getPurchaseTagihanPelunasan')
                    ->first();
    }

    /**
     * Inserting New Data Into Purchase Penerimaan Barang Table Based on
     * Counted Purchase Request Detail Id.
     * @param  Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\PurchasePenerimaanBarang Instance.
     */
    public function insert($data) {
        if (!is_object($data)) {
            $data = (object) $data;
        }
        
        return parent::insert([
            'id_tagihan'             => $data->idTagihan            ?? '',
            'id_order'               => $data->idOrder              ?? '',
            'no_faktur'              => $data->noFaktur             ?? '',
            'id_user1'               => $data->idUser               ?? '',
            'id_user2'               => $data->idUser2              ?? '',
            'nominal_pembayaran'     => $data->nominalPembayaran    ?? '',    
            'nominal_total_terbayar' => $data->nominalTotalTerbayar ?? '',       
            'nominal_total_sisa'     => $data->nominalTotalSisa     ?? '',       
            'tipe_setoran'           => $data->tipeSetoran          ?? '',       
            'no_angsuran'            => $data->noAngsuran           ?? '',       
            'tanggal'                => $data->tanggal              ?? '',
            'waktu'                  => $data->waktu                ?? '',
        ]);
    }
}