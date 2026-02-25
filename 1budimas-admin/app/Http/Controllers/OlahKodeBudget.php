<?php

namespace App\Http\Controllers;
use App\Http\Controllers\Controller;
use Yajra\Datatables\Datatables;
use Illuminate\Http\Request;
use App\Models\Budget;

class OlahKodeBudget extends Controller {
    /**
     * Menampilkan Master Page.
     */
    public function index() {
        return view('contents.olah-kode-budget', [
            'content' => (object) [
                'name'       => 'Kode Budget',
                'breadcrumb' => ['Olah Data Budget', 'Daftar Kode Budget']
            ]
        ]);
    }

    /**
     * Melakukan Request Action Insert.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     */
    public function store(Request $data) {
        return (new Budget)->insert($data)->response();
    }

    /**
     * Melakukan Request Action Update.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     */
    public function update(Request $data) {
        return (new Budget)->updateById($data)->response();
    }

    /**
     * Melakukan Request Action Delete.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     */
    public function destroy(Request $data) {
        return (new Budget)->deleteById($data)->response();
    }

     /**
     * Mendapatkan Semua Data untuk Option.
     * @return Illuminate\Http\JsonResponse Data Berformat Opsi.
     */
    function showOptionData() {
        return option((new Budget)->all(), ['nama']);
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
        $txtMoney  = 'partials.components.txt-money';
        
        return DataTables::of((new Budget)->all())
            ->addColumn('',                 fn() => ""                                              )
            ->addColumn('actions',          fn($i) => view($btnAction, ['id' => $i->id])            )
            ->addColumn('e_nominal',        fn($i) => view($txtMoney, ['val' => $i->nominal])       )
            ->addColumn('e_limit_nominal',  fn($i) => view($txtMoney, ['val' => $i->limit_nominal]) )
            ->addColumn('periode',          fn($i) => bulan($i->bulan)." ".$i->tahun                )
            ->escapeColumns([])
            ->toJson();
    }
}