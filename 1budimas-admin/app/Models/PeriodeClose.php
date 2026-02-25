<?php

namespace App\Models;

class PeriodeClose extends Model
{
    /**
     * Setting Up Intial API Endpoint.
     */
    public function __construct()
    {
        parent::__construct();
        $this->endpoint = "/api/base/periode_closed";
    }

    /**
     * @method Override.
     */
    function all()
    {
        return $this->select('/api/extra/getPeriodeClosed')->get();
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
            'tanggal_close' => $data->tanggalClose ?? '',
            'keterangan' => $data->keterangan ?? '',
            'id_cabang' => $data->idCabang ?? '',
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
        return $this->id_custom($data->id_periode, 'id_periode')->update([
            'tanggal_close' => $data->tanggalClose,
            'keterangan' => $data->keterangan,
            'id_cabang' => $data->idCabang,
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
        return $this->id_custom($data->id_periode, 'id_periode')->delete();
    }
}
