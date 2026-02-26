<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\{
    Model as HTTPRequest,
    PurchaseOrder as PurchaseOrderModel,
    PurchaseOrderDetail,
    PurchaseOrderProsesLog
};
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;
use Yajra\Datatables\Datatables;

class PurchaseOrder extends Controller
{
    public function create()
    {
        /**
         * Menampilkan tampilan untuk membuat Purchase Order.
         *
         * @return Illuminate\View\View `Form Request Order`.
         */
        return view('contents.order-form-add', [
            'breadcrumb' => ['Order', 'Form Request'],
            'data' => (object) [
                'kode' => (new PurchaseOrderModel)->generateKode()
            ],
        ]);
    }

    public function edit(Request $data)
    {
        /**
         * Menampilkan tampilan untuk menyunting Purchase Order.
         *
         * @param  Illuminate\Http\Request|$data HTTP Form Data.
         * @return Illuminate\View\View `Form Edit Order`.
         */
        return view('contents.order-form-edit', [
            'breadcrumb' => ['Order', 'Form Edit'],
            'data' => (object) [
                'order' => (new PurchaseOrderModel)->getDataProsesRequestByIdOrder($data->id),
                'order_details' => (new PurchaseOrderDetail)->getListByIdOrder($data->id),
            ],
        ]);
    }

    public function index()
    {
        /**
         * Menampilkan tampilan untuk melakukan Konfirmasi Purchase Order.
         *
         * @return Illuminate\View\View `Daftar Order`.
         */
        return view('contents.order-list-konfirmasi', [
            'breadcrumb' => ['Order', 'Konfirmasi', 'Daftar Order']
        ]);
    }

    public function laporan()
    {
        /**
         * Menampilkan tampilan untuk melakukan Konfirmasi Purchase Order.
         *
         * @return Illuminate\View\View `Daftar Order`.
         */
        return view('contents.order-laporan', [
            'breadcrumb' => ['Order', 'Laporan']
        ]);
    }

    public function laporanDetail($id)
    {
        /**
         * Menampilkan tampilan detail laporan Purchase Order.
         *
         * @param int $id ID Purchase Order
         * @return Illuminate\View\View
         */
        return view('contents.order-laporan-detail', [
            'breadcrumb' => ['Order', 'Laporan', 'Detail'],
            'id' => $id
        ]);
    }

    public function store(Request $data)
    {
        /**
         * Proses `Insert` data Purchase Order ke Database
         * pada saat submisi `Form Request Order`.
         *
         * @param Illuminate\Http\Request|$data HTTP Form Data.
         */
        (new HTTPRequest)
            ->url('/api/extra/purchase-order/proses/request')
            ->insert($data->all())
            ->response;
        $payload = $data->except(['_token']);
        // dd([
        //     'Payload_Dikirim' => $payload  // Jika JSON gagal di-parse, cek di sini
        // ]);

        return redirect()->route('purchase-order.create')->with('status', 1);
    }

    public function updateData(Request $data)
    {
        /**
         * Proses `Update` data Purchase Order ke Database
         * pada saat submisi `Form Edit Order`.
         *
         * @param Illuminate\Http\Request|$data HTTP Form Data.
         */

        // 1. `Update` Data Purchase Order Berdasarkan Id.
        (new PurchaseOrderModel)->updateById($data, $data->idOrder);

        // 2. `Hapus` Detail dari Purchase Order berdasarkan Id Order.
        (new PurchaseOrderDetail)->deleteByIdOrder($data->idOrder);

        // 3. `Insert` Kembali Detail dari Purchase Order berdasarkan Jumlah Item Produk.
        (new PurchaseOrderDetail)->insertByCountedIdProduk($data);

        // 4. `Insert` Log Proses (Revisi Request) dari Purchase Order.
        (new PurchaseOrderProsesLog)->insert($data);

        return redirect()->route('konfirmasi-order.index')->with('status', 2);
    }

    public function updatePurchasing(Request $request)
{
    // Pastikan data dikirim sebagai JSON murni
    $response = (new HTTPRequest)
        ->url('/api/extra/purchase-order/proses/konfirmasi')
        ->insert($request->all()); // Pastikan helper post() menggunakan json_encode

    // Jika ingin lebih pasti, gunakan Http Client bawaan Laravel:
    /*
    $response = \Illuminate\Support\Facades\Http::withHeaders([
        'Content-Type' => 'application/json'
    ])->post(config('app.api_url').'/api/extra/purchase-order/proses/konfirmasi', $request->all());
    */

    return redirect()->back()->with('status', 2);
}

    public function updateClosed(Request $request)
    {
        $response = (new HttpRequest)
            ->url('/api/extra/purchase-order/proses/closed')
            ->insert([
                'order_id' => $request->input('order_id'),
            ]);

        return redirect()->route('penerimaan-barang.index')->with('status', 2);
    }

    function showData(Request $data)
    {
        /**
         * Menampilkan data Detail dari Purchase Order dalam bentuk JSON.
         *
         * @todo  Biasanya, digunakan untuk menampilkan detail data
         *        pada Modal atau Form Edit.
         * @param Illuminate\Http\Request|$data HTTP Form Data.
         */
        return response()->json((new PurchaseOrderDetail)->getListByIdOrder($data->id));
    }

    function showTableKonfirmasi()
    {
        ddd((new PurchaseOrderModel)->getListProsesKonfirmasi());

        /**
         * Menampilkan data tabel dari Purchase Order dengan proses Konfirmasi
         * dalam bentuk JSON.
         *
         * @todo  Digunakan untuk data pada Tabel.
         */

        // Blade Components
        $btn1 = 'partials.components.btn-details';

        return DataTables::of((new PurchaseOrderModel)->getListProsesKonfirmasi())
            ->addColumn('', fn() => '')
            ->addColumn('actions', fn($i) => view($btn1, ['id' => $i->id]))
            ->escapeColumns([])
            ->toJson();
    }
}
