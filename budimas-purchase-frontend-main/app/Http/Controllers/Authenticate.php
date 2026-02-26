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
        $credentials = $request->validate([
            'username' => 'required',
            'password' => 'required',
        ]);

        $userModel = new User();
        
        // Memanggil API Python: /getUserToken & /api/base/users
        $user = $userModel->fetchUserByCredentials($credentials);

        if ($user) {
            // Login manual ke session Laravel
            Auth::login($user); 
            
            Session::flash('status', 11);
            return redirect()->intended(route('dashboard.index'));
        } else {
            Session::flash('status', 0);
            return back()->withErrors(['login' => 'Kredensial API tidak valid.']);
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
