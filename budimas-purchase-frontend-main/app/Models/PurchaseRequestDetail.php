<?php

namespace App\Models;
use Illuminate\Support\Facades\Session;
use Illuminate\Support\Collection;

class PurchaseRequestDetail extends Model {
    /**
     * Setting Up Initial API Endpoint and Additional Resources.
     */
    public function __construct(){
        parent::__construct();
        $this->endpoint = "/api/base/purchase_request_detail";
    }

    /**
     * Getting Purchase Request Detail List Based on Request Id.
     * @param  int|$id Id of Purchase Request.
     * @return Illuminate\Http\JsonResponse Rows of Purchase Request Detail.
     */
    public function getListByIdRequest($id){
        return $this->where(['id_request', '=', $id])
                    ->select('/api/extra/getPurchaseRequestDetail')
                    ->get();
    }

    /**
     * Getting Purchase Request Detail List Based on Request Id which Has
     * Formated in Product Data Fields.
     * @param  int|$id Id of Purchase Request.
     * @return Illuminate\Http\JsonResponse Rows of Purchase Request Detail.
     */
    public function getListInProduk($id){
        return (new Collection($this->getListByIdRequest($id)))
            ->map(function($i) {
                return (object) [
                    'id'                    => $i->id_produk,
                    'id_produk'             => $i->id_produk,
                    'kode_produk'           => $i->kode_produk,
                    'nama_produk'           => $i->nama_produk,
                    'harga_beli_produk'     => $i->harga_beli_produk,
                    'harga_beli_produk_ppn' => $i->harga_beli_produk_ppn,
                    'jumlah_request'        => $i->jumlah_request,
                    'jumlah_terpenuhi'      => $i->jumlah_terpenuhi,
                    'jumlah_tersisa'        => $i->jumlah_tersisa,
                    'subtotal_request'      => $i->subtotal_request,
                    'id_request_detail'     => $i->id,
                ];
        })->toArray();
    }

    /**
     * Inserting New Data Into Purchase Request Detail Table Based on
     * Counted Product Id.
     * @param  Illuminate\Http\Request|$data Requested HTTP Form Data.
     */
    public function insertByCountedIdProduk($data) {
        for($i=0; $i<count($data->idProduk); $i++) {
            $this->insert([
                'id_request'            => $data->idRequest              ?? '',
                'kode_request'          => $data->kodeRequest            ?? '',
                'id_produk'             => $data->idProduk[$i]           ?? '',
                'nama_produk'           => $data->namaProduk[$i]         ?? '',
                'kode_produk'           => $data->kodeProduk[$i]         ?? '',
                'harga_beli_produk'     => $data->hargaBeliProduk[$i]    ?? '',
                'harga_beli_produk_ppn' => $data->hargaBeliProdukPPN[$i] ?? '',
                'jumlah_request'        => $data->jumlahRequest[$i]      ?? '',
                'jumlah_terpenuhi'      => $data->jumlahTerpenuhi[$i]    ?? '',
                'jumlah_tersisa'        => $data->jumlahTersisa[$i]      ?? '',
                'subtotal_request'      => $data->subtotalRequest[$i]    ?? '',
            ]);
        }
    }

    /**
     * Updating the Remaining Request Quantity from a Certain Data Based on Id.
     * @param  Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\PurchaseRequest Instance.
     */
    public function updateJumlahSisaRequestByCountedId($data) {
        for($i=0; $i<count($data->idRequestDetail); $i++) {
            $this->id($data->idRequestDetail[$i])->update([
                'jumlah_sisa' => $data->jumlahSisa[$i]
            ]);
        }
    }

    /**
     * Updating the Recieved Request Quantity from a Certain Data Based on Id.
     * @param  Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\PurchaseRequest Instance.
     */
    public function updateJumlahDiterimaByCountedId($data) {
        for($i=0; $i<count($data->idRequestDetail); $i++) {
            $this->id($data->idRequestDetail[$i])->update([
                'jumlah_diterima' => $data->jumlahDiterima[$i] + $data->jumlahDatang[$i]
            ]);
        }
    }

    /**
     * Updating the Recieved Request Quantity from a Certain Data Based on Id.
     * @param  Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\PurchaseRequest Instance.
     */
    public function updateJumlahByCountedId($data) {
        for($i=0; $i<count($data->idRequestDetail); $i++) {
            $this->id($data->idRequestDetail[$i])->update([
                'jumlah_terpenuhi' => $data->jumlahDiterima[$i] + $data->jumlahDiterima[$i],
                'jumlah_tersisa' => $data->jumlahDiterima[$i] - $data->jumlahDiterima[$i],
            ]);
        }
    }

    /**
     * Deleting Some Data Based on Request Id.
     * @param  int|$id Id of Purchase Request.
     * @return App\Models\PurchaseRequestDetail Instance.
     */
    public function deleteByIdRequest($id) {
        return $this->where(['id_request', '=', $id])->delete();
    }
}