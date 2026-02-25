<?php

namespace App\Models;
use Illuminate\Support\Facades\Session;

class ProdukKategori extends Model
{
    /**
     * Setting Up Intial API Endpoint.
     */
    public function __construct(){
        parent::__construct();
        $this->endpoint = "/api/base/produk_kategori";
    }
    
    /**
     * Insert Data Baru.
     * 
     * @method Override.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\ProdukKategori Instance.
     */
    public function insert($data) {
        return parent::insert(['nama' => $data->nama ?? '']);
    }

    /**
     * Update Data Berdasarkan Id.
     * 
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\ProdukKategori Instance.
     */
    public function updateById($data) {
        return $this->id($data->id)->update(['nama' => $data->nama ?? '']);
    }

    /**
     * Delete Data Berdasarkan Id.
     * 
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\ProdukKategori Instance.
     */
    public function deleteById($data) {
        return $this->id($data->id)->delete();
    }
}