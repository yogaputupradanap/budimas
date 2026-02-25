<?php

namespace App\Http\Controllers;
use App\Http\Controllers\Controller;
use Yajra\Datatables\Datatables;
use Illuminate\Http\Request;
use App\Models\UserAkses;
use App\Models\Fitur;

class OlahFiturUser extends Controller {
    /**
     * Melakukan Request Action Insert.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     */
    public function store(Request $data) {
        return (new UserAkses)->insert($data)->response();
    }

    /**
     * Melakukan Request Action Update.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     */
    public function update(Request $data) {
        return (new UserAkses)->updateById($data)->response();
    }

    /**
     * Melakukan Request Action Delete.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     */
    public function destroy(Request $data) {
        return (new UserAkses)->deleteById($data)->response();
    }

    /**
     * Mendapatkan Semua Data untuk Option.
     * @return Illuminate\Http\JsonResponse Data Berformat Opsi.
     */
    function showOptionData() {
        return option((new UserAkses)->all(), ['nama']);
    }

    /**
     * Mendapatkan Semua Data untuk Option.
     * @return Illuminate\Http\JsonResponse Data Berformat Opsi.
     */
    function showOptionData2(Request $data) {
        return option((new Fitur)->getFiturUserTersedia($data->id), ['nama']);
    }

    /**
     * Mendapatkan Semua Data untuk Tabel.
     * 
     * @var e_ Edited Column.
     * @var mix|$i Response Items (Columns).
     * @return Yajra\Datatables\Datatables Data Berformat Tabel.
     */
    function showTableData(Request $data) {
        // Blade Components
        $btnDelete = 'partials.components.btn-delete';
        
        return DataTables::of((new UserAkses)->getListByIdUser($data->idUser))
            ->addColumn ( '',        fn()   => ""                                 )
            ->addColumn ( 'actions', fn($i) => view($btnDelete, ['id' => $i->id]) )
            ->escapeColumns([])
            ->toJson();
    }
}