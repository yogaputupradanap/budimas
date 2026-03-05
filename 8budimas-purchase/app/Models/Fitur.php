<?php

namespace App\Models;
use Illuminate\Support\Facades\Session;

class Fitur extends Model
{
    /**
     * Setting Up Intial API Endpoint.
     */
    public function __construct(){
        parent::__construct();
        $this->endpoint = "/api/base/fitur";
    }
    
    function getFiturJabatanTersedia($id) {
        return  $this->select('/api/extra/getFiturJabatanTersedia?id='.$id)->get();
    }
    function getFiturUserTersedia($id) {
        return  $this->select('/api/extra/getFiturUserTersedia?id='.$id)->get();
    }
}