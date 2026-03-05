<?php

use Illuminate\Support\Facades\Route;
/*
 * |--------------------------------------------------------------------------
 * | Import Controller Class
 * |--------------------------------------------------------------------------
 * |
 */
use App\Http\Controllers\Authenticate;
use App\Http\Controllers\CetakNota;
use App\Http\Controllers\Dashboard;
use App\Http\Controllers\KonfirmasiOrder;
use App\Http\Controllers\KonfirmasiRequest;
use App\Http\Controllers\KonfirmasiTagihan;
use App\Http\Controllers\Pembayaran;
use App\Http\Controllers\Profile;
use App\Http\Controllers\PurchaseKonfirmasi;
use App\Http\Controllers\PurchaseOrder;
use App\Http\Controllers\PurchasePembayaran;
use App\Http\Controllers\PurchasePenerimaanBarang;
use App\Http\Controllers\PurchaseTagihan;
use App\Http\Controllers\TestController;

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
        Route::get('dashboard', [Dashboard::class, 'index'])->name('dashboard.index');

        // Edit Profile
        Route::get('profile', [Profile::class, 'index'])->name('profile.index');
        Route::post('profile/update', [Profile::class, 'update'])->name('profile.update');

        // Request
        Route::get('purchase-order', [PurchaseOrder::class, 'create'])
                ->name('purchase-order.create');
        Route::post('purchase-order/store', [PurchaseOrder::class, 'store'])
                ->name('purchase-order.store');
        Route::get('purchase-order/edit/{id}', [PurchaseOrder::class, 'edit'])
                ->name('purchase-order.edit');
        Route::get('laporan-order/', [PurchaseOrder::class, 'laporan'])
                ->name('laporan-order');
        Route::get('laporan-order/{id}', [PurchaseOrder::class, 'laporanDetail'])
                ->name('laporan-order.detail');
        Route::post('purchase-order/update', [PurchaseOrder::class, 'updateData'])
                ->name('purchase-order.update.data');
        Route::get('konfirmasi-order', [PurchaseOrder::class, 'index'])
                ->name('konfirmasi-order.index');
        Route::post('konfirmasi-order/store', [PurchaseOrder::class, 'updatePurchasing'])
                ->name('konfirmasi-order.store');
        Route::post('purchase-order/data/table', [PurchaseOrder::class, 'showTableKonfirmasi'])
                ->name('purchase-order.show.table');
        Route::post('purchase-order/data/detail', [PurchaseOrder::class, 'showData'])
                ->name('purchase-order.show.table2');
        Route::post('purchase-order/destroy', [PurchaseOrder::class, 'updateClosed'])
                ->name('purchase-order.destroy');

        Route::get('penerimaan-barang', [PurchasePenerimaanBarang::class, 'index'])
                ->name('penerimaan-barang.index');
        Route::post('penerimaan-barang/data/table', [PurchasePenerimaanBarang::class, 'showTable'])
                ->name('penerimaan-barang.show.table');
        Route::get('penerimaan-barang/create/{id}', [PurchasePenerimaanBarang::class, 'create'])
                ->name('penerimaan-barang.create');
        Route::post('penerimaan-barang/store', [PurchasePenerimaanBarang::class, 'store'])
                ->name('penerimaan-barang.store');
        // Route::get('laporan-purchase', [PurchasePenerimaanBarang::class, 'laporan'])
        //         ->name('laporan-purchase');

        Route::get('transaksi-konfirmasi', [PurchaseKonfirmasi::class, 'index'])
                ->name('transaksi-konfirmasi.index');
        // Route::get('transaksi-tagihan', [PurchaseTagihan::class, 'index'])
        //         ->name('transaksi-tagihan.index');
        // Route::get('transaksi-pembayaran', [PurchasePembayaran::class, 'index'])
        //         ->name('transaksi-pembayaran.index');
        Route::get('transaksi-pembayaran/list', [PurchasePembayaran::class, 'create'])
                ->name('transaksi-pembayaran.create');
        Route::post('konfirmasi-purchase/store', [PurchaseKonfirmasi::class, 'store'])
                ->name('konfirmasi-order.create');

        // Konfirmasi Request
        Route::get('konfirmasi-request', [KonfirmasiRequest::class, 'index'])->name('konfirmasi-request.index');
        Route::get('konfirmasi-request/edit/{id}', [KonfirmasiRequest::class, 'edit'])->name('konfirmasi-request.edit');
        Route::post('konfirmasi-request/data', [KonfirmasiRequest::class, 'showData'])->name('konfirmasi-request.show');
        Route::post('konfirmasi-request/data/table', [KonfirmasiRequest::class, 'showTableData'])->name('konfirmasi-request.show2');
        Route::post('konfirmasi-request/store', [KonfirmasiRequest::class, 'store'])->name('konfirmasi-request.store');
        Route::post('konfirmasi-request/update', [KonfirmasiRequest::class, 'update'])->name('konfirmasi-request.update');
        Route::post('konfirmasi-request/destroy', [KonfirmasiRequest::class, 'destroy'])->name('konfirmasi-request.destroy');

        // Konfirmasi Tagihan
        Route::get('konfirmasi-tagihan', [KonfirmasiTagihan::class, 'index'])->name('konfirmasi-tagihan.index');
        Route::post('konfirmasi-tagihan/data/table', [KonfirmasiTagihan::class, 'showTableData'])->name('konfirmasi-tagihan.show2');
        Route::post('konfirmasi-tagihan/store', [KonfirmasiTagihan::class, 'store'])->name('konfirmasi-tagihan.store');

        // Pembayaran
        Route::get('pembayaran', [Pembayaran::class, 'index'])->name('pembayaran.index');
        Route::get('pembayaran/list', [Pembayaran::class, 'create'])->name('pembayaran.create');
        Route::post('pembayaran/data', [Pembayaran::class, 'showData'])->name('pembayaran.show');
        Route::post('pembayaran/data/table', [Pembayaran::class, 'showTableData'])->name('pembayaran.show2');

        Route::get('cetak-nota/purchase/faktur', [CetakNota::class, 'purchaseFaktur'])->name('cetak-nota.purchase-faktur');
        Route::get('cetak-nota/purchase/riwayat-pelunasan', [CetakNota::class, 'purchaseRiwayatPelunasan'])->name('cetak-nota.purchase-riwayat-pelunasan');
});

