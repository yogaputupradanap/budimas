<?php

namespace App\Models;

use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Session;

class Plafon extends Model
{
    /**
     * Setting Up Intial API Endpoint.
     */
    public function __construct()
    {
        parent::__construct();
        $this->endpoint = '/api/base/plafon';
    }

    /**
     * @method Override.
     */
    function all()
    {
        return $this->select('/api/extra/getPlafon')->get();
    }

    /**
     * Insert Data Baru.
     *
     * @method Override.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\Plafon Instance.
     */
    public function simpanData($data)
{
    try {
        // Karena $data adalah ARRAY, gunakan sintaks $data['key']
        $limitBon = $data['limit'] ?? 0;
        
        // Langsung insert satu record
        // Menggunakan return parent::insert agar mengembalikan object/ID hasil insert
        return parent::insert([
            'id_customer'   => $data['id_customer'] ?? '',
            'id_principal'  => $data['id_principal'] ?? '',
            'id_user'       => $data['id_user'] ?? '',
            'id_sales'      => $data['id_sales'] ?? '',
            'limit_bon'     => $limitBon,
            'sisa_bon'      => $limitBon,
                'kode'      => ($data['kode'] ?? 'PL') . '-' . $data['id_principal'] . '-' . rand(10,99), 
            'top'           => $data['top'] ?? '',
            'lock_order'    => $data['lock_order'] ?? '',
            'id_tipe_harga' => $data['id_tipe_harga'] ?? ''
        ]);

    } catch (\Exception $e) {
        Log::error('Error saat insert Plafon:', [
            'error_message' => $e->getMessage(),
            'data' => $data,
            'time' => now()->format('Y-m-d H:i:s')
        ]);
        throw $e;
    }
}

    /**
     * Update Data Berdasarkan Id.
     *
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\Plafon Instance.
     */
    public function updateById($data)
    {
        try {
            return $this->id($data->id)->update([
                'id_customer' => $data->idCustomer ?? '',
                'id_principal' => $data->idPrincipal ?? '',
                'id_user' => $data->idUser ?? '',
                'id_sales' => $data->idSales ?? '',
                'limit_bon' => $data->limit ?? 0,
                'sisa_bon' => $data->sisaBon ?? 0, // Terima hasil perhitungan dari blade
                'kode' => $data->kode ?? '',
                'top' => $data->top ?? '',
                'lock_order' => $data->lockOrder ?? '',
                'id_tipe_harga' => $data->idTipeHarga ?? ''
            ]);
        } catch (\Exception $e) {
            Log::error('Error saat update Plafon:', [
                'error_message' => $e->getMessage(),
                'error_line' => $e->getLine(),
                'error_file' => $e->getFile(),
                'data' => $data,
                'time' => now()->format('Y-m-d H:i:s')
            ]);

            throw $e;
        }
    }

    /**
     * Delete Data Berdasarkan Id.
     *
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\Plafon Instance.
     */
    public function deleteById($data)
    {
        return $this->id($data->id)->delete();
    }

    /**
     * Mendapatkan List Data dengan Filter.
     *
     * @param array|$data Filter Data Array.
     * @return Collection List of App\Models\Plafon Instance.
     */
    function getFilteredList($data)
    {
        $model = $this;

        if (!empty($data['kode'])) {
            $model = $model->where(['plafon.kode', '=', $data['kode']]);
        }
        if (!empty($data['id_user'])) {
            $model = $model->whereOr(['id_user', '=', $data['id_user']]);
        }
        if (!empty($data['id_customer'])) {
            $model = $model->whereOr(['id_customer', '=', $data['id_customer']]);
        }
        if (!empty($data['id_principal'])) {
            $model = $model->whereOr(['id_principal', '=', $data['id_principal']]);
        }

        return $model->orderBy('id')->select('/api/extra/getPlafon')->get();
    }

    /**
     * Mendapatkan Data untuk Export CSV.
     *
     * @return Collection List of App\Models\Plafon Instance.
     */
    function ExportCsv()
    {
        return $this->select('/api/extra/getPlafonCsv')->get();
    }
}
