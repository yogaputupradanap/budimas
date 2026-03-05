<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;

class Dashboard extends Controller {

    public function index() {
        /**
         * Menampilkan tampilan untuk Dashboard.
         * 
         * @return Illuminate\View\View `Daftar Fitur`.
         */

        return view('contents.dashboard', [
            'breadcrumb' => ['Dashboard', 'Fitur']
        ]);
    }
    
}
