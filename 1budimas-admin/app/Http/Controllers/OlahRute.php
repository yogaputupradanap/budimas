<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\Rute;
use App\Models\RuteCabang;
use Illuminate\Http\Request;
use Yajra\Datatables\Datatables;

class OlahRute extends Controller
{
    /**
     * Menampilkan Master Page.
     */
    public function index()
    {
        return view('contents.olah-rute', [
            'content' => (object) [
                'name' => 'Rute',
                'breadcrumb' => ['Olah Data Rute', 'Daftar Rute']
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
            // Insert rute
            $rute = new Rute();
            $rute->insert($data);

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
        try {
            // Update rute
            $rute = (new Rute)->updateById($data);

            return response()->json(['success' => true], 200);
        } catch (\Exception $e) {
            return response()->json(['error' => $e->getMessage()], 500);
        }
    }

    /**
     * Melakukan Request Action Delete.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     */
    public function destroy(Request $data)
    {
        return (new Rute)->deleteById($data)->response();
    }

    /**
     * Mendapatkan Semua Data untuk Option.
     * @return Illuminate\Http\JsonResponse Data Berformat Opsi.
     */
    function showOptionData()
    {
        return option((new Rute)->all(), ['kode', 'nama_rute']);
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
        $button1 = 'partials.components.btn-actions';

        return DataTables::of((new Rute)->all())
            ->addColumn('', fn() => '')
            ->addColumn('actions', fn($i) => view($button1, ['id' => $i->id]))
            ->escapeColumns([])
            ->toJson();
    }
}
