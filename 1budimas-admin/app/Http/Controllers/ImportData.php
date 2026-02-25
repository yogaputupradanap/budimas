<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Services\ImportData as ImportDataService;
use Illuminate\Http\Request;

class ImportData extends Controller
{
    public $service;  // Service which Used to Pass and Receive the Data.
    public $view;  // Base View Location which Used to Redirecting.
    public $route;  // Base Route Name which Used to Redirecting.

    public function __construct()
    {
        $this->service = new ImportDataService;
        $this->view = 'contents.olah-data-import';
        $this->route = 'import-data.';
    }

    public function create()
    {
        return view($this->view, [
            'content' => (object) [
                'name' => 'Import Data',
                'breadcrumb' => ['Operasi Data', 'Import Data']
            ]
        ]);
    }

    public function store(Request $request)
    {
        try {
            $file = $request->file('file');
            $fileName = $file->getClientOriginalName();
            $insert = $this->service->setData($request)->insert();
            return response()->json(['success' => true], 200);
        } catch (\Exception $e) {
            return response()->json($e->getMessage(), 500);
        }
    }

    public function show(Request $request)
    {
        return response()->json($this->service->setData($request)->getNamaKolomList());
    }
}
