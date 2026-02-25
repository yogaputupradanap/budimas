<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\Plafon;
use App\Models\PlafonJadwal;
use Illuminate\Http\Request;
use Yajra\Datatables\Datatables;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Log;

class OlahPlafon extends Controller
{
    /**
     * Menampilkan Master Page.
     */
    public function index()
    {
        return view('contents.olah-plafon', [
            'content' => (object) [
                'name' => 'Plafon',
                'breadcrumb' => ['Olah Plafon', 'Daftar Plafon']
            ]
        ]);
    }

    /**
     * Melakukan Request Action Insert.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     */
    public function store(Request $request)
    {
        // Validasi input
        $request->validate([
            'id_customer'  => 'required|integer',
            'id_principal' => 'required|array|min:1',
            'id_principal.*' => 'integer',
            'id_sales'     => 'required|integer',
            'limit'        => 'required|numeric|min:0',
            'kode'         => 'nullable|string',
            'top'          => 'nullable|integer',
            'lock_order'   => 'nullable|boolean',
            'id_tipe_harga'=> 'nullable|integer',
        ]);

        try {
            $modelPlafon = new Plafon();
            $principalIds = $request->id_principal;

            $insertedIds = [];

            foreach ($principalIds as $principalId) {
                // Insert ke tabel plafon dan ambil ID
                $plafonId = $modelPlafon->simpanData([
                    'id_customer'   => $request->id_customer,
                    'id_principal'  => $principalId,
                    'id_sales'      => $request->id_sales,
                    'id_user'       => auth()->id(), // pastikan user login
                    'kode'          => $request->kode,
                    'limit'         => $request->limit,
                    'top'           => $request->top,
                    'lock_order'    => $request->lock_order,
                    'id_tipe_harga' => $request->id_tipe_harga,
                ]);

                if (!$plafonId) {
                    throw new \Exception("Gagal menyimpan Plafon untuk principal ID: $principalId");
                }

                $insertedIds[] = $plafonId;
            }

            return response()->json([
                'status' => 'success',
                'message' => 'Plafon berhasil disimpan',
                'data' => $insertedIds
            ], 201);

        } catch (\Exception $e) {
            Log::error("Gagal Simpan Plafon: " . $e->getMessage());

            return response()->json([
                'status' => 'error',
                'message' => 'Terjadi kesalahan saat menyimpan data Plafon',
                'error' => $e->getMessage()
            ], 500);
        }
    }
    /**
     * Melakukan Request Action Update.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     */
    public function update(Request $data)
    {
        return (new Plafon)->updateById($data)->response();
    }

    /**
     * Melakukan Request Action Delete.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     */
    public function destroy(Request $data)
    {
        return (new Plafon)->deleteById($data)->response();
    }

    /**
     * Mendapatkan Semua Data untuk Option.
     * @return Illuminate\Http\JsonResponse Data Berformat Opsi.
     */
    function showOptionData()
    {
        return option((new Plafon)->all(), ['nama']);
    }

    /**
     * Mendapatkan Semua Data untuk Tabel.
     *
     * @var e_ Edited Column.
     * @var mix|$i Response Items (Columns).
     * @return Yajra\Datatables\Datatables Data Berformat Tabel.
     */
    public function showTableData(Request $request)
    {
        $draw = $request->get('draw');
        $start = $request->get('start');
        $length = $request->get('length');
        $search = $request->get('search')['value'];
        $order = $request->get('order');
        $columns = $request->get('columns');

        $plafon = new Plafon();

        // Buat query string untuk filter dan sorting
        $queryParams = [
            'draw' => $draw,
            'start' => $start,
            'length' => $length,
            'search[value]' => $search,
        ];

        if (!empty($order)) {
            $columnIndex = $order[0]['column'];
            $columnName = $columns[$columnIndex]['data'];
            $queryParams['order[0][column]'] = $columnName;
            $queryParams['order[0][dir]'] = $order[0]['dir'];
        }

        // Gabungkan query params ke dalam string
        $queryString = http_build_query($queryParams);

        // Panggil API dengan query string
        $response = $plafon->select1('/api/extra/getPlafon?' . $queryString);

        // Format ulang data untuk actions column dan lainnya
        $formattedData = array_map(function ($item) {
            $item->actions = view('partials.components.btn-actions', ['id' => $item->id])->render();
            $item->detail_jadwal = view('partials.components.btn-details', ['id' => $item->id, 'name' => 'jadwal'])->render();
            $item->limit_bon_display = view('partials.components.txt-money', ['val' => $item->limit_bon])->render();
            return $item;
        }, $plafon->get1());

        return response()->json([
            'draw' => $plafon->getDraw(),
            'recordsTotal' => $plafon->count1(),
            'recordsFiltered' => $plafon->filteredCount(),
            'data' => $formattedData
        ]);
    }
}
