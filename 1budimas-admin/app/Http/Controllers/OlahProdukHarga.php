<?php

namespace App\Http\Controllers;
use App\Http\Controllers\Controller;
use Yajra\Datatables\Datatables;
use Illuminate\Http\Request;
use App\Models\ProdukHarga;

class OlahProdukHarga extends Controller {
    /**
     * Melakukan Request Action Insert.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     */
    public function store(Request $data) {
        return (new ProdukHarga)->insert($data)->response();
    }

    /**
     * Melakukan Request Action Update.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     */
    public function update(Request $data) {
        return (new ProdukHarga)->updateById($data)->response();
    }

    /**
     * Melakukan Request Action Delete.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     */
    public function destroy(Request $data) {
        return (new ProdukHarga)->deleteById($data)->response();
    }
    
    /**
     * Mendapatkan Semua Data untuk Option.
     * @return Illuminate\Http\JsonResponse Data Berformat Opsi.
     */
    function showOptionData() {
        return option((new ProdukHarga)->all(), ['nama']);
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
        $txtMoney  = 'partials.components.txt-money';
        
        return DataTables::of((new ProdukHarga)->getListByIdProduk($data->idProduk))
            ->addColumn('', fn() => "")
            ->addColumn('actions', fn($i) => view($btnAction, ['id' => $i->id])  )
            ->addColumn('e_harga', fn($i) => view($txtMoney,  ['val' => $i->harga]) )
            ->escapeColumns([])
            ->toJson();
    }
}