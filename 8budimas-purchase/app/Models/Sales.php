<?php

namespace App\Models;
use Illuminate\Support\Facades\Session;

class Sales extends Model
{
    /**
     * Setting Up Intial API Endpoint.
     */
    public function __construct(){
        parent::__construct();
        $this->endpoint = "/api/base/sales";
    }
    
    /**
     * @method Override.
     */
    function all() {
        return $this->select('/api/extra/getSales')->get();
    }
    
    /**
     * Insert Data Baru.
     * 
     * @method Override.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\Sales Instance.
     */
    public function insert($data) {
        if (!is_object($data)) {
            $data = (object) $data;
        }
        
        return parent::insert([
            'id_user'      => $data->idUser ?? '',
            'id_principal' => $data->idPrincipal ?? '',
            'id_wilayah1'  => $data->idWilayah1 ?? '',
            'id_wilayah2'  => $data->idWilayah2 ?? '',
            'id_tipe'      => $data->idTipe ?? '',
        ]);
    }

    /**
     * Update Data Berdasarkan Id.
     * 
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\Sales Instance.
     */
    public function updateById($data) {
        return $this->id($data->id)->update([
            'id_user'      => $data->idUser ?? '',
            'id_principal' => $data->idPrincipal ?? '',
            'id_wilayah1'  => $data->idWilayah1 ?? '',
            'id_wilayah2'  => $data->idWilayah2 ?? '',
            'id_tipe'      => $data->idTipe ?? '',
        ]);
    }

    /**
     * Delete Data Berdasarkan Id.
     * 
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\Sales Instance.
     */
    public function deleteById($data) {
        return $this->id($data->id)->delete();
    }
}