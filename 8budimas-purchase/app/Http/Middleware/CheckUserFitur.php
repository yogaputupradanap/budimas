<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Support\Facades\Auth;

class CheckUserFitur
{
    /**
     * Handle an incoming request.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \Closure  $next
     * @return mixed
     */
    public function handle($request, Closure $next, $fitur)
    {
        if (Auth::check()) {
            $userFitur = userFitur();

            if (fitur($userFitur, $fitur)) {
                view()->share('x', userFitur());
                return $next($request);
            }
            
        }

        return redirect(route('login'));
    }
}

