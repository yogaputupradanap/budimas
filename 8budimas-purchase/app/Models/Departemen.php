<?php

namespace App\Models;
use Illuminate\Support\Facades\Session;

class Departemen extends Model
{
    /**
     * Setting Up Intial API Endpoint.
     */
    public function __construct(){
        parent::__construct();
        $this->endpoint = "/api/base/departemen";
    }
    
}