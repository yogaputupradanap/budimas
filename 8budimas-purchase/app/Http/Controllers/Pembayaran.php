<?php

namespace App\Http\Controllers;
use App\Http\Controllers\Controller;
use Yajra\Datatables\Datatables;
use Illuminate\Http\Request;
use App\Models\{
    PurchaseOrder,
    PurchaseOrderDetail,
    PurchaseTagihan,
    PurchaseTagihanPelunasan,
    Jurnal,
};

class Pembayaran extends Controller
{
    public $service;  // Service which Used to Pass and Receive the Data.
    public $view;     // Base View Location which Used to Redirecting.
    public $route;    // Base Route Name which Used to Redirecting.

    public function __construct() {
        // $this->service  = new PurchaseRequestService;
        $this->view     = 'contents.206-pembayaran.';
        $this->route    = 'purchase-request.';
    }
    
    public function index(){
        return view('contents.tagihan-list-pembayaran', [
            'content'  => (object) [
                'name'       => 'Request',
                'breadcrumb' => ['Purchase', 'Pelunasan', 'Daftar Purchase']
            ]
        ]);
    }

    /**
     * 
     */
    function showData(Request $data){
        return response()->json((new PurchaseTagihanPelunasan)->getDataTerakhirByIdOrder($data->id));
    }

    /**
     * 
     */
    function showTableData() {
        // Blade Components
        $btnDetail = 'partials.components.btn-details';
        $btnPrint  = 'partials.components.btn-print';
        
        return DataTables::of((new PurchaseOrder)->getListPembayaran())
            ->addColumn ( '',        fn()   => ""                                 )
            ->addColumn ( 'actions', fn($i) => view($btnDetail, ['id' => $i->id]) )
            ->addColumn ( 'print',   fn($i) => view($btnPrint,  ['id' => $i->id]) )
            ->escapeColumns([])
            ->toJson();
    }

    public function store(Request $data) {
        if (!empty($data->nominalPembayaran)) {
            // 1. Insert Purchase Tagihan Peluanasan.
            (new PurchaseTagihanPelunasan)->insert($data);

            // 2.   Insert Jurnal
            // 2.1. Insert Jurnal Kredit
            $data['idTransaksi']     = $data->noFaktur;
            $data['idTipeTransaksi'] = 1; // Pembelian
            $data['idAkun']          = 1; // Kas
            $data['nominalDebit']    = null;
            $data['nominalKredit']   = $data->nominalPembayaran;

            (new Jurnal)->insert($data);

            // 2.2. Insert Jurnal Debit
            $data['idAkun']          = 2; // Pembayaran Purchase
            $data['nominalDebit']    = $data->nominalPembayaran;
            $data['nominalKredit']   = null;

            (new Jurnal)->insert($data);
        }

        if ($data->nominalTotalSisa <= 0) {
            // 3. Updating Purchase Order Process Based on Id.
            (new PurchaseOrder)->updatePembayaranLunas($data->idOrder);  
        }

        return redirect()->route('pembayaran.index')->with('status', 1);
    }
}
