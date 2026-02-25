<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Session;

class Authenticate extends Controller
{
    public function index()
    {
        if (Auth::check()) {
            return modul(userFitur())
                ? redirect()->intended(route('dashboard.index'))
                : view('contents.login');
        } else {
            return view('contents.login');
        }
    }

    public function proses(Request $request)
    {
        $validation = $request->validate([
            'username' => 'required',
            'password' => 'required',
        ]);

        if (Auth::attempt($validation)) {
            Session::flash('status', 11);
            Log::info('Login berhasil');
            return redirect()->intended(route('dashboard.index'));
        } else {
            Session::flash('status', 0);
            Log::info('Login gagal');
            return back();
        }
    }

    public function logout()
    {
        Auth::logout();
        Session::invalidate();
        Session::regenerateToken();
        return redirect()->intended(route('login'));
    }
}
