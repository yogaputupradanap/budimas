<?php

namespace App\Models;
use Illuminate\Support\Facades\Session;

class Plafon extends Model
{
    /**
     * Setting Up Intial API Endpoint.
     */
    public function __construct(){
        parent::__construct();
        $this->endpoint = "/api/base/plafon";
    }
    
    /**
     * @method Override.
     */
    function all() {
        return $this->select('/api/extra/getPlafon')->get();
    } 

    /**
     * Insert Data Baru.
     * 
     * @method Override.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\Plafon Instance.
     */
    public function insert($data) {
        if (!is_object($data)) {
            $data = (object) $data;
        }
        return parent::insert([
            'id_customer'   =>  $data->idCustomer ?? '',
            'id_principal'  =>  $data->idPrincipal ?? '',
            'id_user'       =>  $data->idUser ?? '',
            'limit_bon'     =>  $data->limit ?? '',
            'kode'          =>  $data->kode ?? '',
            'top'           =>  $data->top ?? '',
            'lock_order'    =>  $data->lockOrder ?? '',
            'id_tipe_harga' =>  $data->idTipeHarga ?? ''
        ]);
    }

    /**
     * Update Data Berdasarkan Id.
     * 
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\Plafon Instance.
     */
    public function updateById($data) {
        return $this->id($data->id)->update([
            'id_customer'   =>  $data->idCustomer ?? '',
            'id_principal'  =>  $data->idPrincipal ?? '',
            'id_user'       =>  $data->idUser ?? '',
            'limit_bon'     =>  $data->limit ?? '',
            'kode'          =>  $data->kode ?? '',
            'top'           =>  $data->top ?? '',
            'lock_order'    =>  $data->lockOrder ?? '',
            'id_tipe_harga' =>  $data->idTipeHarga ?? ''
        ]);
    }

    /**
     * Delete Data Berdasarkan Id.
     * 
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\Plafon Instance.
     */
    public function deleteById($data) {
        return $this->id($data->id)->delete();
    }

    function getFilteredList($data) {
        $model = $this;
        
        if(!empty($data['kode'])) {
            $model = $model->where(['plafon.kode', '=', $data['kode']]);
        } 
        if(!empty($data['id_user'])) {
            $model = $model->whereOr(['id_user', '=', $data['id_user']]);
        }
        if(!empty($data['id_customer'])) {
            $model = $model->whereOr(['id_customer', '=', $data['id_customer']]);
        }
        if(!empty($data['id_principal'])) {
            $model = $model->whereOr(['id_principal', '=', $data['id_principal']]);
        }

        return  $model->orderBy('id')->select('/api/extra/getPlafon')->get();
    }
}