<?php

namespace App\Models;
use Illuminate\Support\Facades\Session;

class PurchasePenerimaanBarangDetail extends Model {
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
    public function insertByCountedIdRequestDetail($data) {
        for($i=0; $i<count($data->idRequestDetail); $i++) {
            return $this->insert([
                
                'id_request_detail' => $data->idRequestDetail[$i]                           ?? '',
                'id_produk'         => $data->idProduk[$i]                                  ?? '',    
                'nama_produk'       => $data->namaProduk[$i]                                ?? '',    
                'kode_produk'       => $data->kodeProduk[$i]                                ?? '',    
                'harga_beli_produk' => $data->hargaBeliProduk[$i]                           ?? '',       
                'jumlah_datang'     => $data->jumlahDatang[$i]                              ?? '',     
                'valuasi'           => $data->hargaBeliProduk[$i] * $data->jumlahDatang[$i] ?? '',
                'tanggal'           => $data->tanggal                                       ?? '',
                'waktu'             => $data->waktu                                         ?? '',
            ]);
        }
    }
}