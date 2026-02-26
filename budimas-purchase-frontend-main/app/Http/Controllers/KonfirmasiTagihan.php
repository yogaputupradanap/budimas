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
};

class KonfirmasiTagihan extends Controller
{
    public $service;  // Service which Used to Pass and Receive the Data.
    public $view;     // Base View Location which Used to Redirecting.
    public $route;    // Base Route Name which Used to Redirecting.

    public function __construct() {
        // $this->service  = new PurchaseRequestService;
        $this->view     = 'contents.205-konfirmasi-tagihan.';
        $this->route    = 'purchase-request.';
    }

    public function index() {
        return view('contents.tagihan-list-konfirmasi', [
            'content'  => (object) [
                'name'       => 'Request',
                'breadcrumb' => ['Order', 'Konfirmasi Tagihan', 'List Order']
            ]
        ]);
    }

    /**
     * 
     */
    function showData(Request $request){
        return response()->json((new PurchaseOrderDetail)->getListByIdRequest($request->id));
    }

    /**
     * 
     */
    function showTableData() {
        // Blade Components
        $btnDetail = 'partials.components.btn-details';
        $btnPrint  = 'partials.components.btn-print';
        
        return DataTables::of((new PurchaseOrder)->getListTagihan())
            ->addColumn ( '',        fn()   => ""                                 )
            ->addColumn ( 'actions', fn($i) => view($btnDetail, ['id' => $i->id]) )
            ->addColumn ( 'print',   fn($i) => view($btnPrint,  ['id' => $i->id]) )
            ->escapeColumns([])
            ->toJson();
    }

    public function store(Request $data) {
        // 1. Updating Purchase Order Process Based on Id.
        (new PurchaseOrder)->updatePembayaranTagihan($data->idOrder);
        
        // 2. Insert Purchase Tagihan and Pushing The Id Into HTTP Form Data Object ($data)
        $data['idTagihan'] = (new PurchaseTagihan)->insertReturningId($data);

        // 3. Insert Purchase Tagihan Peluanasan.
        $data['nominalTotalSisa'] = $data->totalSisa;
        (new PurchaseTagihanPelunasan)->insert($data);

        return redirect()->route('konfirmasi-tagihan.index')->with('status', 2);
    }
}
