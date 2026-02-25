<?php

namespace App\Models;

use Illuminate\Support\Facades\Session;

class Armada extends Model
{
    /**
     * Setting Up Intial API Endpoint.
     */
    public function __construct()
    {
        parent::__construct();
        $this->endpoint = "/api/base/armada";
    }

    /**
     * @method Override.
     */
    function all()
    {
        return $this->select('/api/extra/getArmada')->get();
    }

    /**
     * Insert Data Baru.
     *
     * @method Override.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\Armada Instance.
     */
    public function insert($data)
    {
        return parent::insert([
            'id_tipe'      => $data->idTipe ?? '',
            'id_status'    => $data->idStatus ?? '',
            'nama'         => $data->nama ?? '',
            'no_pelat'     => $data->noPelat ?? '',
            'kubikasi'     => $data->kubikasi ?? '',
            'tanggal_stnk' => $data->tanggalStnk ?? '',
            'tanggal_uji'  => $data->tanggalUji ?? '',
            'keterangan'   => $data->keterangan ?? '',
            'id_cabang'    => $data->idCabang ?? '',
        ]);
    }

    /**
     * Update Data Berdasarkan Id.
     *
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\Armada Instance.
     */
    public function updateById($data)
    {
        return $this->id($data->id)->update([
            'id_tipe'      => $data->idTipe,
            'id_status'    => $data->idStatus,
            'nama'         => $data->nama,
            'no_pelat'     => $data->noPelat,
            'kubikasi'     => $data->kubikasi,
            'tanggal_stnk' => $data->tanggalStnk,
            'tanggal_uji'  => $data->tanggalUji,
            'keterangan'   => $data->keterangan,
            'id_cabang'    => $data->idCabang,
        ]);
    }

    /**
     * Delete Data Berdasarkan Id.
     *
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\Armada Instance.
     */
    public function deleteById($data)
    {
        return $this->id($data->id)->delete();
    }
}
