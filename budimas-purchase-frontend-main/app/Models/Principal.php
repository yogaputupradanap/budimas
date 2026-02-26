<?php

namespace App\Models;
use Illuminate\Support\Facades\Session;

class Principal extends Model
{
    /**
     * Setting Up Intial API Endpoint.
     */
    public function __construct(){
        parent::__construct();
        $this->endpoint = "/api/base/principal";
    }
    
    /**
     * @method Override.
     */
    function all() {
        return  $this->select('/api/extra/getPrincipal')->get();
    }

    /**
     * Insert Data Baru.
     * 
     * @method Override.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\Principal Instance.
     */
    public function insert($data) {
        if (!is_object($data)) {
            $data = (object) $data;
        }
        return parent::insert([
            'nama'          => $data->nama ?? '',
            'alamat'        => $data->alamat ?? '',
            'telepon'       => $data->telepon ?? '',
            'npwp'          => $data->npwp ?? '',
            'id_wilayah1'   => $data->idWilayah1 ?? '',
            'id_wilayah2'   => $data->idWilayah2 ?? '',
            'id_wilayah3'   => $data->idWilayah3 ?? '',
            'id_wilayah4'   => $data->idWilayah4 ?? '',
            'no_rekening'   => $data->noRek ?? '',
            'pic'           => $data->pic ?? '',
            'id_perusahaan' => $data->idPerusahaan ?? ''
        ]);
    }

    /**
     * Update Data Berdasarkan Id.
     * 
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\Principal Instance.
     */
    public function updateById($data) {
        return $this->id($data->id)->update([
            'nama'          => $data->nama ?? '',
            'alamat'        => $data->alamat ?? '',
            'telepon'       => $data->telepon ?? '',
            'npwp'          => $data->npwp ?? '',
            'id_wilayah1'   => $data->idWilayah1 ?? '',
            'id_wilayah2'   => $data->idWilayah2 ?? '',
            'id_wilayah3'   => $data->idWilayah3 ?? '',
            'id_wilayah4'   => $data->idWilayah4 ?? '',
            'no_rekening'   => $data->noRek ?? '',
            'pic'           => $data->pic ?? '',
            'id_perusahaan' => $data->idPerusahaan ?? ''
        ]);
    }

    /**
     * Delete Data Berdasarkan Id.
     * 
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\Principal Instance.
     */
    public function deleteById($data) {
        return $this->id($data->id)->delete();
    }
}