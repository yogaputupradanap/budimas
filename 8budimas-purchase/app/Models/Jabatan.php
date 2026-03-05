<?php

namespace App\Models;
use Illuminate\Support\Facades\Session;

class Jabatan extends Model
{
    /**
     * Setting Up Intial API Endpoint.
     */
    public function __construct(){
        parent::__construct();
        $this->endpoint = "/api/base/jabatan";
    }
    
}