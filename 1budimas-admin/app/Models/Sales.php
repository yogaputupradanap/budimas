<?php

namespace App\Models;

use Exception;

class Sales extends Model
{
    /**
     * Setting Up Intial API Endpoint.
     */
    public function __construct()
    {
        parent::__construct();
        $this->endpoint = '/api/base/sales';
    }

    /**
     * @method Override.
     */
    function all()
    {
        return $this->select('/api/extra/getSales')->get();
    }

    function all_on_multiple_principal()
    {
        return $this->select('/api/base/sales_principal_assignment')->get();
    }

    /**
     * Insert Data Baru.
     *
     * @method Override.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\Sales Instance.
     */
    public function insert($data)
    {
        try {
            // Insert ke table sales
            $this->endpoint = '/api/base/sales';
            $this->returning('id');  // Memastikan ID dikembalikan setelah insert

            $salesResponse = null;
            $isMoreThanOnePrincipal = is_array($data->idPrincipal) && count($data->idPrincipal) > 1;
            if ($isMoreThanOnePrincipal) {
                $salesResponse = parent::insert([
                    'id_user' => $data->idUser ?? '',
                    'id_wilayah1' => $data->idWilayah1 ?? '',
                    'id_wilayah2' => $data->idWilayah2 ?? '',
                    'id_tipe' => $data->idTipe ?? '',
                ]);
            } else {
                $salesResponse = parent::insert([
                    'id_user' => $data->idUser ?? '',
                    'id_principal' => $data->idPrincipal[0] ?? '',
                    'id_wilayah1' => $data->idWilayah1 ?? '',
                    'id_wilayah2' => $data->idWilayah2 ?? '',
                    'id_tipe' => $data->idTipe ?? '',
                ]);
            }

            if ($salesResponse->get() && !empty($salesResponse->get()[0]->id)) {
                $salesId = $salesResponse->get()[0]->id;

                // Insert ke table sales_detail
                $this->endpoint = '/api/base/sales_detail';
                $detailResponse = parent::insert([
                    'id_sales' => $salesId,
                    'kode_sales' => $data->kodeSales ?? '',
                ]);
                if ($isMoreThanOnePrincipal) {
                    $this->endpoint = '/api/base/sales_principal_assignment';
                    foreach ($data->idPrincipal as $principalId) {
                        parent::insert([
                            'id_sales' => $salesId,
                            'id_principal' => $principalId,
                        ]);
                    }
                }


                // Set response untuk parent model
                $this->response = (object)[
                    'status' => 200,
                    'result' => [
                        'sales' => $salesResponse->get(),
                        'sales_detail' => $detailResponse->get()
                    ]
                ];
            } else {
                $this->response = (object)[
                    'status' => 422,
                    'result' => ['message' => 'Gagal menyimpan data sales']
                ];
            }
        } catch (Exception $e) {
            $this->response = (object)[
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
            // Update table sales
            $this->endpoint = '/api/base/sales';
            $isMoreThanOnePrincipal = is_array($data->idPrincipal) && count($data->idPrincipal) > 1;

            if ($isMoreThanOnePrincipal) {
                $salesResponse = $this
                    ->where(['id', '=', $data->idSales])
                    ->update([
                        'id_user' => $data->idUser ?? '',
                        'id_principal' => '',
                        'id_wilayah1' => $data->idWilayah1 ?? '',
                        'id_wilayah2' => $data->idWilayah2 ?? '',
                        'id_tipe' => $data->idTipe ?? '',
                    ]);
            } else {
                $salesResponse = $this
                    ->where(['id', '=', $data->idSales])
                    ->update([
                        'id_user' => $data->idUser ?? '',
                        'id_principal' => $data->idPrincipal[0] ?? '',
                        'id_wilayah1' => $data->idWilayah1 ?? '',
                        'id_wilayah2' => $data->idWilayah2 ?? '',
                        'id_tipe' => $data->idTipe ?? '',
                    ]);
            }
            // Cek apakah sales_detail sudah ada
            $this->endpoint = '/api/base/sales_detail';
            $existingDetail = $this->where(['id_sales', '=', $data->idSales])->select()->get();

            if (empty($existingDetail)) {
                // Jika belum ada, insert baru
                $detailResponse = parent::insert([
                    'id_sales' => $data->idSales,
                    'kode_sales' => $data->kodeSales ?? '',
                ]);
            } else {
                // Jika sudah ada, update
                $detailResponse = $this
                    ->where(['id_sales', '=', $data->idSales])
                    ->update([
                        'kode_sales' => $data->kodeSales ?? '',
                    ]);
            }

            // Hapus assignment principal lama
            $this->endpoint = '/api/base/sales_principal_assignment';
            $this->where(['id_sales', '=', $data->idSales])->delete();

            if ($isMoreThanOnePrincipal) {

                // Tambah assignment principal baru
                foreach ($data->idPrincipal as $principalId) {
                    parent::insert([
                        'id_sales' => $data->idSales,
                        'id_principal' => $principalId,
                    ]);
                }
            }

            $this->response = (object)[
                'status' => 200,
                'result' => [
                    'sales' => $salesResponse->get(),
                    'sales_detail' => $detailResponse->get()
                ]
            ];
        } catch (Exception $e) {
            $this->response = (object)[
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

            // Hapus dari table sales_principal_assignment terlebih dahulu
            $this->endpoint = '/api/base/sales_principal_assignment';
            $this->where(['id_sales', '=', $data->id])->delete();

            // Hapus dari table sales_detail terlebih dahulu
            $this->endpoint = '/api/base/sales_detail';
            $detailResponse = $this->where(['id_sales', '=', $data->id])->delete();

            // Hapus dari table sales
            $this->endpoint = '/api/base/sales';
            $salesResponse = $this->where(['id', '=', $data->id])->delete();

            $this->response = (object)[
                'status' => 200,
                'result' => [
                    'sales' => $salesResponse->get(),
                    'sales_detail' => $detailResponse->get()
                ]
            ];
        } catch (Exception $e) {
            $this->response = (object)[
                'status' => 500,
                'result' => ['message' => 'Error saat menghapus data: ' . $e->getMessage()]
            ];
        }

        return $this;
    }

    function ExportCsv()
    {
        return $this->select('/api/extra/getSalesCsv')->get();
    }
}
