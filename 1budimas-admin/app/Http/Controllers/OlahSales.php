<?php

namespace App\Http\Controllers;

use App\Models\JabatanAkses;
use App\Models\Sales;
use App\Models\User;
use App\Models\UserAkses;
use Illuminate\Http\Request;
use Yajra\Datatables\Datatables;

class OlahSales extends Controller
{
    /**
     * Menampilkan Master Page.
     */
    public function index()
    {
        return view('contents.olah-sales', [
            'content' => (object)[
                'name' => 'Sales',
                'breadcrumb' => ['Olah Data Sales', 'Daftar Sales']
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
            // Get the inserted user ID
            $idUser = (new User)->returning('id')->insert($data);

            // Add idUser to the data object
            $data->merge(['idUser' => $idUser]);

            // Process user access features
            $nFitur = (new JabatanAkses)->getListByIdJabatan($data->idJabatan);
            $userAkses = (new UserAkses);

            if (!empty($idUser) && !empty($nFitur)) {
                foreach ($nFitur as $fitur) {
                    if (property_exists($fitur, 'id_fitur')) {
                        $userAkses->insertBulk([$idUser, $fitur->id_fitur]);
                    }
                }
            }

            // Now insert sales with both data and idUser
            $sales = (new Sales)->insert($data);

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
            // Update data user terlebih dahulu
            $user = (new User)->updateById($data);

            // Setelah user diupdate, update data sales
            $sales = (new Sales)->updateById($data);

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
        return (new Sales)->deleteById($data)->response();
    }

    /**
     * Mendapatkan Semua Data untuk Option.
     * @return Illuminate\Http\JsonResponse Data Berformat Opsi.
     */
    function showOptionData()
    {
        return option((new Sales)->all(), ['kode_sales', 'nama', 'nama_cabang']);
    }

    /**
     * Mendapatkan Semua Data multiple sales.
     * @return Illuminate\Http\JsonResponse Data Berformat Opsi.
     */
    function showDataMultiplePrincipal()
    {
        return (new Sales)->all_on_multiple_principal();
    }


    /**
     * Mendapatkan Semua Data untuk Tabel.
     *
     * @return Yajra\Datatables\Datatables Data Berformat Tabel.
     * @var mix|$i Response Items (Columns).
     * @var e_ Edited Column.
     */
    function showTableData()
    {
        // Blade Components
        $btnAction = 'partials.components.btn-actions';

        return DataTables::of((new Sales)->all())
            ->addColumn('', fn() => '')
            ->addColumn('actions', fn($i) => view($btnAction, ['id' => $i->id]))
            ->addColumn('e_area', fn($i) => $i->nama_wilayah1 . ' - ' . $i->nama_wilayah2)
            ->escapeColumns([])
            ->toJson();
    }
}
