<?php

namespace App\Models;
use Illuminate\Support\Facades\Session;
use Illuminate\Support\Collection;

class Produk extends Model {
    /**
     * Setting Up Intial API Endpoint.
     */
    public function __construct(){
        parent::__construct();
        $this->endpoint = "/api/base/produk";
    }
    
    /**
     * @method Override.
     */
    function all() {
        return $this->select('/api/extra/getProduk')->get();
    }

    /**
     *
     */
    function getListByIdPrincipal($id) {
        return $this->where(['id_principal', '=', $id])
                    ->select('/api/extra/getProduk')
                    ->get();
    }

    /**
     * 
     */
    public function getListInPurchase($id){
        return (new Collection($this->getListByIdPrincipal($id)))
            ->map(function($i) {
                return (object) [
                    'id_produk'                    => $i->id,
                    'kode_produk'                  => $i->kode_sku,
                    'nama_produk'                  => $i->nama,
                    'harga_beli_produk'            => $i->harga_beli,
                    'id_produk_uom'                => null,
                    'nama_produk_uom'              => null,
                    'kode_produk_uom'              => null,
                    'level_produk_uom'             => null,
                    'harga_beli_produk_dikonversi' => null,
                    'id'                           => null,
                    'id_order'                     => null,
                    'kode_order'                   => null,
                    'jumlah_order'                 => null,
                    'jumlah_terpenuhi'             => null,
                    'jumlah_tersisa'               => null,
                    'subtotal_order'               => null,
                    'harga_beli_produk_ppn'        => null,
                ];
        })->toArray();
    }

    /**
     * Insert Data Baru.
     * 
     * @method Override.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\Produk Instance.
     */
    public function insert($data) {
        if (!is_object($data)) {
            $data = (object) $data;
        }
        return parent::insert([
            'id_principal'    => $data->idPrincipal ?? '',
            'id_brand'        => $data->idBrand ?? '',
            'id_kategori'     => $data->idKategori ?? '',
            'id_status'       => $data->idStatus ?? '',
            'nama'            => $data->nama ?? '',
            'kode_sku'        => $data->kodeSku ?? '',
            'kode_ean'        => $data->kodeEan ?? '',
            'harga_beli'      => $data->hargaBeli ?? '',
            'keterangan'      => $data->keterangan ?? ''
        ]);
    }

    /**
     * Update Data Berdasarkan Id.
     * 
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\Produk Instance.
     */
    public function updateById($data) {
        return $this->id($data->id)->update([
            'id_principal'    => $data->idPrincipal ?? '',
            'id_brand'        => $data->idBrand ?? '',
            'id_kategori'     => $data->idKategori ?? '',
            'id_status'       => $data->idStatus ?? '',
            'nama'            => $data->nama ?? '',
            'kode_sku'        => $data->kodeSku ?? '',
            'kode_ean'        => $data->kodeEan ?? '',
            'harga_beli'      => $data->hargaBeli ?? '',
            'keterangan'      => $data->keterangan ?? ''
        ]);
    }

    /**
     * Delete Data Berdasarkan Id.
     * 
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\Produk Instance.
     */
    public function deleteById($data) {
        return $this->id($data->id)->delete();
    }
}