<?php

namespace App\Models;

use Illuminate\Support\Facades\Session;

class Rute extends Model
{
    /**
     * Setting Up Intial API Endpoint.
     */
    public function __construct()
    {
        parent::__construct();
        $this->endpoint = "/api/base/rute";
    }

    /**
     * @method Override.
     */
    function all()
    {
        return $this->select('/api/extra/getRute')->get();
    }

    /**
     * Insert Data Baru.
     *
     * @method Override.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\Rute Instance.
     */
    public function insert($data)
    {
        return parent::insert([
            'id_cabang'    => $data->idCabang ?? '',
            'kode'         => $data->kode ?? '',
            'nama_rute'    => $data->namaRute ?? '',
            'deskripsi'    => $data->deskripsi ?? ''
        ]);
    }

    /**
     * Update Data Berdasarkan Id.
     *
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\Rute Instance.
     */
    public function updateById($data)
    {
        return $this->id($data->id)->update([
            'id_cabang'    => $data->idCabang ?? '',
            'kode'         => $data->kode ?? '',
            'nama_rute'    => $data->namaRute ?? '',
            'deskripsi'    => $data->deskripsi ?? ''
        ]);
    }

    /**
     * Delete Data Berdasarkan Id.
     *
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\Rute Instance.
     */
    public function deleteById($data)
    {
        return $this->id($data->id)->delete();
    }
}
