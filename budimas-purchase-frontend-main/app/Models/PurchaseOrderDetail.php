<?php

namespace App\Models;
use Illuminate\Support\Facades\Session;
use Illuminate\Support\Collection;

class PurchaseOrderDetail extends Model {
    
    public function __construct(){
        /**
         * Set Endpoint Awal (Base) untuk Requesting API.
         */
        
        parent::__construct();
        $this->endpoint = "/api/base/purchase_order_detail";
    }

    /**
     * Getting Purchase Request Detail List Based on Request Id.
     * @param  int|$id Id of Purchase Request.
     * @return Illuminate\Http\JsonResponse Rows of Purchase Request Detail.
     */
    public function getListByIdOrder($id){
        return $this->where(['order_id', '=', $id])->select()->get();
    }

    /**
     * Inserting New Data Into Purchase Request Detail Table Based on
     * Counted Product Id.
     * @param  Illuminate\Http\Request|$data Requested HTTP Form Data.
     */
    // public function insertByCountedIdProduk($data) {
    //     for($i=0; $i<count($data->idProduk); $i++) {
    //         $this->insert([
    //             'id_produk'                    => $data->idProduk[$i]                  ?? '',
    //             'kode_produk'                  => $data->kodeProduk[$i]                ?? '',
    //             'nama_produk'                  => $data->namaProduk[$i]                ?? '',
    //             'harga_beli_produk'            => $data->hargaBeliProduk[$i]           ?? '',
    //             'id_produk_uom'                => $data->idProdukUOM[$i]               ?? '',
    //             'nama_produk_uom'              => $data->namaProdukUOM[$i]             ?? '',
    //             'kode_produk_uom'              => $data->kodeProdukUOM[$i]             ?? '',
    //             'level_produk_uom'             => $data->levelProdukUOM[$i]            ?? '',
    //             'harga_beli_produk_dikonversi' => $data->hargaBeliProdukDikonversi[$i] ?? '',
    //             'id_order'                     => $data->idOrder                       ?? '',
    //             'kode_order'                   => $data->kodeOrder                     ?? '',
    //             'jumlah_order'                 => $data->jumlahOrder[$i]               ?? '',
    //             'jumlah_terpenuhi'             => $data->jumlahTerpenuhi[$i]           ?? '',
    //             'jumlah_tersisa'               => $data->jumlahTersisa[$i]             ?? '',
    //             'subtotal_order'               => $data->subtotalOrder[$i]             ?? '',
    //             'harga_beli_produk_ppn'        => $data->hargaBeliProdukPPN[$i]        ?? '',
    //         ]);
    //     }
    // }
    public function insertByCountedIdProduk($data) {
        for($i=0; $i<count($data->idProduk); $i++) {
            $this->insert([
                'produk_id'          => $data->idProduk[$i]         ?? '',
                'produk_kode'        => $data->kodeProduk[$i]       ?? '',
                'produk_nama'        => $data->namaProduk[$i]       ?? '',
                'produk_harga_beli'  => $data->hargaBeliProduk[$i]  ?? '',
                'order_id'           => $data->idOrder              ?? '',
                'ppn'                => 0.11,
            ]);
        }
    }

    /**
     * @param  int|$id Id of Purchase Request.
     * @return App\Models\PurchaseOrderDetail Instance.
     */
    public function deleteByIdOrder($id) {
        return $this->where(['order_id', '=', $id])->delete();
    }

}