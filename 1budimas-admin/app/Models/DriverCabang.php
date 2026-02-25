<?php

namespace App\Models;

use Illuminate\Support\Facades\Session;

class DriverCabang extends Model
{

    public function __construct()
    {
        parent::__construct();
        $this->endpoint = "/api/base/driver_cabang";
    }


    public function insert($data)
    {
        return parent::insert([
            'id_cabang'    => $data->idCabang ?? '',
            'id_driver'    => $data->idDriver ?? '',
        ]);
    }


    public function updateById($data)
    {
        return $this->id($data->id)->update([
            'id_cabang'    => $data->idCabang,
            'id_driver'    => $data->idDriver,
        ]);
    }

    public function deleteById($data)
    {
        return $this->id($data->id)->delete();
    }
}
