<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Support\Facades\Auth;

class CheckUserRole
{
    /**
     * Handle an incoming request.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \Closure  $next
     * @return mixed
     */
    public function handle($request, Closure $next, ...$roles)
    {
        $jabatan = Auth::check() ? Auth::user()->first()->id_jabatan : null;

        foreach($roles as $role) {
            if ( $jabatan == $role ) { 
                return $next($request); 
            } 
        }
        
        return redirect(route('login'));
    }
}

