<?php

use App\Http\Controllers\Authenticate;
use App\Http\Controllers\OpsiWilayah;
use App\Http\Controllers\TestController;
use Illuminate\Support\Facades\Route;

/*
 * |--------------------------------------------------------------------------
 * | Import Controller Class
 * |--------------------------------------------------------------------------
 * |
 */

/*
 * |--------------------------------------------------------------------------
 * | Web Routes
 * |--------------------------------------------------------------------------
 * |
 * | Here is where you can register web routes for your application. These
 * | routes are loaded by the RouteServiceProvider within a group which
 * | contains the "web" middleware group. Now create something great!
 * |
 */

// Test
Route::get('/test', [TestController::class, 'test'])->name('test');
// Authentication
Route::get('/logout', [Authenticate::class, 'logout'])->name('logout');
Route::get('/', [Authenticate::class, 'index'])->name('login');
Route::post('/', [Authenticate::class, 'proses'])->name('login.proses');

// Default
Route::group(['middleware' => 'modul'], function () {
    // Dashboard
    Route::get('dashboard', 'Dashboard@index')->name('dashboard.index');

    // Edit Profile
    Route::get('profile', 'Profile@index');
    Route::post('profile/update', 'Profile@update');
});

// Olah Armada
Route::group(['middleware' => 'fitur:111'], function () {
    Route::get('olah-armada', 'OlahArmada@index');
    // Armada
    Route::post('olah-armada/insert', 'OlahArmada@store');
    Route::post('olah-armada/update', 'OlahArmada@update');
    Route::post('olah-armada/delete', 'OlahArmada@destroy');
    Route::post('olah-armada/data/table', 'OlahArmada@showTableData');
    // Tipe
    Route::get('olah-armada/tipe', 'OlahArmadaTipe@index');
    Route::post('olah-armada/tipe/insert', 'OlahArmadaTipe@store');
    Route::post('olah-armada/tipe/update', 'OlahArmadaTipe@update');
    Route::post('olah-armada/tipe/delete', 'OlahArmadaTipe@destroy');
    Route::post('olah-armada/tipe/data/table', 'OlahArmadaTipe@showTableData');
});
// Olah Cabang
Route::group(['middleware' => 'fitur:102'], function () {
    Route::get('olah-cabang', 'OlahCabang@index');
    Route::post('olah-cabang/insert', 'OlahCabang@store');
    Route::post('olah-cabang/update', 'OlahCabang@update');
    Route::post('olah-cabang/delete', 'OlahCabang@destroy');
    Route::post('olah-cabang/data/table', 'OlahCabang@showTableData');
});
// Olah Customer
Route::group(['middleware' => 'fitur:106'], function () {
    // Customer
    Route::get('olah-customer', 'OlahCustomer@index');
    Route::post('olah-customer/insert', 'OlahCustomer@store');
    Route::post('olah-customer/update', 'OlahCustomer@update');
    Route::post('olah-customer/delete', 'OlahCustomer@destroy');
    Route::post('olah-customer/data/table', 'OlahCustomer@showTableData');
    // Tipe
    Route::get('olah-customer/tipe', 'OlahCustomerTipe@index');
    Route::post('olah-customer/tipe/insert', 'OlahCustomerTipe@store');
    Route::post('olah-customer/tipe/update', 'OlahCustomerTipe@update');
    Route::post('olah-customer/tipe/delete', 'OlahCustomerTipe@destroy');
    Route::post('olah-customer/tipe/data/table', 'OlahCustomerTipe@showTableData');
});
// Olah Data
Route::group(['middleware' => 'fitur:114'], function () {
    // Import Data
    Route::get('olah-data/import', 'ImportData@create')->name('import-data.create');
    Route::post('olah-data/import', 'ImportData@store')->name('import-data.store');
    Route::post('olah-data/import/show', 'ImportData@show')->name('import-data.show');
    // Export Data
    Route::get('olah-data/export', 'ExportData@create');
    Route::post('olah-data/export', 'ExportData@show');
});
// Olah Driver
Route::group(['middleware' => 'fitur:110'], function () {
    Route::get('olah-driver', 'OlahDriver@index');
    Route::post('olah-driver/insert', 'OlahDriver@store');
    Route::post('olah-driver/update', 'OlahDriver@update');
    Route::post('olah-driver/delete', 'OlahDriver@destroy');
    Route::post('olah-driver/data/table', 'OlahDriver@showTableData');
});
// Olah Fitur
Route::group(['middleware' => 'fitur:113'], function () {
    // Jabatan
    Route::get('olah-fitur/jabatan', 'OlahFiturJabatan@index');
    Route::post('olah-fitur/jabatan/insert', 'OlahFiturJabatan@store');
    Route::post('olah-fitur/jabatan/update', 'OlahFiturJabatan@update');
    Route::post('olah-fitur/jabatan/delete', 'OlahFiturJabatan@destroy');
    Route::post('olah-fitur/jabatan/data/table', 'OlahFiturJabatan@showTableData');
    Route::post('olah-fitur/jabatan/data/table2', 'OlahFiturJabatan@showTableData2');

    // User
    Route::post('olah-fitur/user/insert', 'OlahFiturUser@store');
    Route::post('olah-fitur/user/update', 'OlahFiturUser@update');
    Route::post('olah-fitur/user/delete', 'OlahFiturUser@destroy');
    Route::post('olah-fitur/user/data/table', 'OlahFiturUser@showTableData');
});
// Olah Kode Budget
Route::group(['middleware' => 'fitur:109'], function () {
    Route::get('olah-kode-budget', 'OlahKodeBudget@index');
    Route::post('olah-kode-budget/insert', 'OlahKodeBudget@store');
    Route::post('olah-kode-budget/update', 'OlahKodeBudget@update');
    Route::post('olah-kode-budget/delete', 'OlahKodeBudget@destroy');
    Route::post('olah-kode-budget/data/table', 'OlahKodeBudget@showTableData');
});
// Olah Perusahaan
Route::group(['middleware' => 'fitur:103'], function () {
    Route::get('olah-perusahaan', 'OlahPerusahaan@index');
    Route::post('olah-perusahaan/insert', 'OlahPerusahaan@store');
    Route::post('olah-perusahaan/update', 'OlahPerusahaan@update');
    Route::post('olah-perusahaan/delete', 'OlahPerusahaan@destroy');
    Route::post('olah-perusahaan/data/table', 'OlahPerusahaan@showTableData');
});
// Olah Plafon
Route::group(['middleware' => 'fitur:107'], function () {
    // Plafon
    Route::get('olah-plafon', 'OlahPlafon@index');
    Route::post('olah-plafon/insert', 'OlahPlafon@store');
    Route::post('olah-plafon/update', 'OlahPlafon@update');
    Route::post('olah-plafon/delete', 'OlahPlafon@destroy');
    Route::post('olah-plafon/data/table', 'OlahPlafon@showTableData');
    // Jadwal
    Route::post('olah-plafon/jadwal/insert', 'OlahPlafonJadwal@store');
    Route::post('olah-plafon/jadwal/update', 'OlahPlafonJadwal@update');
    Route::post('olah-plafon/jadwal/delete', 'OlahPlafonJadwal@destroy');
    Route::post('olah-plafon/jadwal/data/table', 'OlahPlafonJadwal@showTableData');
    // Week
    Route::get('olah-plafon/week', 'OlahPlafonWeek@index');
    Route::post('olah-plafon/week/insert', 'OlahPlafonWeek@store');
    Route::post('olah-plafon/week/update', 'OlahPlafonWeek@update');
    Route::post('olah-plafon/week/delete', 'OlahPlafonWeek@destroy');
    Route::post('olah-plafon/week/data/table', 'OlahPlafonWeek@showTableData');
});
// Olah Principal
Route::group(['middleware' => 'fitur:105'], function () {
    Route::get('olah-principal', 'OlahPrincipal@index');
    Route::post('olah-principal/insert', 'OlahPrincipal@store');
    Route::post('olah-principal/update', 'OlahPrincipal@update');
    Route::post('olah-principal/delete', 'OlahPrincipal@destroy');
    Route::post('olah-principal/data/table', 'OlahPrincipal@showTableData');
});
// Olah Produk
Route::group(['middleware' => 'fitur:108'], function () {
    // Produk
    Route::get('olah-produk', 'OlahProduk@index')->name('olah-produk.index');
    Route::get('olah-produk/create', 'OlahProduk@create')->name('olah-produk.create');
    Route::post('olah-produk/insert', 'OlahProduk@store');
    Route::post('olah-produk/update', 'OlahProduk@update');
    Route::post('olah-produk/delete', 'OlahProduk@destroy');
    Route::post('olah-produk/data/table', 'OlahProduk@showTableData');
    // Brand
    Route::get('olah-produk/brand', 'OlahProdukBrand@index');
    Route::post('olah-produk/brand/insert', 'OlahProdukBrand@store');
    Route::post('olah-produk/brand/update', 'OlahProdukBrand@update');
    Route::post('olah-produk/brand/delete', 'OlahProdukBrand@destroy');
    Route::post('olah-produk/brand/data/table', 'OlahProdukBrand@showTableData');
    // Tipe Harga
    Route::get('olah-produk/tipe-harga', 'OlahProdukTipeHarga@index');
    Route::post('olah-produk/tipe-harga/insert', 'OlahProdukTipeHarga@store');
    Route::post('olah-produk/tipe-harga/update', 'OlahProdukTipeHarga@update');
    Route::post('olah-produk/tipe-harga/delete', 'OlahProdukTipeHarga@destroy');
    Route::post('olah-produk/tipe-harga/data/table', 'OlahProdukTipeHarga@showTableData');
    // Kategori
    Route::get('olah-produk/kategori', 'OlahProdukKategori@index');
    Route::post('olah-produk/kategori/insert', 'OlahProdukKategori@store');
    Route::post('olah-produk/kategori/update', 'OlahProdukKategori@update');
    Route::post('olah-produk/kategori/delete', 'OlahProdukKategori@destroy');
    Route::post('olah-produk/kategori/data/table', 'OlahProdukKategori@showTableData');
    // Satuan
    Route::post('olah-produk/satuan/insert', 'OlahProdukSatuan@store');
    Route::post('olah-produk/satuan/update', 'OlahProdukSatuan@update');
    Route::post('olah-produk/satuan/delete', 'OlahProdukSatuan@destroy');
    Route::post('olah-produk/satuan/data/table', 'OlahProdukSatuan@showTableData');
    // Harga
    Route::post('olah-produk/harga/insert', 'OlahProdukHarga@store');
    Route::post('olah-produk/harga/update', 'OlahProdukHarga@update');
    Route::post('olah-produk/harga/delete', 'OlahProdukHarga@destroy');
    Route::post('olah-produk/harga/data/table', 'OlahProdukHarga@showTableData');
});
// Olah Rute
Route::group(['middleware' => 'fitur:112'], function () {
    Route::get('olah-rute', 'OlahRute@index');
    Route::post('olah-rute/insert', 'OlahRute@store');
    Route::post('olah-rute/update', 'OlahRute@update');
    Route::post('olah-rute/delete', 'OlahRute@destroy');
    Route::post('olah-rute/data/table', 'OlahRute@showTableData');
});
// Olah Sales
Route::group(['middleware' => 'fitur:104'], function () {
    Route::get('olah-sales', 'OlahSales@index');
    Route::post('olah-sales/insert', 'OlahSales@store');
    Route::post('olah-sales/update', 'OlahSales@update');
    Route::post('olah-sales/delete', 'OlahSales@destroy');
    Route::post('olah-sales/data/table', 'OlahSales@showTableData');
    Route::post('olah-sales/data/option', 'OlahSales@showOptionData');
    Route::post('olah-sales/multiple-principal/data', 'OlahSales@showDataMultiplePrincipal');
});
// Olah User
Route::group(['middleware' => 'fitur:101'], function () {
    Route::get('olah-user', 'OlahUser@index');
    Route::post('olah-user/insert', 'OlahUser@store');
    Route::post('olah-user/update', 'OlahUser@update');
    Route::post('olah-user/delete', 'OlahUser@destroy');
    Route::post('olah-user/data/table', 'OlahUser@showTableData');
});

