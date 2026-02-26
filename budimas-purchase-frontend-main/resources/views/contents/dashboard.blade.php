@extends('layouts.main')
@section('content')
@include('partials.breadcrumb')
<!-- ============================================================== -->
<!-- Container fluid  -->
<!-- ============================================================== -->
<div class="container-fluid">
    <div class="row m-md-1">
        <div class="col-6 col-lg-2 col-xlg-3">
            <a href="{{ route('purchase-order.create') }}">
                <div class="card card-hover">
                    <div class="box text-center">
                        <h1 class="font-light text-info">
                            <i class="mdi mdi-file-document"></i>
                        </h1>
                        <h6 class="text-info stroke-info-text fw-normal">Request Order</h6>
                    </div>
                </div>
            </a>
        </div>
        <div class="col-6 col-lg-2 col-xlg-3">
            <a href="{{ route('konfirmasi-order.index') }}">
                <div class="card card-hover">
                    <div class="box text-center">
                        <h1 class="font-light text-info">
                            <i class="mdi mdi-file-check"></i>
                        </h1>
                        <h6 class="text-info stroke-info-text fw-normal">Konf. Order</h6>
                    </div>
                </div>
            </a>
        </div>
        <div class="col-6 col-lg-2 col-xlg-3">
            <a href="{{ route('penerimaan-barang.index') }}">
                <div class="card card-hover">
                    <div class="box text-center">
                        <h1 class="font-light text-info">
                            <i class="mdi mdi-clipboard-text"></i>
                        </h1>
                        <h6 class="text-info stroke-info-text fw-normal">Penerimaan Barang</h6>
                    </div>
                </div>
            </a>
        </div>
        <div class="col-6 col-lg-2 col-xlg-3">
            <a href="{{ route('transaksi-konfirmasi.index') }}">
                <div class="card card-hover">
                    <div class="box text-center">
                        <h1 class="font-light text-info">
                            <i class="mdi mdi-clipboard-check"></i>
                        </h1>
                        <h6 class="text-info stroke-info-text fw-normal">Konf. Purchase</h6>
                    </div>
                </div>
            </a>
        </div>
        {{-- <div class="col-6 col-lg-2 col-xlg-3">
            <a href="{{ route('transaksi-tagihan.index') }}">
                <div class="card card-hover">
                    <div class="box text-center">
                        <h1 class="font-light text-info">
                            <i class="mdi mdi-credit-card"></i>
                        </h1>
                        <h6 class="text-info stroke-info-text fw-normal">Pembuatan Tagihan</h6>
                    </div>
                </div>
            </a>
        </div>
        <div class="col-6 col-lg-2 col-xlg-3">
            <a href="{{ route('transaksi-pembayaran.index') }}">
                <div class="card card-hover">
                    <div class="box text-center">
                        <h1 class="font-light text-info">
                            <i class="mdi mdi-cash-multiple"></i>
                        </h1>
                        <h6 class="text-info stroke-info-text fw-normal">Pembayaran</h6>
                    </div>
                </div>
            </a>
        </div> --}}
        <div class="col-6 col-lg-2 col-xlg-3">
            <a href="{{ route('laporan-order') }}">
                <div class="card card-hover">
                    <div class="box text-center">
                        <h1 class="font-light text-info">
                            <i class="mdi mdi-book-open"></i>
                        </h1>
                        <h6 class="text-info stroke-info-text fw-normal">Laporan</h6>
                    </div>
                </div>
            </a>
        </div>
        {{-- <div class="col-6 col-lg-2 col-xlg-3">
            <a href="{{ route('laporan-purchase') }}">
                <div class="card card-hover">
                    <div class="box text-center">
                        <h1 class="font-light text-info">
                            <i class="mdi mdi-book-open"></i>
                        </h1>
                        <h6 class="text-info stroke-info-text fw-normal"><em>Lap.</em> Purchase</h6>
                    </div>
                </div>
            </a>
        </div> --}}
    </div>
</div>
<!-- ============================================================== -->
<!-- End Container fluid  -->
<!-- ============================================================== -->
@endsection