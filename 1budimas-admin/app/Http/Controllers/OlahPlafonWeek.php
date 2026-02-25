<?php

namespace App\Http\Controllers;
use App\Http\Controllers\Controller;
use Yajra\Datatables\Datatables;
use Illuminate\Http\Request;
use App\Models\PlafonWeek;

class OlahPlafonWeek extends Controller {
    /**
     * Menampilkan Master Page.
     */
    public function index() {
        return view('contents.olah-plafon-week', [
            'content' => (object) [
                'name'       => 'Plafon Week',
                'breadcrumb' => ['Olah Plafon', 'Daftar Plafon', 'Daftar Plafon Week']
            ]
        ]);
    }

    /**
     * Melakukan Request Action Insert.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     */
    public function store(Request $data) {
        return (new PlafonWeek)->insert($data)->response();
    }

    /**
     * Melakukan Request Action Update.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     */
    public function update(Request $data) {
        return (new PlafonWeek)->updateById($data)->response();
    }

    /**
     * Melakukan Request Action Delete.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     */
    public function destroy(Request $data) {
        return (new PlafonWeek)->deleteById($data)->response();
    }

     /**
     * Mendapatkan Semua Data untuk Option.
     * @return Illuminate\Http\JsonResponse Data Berformat Opsi.
     */
    function showOptionData() {
        return option((new PlafonWeek)->all(), ['nama']);
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
        $btnAction = 'partials.components.btn-actions';
        
        return DataTables::of((new PlafonWeek)->all())
            ->addColumn ( '',         fn()   => ""                                 )
            ->addColumn ( 'actions',  fn($i) => view($btnAction, ['id' => $i->id]) )
            ->editColumn( 'tanggal', fn($i) => stringDateFormater($i->tanggal)     )
            ->escapeColumns([])
            ->toJson();
    }
}