// Olah Cabang
// Route::group(['middleware' => 'fitur:102'], function () {
//     Route:: get ( 'olah-cabang',                        'OlahCabang@index'                  );
//     Route:: post( 'olah-cabang/insert',                 'OlahCabang@store'                  );
//     Route:: post( 'olah-cabang/update',                 'OlahCabang@update'                 );
//     Route:: post( 'olah-cabang/delete',                 'OlahCabang@destroy'                );
//     Route:: post( 'olah-cabang/data/table',             'OlahCabang@showTableData'          );
// });
// Olah Customer
// Route::group(['middleware' => 'fitur:106'], function () {
//     // Customer
//     Route:: get ( 'olah-customer',                      'OlahCustomer@index'                );
//     Route:: post( 'olah-customer/insert',               'OlahCustomer@store'                );
//     Route:: post( 'olah-customer/update',               'OlahCustomer@update'               );
//     Route:: post( 'olah-customer/delete',               'OlahCustomer@destroy'              );
//     Route:: post( 'olah-customer/data/table',           'OlahCustomer@showTableData'        );
//     // Tipe
//     Route:: get ( 'olah-customer/tipe',                 'OlahCustomerTipe@index'            );
//     Route:: post( 'olah-customer/tipe/insert',          'OlahCustomerTipe@store'            );
//     Route:: post( 'olah-customer/tipe/update',          'OlahCustomerTipe@update'           );
//     Route:: post( 'olah-customer/tipe/delete',          'OlahCustomerTipe@destroy'          );
//     Route:: post( 'olah-customer/tipe/data/table',      'OlahCustomerTipe@showTableData'    );
// });
// Olah Data
// Route::group(['middleware' => 'fitur:114'], function () {
//     // Import Data
//     Route:: get ( 'olah-data/import',                   'ImportData@create'                );
//     Route:: post( 'olah-data/import',                   'ImportData@store'                 );
//     Route:: post( 'olah-data/import/show',              'ImportData@show'                  );
//     // Export Data
//     Route:: get ( 'olah-data/export',                   'ExportData@create'                );
//     Route:: post( 'olah-data/export',                   'ExportData@show'                  );
// });
// Olah Driver
// Route::group(['middleware' => 'fitur:110'], function () {
//     Route:: get ( 'olah-driver',                        'OlahDriver@index'                 );
//     Route:: post( 'olah-driver/insert',                 'OlahDriver@store'                 );
//     Route:: post( 'olah-driver/update',                 'OlahDriver@update'                );
//     Route:: post( 'olah-driver/delete',                 'OlahDriver@destroy'               );
//     Route:: post( 'olah-driver/data/table',             'OlahDriver@showTableData'         );
// });
// Olah Fitur
// Route::group(['middleware' => 'fitur:113'], function () {
//     // Jabatan
//     Route:: get ( 'olah-fitur/jabatan',                 'OlahFiturJabatan@index'           );
//     Route:: post( 'olah-fitur/jabatan/insert',          'OlahFiturJabatan@store'           );
//     Route:: post( 'olah-fitur/jabatan/update',          'OlahFiturJabatan@update'          );
//     Route:: post( 'olah-fitur/jabatan/delete',          'OlahFiturJabatan@destroy'         );
//     Route:: post( 'olah-fitur/jabatan/data/table',      'OlahFiturJabatan@showTableData'   );
//     Route:: post( 'olah-fitur/jabatan/data/table2',     'OlahFiturJabatan@showTableData2'  );

