<?php

namespace App\Models;
use Illuminate\Support\Facades\Session;

class PlafonWeek extends Model
{
    /**
     * Setting Up Intial API Endpoint.
     */
    public function __construct(){
        parent::__construct();
        $this->endpoint = "/api/base/plafon_week";
    }
    
    function getCurrentWeek() {
        return $this->select('/api/extra/getcurrentPlafonWeek')->first();
    } 

    /**
     * Insert Data Baru.
     * 
     * @method Override.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\PlafonWeek Instance.
     */
    public function insert($data) {
        return parent::insert([
            'tanggal' => $data->tanggal ?? '',
            'minggu'  => $data->minggu ?? ''
        ]);
    }

    /**
     * Update Data Berdasarkan Id.
     * 
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\PlafonWeek Instance.
     */
    public function updateById($data) {
        return $this->id($data->id)->update([
            'tanggal' => $data->tanggal ?? '',
            'minggu'  => $data->minggu ?? ''
        ]);
    }

    /**
     * Delete Data Berdasarkan Id.
     * 
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\PlafonWeek Instance.
     */
    public function deleteById($data) {
        return $this->id($data->id)->delete();
    }
}