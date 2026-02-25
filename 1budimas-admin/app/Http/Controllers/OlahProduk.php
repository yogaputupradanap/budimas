<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\Produk;
use App\Models\ProdukHarga;
use App\Models\ProdukSatuan;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;
use Yajra\Datatables\Datatables;

class OlahProduk extends Controller
{
    /**
     * Menampilkan Master Page.
     * @param array|$nav Keterangan Breadcrumb Navigations.
     */
    public function index()
    {
        return view('contents.olah-produk', [
            'content' => (object) [
                'name' => 'Produk',
                'breadcrumb' => ['Olah Produk', 'Daftar Produk']
            ]
        ]);
    }

    /**
     * Menampilkan form tambah produk.
     */
    public function create()
    {
        return view('contents.olah-produk-create', [
            'content' => (object) [
                'name' => 'Produk',
                'breadcrumb' => ['Olah Produk', 'Tambah Produk']
            ]
        ]);
    }

    /**
     * Melakukan Request Action Insert.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     */
    public function store(Request $data)
    {
        try {
            // 1. Insert Produk dan dapatkan ID nya
            $idProduk = (new Produk)->returning('id')->insert($data);

            // 2. Insert multiple Harga Produk
            if (!empty($data->hargaList)) {
                foreach ($data->hargaList as $harga) {
                    $hargaData = new Request($harga);
                    $hargaData->merge(['idProduk' => $idProduk]);
                    (new ProdukHarga)->insert($hargaData);
                }
            }

            // 3. Insert multiple Satuan Produk
            if (!empty($data->satuanList)) {
                foreach ($data->satuanList as $satuan) {
                    $satuanData = new Request($satuan);
                    $satuanData->merge(['idProduk' => $idProduk]);
                    (new ProdukSatuan)->insert($satuanData);
                }
            }

            return response()->json(['success' => true], 200);
        } catch (\Exception $e) {
            return response()->json(['error' => $e->getMessage()], 500);
        }
    }

    /**
     * Melakukan Request Action Update.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     */
    public function update(Request $data)
    {
        return (new Produk)->updateById($data)->response();
    }

    /**
     * Melakukan Request Action Delete.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     */
    public function destroy(Request $request)
    {
        Log::info('Deleting data with ID: ' . $request->id);

        try {
            $response = (new Produk)->deleteById($request);

            Log::info('Delete response:', (array) $response);

            if ($response && isset($response->status) && $response->status == 200) {
                return response()->json(['success' => true]);
            } else {
                return response()->json(['success' => false, 'error' => $response], 500);
            }
        } catch (\Exception $e) {
            Log::error('Error deleting data:', ['error' => $e->getMessage()]);
            return response()->json(['success' => false, 'error' => $e->getMessage()], 500);
        }
    }

    /**
     * Mendapatkan Semua Data untuk Option.
     * @return Illuminate\Http\JsonResponse Data Berformat Opsi.
     */
    function showOptionData()
    {
        return option((new Produk)->all(), ['nama']);
    }

    /**
     * Mendapatkan Semua Data untuk Tabel.
     *
     * @var e_ Edited Column.
     * @var mix|$i Response Items (Columns).
     * @return Yajra\Datatables\Datatables Data Berformat Tabel.
     */
    function showTableData()
    {
        // Blade Components
        $btnAction = 'partials.components.btn-actions';
        $btnDetail = 'partials.components.btn-details';
        $btnStatus = 'partials.components.btn-status';
        $txtMoney = 'partials.components.txt-money';

        return DataTables::of((new Produk)->all())
            ->addColumn('', fn() => '')
            ->addColumn('actions', fn($i) => view($btnAction, ['id' => $i->id]))
            ->addColumn('detail_harga', fn($i) => view($btnDetail, ['id' => $i->id, 'name' => 'harga']))
            ->addColumn('detail_satuan', fn($i) => view($btnDetail, ['id' => $i->id, 'name' => 'satuan']))
            ->addColumn('e_status', fn($i) => view($btnStatus, ['id' => $i->id_status]))
            ->addColumn('e_harga_beli', fn($i) => view($txtMoney, ['val' => $i->harga_beli]))
            ->escapeColumns([])
            ->toJson();
    }
}
