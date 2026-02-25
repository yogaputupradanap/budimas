<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\Customer;
use Illuminate\Http\Request;
use Yajra\Datatables\Datatables;

class OlahCustomer extends Controller
{
    /**
     * Menampilkan Master Page.
     */
    public function index()
    {
        return view('contents.olah-customer', [
            'content' => (object) [
                'name' => 'Customer',
                'breadcrumb' => ['Olah Data Customer', 'Daftar Customer']
            ]
        ]);
    }

    /**
     * Melakukan Request Action Insert.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     */
    public function store(Request $data)
    {
        return (new Customer)->insert($data)->response();
    }

    /**
     * Melakukan Request Action Update.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     */
    public function update(Request $data)
    {
        return (new Customer)->updateById($data)->response();
    }

    /**
     * Melakukan Request Action Delete.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     */
    public function destroy(Request $data)
    {
        return (new Customer)->deleteById($data)->response();
    }

    /**
     * Mendapatkan Semua Data untuk Option.
     * @return Illuminate\Http\JsonResponse Data Berformat Opsi.
     */
    function showOptionData()
    {
        return option((new Customer)->all(), ['kode', 'nama', 'nama_cabang']);
    }

    /**
     * Mendapatkan Semua Data untuk Tabel.
     *
     * @var e_ Edited Column.
     * @var mix|$i Response Items (Columns).
     * @return Yajra\Datatables\Datatables Data Berformat Tabel.
     */
    public function showTableData(Request $request)
    {
        $draw = $request->get('draw');
        $start = $request->get('start');
        $length = $request->get('length');
        $search = $request->get('search')['value'];
        $order = $request->get('order');
        $columns = $request->get('columns');

        $customer = new Customer();

        // Buat query string untuk filter dan sorting
        $queryParams = [
            'draw' => $draw,
            'start' => $start,
            'length' => $length,
            'search[value]' => $search,
        ];

        if (!empty($order)) {
            $columnIndex = $order[0]['column'];
            $columnName = $columns[$columnIndex]['data'];
            $queryParams['order[0][column]'] = $columnName;
            $queryParams['order[0][dir]'] = $order[0]['dir'];
        }

        // Gabungkan query params ke dalam string
        $queryString = http_build_query($queryParams);

        // Panggil API dengan query string
        $response = $customer->select1('/api/extra/getCustomer?' . $queryString);

        // Format ulang data untuk actions column
        $formattedData = array_map(function ($item) {
            $item->actions = view('partials.components.btn-actions', ['id' => $item->id])->render();
            return $item;
        }, $customer->get1());

        return response()->json([
            'draw' => $customer->getDraw(),
            'recordsTotal' => $customer->count1(),
            'recordsFiltered' => $customer->filteredCount(),
            'data' => $formattedData
        ]);
    }
}
