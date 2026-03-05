<?php

namespace App\Providers;

use Illuminate\Support\Facades\URL;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     *
     * @return void
     */
    public function register()
    {
        //
    }

    /**
     * Bootstrap any application services.
     *
     * @return void
     */
    public function boot()
    {
        // sulution => this form is not secure. auto fill has been turn off
        // Server wajib production
        if (env('APP_ENV') !== 'local') {
            URL::forceScheme('https');
        }
    }
}
