<?php

namespace App\Models;
use Illuminate\Support\Facades\Session;

class ProdukHarga extends Model
{
    /**
     * Setting Up Intial API Endpoint.
     */
    public function __construct(){
        parent::__construct();
        $this->endpoint = "/api/base/produk_harga_jual";
    }
    
    function all() {
        return  $this->select('/api/extra/getProdukHarga')->get();
    }

    /**
     * 
     */
    function getListByIdProduk($id) {
        return $this->where(['id_produk', '=', $id])
                    ->orderBy('produk_harga_jual.id')
                    ->select('/api/extra/getProdukHarga')
                    ->get();
    } 

    /**
     * Insert Data Baru.
     * 
     * @method Override.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\ProdukHarga Instance.
     */
    public function insert($data) {
        return parent::insert([
            'id_produk'      => $data->idProduk ?? '',
            'id_tipe_harga'  => $data->idTipeHarga ?? '',
            'harga'          => $data->harga ?? '',
        ]);
    }

    /**
     * Update Data Berdasarkan Id.
     * 
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\ProdukHarga Instance.
     */
    public function updateById($data) {
        return $this->id($data->id)->update([
            'id_produk'      => $data->idProduk ?? '',
            'id_tipe_harga'  => $data->idTipeHarga ?? '',
            'harga'          => $data->harga ?? '',
        ]);
    }

    /**
     * Delete Data Berdasarkan Id.
     * 
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\ProdukHarga Instance.
     */
    public function deleteById($data) {
        return $this->id($data->id)->delete();
    }
}