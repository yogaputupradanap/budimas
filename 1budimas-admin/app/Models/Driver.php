<?php

namespace App\Models;

use Illuminate\Support\Facades\Session;
use Exception;

class Driver extends Model
{
    /**
     * Setting Up Intial API Endpoint.
     */
    public function __construct()
    {
        parent::__construct();
        $this->endpoint = "/api/base/driver";
    }

    /**
     * @method Override.
     */
    function all()
    {
        return $this->select('/api/extra/getDriver')->get();
    }

    /**
     * Insert Data Baru.
     *
     * @method Override.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\Driver Instance.
     */
    public function insert($data)
    {
        try {
            // Insert ke table driver
            $this->endpoint = '/api/base/driver';
            $this->returning('id');

            $driverResponse = parent::insert([
                'id_user' => $data->idUser ?? '',
                'id_armada' => $data->idArmada ?? null,
                'id_wilayah1' => $data->idWilayah1 ?? '',
                'id_wilayah2' => $data->idWilayah2 ?? '',
            ]);

            // Cek apakah response berhasil
            if ($driverResponse && $driverResponse->response && $driverResponse->response->status == 200) {
                $this->response = (object) [
                    'status' => 200,
                    'result' => $driverResponse->get()
                ];
            } else {
                $this->response = (object) [
                    'status' => 422,
                    'result' => ['message' => 'Gagal menyimpan data driver']
                ];
            }
        } catch (Exception $e) {
            $this->response = (object) [
                'status' => 500,
                'result' => ['message' => 'Error saat menyimpan data: ' . $e->getMessage()]
            ];
        }

        return $this;
    }

    /**
     * Update Data Berdasarkan Id.
     *
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return Model Instance with response.
     */
    public function updateById($data)
    {
        try {
            // Update table driver
            $this->endpoint = '/api/base/driver';
            $driverResponse = $this
                ->where(['id', '=', $data->idDriver])
                ->update([
                    'id_user' => $data->idUser ?? '',
                    'id_armada' => $data->idArmada ?? '',
                    'id_wilayah1' => $data->idWilayah1 ?? '',
                    'id_wilayah2' => $data->idWilayah2 ?? '',
                ]);

            $this->response = (object) [
                'status' => 200,
                'result' => $driverResponse->get()
            ];
        } catch (Exception $e) {
            $this->response = (object) [
                'status' => 500,
                'result' => ['message' => $e->getMessage()]
            ];
        }

        return $this;
    }

    /**
     * Delete Data Berdasarkan Id.
     *
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return Model Instance with response.
     */
    public function deleteById($data)
    {
        try {

            // Hapus dari table driver
            $this->endpoint = '/api/base/driver';
            $driverResponse = $this->where(['id', '=', $data->id])->delete();

            $this->response = (object) [
                'status' => 200,
                'result' => [
                    'driver' => $driverResponse->get()
                ]
            ];
        } catch (Exception $e) {
            $this->response = (object) [
                'status' => 500,
                'result' => ['message' => 'Error saat menghapus data: ' . $e->getMessage()]
            ];
        }

        return $this;
    }
}
