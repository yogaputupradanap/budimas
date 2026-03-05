<?php

namespace App\Models;
use Illuminate\Support\Facades\Session;

class ProdukBrand extends Model
{
    /**
     * Setting Up Intial API Endpoint.
     */
    public function __construct(){
        parent::__construct();
        $this->endpoint = "/api/base/produk_brand";
    }

    /**
     * Insert Data Baru.
     * 
     * @method Override.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\ProdukBrand Instance.
     */
    public function insert($data) {
        if (!is_object($data)) {
            $data = (object) $data;
        }
        return parent::insert(['nama' => $data->nama ?? '']);
    }

    /**
     * Update Data Berdasarkan Id.
     * 
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\ProdukBrand Instance.
     */
    public function updateById($data) {
        return $this->id($data->id)->update(['nama' => $data->nama ?? '']);
    }

    /**
     * Delete Data Berdasarkan Id.
     * 
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\ProdukBrand Instance.
     */
    public function deleteById($data) {
        return $this->id($data->id)->delete();
    }
}