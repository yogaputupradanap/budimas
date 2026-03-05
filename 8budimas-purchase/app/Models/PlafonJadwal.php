<?php

namespace App\Models;
use Illuminate\Support\Facades\Session;

class PlafonJadwal extends Model
{
    /**
     * Setting Up Intial API Endpoint.
     */
    public function __construct(){
        parent::__construct();
        $this->endpoint = "/api/base/plafon_jadwal";
    }
    
    /**
     * @method Override.
     */
    function all() {
        return $this->select('/api/extra/getPlafonJadwal')->get();
    } 

    /**
     * 
     */
    function getListByIdPlafon($id) {
        return $this->where(['id_plafon', '=', $id])->orderBy('id')->select()->get();
    } 
    
    /**
     * Insert Data Baru.
     * r
     * @method Override.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\PlafonJadwal Instance.
     */
    public function insert($data) {
        if (!is_object($data)) {
            $data = (object) $data;
        }
        return parent::insert([
            'id_plafon'          => $data->idPlafon ?? '',
            'id_tipe_kunjungan'  => $data->idTipeKunjungan ?? '',
            'id_hari'            => $data->idHari ?? '',
            'id_minggu'          => $data->idMinggu ?? '',
            'id_status'          => $data->idStatus ?? ''
        ]);
    }

    /**
     * Update Data Berdasarkan Id.
     * 
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\PlafonJadwal Instance.
     */
    public function updateById($data) {
        return $this->id($data->id)->update([
            'id_plafon'          => $data->idPlafon ?? '',
            'id_tipe_kunjungan'  => $data->idTipeKunjungan ?? '',
            'id_hari'            => $data->idHari ?? '',
            'id_minggu'          => $data->idMinggu ?? '',
            'id_status'          => $data->idStatus ?? ''
        ]);
    }

    /**
     * Delete Data Berdasarkan Id.
     * 
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\PlafonJadwal Instance.
     */
    public function deleteById($data) {
        return $this->id($data->id)->delete();
    }
}