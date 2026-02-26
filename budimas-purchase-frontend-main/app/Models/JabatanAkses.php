<?php

namespace App\Models;
use Illuminate\Support\Facades\Session;

class JabatanAkses extends Model
{
    /**
     * Setting Up Intial API Endpoint.
     */
    public function __construct(){
        parent::__construct();
        $this->endpoint = "/api/base/jabatan_akses";
    }

    function getListByIdJabatan($id) {
        return  $this->select('/api/extra/getFiturJabatan?id='.$id)->get();
    }
    function getDefaultFiturListByIdJabatan($id){
        return $this->where(['id_jabatan', '=', $id])->select()->get();
    }

    /**
     * Delete Data Berdasarkan Id.
     * 
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\User Instance.
     */
    public function deleteById($data) {
        return $this->id($data->id)->delete();
    }

    function insert($data) {
        if (!is_object($data)) {
            $data = (object) $data;
        }
        return parent::insert([
            'id_jabatan' => $data->idJabatan,
            'id_fitur'   => $data->idFitur
        ]);
    }
}