<?php

namespace App\Http\Controllers;
use App\Http\Controllers\Controller;
use Yajra\Datatables\Datatables;
use Illuminate\Http\Request;
use App\Models\ProdukTipeHarga;

class OlahProdukTipeHarga extends Controller {
    /**
     * Menampilkan Master Page.
     * @param array|$nav Keterangan Breadcrumb Navigations.
     */
    public function index() {
        return view('contents.olah-produk-tipe-harga', [
            'content' => (object) [
                'name'       => 'Produk Tipe Harga',
                'breadcrumb' => ['Olah Data Produk', 'Daftar Produk', 'Daftar Produk Tipe Harga']
            ]
        ]);
    }

    /**
     * Melakukan Request Action Insert.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     */
    public function store(Request $data) {
        return (new ProdukTipeHarga)->insert($data)->response();
    }

    /**
     * Melakukan Request Action Update.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     */
    public function update(Request $data) {
        return (new ProdukTipeHarga)->updateById($data)->response();
    }

    /**
     * Melakukan Request Action Delete.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     */
    public function destroy(Request $data) {
        return (new ProdukTipeHarga)->deleteById($data)->response();
    }
    
    /**
     * Mendapatkan Semua Data untuk Option.
     * @return Illuminate\Http\JsonResponse Data Berformat Opsi.
     */
    function showOptionData() {
        return option((new ProdukTipeHarga)->all(), ['kode', 'nama']);
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

        return DataTables::of((new ProdukTipeHarga)->all())
            ->addColumn('', fn() => "")
            ->addColumn('actions', fn($i) => view($btnAction, ['id' => $i->id]))
            ->escapeColumns([])
            ->toJson();
    }
}