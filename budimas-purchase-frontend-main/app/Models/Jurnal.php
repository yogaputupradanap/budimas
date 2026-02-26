<?php

namespace App\Models;
use Illuminate\Support\Facades\Session;

class Jurnal extends Model {
    /** 
     * Setting Up Intial API Endpoint. 
     */
    public function __construct(){
        parent::__construct();
        $this->endpoint = "/api/base/jurnal";
    }

    /**
     * Insert Data Baru.
     * 
     * @method Override.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\Jurnal Instance.
     */
    public function insert($data) {
        if (!is_object($data)) {
            $data = (object) $data;
        }
        return parent::insert([
            'id_cabang'         => $data->idCabang        ?? '',
            'id_user'           => $data->idUser          ?? '',
            'id_transaksi'      => $data->idTransaksi     ?? '',
            'id_tipe_transaksi' => $data->idTipeTransaksi ?? '',
            'id_akun'           => $data->idAkun          ?? '',
            'debit'             => $data->nominalDebit    ?? '',
            'kredit'            => $data->nominalKredit   ?? '',
            'tanggal'           => $data->tanggal         ?? '',
            'waktu'             => $data->waktu           ?? '',
            // 'keterangan'        => $data->keterangan      ?? '',
        ]);
    }
}