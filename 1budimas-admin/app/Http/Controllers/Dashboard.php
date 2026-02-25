<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;

class Dashboard extends Controller
{
    /**
     * Menampilkan Master Page.
     * @param array|$nav Keterangan Breadcrumb Navigations.
     */
    public function index() {
        return view('contents.dashboard', [
            'content' => (object) [
                'breadcrumb' => ['Dashboard', 'Fitur']
            ]
        ]);
    }
}
