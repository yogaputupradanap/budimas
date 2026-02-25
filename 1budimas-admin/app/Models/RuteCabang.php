<?php

namespace App\Models;

use Illuminate\Support\Facades\Session;

class RuteCabang extends Model
{

    public function __construct()
    {
        parent::__construct();
        $this->endpoint = "/api/base/rute_cabang";
    }


    public function insert($data)
    {
        return parent::insert([
            'id_cabang'    => $data->idCabang ?? '',
            'id_rute'    => $data->idRute ?? '',
        ]);
    }


    public function updateById($data)
    {
        return $this->id($data->id)->update([
            'id_cabang'    => $data->idCabang,
            'id_rute'    => $data->idRute,
        ]);
    }

    public function deleteById($data)
    {
        return $this->id($data->id)->delete();
    }
}
