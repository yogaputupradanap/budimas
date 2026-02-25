<?php

namespace App\Models;

use Illuminate\Support\Facades\Session;

class ArmadaCabang extends Model
{

    public function __construct()
    {
        parent::__construct();
        $this->endpoint = "/api/base/armada_cabang";
    }


    public function insert($data)
    {
        return parent::insert([
            'id_cabang'    => $data->idCabang ?? '',
            'id_armada'    => $data->idArmada ?? '',
        ]);
    }


    public function updateById($data)
    {
        return $this->id($data->id)->update([
            'id_cabang'    => $data->idCabang,
            'id_armada'    => $data->idArmada,
        ]);
    }

    public function deleteById($data)
    {
        return $this->id($data->id)->delete();
    }
}
