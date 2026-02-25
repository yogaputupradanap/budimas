<?php

namespace App\Models;

use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Session;

class Produk extends Model
{
    public function __construct()
    {
        parent::__construct();
        $this->endpoint = '/api/base/produk';
    }

    /**
     * @method Override.
     */
    function all()
    {
        return $this->select('/api/extra/getProduk')->get();
    }

    /**
     * Insert Data Baru.
     *
     * @method Override.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\Produk Instance.
     */
    public function insert($data)
    {
        return parent::insert([
            'id_principal' => $data->idPrincipal ?? '',
            'id_brand' => $data->idBrand ?? '',
            'id_kategori' => $data->idKategori ?? '',
            'id_status' => $data->idStatus ?? '',
            'ppn' => $data->ppn ?? '',
            'nama' => $data->nama ?? '',
            'kode_sku' => $data->kodeSku ?? '',
            'kode_ean' => $data->kodeEan ?? '',
            'harga_beli' => $data->hargaBeli ?? '',
            'keterangan' => $data->keterangan ?? ''
        ])->first()->id;
    }

    /**
     * Update Data Berdasarkan Id.
     *
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\Produk Instance.
     */
    public function updateById($data)
    {
        return $this->id($data->id)->update([
            'id_principal' => $data->idPrincipal ?? '',
            'id_brand' => $data->idBrand ?? '',
            'id_kategori' => $data->idKategori ?? '',
            'id_status' => $data->idStatus ?? '',
            'ppn' => $data->ppn ?? '',
            'nama' => $data->nama ?? '',
            'kode_sku' => $data->kodeSku ?? '',
            'kode_ean' => $data->kodeEan ?? '',
            'harga_beli' => $data->hargaBeli ?? '',
            'keterangan' => $data->keterangan ?? ''
        ]);
    }

    /**
     * Delete Data Berdasarkan Id.
     *
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\Produk Instance.
     */
    public function deleteById($data)
    {
        return $this->id($data->id)->delete();
    }

    public function delete()
    {
        $this->builder()->response = Http::withToken($this->token)
            ->delete(self::$baseURL . $this->endpoint . $this->query)
            ->object();

        $this->demolisher();
        return $this->response;
    }
}
