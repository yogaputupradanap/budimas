<?php

namespace App\Models;
use Illuminate\Support\Facades\Session;

class PurchaseRequestLogProses extends Model {
    /** 
     * Setting Up Initial API Endpoint and Additional Resources. 
     */
    public function __construct() {
        parent::__construct();
        $this->endpoint = "/api/base/purchase_request_log_proses";
    }

    /**
     * Inserting New Data Into Purchase Log Process.
     * @method Override.
     * @param  Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\PurchaseLogProses Instance.
     */
    public function insert($data) {
        if (!is_object($data)) {
            $data = (object) $data;
        }
        
        return parent::insert([
            'id_user'      => $data->idUser    ?? '',
            'id_request'   => $data->idRequest ?? '',
            'id_proses'    => $data->idProses  ?? '',
            'kode_request' => $data->kode      ?? '',
            'tanggal'      => date('Y-m-d'),
            'waktu'        => date('H:i:s'),
        ]);
    }
}