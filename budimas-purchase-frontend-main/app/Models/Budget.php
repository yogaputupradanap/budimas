<?php

namespace App\Models;
use Illuminate\Support\Facades\Session;

class Budget extends Model {
    /**
     * Setting Up Intial API Endpoint.
     */
    public function __construct(){
        parent::__construct();
        $this->endpoint = "/api/base/budget";
    }
    
    /**
     * @method Override.
     */
    function all() {
        return $this->select('/api/extra/getBudget')->get();
    }

    /**
     * Insert Data Baru.
     * 
     * @method Override.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\Budget Instance.
     */
    public function insert($data) {
        if (!is_object($data)) {
            $data = (object) $data;
        }
        return parent::insert([
            'id_principal'  => $data->idPrincipal ?? '',
            'id_departemen' => $data->idDepartemen ?? '',
            'bulan'         => $data->bulan ?? '',
            'tahun'         => $data->tahun ?? '',
            'nominal'       => $data->nominal ?? '',
            'limit_nominal' => $data->limit ?? '',
            'kode'          => $data->kode ?? '',
            'keterangan'    => $data->keterangan ?? ''
        ]);
    }

    /**
     * Update Data Berdasarkan Id.
     * 
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\Budget Instance.
     */
    public function updateById($data) {
        return $this->id($data->id)->update([
            'id_principal'  => $data->idPrincipal ?? '',
            'id_departemen' => $data->idDepartemen ?? '',
            'bulan'         => $data->bulan ?? '',
            'tahun'         => $data->tahun ?? '',
            'nominal'       => $data->nominal ?? '',
            'limit_nominal' => $data->limit ?? '',
            'kode'          => $data->kode ?? '',
            'keterangan'    => $data->keterangan ?? ''
        ]);
    }

    /**
     * Delete Data Berdasarkan Id.
     * 
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\Budget Instance.
     */
    public function deleteById($data) {
        return $this->id($data->id)->delete();
    }
}