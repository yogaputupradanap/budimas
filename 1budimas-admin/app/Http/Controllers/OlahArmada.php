<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Yajra\Datatables\Datatables;
use Illuminate\Http\Request;
use App\Models\Armada;

class OlahArmada extends Controller
{
    /**
     * Menampilkan Master Page.
     */
    public function index()
    {
        return view('contents.olah-armada', [
            'content' => (object) [
                'name'       => 'Armada',
                'breadcrumb' => ['Olah Data Armada', 'Daftar Armada']
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
            // Insert armada
            $armada = new Armada();
            $armada->insert($data);

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
            // Update armada
            $armada = (new Armada)->updateById($data);

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
        return (new Armada)->deleteById($data)->response();
    }

    /**
     * Mendapatkan Semua Data untuk Option.
     * @return Illuminate\Http\JsonResponse Data Berformat Opsi.
     */
    function showOptionData()
    {
        return option((new Armada)->all(), ['nama']);
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
        $btnStatus = 'partials.components.btn-status';
        $txtKet    = 'partials.components.txt-ket';
        $txtNumber = 'partials.components.txt-number';

        return DataTables::of((new Armada)->all())
            ->addColumn('',              fn()   => "")
            ->addColumn('actions',       fn($i) => view($btnAction, ['id' => $i->id]))
            ->addColumn('e_kubikasi',    fn($i) => view($txtNumber, ['val' => $i->kubikasi]))
            ->addColumn('e_status',      fn($i) => view($btnStatus, ['id' => $i->id_status]))
            ->addColumn('e_kendaraan',   fn($i) => $i->nama . view($txtKet, ['val' => $i->no_pelat]))
            ->editColumn('tanggal_stnk',  fn($i) => stringDateFormater($i->tanggal_stnk))
            ->editColumn('tanggal_uji',   fn($i) => stringDateFormater($i->tanggal_uji))
            ->escapeColumns([])
            ->toJson();
    }
}
