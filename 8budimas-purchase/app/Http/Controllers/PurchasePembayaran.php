<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Yajra\Datatables\Datatables;

use App\Models\{
    PurchaseOrder as PurchaseOrderModel,
    PurchaseOrderDetail
};

class PurchasePembayaran extends Controller {

    public function index() {
        return view('contents.transaksi-pembayaran-add', [
            'breadcrumb' => ['Pembayaran Purchase', 'Form Pembayaran']
        ]);
    }

    public function create(Request $data) {
        /**
         * Menampilkan tampilan untuk membuat Purchase Order.
         * 
         * @return Illuminate\View\View `Form Request Order`.
         */

        return view('contents.transaksi-pembayaran-list', [
            'breadcrumb' => ['Pembayaran Purchase', 'Daftar Tagihan'],
        ]);
    }

    public function store(Request $data) {
        /**
         * Menampilkan tampilan untuk membuat Purchase Order.
         * 
         * @return Illuminate\View\View `Form Request Order`.
         */

         return redirect()->route('penerimaan-barang.index')->with('status', 2);
    }

    function showTable() {
        /** 
         * Menampilkan data tabel dari Purchase Order dengan proses Konfirmasi
         * dalam bentuk JSON.
         * 
         * @todo  Digunakan untuk data pada Tabel.
         */

        // Blade Components
        $btn1 = 'partials.components.btn-form';
        
        return DataTables::of((new PurchaseOrderModel)->getListProsesPurchasing())
            ->addColumn ( '',        fn()   => ""                            )
            ->addColumn ( 'actions', fn($i) => view($btn1, ['id' => $i->id]) )
            ->escapeColumns([])
            ->toJson();
    }

    // public function store(Request $data) {
    //     // 1. Updating Purchase Request Detail Recieved Quantity Data Based on Id.
    //     (new PurchaseRequestDetail)->updateJumlahDiterimaByCountedId($data);

    //     // 2. Inserting Purchase Penerimaan Barang Based on Counted Id Request Detail.
    //     (new PurchasePenerimaanBarang)->insertByCountedIdRequestDetail($data);

    //     // 3. Updating Purchase Request Process Based on Id.
    //     (new PurchaseOrder)->updateKonfirmasiTagihan($data->idOrder);
        
    //     for($i=0; $i<count($data->idProduk); $i++) { 
    //         // 4. Cheking Product Stock.
    //         $stok = (new Stok)->getDataByIdProdukCabang($data->idProduk[$i], $data->idCabang);

    //         if(empty($stok)) {
    //             // 4.1. If Product Has No Record, 
    //             //      Inserting The New Data of Product Stock.
    //             $data['stokReady']     = $data->jumlahDatang[$i];
    //             $data['stokAwal']      = 0;
    //             $data['stokPeralihan'] = $data->jumlahDatang[$i];
    //             $data['stokAkhir']     = $data->jumlahDatang[$i];

    //             (new Stok)->insertByProdukIndex($data, $i);

    //         } else {
    //             // 4.2. If Product Has Record, Getting The Id and 
    //             //      Updating the Ready Stock Data.
    //             $data['stokReady']     = $stok->stok_ready + $data->jumlahDatang[$i];
    //             $data['stokAwal']      = $stok->stok_ready;
    //             $data['stokPeralihan'] = $data->jumlahDatang[$i];
    //             $data['stokAkhir']     = $data->stokReady;
                
    //             (new Stok)->updateStokReadyById($stok->id, $data);
    //         }

    //         // 5. Inserting Inventory Based on Counted Id Request Detail.
    //         $data['idProdukUom']     = (new ProdukSatuan)->getDataByIdProduk($data->idProduk[$i])->id ?? '';
    //         $data['valuasi']         = $data->hargaBeliProduk[$i] * $data->jumlahDatang[$i];
    //         $data['idTransaksi']     = $data->noFaktur;
    //         $data['idTipeTransaksi'] = 1; // Purchasing
    //         $data['idTipeStok']      = 1; // Stok Ready

    //         (new Inventori)->insertByProdukIndex($data, $i);
    //     }
        
    //     return redirect()->route('konfirmasi-order.index')->with('status', 2);
    // }
}
