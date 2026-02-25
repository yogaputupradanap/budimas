<?php

namespace App\Models;
use Illuminate\Support\Facades\Session;

class ProdukTipeHarga extends Model
{
    /**
     * Setting Up Intial API Endpoint.
     */
    public function __construct(){
        parent::__construct();
        $this->endpoint = "/api/base/produk_tipe_harga";
    }

    
    /**
     * Insert Data Baru.
     * 
     * @method Override.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\ProdukTipeHarga Instance.
     */
    public function insert($data) {
        return parent::insert([
            'nama' => $data->nama ?? '',
            'kode' => $data->kode ?? ''
        ]);
    }

    /**
     * Update Data Berdasarkan Id.
     * 
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\ProdukTipeHarga Instance.
     */
    public function updateById($data) {
        return $this->id($data->id)->update([
            'nama' => $data->nama ?? '',
            'kode' => $data->kode ?? ''
        ]);
    }

    /**
     * Delete Data Berdasarkan Id.
     * 
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\ProdukTipeHarga Instance.
     */
    public function deleteById($data) {
        return $this->id($data->id)->delete();
    }
}