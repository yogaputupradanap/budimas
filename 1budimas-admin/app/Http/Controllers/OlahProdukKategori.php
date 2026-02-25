<?php

namespace App\Http\Controllers;
use App\Http\Controllers\Controller;
use Yajra\Datatables\Datatables;
use Illuminate\Http\Request;
use App\Models\ProdukKategori;

class OlahProdukKategori extends Controller {
    /**
     * Menampilkan Master Page.
     * @param array|$nav Keterangan Breadcrumb Navigations.
     */
    public function index() {
        return view('contents.olah-produk-kategori', [
            'content' => (object) [
                'name'       => 'Produk Kategori',
                'breadcrumb' => ['Olah Produk', 'Daftar Produk', 'Daftar Produk Kategori']
            ]
        ]);
    }

    /**
     * Melakukan Request Action Insert.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     */
    public function store(Request $data) {
        return (new ProdukKategori)->insert($data)->response();
    }

    /**
     * Melakukan Request Action Update.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     */
    public function update(Request $data) {
        return (new ProdukKategori)->updateById($data)->response();
    }

    /**
     * Melakukan Request Action Delete.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     */
    public function destroy(Request $data) {
        return (new ProdukKategori)->deleteById($data)->response();
    }

     /**
     * Mendapatkan Semua Data untuk Option.
     * @return Illuminate\Http\JsonResponse Data Berformat Opsi.
     */
    function showOptionData() {
        return option((new ProdukKategori)->all(), ['nama']);
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
        $button1 = 'partials.components.btn-actions';
        
        return DataTables::of((new ProdukKategori)->all())
            ->addColumn('', fn() => "")
            ->addColumn('actions', fn($i) => view($button1, ['id' => $i->id]))
            ->escapeColumns([])
            ->toJson();
    }
}