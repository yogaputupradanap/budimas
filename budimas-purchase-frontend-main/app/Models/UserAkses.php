<?php

namespace App\Models;
use Illuminate\Support\Facades\Session;

class UserAkses extends Model
{
    /**
     * Setting Up Intial API Endpoint.
     */
    public function __construct(){
        parent::__construct();
        $this->endpoint = "/api/base/users_akses";
    }
    
    function getListByIdUser($id) {
        return $this->where(['id_user', '=', $id])->select('/api/extra/getFiturUser')->get();
    }
    function getUserDistinctList() {
        return  $this->select('/api/extra/getUserAksesDistinct')->get();
    }

    /**
     * Delete Data Berdasarkan Id User.
     * 
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\UserAkses Instance.
     */
    function deleteByIdUser($id){
        return $this->where(['id_user', '=', $id])->delete();
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
            'id_user'  => $data->idUser,
            'id_fitur' => $data->idFitur
        ]);
    }
    
    function insertBulk($data) {
        return parent::insert([
            'id_user'  => $data[0],
            'id_fitur' => $data[1]
        ]);
    }
}