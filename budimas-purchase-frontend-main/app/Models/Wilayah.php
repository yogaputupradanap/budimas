<?php

namespace App\Models;
use Illuminate\Support\Facades\Session;

class Wilayah extends Model
{
    /**
     * Mendapatkan Semua Data Wilayah1.
     * @return object (N) Data Wilayah1.
     */
    function getProvinsi() {
        return $this->orderBy('id')->select('/api/base/wilayah1')->get();
    }

    /**
     * Mendapatkan Data Wilayah2 Berdasarkan Id Wilayah1.
     * 
     * @param integer|$id id_wilayah1.
     * @return object (N) Data Wilayah2.
     */ 
    function getKabupatenKota($id) {
        return $this->orderBy('id')->where(["id_wilayah1", "=", $id])
               ->select('/api/base/wilayah2')->get();
    }

    /**
     * Mendapatkan Data Wilayah3 Berdasarkan Id Wilayah2.
     * 
     * @param integer|$id id_wilayah2.
     * @return object (N) Data Wilayah3.
     */  
    function getKecamatan($id) {
        return $this->orderBy('id')->where(["id_wilayah2", "=", $id])
               ->select('/api/base/wilayah3')->get();
    }
    
    /**
     * Mendapatkan Data Wilayah4 Berdasarkan Id Wilayah3.
     * 
     * @param integer|$id id_wilayah3.
     * @return object (N) Data Wilayah4.
     */  
    function getKelurahan($id) {
        return $this->orderBy('id')->where(["id_wilayah3", "=", $id])
               ->select('/api/base/wilayah4')->get();
    }
}