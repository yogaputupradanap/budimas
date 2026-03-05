<?php

namespace App\Models;
use Illuminate\Support\Facades\Session;

class PurchasePenerimaanBarang extends Model {
    /** 
     * Setting Up Initial API Endpoint and Additional Resources. 
     */
    public function __construct() {
        parent::__construct();
        $this->endpoint = "/api/base/purchase_penerimaan_barang";
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
            'id_request'        => $data->idRequest   ?? '',    
            'kode_request'      => $data->kodeRequest ?? '',    
            'id_user1'          => $data->idUser1     ?? '',
            'id_user2'          => $data->idUser      ?? '',
            'tanggal'           => $data->tanggal     ?? '',
            'waktu'             => $data->waktu       ?? '',
            'batch_number'      => $data->batchNumber ?? '',
        ]);
    }
}