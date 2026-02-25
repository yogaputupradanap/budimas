<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Yajra\Datatables\Datatables;
use Illuminate\Http\Request;
use App\Models\Driver;
use App\Models\JabatanAkses;
use App\Models\User;
use App\Models\UserAkses;

class OlahDriver extends Controller
{
    /**
     * Menampilkan Master Page.
     */
    public function index()
    {
        return view('contents.olah-driver', [
            'content' => (object) [
                'name'       => 'Driver',
                'breadcrumb' => ['Olah Data Driver', 'Daftar Driver']
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


            // Get the inserted user ID (sama persis seperti di Sales - TANPA LOG)
            $idUser = (new User)->returning('id')->insert($data);

            // Add idUser to the data object
            $data->merge(['idUser' => $idUser]);

            // Now insert driver with both data and idUser
            $driver = (new Driver)->insert($data);

            return response()->json(['success' => true], 200);
        } catch (\Exception $e) {
            return response()->json(['error' => $e->getMessage()], 500);
        }
    }

    public function update(Request $data)
    {
        try {
            // Update data user terlebih dahulu
            $result_data = (new User)->updateById($data);

            // $data->merge(['id' => $data->id_driver]);

            $data = (new Driver)->updateById($data);

            return response()->json(['success' => true, 'result' => $result_data], 200);
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
        return (new Driver)->deleteById($data)->response();
    }

    /**
     * Mendapatkan Semua Data untuk Option.
     * @return Illuminate\Http\JsonResponse Data Berformat Opsi.
     */
    function showOptionData()
    {
        return option((new Driver)->all(), ['nama']);
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

        return DataTables::of((new Driver)->all())
            ->addColumn('',         fn()   => "")
            ->addColumn('actions',  fn($i) => view($button1, ['id' => $i->id]))
            ->addColumn('e_area',   fn($i) => $i->nama_wilayah1 . " - " . $i->nama_wilayah2)
            ->escapeColumns([])
            ->toJson();
    }
}
