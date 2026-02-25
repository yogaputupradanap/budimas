<?php

namespace App\Http\Controllers;
use App\Http\Controllers\Controller;
use Yajra\Datatables\Datatables;
use Illuminate\Http\Request;
use App\Models\PlafonJadwal;

class OlahPlafonJadwal extends Controller {
    /**
     * Melakukan Request Action Insert.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     */
    public function store(Request $data) {
        return (new PlafonJadwal)->insert($data)->response();
    }

    /**
     * Melakukan Request Action Update.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     */
    public function update(Request $data) {
        return (new PlafonJadwal)->updateById($data)->response();
    }

    /**
     * Melakukan Request Action Delete.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     */
    public function destroy(Request $data) {
        return (new PlafonJadwal)->deleteById($data)->response();
    }

     /**
     * Mendapatkan Semua Data untuk Option.
     * @return Illuminate\Http\JsonResponse Data Berformat Opsi.
     */
    function showOptionData() {
        return option((new PlafonJadwal)->all(), ['nama']);
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
        $btnAction = 'partials.components.btn-actions';
        $btnStatus = 'partials.components.btn-status';
        
        return DataTables::of((new PlafonJadwal)->getListByIdPlafon($data->idPlafon))
            ->addColumn( '',                 fn()   => ""                                        )
            ->addColumn( 'actions',          fn($i) => view($btnAction, ['id' => $i->id])        )
            ->addColumn( 'e_hari',           fn($i) => hari($i->id_hari)                         )
            ->addColumn( 'e_minggu',         fn($i) => minggu($i->id_minggu)                     )
            ->addColumn( 'e_tipe_kunjungan', fn($i) => tipe_kunjungan($i->id_tipe_kunjungan)     )
            ->addColumn( 'e_status',         fn($i) => view($btnStatus, ['id' => $i->id_status]) )
            ->escapeColumns([])
            ->toJson();
    }
}