//     // User
//     Route:: post( 'olah-fitur/user/insert',             'OlahFiturUser@store'              );
//     Route:: post( 'olah-fitur/user/update',             'OlahFiturUser@update'             );
//     Route:: post( 'olah-fitur/user/delete',             'OlahFiturUser@destroy'            );
//     Route:: post( 'olah-fitur/user/data/table',         'OlahFiturUser@showTableData'      );
// });
// Olah Kode Budget
// Route::group(['middleware' => 'fitur:109'], function () {
//     Route:: get ( 'olah-kode-budget',                   'OlahKodeBudget@index'             );
//     Route:: post( 'olah-kode-budget/insert',            'OlahKodeBudget@store'             );
//     Route:: post( 'olah-kode-budget/update',            'OlahKodeBudget@update'            );
//     Route:: post( 'olah-kode-budget/delete',            'OlahKodeBudget@destroy'           );
//     Route:: post( 'olah-kode-budget/data/table',        'OlahKodeBudget@showTableData'     );
// });
// Olah Perusahaan
// Route::group(['middleware' => 'fitur:103'], function () {
//     Route:: get ( 'olah-perusahaan',                    'OlahPerusahaan@index'             );
//     Route:: post( 'olah-perusahaan/insert',             'OlahPerusahaan@store'             );
//     Route:: post( 'olah-perusahaan/update',             'OlahPerusahaan@update'            );
//     Route:: post( 'olah-perusahaan/delete',             'OlahPerusahaan@destroy'           );
//     Route:: post( 'olah-perusahaan/data/table',         'OlahPerusahaan@showTableData'     );
// });
// Olah Plafon
// Route::group(['middleware' => 'fitur:107'], function () {
//     // Plafon
//     Route:: get ( 'olah-plafon',                        'OlahPlafon@index'                 );
//     Route:: post( 'olah-plafon/insert',                 'OlahPlafon@store'                 );
//     Route:: post( 'olah-plafon/update',                 'OlahPlafon@update'                );
//     Route:: post( 'olah-plafon/delete',                 'OlahPlafon@destroy'               );
//     Route:: post( 'olah-plafon/data/table',             'OlahPlafon@showTableData'         );
//     // Jadwal
//     Route:: post( 'olah-plafon/jadwal/insert',          'OlahPlafonJadwal@store'           );
//     Route:: post( 'olah-plafon/jadwal/update',          'OlahPlafonJadwal@update'          );
//     Route:: post( 'olah-plafon/jadwal/delete',          'OlahPlafonJadwal@destroy'         );
//     Route:: post( 'olah-plafon/jadwal/data/table',      'OlahPlafonJadwal@showTableData'   );
//     // Week
//     Route:: get ( 'olah-plafon/week',                   'OlahPlafonWeek@index'             );
//     Route:: post( 'olah-plafon/week/insert',            'OlahPlafonWeek@store'             );
//     Route:: post( 'olah-plafon/week/update',            'OlahPlafonWeek@update'            );
//     Route:: post( 'olah-plafon/week/delete',            'OlahPlafonWeek@destroy'           );
//     Route:: post( 'olah-plafon/week/data/table',        'OlahPlafonWeek@showTableData'     );
// });
// Olah Principal
// Route::group(['middleware' => 'fitur:105'], function () {
//     Route:: get ( 'olah-principal',                     'OlahPrincipal@index'              );
//     Route:: post( 'olah-principal/insert',              'OlahPrincipal@store'              );
//     Route:: post( 'olah-principal/update',              'OlahPrincipal@update'             );
//     Route:: post( 'olah-principal/delete',              'OlahPrincipal@destroy'            );
//     Route:: post( 'olah-principal/data/table',          'OlahPrincipal@showTableData'      );
// });
// Olah Produk
// Route::group(['middleware' => 'fitur:108'], function () {
//     // Produk
//     Route:: get ( 'olah-produk',                        'OlahProduk@index'                 );
//     Route:: post( 'olah-produk/insert',                 'OlahProduk@store'                 );
//     Route:: post( 'olah-produk/update',                 'OlahProduk@update'                );
//     Route:: post( 'olah-produk/delete',                 'OlahProduk@destroy'               );
//     Route:: post( 'olah-produk/data/table',             'OlahProduk@showTableData'         );
//     // Brand
//     Route:: get ( 'olah-produk/brand',                  'OlahProdukBrand@index'            );
//     Route:: post( 'olah-produk/brand/insert',           'OlahProdukBrand@store'            );
//     Route:: post( 'olah-produk/brand/update',           'OlahProdukBrand@update'           );
//     Route:: post( 'olah-produk/brand/delete',           'OlahProdukBrand@destroy'          );
//     Route:: post( 'olah-produk/brand/data/table',       'OlahProdukBrand@showTableData'    );
//     // Tipe Harga
//     Route:: get ( 'olah-produk/tipe-harga',             'OlahProdukTipeHarga@index'        );
//     Route:: post( 'olah-produk/tipe-harga/insert',      'OlahProdukTipeHarga@store'        );
//     Route:: post( 'olah-produk/tipe-harga/update',      'OlahProdukTipeHarga@update'       );
//     Route:: post( 'olah-produk/tipe-harga/delete',      'OlahProdukTipeHarga@destroy'      );
//     Route:: post( 'olah-produk/tipe-harga/data/table',  'OlahProdukTipeHarga@showTableData');
//     // Kategori
//     Route:: get ( 'olah-produk/kategori',               'OlahProdukKategori@index'         );
//     Route:: post( 'olah-produk/kategori/insert',        'OlahProdukKategori@store'         );
//     Route:: post( 'olah-produk/kategori/update',        'OlahProdukKategori@update'        );
//     Route:: post( 'olah-produk/kategori/delete',        'OlahProdukKategori@destroy'       );
//     Route:: post( 'olah-produk/kategori/data/table',    'OlahProdukKategori@showTableData' );
//     // Satuan
//     Route:: post( 'olah-produk/satuan/insert',          'OlahProdukSatuan@store'           );
//     Route:: post( 'olah-produk/satuan/update',          'OlahProdukSatuan@update'          );
//     Route:: post( 'olah-produk/satuan/delete',          'OlahProdukSatuan@destroy'         );
//     Route:: post( 'olah-produk/satuan/data/table',      'OlahProdukSatuan@showTableData'   );
//     // Harga
//     Route:: post( 'olah-produk/harga/insert',           'OlahProdukHarga@store'            );
//     Route:: post( 'olah-produk/harga/update',           'OlahProdukHarga@update'           );
//     Route:: post( 'olah-produk/harga/delete',           'OlahProdukHarga@destroy'          );
//     Route:: post( 'olah-produk/harga/data/table',       'OlahProdukHarga@showTableData'    );
// });
// Olah Rute
// Route::group(['middleware' => 'fitur:112'], function () {
//     Route:: get ( 'olah-rute',                          'OlahRute@index'                   );
//     Route:: post( 'olah-rute/insert',                   'OlahRute@store'                   );
//     Route:: post( 'olah-rute/update',                   'OlahRute@update'                  );
//     Route:: post( 'olah-rute/delete',                   'OlahRute@destroy'                 );
//     Route:: post( 'olah-rute/data/table',               'OlahRute@showTableData'           );
// });
// // Olah Sales
// Route::group(['middleware' => 'fitur:104'], function () {
//     Route:: get ( 'olah-sales',                         'OlahSales@index'                  );
//     Route:: post( 'olah-sales/insert',                  'OlahSales@store'                  );
//     Route:: post( 'olah-sales/update',                  'OlahSales@update'                 );
//     Route:: post( 'olah-sales/delete',                  'OlahSales@destroy'                );
//     Route:: post( 'olah-sales/data/table',              'OlahSales@showTableData'          );
// });
// // Olah User
// Route::group(['middleware' => 'fitur:101'], function () {
//     Route:: get ( 'olah-user',                          'OlahUser@index'                   );
//     Route:: post( 'olah-user/insert',                   'OlahUser@store'                   );
//     Route:: post( 'olah-user/update',                   'OlahUser@update'                  );
//     Route:: post( 'olah-user/delete',                   'OlahUser@destroy'                 );
//     Route:: post( 'olah-user/data/table',               'OlahUser@showTableData'           );
// });
// Option Data.
// Route::group(['middleware' => 'modul'], function () {
//     Route:: post( 'olah-armada/data/option',            'OlahArmada@showOptionData'         );
//     Route:: post( 'olah-armada/tipe/data/option',       'OlahArmadaTipe@showOptionData'     );
//     Route:: post( 'olah-cabang/data/option',            'OlahCabang@showOptionData'         );
//     Route:: post( 'olah-customer/data/option',          'OlahCustomer@showOptionData'       );
//     Route:: post( 'olah-customer/tipe/data/option',     'OlahCustomerTipe@showOptionData'   );
//     Route:: post( 'olah-driver/data/option',            'OlahDriver@showOptionData'         );
//     Route:: post( 'olah-departemen/data/option',        'OlahDepartemen@showOptionData'     );
//     Route:: post( 'olah-fitur/user/data/option2',       'OlahFiturUser@showOptionData2'     );
//     Route:: post( 'olah-fitur/jabatan/data/option2',    'OlahFiturJabatan@showOptionData2'  );
//     Route:: post( 'olah-jabatan/data/option',           'OlahJabatan@showOptionData'        );
//     Route:: post( 'olah-perusahaan/data/option',        'OlahPerusahaan@showOptionData'     );
//     Route:: post( 'olah-produk/data/option',            'OlahProduk@showOptionData'         );
//     Route:: post( 'olah-produk/data/option2',           'OlahProduk@showOptionData2'        );
//     Route:: post( 'olah-produk/brand/data/option',      'OlahProdukBrand@showOptionData'    );
//     Route:: post( 'olah-produk/kategori/data/option',   'OlahProdukKategori@showOptionData' );
//     Route:: post( 'olah-produk/satuan/data/option',     'OlahProdukSatuan@showOptionData'   );
//     Route:: post( 'olah-produk/satuan/data/option2',    'OlahProdukSatuan@showOptionData2'  );
//     Route:: post( 'olah-produk/satuan/data/option3',    'OlahProdukSatuan@showOptionData3'  );
//     Route:: post( 'olah-produk/satuan/data1',           'OlahProdukSatuan@showData1'        );
//     Route:: post( 'olah-produk/harga/data/option',      'OlahProdukHarga@showOptionData'    );
//     Route:: post( 'olah-produk/tipe-harga/data/option', 'OlahProdukTipeHarga@showOptionData');
//     Route:: post( 'olah-principal/data/option',         'OlahPrincipal@showOptionData'      );
//     Route:: post( 'olah-plafon/data/option',            'OlahPlafon@showOptionData'         );
//     Route:: post( 'olah-sales/tipe/data/option',        'OlahSalesTipe@showOptionData'      );
//     Route:: post( 'olah-user/data/option1',             'OlahUser@showOptionData1'          );
//     Route:: post( 'olah-user/data/option2',             'OlahUser@showOptionData2'          );
//     Route:: post( 'olah-user/data/option3',             'OlahUser@showOptionData3'          );
//     Route:: post( 'olah-user/data/option4',             'OlahUser@showOptionData4'          );
//     Route:: post( 'olah-user/data/option5',             'OlahUser@showOptionData5'          );
//     Route:: post( 'olah-wilayah/data/option',           'OlahWilayah@showOptionData'        );
// });

