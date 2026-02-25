<?php

namespace App\Http\Controllers;

use App\Services\ExportData as ExportDataService;
use App\Http\Controllers\Controller;
use Illuminate\Http\Request;

class ExportData extends Controller
{
    public $service;
    public $view;
    public $route;

    public function __construct()
    {
        $this->service  = new ExportDataService;
        $this->view     = 'contents.olah-data-export';
        $this->route    = 'export-data.';
    }

    public function create()
    {
        return view($this->view, [
            'content' => (object) [
                'name'       => 'Export Data',
                'breadcrumb' => ['Operasi Data', 'Export Data']
            ]
        ]);
    }

    public function show(Request $request)
    {
        try {
            return response()->json($this->service->setData($request)->getAll());
        } catch (\Exception $e) {
            return response()->json([
                'status'  => 'error',
            ], 500);
        }
    }
}
