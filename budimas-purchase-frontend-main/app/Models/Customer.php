<?php

namespace App\Models;
use Illuminate\Support\Facades\Session;

class Customer extends Model
{
    /**
     * Setting Up Intial API Endpoint.
     */
    public function __construct(){
        parent::__construct();
        $this->endpoint = "/api/base/customer";
    }

    /**
     * @method Override.
     */
    function all() {
        return $this->select('/api/extra/getCustomer')->get();
    } 

    /**
     * Insert Data Baru.
     * 
     * @method Override.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\Customer Instance.
     */
    public function insert($data) {
        if (!is_object($data)) {
            $data = (object) $data;
        }
        return parent::insert([
            'nama'             => $data->nama ?? '',
            'alamat'           => $data->alamat ?? '',
            'telepon'          => $data->telepon ?? '',
            'npwp'             => $data->npwp ?? '',
            'id_wilayah1'      => $data->idWilayah1 ?? '',
            'id_wilayah2'      => $data->idWilayah2 ?? '',
            'id_wilayah3'      => $data->idWilayah3 ?? '',
            'id_wilayah4'      => $data->idWilayah4 ?? '',
            'id_tipe'          => $data->idTipe ?? '',
            'id_cabang'        => $data->idCabang ?? '',
            'no_rekening'      => $data->noRek ?? '',
            'pic'              => $data->pic ?? '',
            'longitude'        => $data->longitude ?? '',
            'latitude'         => $data->latitude ?? ''
        ]);
    }

    /**
     * Update Data Berdasarkan Id.
     * 
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\Customer Instance.
     */
    public function updateById($data) {
        return $this->id($data->id)->update([
            'nama'             => $data->nama ?? '',
            'alamat'           => $data->alamat ?? '',
            'telepon'          => $data->telepon ?? '',
            'npwp'             => $data->npwp ?? '',
            'id_wilayah1'      => $data->idWilayah1 ?? '',
            'id_wilayah2'      => $data->idWilayah2 ?? '',
            'id_wilayah3'      => $data->idWilayah3 ?? '',
            'id_wilayah4'      => $data->idWilayah4 ?? '',
            'id_tipe'          => $data->idTipe ?? '',
            'id_cabang'        => $data->idCabang ?? '',
            'no_rekening'      => $data->noRek ?? '',
            'pic'              => $data->pic ?? '',
            'longitude'        => $data->longitude ?? '',
            'latitude'         => $data->latitude ?? ''
        ]);
    }

    /**
     * Delete Data Berdasarkan Id.
     * 
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\Customer Instance.
     */
    public function deleteById($data) {
        return $this->id($data->id)->delete();
    }

    function getFilteredList($data) {
        $model = $this;
        
        if(!empty($data['kode'])) {
            $model = $model->where(['kode' ?? '', '=' ?? '', $data['kode']]);
        }
        if(!empty($data['nama'])) { // %25 Adalah Encoding untuk Special Character %
            $model = $model->whereOr(['nama' ?? '', ' ILIKE' ?? '', '%25'.$data['nama'].'%25']);
        }

        return $model->orderBy('id')->select()->get();
    }
}