// Olah Periode Close
Route::group(['middleware' => 'fitur:115'], function () {
    Route::get('olah-periode-close', 'OlahPeriodeClose@index');
    Route::post('olah-periode-close/insert', 'OlahPeriodeClose@store');
    Route::post('olah-periode-close/update', 'OlahPeriodeClose@update');
    Route::post('olah-periode-close/delete', 'OlahPeriodeClose@destroy');
    Route::post('olah-periode-close/data/table', 'OlahPeriodeClose@showTableData');
});

// Option Data.
Route::group(['middleware' => 'modul'], function () {
    Route::post('olah-armada/data/option', 'OlahArmada@showOptionData');
    Route::post('olah-armada/tipe/data/option', 'OlahArmadaTipe@showOptionData');
    Route::post('olah-cabang/data/option', 'OlahCabang@showOptionData');
    Route::post('olah-customer/data/option', 'OlahCustomer@showOptionData');
    Route::post('olah-customer/tipe/data/option', 'OlahCustomerTipe@showOptionData');
    Route::post('olah-driver/data/option', 'OlahDriver@showOptionData');
    Route::post('olah-departemen/data/option', 'OlahDepartemen@showOptionData');
    Route::post('olah-fitur/user/data/option2', 'OlahFiturUser@showOptionData2');
    Route::post('olah-fitur/jabatan/data/option2', 'OlahFiturJabatan@showOptionData2');
    Route::post('olah-jabatan/data/option', 'OlahJabatan@showOptionData');
    Route::post('olah-perusahaan/data/option', 'OlahPerusahaan@showOptionData');
    Route::post('olah-produk/data/option', 'OlahProduk@showOptionData');
    Route::post('olah-produk/brand/data/option', 'OlahProdukBrand@showOptionData');
    Route::post('olah-produk/kategori/data/option', 'OlahProdukKategori@showOptionData');
    Route::post('olah-produk/satuan/data/option', 'OlahProdukSatuan@showOptionData');
    Route::post('olah-produk/harga/data/option', 'OlahProdukHarga@showOptionData');
    Route::post('olah-produk/tipe-harga/data/option', 'OlahProdukTipeHarga@showOptionData');
    Route::post('olah-principal/data/option', 'OlahPrincipal@showOptionData');
    Route::post('olah-plafon/data/option', 'OlahPlafon@showOptionData');
    Route::post('olah-sales/tipe/data/option', 'OlahSalesTipe@showOptionData');
    Route::post('olah-user/data/option1', 'OlahUser@showOptionData1');
    Route::post('olah-user/data/option2', 'OlahUser@showOptionData2');
    Route::post('olah-user/data/option3', 'OlahUser@showOptionData3');
    Route::post('olah-wilayah/data/option', 'OlahWilayah@showOptionData');
    Route::post('olah-rute/data/option', 'OlahRute@showOptionData');
});

