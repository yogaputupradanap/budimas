<?php

namespace App\Models;
use Illuminate\Support\Facades\Session;

class PurchaseTagihan extends Model {
    /** 
     * Setting Up Initial API Endpoint and Additional Resources. 
     */
    public function __construct() {
        parent::__construct();
        $this->endpoint = "/api/base/purchase_tagihan";
    }

    /**
     * Inserting New Data Into Purchase Penerimaan Barang Table Based on
     * Counted Purchase Request Detail Id.
     * @param  Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\PurchasePenerimaanBarang Instance.
     */
    public function insertReturningId($data) {
        return $this->returning('id')->insert([
            'id_order'             => $data->idOrder             ?? '',
            'no_faktur'            => $data->noFaktur            ?? '',
            'id_request'           => $data->idRequest           ?? '',    
            'kode_request'         => $data->kodeRequest         ?? '',
            'id_user1'             => $data->idUser              ?? '',
            'id_user2'             => $data->idUser2             ?? '',
            'nominal_total_faktur' => $data->totalTagihan        ?? '',    
            'nominal_total_audit'  => $data->totalTagihanAudit   ?? '',       
            'jatuh_tempo'          => $data->jatuhTempo          ?? '',       
            'tanggal'              => $data->tanggal             ?? '',
            'waktu'                => $data->waktu               ?? '',
        ])->first()->id;
    }
}