<?php

// | CONTROLLER BASE AND NAMESPACING.
namespace App\Http\Controllers;
use App\Http\Controllers\Controller;

// | HELPER.
use Illuminate\Http\Request;
use Illuminate\Support\Collection;

// | MODEL.
use App\Models\{
    PurchaseOrder          as PO, 
    PurchaseOrderDetail    as PO_DTL, 
    PurchaseOrderProsesLog as PO_P_LOG
};

class PurchaseOrderRequest extends Controller {
   
    public function index() {
        /** 
         * MENAMPILKAN VIEW [FORM REQUEST ORDER] (ADD ORDER).
         * 
         */
        return view('contents.request-list-konfirmasi', [
            'content'  => (object) [
                'name'       => 'Request',
                'breadcrumb' => ['Request', 'Konfirmasi Cabang', 'Daftar Request']
            ]
        ]);
    }

    /** 
     * Redirecting to The Edit Draft Purchase Page. 
     */
    public function edit(Request $data) {;
        return view('contents.request-form-edit', [
            'nProduk'         => (new PurchaseRequestDetail)->getListInProduk($data->id),
            'purchaseRequest' => (new PurchaseRequest)->find($data->id),
            'content'         => (object) [
                'name'        => 'Request',
                'breadcrumb'  => ['Request', 'Form Edit Request']
            ]
        ]);
    }

    public function store(Request $data) {
        (new PurchaseRequest)->updateDisetujui($data);
        return redirect()->route('konfirmasi-request.index')->with('status', 3);
    }

    /**
     * Issuing an Updating Action.
     * The Update is Process to Update The Latest Data of Purchase Request
     * which Include; Purchase Request, The Details and Log of The Process.
     * This is Triggered after Submitting `Edit Draft Purchase` Form.
     * 
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     */
    public function update(Request $data) {
        // 1. Updating Purchase Request Data Based on Id
        (new PurchaseRequest)->updateById($data, $data->idRequest);

        // 2. Deleting Previous Purchase Request Detail Data By Received Id Request.
        (new PurchaseRequestDetail)->deleteByIdRequest($data->idRequest);

        // 3. Re-Inserting Latest Purchase Request Detail Data Based on Counted Product Id.
        (new PurchaseRequestDetail)->insertByCountedIdProduk($data);

        return redirect()->route('konfirmasi-request.index')->with('status', 2);
    }

    /** 
     * 
     */
    public function destroy(Request $data) {
        (new PurchaseRequest)->updateClosed($data);
        return redirect()->route('konfirmasi-request.index')->with('status', 3);
    }

    /**
     * 
     */
    function showData(Request $request){
        return response()->json((new PurchaseRequestDetail)->getListByIdRequest($request->id));
    }

    function showTableData() {
        // Blade Components
        $btn1 = 'partials.components.btn-details';

        return DataTables::of((new PurchaseRequest)->getListKonfirmasi())
            ->addColumn ( '',        fn()   => ""                            )
            ->addColumn ( 'actions', fn($i) => view($btn1, ['id' => $i->id]) )
            ->escapeColumns([])
            ->toJson();
    }
}
