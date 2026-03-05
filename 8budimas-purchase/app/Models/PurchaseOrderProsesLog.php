<?php

namespace App\Models;
use Illuminate\Support\Facades\Session;

class PurchaseOrderProsesLog extends Model {

    public function __construct() {
        parent::__construct();
        $this->endpoint = "/api/base/purchase_order_proses_log";
    }

    public function insert($data) {
        if (!is_object($data)) {
            $data = (object) $data;
        }
        
        return parent::insert([
            'id_order'               => $data->idOrder              ?? '',
            'id_proses_diselesaikan' => $data->idProsesDiselesaikan ?? '',
            'id_user'                => $data->idUser               ?? '',
            'id_user_jabatan'        => $data->idUserJabatan        ?? '',
            'tanggal'                => $data->tanggal              ?? '',
            'waktu'                  => $data->waktu                ?? '',
        ]);
    }

    public function deleteById($id) {
        return $this->id($id)->delete();
    }

}