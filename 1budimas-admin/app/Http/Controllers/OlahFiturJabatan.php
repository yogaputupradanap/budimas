<?php

namespace App\Http\Controllers;
use App\Http\Controllers\Controller;
use Yajra\Datatables\Datatables;
use Illuminate\Http\Request;
use App\Models\JabatanAkses;
use App\Models\Jabatan;
use App\Models\Fitur;

class OlahFiturJabatan extends Controller {
    /**
     * Menampilkan Master Page.
     */
    public function index() {
        return view('contents.olah-fitur-jabtan', [
            'content' => (object) [
                'name'       => 'Fitur Jabatan',
                'breadcrumb' => ['Olah Fitur', 'Daftar Fitur Default (Jabatan)']
            ]
        ]);
    }

    /**
     * Melakukan Request Action Insert.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     */
    public function store(Request $data) {
        \Log::info('Data Masuk:', $data->all()); // Cek file storage/logs/laravel.log
        return (new JabatanAkses)->insert($data)->response();
    }

    /**
     * Melakukan Request Action Update.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     */
    public function update(Request $data) {
        return (new JabatanAkses)->updateById($data)->response();
    }

    /**
     * Melakukan Request Action Delete.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     */
    public function destroy(Request $data) {
        return (new JabatanAkses)->deleteById($data)->response();
    }

     /**
     * Mendapatkan Semua Data untuk Option.
     * @return Illuminate\Http\JsonResponse Data Berformat Opsi.
     */
    function showOptionData() {
        return option((new JabatanAkses)->all(), ['nama']);
    }

    /**
     * Mendapatkan Semua Data untuk Option.
     * @return Illuminate\Http\JsonResponse Data Berformat Opsi.
     */
    function showOptionData2(Request $data) {
        return option((new Fitur)->getFiturJabatanTersedia($data->id), ['nama']);
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
        $btnDetail = 'partials.components.btn-details';
        
        return DataTables::of((new Jabatan)->all())
            ->addColumn ( '',        fn()   => ""                                 )
            ->addColumn ( 'details', fn($i) => view($btnDetail, ['id' => $i->id]) )
            ->escapeColumns([])
            ->toJson();
    }

    /**
     * Mendapatkan Semua Data untuk Tabel.
     * 
     * @var e_ Edited Column.
     * @var mix|$i Response Items (Columns).
     * @return Yajra\Datatables\Datatables Data Berformat Tabel.
     */
    function showTableData2(Request $data) {
        // Blade Components
        $btnDelete = 'partials.components.btn-delete';

        return DataTables::of((new JabatanAkses)->getListByIdJabatan($data->idJabatan))
            ->addColumn ( '',        fn()   => ""                                 )
            ->addColumn ( 'actions', fn($i) => view($btnDelete, ['id' => $i->id]) )
            ->escapeColumns([])
            ->toJson();
    }
}