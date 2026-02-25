<?php

namespace App\Http\Controllers;
use App\Http\Controllers\Controller;
use Yajra\Datatables\Datatables;
use Illuminate\Http\Request;
use App\Models\Cabang;

class OlahCabang extends Controller {
    /**
     * Menampilkan Master Page.
     */
    public function index() {
        return view('contents.olah-cabang', [
            'content' => (object) [
                'name'       => 'Cabang',
                'breadcrumb' => ['Olah Data Cabang', 'Daftar Cabang']
            ]
        ]);
    }

    /**
     * Melakukan Request Action Insert.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     */
    public function store(Request $data) {
        return (new Cabang)->insert($data)->response();
    }

    /**
     * Melakukan Request Action Update.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     */
    public function update(Request $data) {
        return (new Cabang)->updateById($data)->response();
    }

    /**
     * Melakukan Request Action Delete.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     */
    public function destroy(Request $data) {
        return (new Cabang)->deleteById($data)->response();
    }

     /**
     * Mendapatkan Semua Data untuk Option.
     * @return Illuminate\Http\JsonResponse Data Berformat Opsi.
     */
    function showOptionData() {
        return option((new Cabang)->all(), ['nama']);
    }

    /**
     * Mendapatkan Semua Data untuk Tabel.
     * 
     * @var e_ Edited Column.
     * @var mix|$i Response Items (Columns).
     * @return Yajra\Datatables\Datatables Data Berformat Tabel.
     */
    function showTableData() {
        // Blade Components
        $button1 = 'partials.components.btn-actions';
        
        return DataTables::of((new Cabang)->all())
            ->addColumn('', fn() => "")
            ->addColumn('actions', fn($i) => view($button1, ['id' => $i->id]))
            ->escapeColumns([])
            ->toJson();
    }
}