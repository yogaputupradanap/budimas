<?php

namespace App\Models;
use Illuminate\Support\Facades\Session;

class ProdukSatuan extends Model
{
    /**
     * Setting Up Intial API Endpoint.
     */
    public function __construct(){
        parent::__construct();
        $this->endpoint = "/api/base/produk_uom";
    }
    
    /**
     * 
     */
    function getListByIdProduk($id) {
        return $this->where(['id_produk', '=', $id])->orderBy('produk_uom.id')->select()->get();
    } 

    /**
     * Insert Data Baru.
     * 
     * @method Override.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\ProdukSatuan Instance.
     */
    public function insert($data) {
        return parent::insert([
            'id_produk'       => $data->idProduk       ?? '',
            'kode'            => $data->kode           ?? '',
            'nama'            => $data->nama           ?? '',
            'level'           => $data->level          ?? '',
            'berat_satuan'    => $data->beratSatuan    ?? '',
            'berat_bersih'    => $data->beratBersih    ?? '',
            'berat_kotor'     => $data->beratKotor     ?? '',
            'packing_satuan'  => $data->packingSatuan  ?? '',
            'packing_panjang' => $data->packingPanjang ?? '',
            'packing_tinggi'  => $data->packingTinggi  ?? '',
            'packing_lebar'   => $data->packingLebar   ?? '',
            'faktor_konversi' => $data->faktorKonversi ?? '',
        ]);
    }

    /**
     * Update Data Berdasarkan Id.
     * 
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\ProdukSatuan Instance.
     */
    public function updateById($data) {
        return $this->id($data->id)->update([
            'id_produk'       => $data->idProduk       ?? '',
            'kode'            => $data->kode           ?? '',
            'nama'            => $data->nama           ?? '',
            'level'           => $data->level          ?? '',
            'berat_satuan'    => $data->beratSatuan    ?? '',
            'berat_bersih'    => $data->beratBersih    ?? '',
            'berat_kotor'     => $data->beratKotor     ?? '',
            'packing_satuan'  => $data->packingSatuan  ?? '',
            'packing_panjang' => $data->packingPanjang ?? '',
            'packing_tinggi'  => $data->packingTinggi  ?? '',
            'packing_lebar'   => $data->packingLebar   ?? '',
            'faktor_konversi' => $data->faktorKonversi ?? '',
        ]);
    }

    /**
     * Delete Data Berdasarkan Id.
     * 
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\ProdukSatuan Instance.
     */
    public function deleteById($data) {
        return $this->id($data->id)->delete();
    }
}