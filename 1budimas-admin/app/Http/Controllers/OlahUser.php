<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\JabatanAkses;
use App\Models\User;
use App\Models\UserAkses;
use Illuminate\Http\Request;
use Yajra\Datatables\Datatables;

class OlahUser extends Controller
{
    /**
     * Menampilkan Master Page.
     */
    public function index()
    {
        return view('contents.olah-user', [
            'content' => (object) [
                'name' => 'User',
                'breadcrumb' => ['Olah Data User', 'Daftar User']
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
            // Menambah user baru dan mengembalikan id user yang baru ditambahkan
            $idUser = (new User)->returning('id')->insert($data);

            // Mengambil fitur-fitur berdasarkan jabatan yang dipilih
            $nFitur = (new JabatanAkses)->getListByIdJabatan($data->idJabatan);

            // Instance dari UserAkses
            $userAkses = (new UserAkses);

            // Jika user dan fitur tersedia, tambahkan akses fitur untuk user
            if (!empty($idUser) && !empty($nFitur)) {
                foreach ($nFitur as $fitur) {
                    // Pastikan idFitur ada sebelum memasukkan ke tabel users_akses
                    if (property_exists($fitur, 'id_fitur')) {
                        $userAkses->insertBulk([$idUser, $fitur->id_fitur]);
                    }
                }
            }

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
        $update = (new User)->updateById($data);
        $nFitur = (new JabatanAkses)->getListByIdJabatan($data->idJabatan);
        $userAkses = (new UserAkses);

        if (!empty($data->idJabatanEx) && ($data->idJabatanEx != $data->idJabatan)) {
            $userAkses->deleteByIdUser($data->id);
            foreach ($nFitur as $fitur) {
                $userAkses->insertBulk([$data->id, $fitur->id_fitur]);
            }
        }

        return $update->response();
    }

    /**
     * Melakukan Request Action Delete.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     */
    public function destroy(Request $data)
    {
        (new UserAkses)->deleteByIdUser($data->id);
        return (new User)->deleteById($data)->response();
    }

    /**
     * Mendapatkan Semua Data untuk Option.
     * @return Illuminate\Http\JsonResponse Data Berformat Opsi.
     */
    function showOptionData1()
    {
        return option((new User)->all(), ['nik', 'nama', 'nama_cabang']);
    }

    /**
     * Mendapatkan List dengan Jabatan Sales untuk Option.
     * @return Illuminate\Http\JsonResponse Data Berformat Opsi.
     */
    function showOptionData2()
    {
        return option((new User)->getListByJabatanSales(), ['nik', 'nama', 'nama_cabang']);
    }

    /**
     * Mendapatkan List dengan Jabatan Driver untuk Option.
     * @return Illuminate\Http\JsonResponse Data Berformat Opsi.
     */
    function showOptionData3()
    {
        return option((new User)->getListByJabatanDriver(), ['nik', 'nama', 'nama_cabang']);
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
        $btnDetail = 'partials.components.btn-details';

        return DataTables::of((new User)->all())
            ->addColumn('', fn() => '')
            ->addColumn('actions', fn($i) => view($btnAction, ['id' => $i->id]))
            ->addColumn('details', fn($i) => view($btnDetail, ['id' => $i->id]))
            ->escapeColumns([])
            ->toJson();
    }
}