// Order
// Route:: get ( 'purchase-order',                 'PurchaseOrder@index'        )->name('purchase-order.index'  );
// Route:: get ( 'purchase-order/create/{id}',     'PurchaseOrder@create'       )->name('purchase-order.create' );
// Route:: post( 'purchase-order/data',            'PurchaseOrder@showData'     )->name('purchase-order.show'   );
// Route:: post( 'purchase-order/data/table',      'PurchaseOrder@showTableData')->name('purchase-order.show2'  );
// Route:: post( 'purchase-order/store',           'PurchaseOrder@store'        )->name('purchase-order.store'  );
// Route:: post( 'purchase-order/destroy',         'PurchaseOrder@destroy'      )->name('purchase-order.destroy');

// Konfirmasi Order
// Route:: get ( 'konfirmasi-order',               'KonfirmasiOrder@index'         )->name('konfirmasi-order.index');
// Route:: post( 'konfirmasi-order/data',          'KonfirmasiOrder@showData'      )->name('konfirmasi-order.show' );
// Route:: post( 'konfirmasi-order/data/table',    'KonfirmasiOrder@showTableData' )->name('konfirmasi-order.show2');
// Route:: post( 'konfirmasi-order/store',         [KonfirmasiOrder::class, 'store']        )->name('konfirmasi-order.store');
