<?php

namespace App\Models;

use Illuminate\Support\Facades\Session;

class Perusahaan extends Model
{
    /**
     * Setting Up Intial API Endpoint.
     */
    public function __construct()
    {
        parent::__construct();
        $this->endpoint = "/api/base/perusahaan";
    }

    /**
     * Insert Data Baru.
     *
     * @method Override.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\Perusahaan Instance.
     */
    public function insert($data)
    {
        return parent::insert([
            'kode'        => $data->kode ?? '',
            'nama'        => $data->nama ?? '',
            'alamat'      => $data->alamat ?? '',
            'telepon'     => $data->telepon ?? '',
            'npwp'        => $data->npwp ?? '',
            'id_wilayah1' => $data->idWilayah1 ?? '',
            'id_wilayah2' => $data->idWilayah2 ?? '',
            'id_wilayah3' => $data->idWilayah3 ?? '',
            'id_wilayah4' => $data->idWilayah4 ?? ''
        ]);
    }

    /**
     * Update Data Berdasarkan Id.
     *
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\Perusahaan Instance.
     */
    public function updateById($data)
    {
        return $this->id($data->id)->update([
            'kode'        => $data->kode ?? '',
            'nama'        => $data->nama ?? '',
            'alamat'      => $data->alamat ?? '',
            'telepon'     => $data->telepon ?? '',
            'npwp'        => $data->npwp ?? '',
            'id_wilayah1' => $data->idWilayah1 ?? '',
            'id_wilayah2' => $data->idWilayah2 ?? '',
            'id_wilayah3' => $data->idWilayah3 ?? '',
            'id_wilayah4' => $data->idWilayah4 ?? ''
        ]);
    }

    /**
     * Delete Data Berdasarkan Id.
     *
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\Perusahaan Instance.
     */
    public function deleteById($data)
    {
        return $this->id($data->id)->delete();
    }

    public function all()
    {
        return $this->select('/api/extra/getPerusahaan')->get();
    }

    function GetSample(){
        return parent::limit(1)->all();
    }
}
