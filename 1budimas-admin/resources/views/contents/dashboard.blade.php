@extends('layouts.main')
@section('content')
    @include('partials.breadcrumb')
    <!-- ============================================================== -->
    <!-- Content Container  -->
    <!-- ============================================================== -->
    <div class="container-fluid">
        <div class="row m-md-1">
            @php $x = userFitur(); @endphp
            @if (fitur($x, 111))
                <div class="col-md-6 col-lg-2 col-xlg-3">
                    <a href="/olah-armada">
                        <div class="card card-hover">
                            <div class="box text-center">
                                <h1 class="font-light text-info">
                                    <i class="mdi mdi-truck"></i>
                                </h1>
                                <h6 class="text-info stroke-info-text fw-normal">Olah Data Armada</h6>
                            </div>
                        </div>
                    </a>
                </div>
            @endif
            @if (fitur($x, 102))
                <div class="col-md-6 col-lg-2 col-xlg-3">
                    <a href="/olah-cabang">
                        <div class="card card-hover">
                            <div class="box ng text-center">
                                <h1 class="font-light text-info">
                                    <i class="mdi mdi-source-branch"></i>
                                </h1>
                                <h6 class="text-info stroke-info-text fw-normal">Olah Data Cabang</h6>
                            </div>
                        </div>
                    </a>
                </div>
            @endif
            @if (fitur($x, 106))
                <div class="col-md-6 col-lg-2 col-xlg-3">
                    <a href="/olah-customer">
                        <div class="card card-hover">
                            <div class="box text-center">
                                <h1 class="font-light text-info">
                                    <i class="mdi mdi-store"></i>
                                </h1>
                                <h6 class="text-info stroke-info-text fw-normal">Olah Data Customer</h6>
                            </div>
                        </div>
                    </a>
                </div>
            @endif
            @if (fitur($x, 114))
                <div class="col-md-6 col-lg-2 col-xlg-3">
                    <a href="/olah-data/import">
                        <div class="card card-hover">
                            <div class="box e text-center">
                                <h1 class="font-light text-info">
                                    <i class="mdi mdi-file"></i>
                                </h1>
                                <h6 class="text-info stroke-info-text fw-normal">Operasi Data</h6>
                            </div>
                        </div>
                    </a>
                </div>
            @endif
            @if (fitur($x, 110))
                <div class="col-md-6 col-lg-2 col-xlg-3">
                    <a href="/olah-driver">
                        <div class="card card-hover">
                            <div class="box ss text-center">
                                <h1 class="font-light text-info">
                                    <i class="mdi mdi-account-settings"></i>
                                </h1>
                                <h6 class="text-info stroke-info-text fw-normal">Olah Data Driver</h6>
                            </div>
                        </div>
                    </a>
                </div>
            @endif
            @if (fitur($x, 113))
                <div class="col-md-6 col-lg-2 col-xlg-3">
                    <a href="/olah-fitur/jabatan">
                        <div class="card card-hover">
                            <div class="box text-center">
                                <h1 class="font-light text-info">
                                    <i class="mdi mdi-apps"></i>
                                </h1>
                                <h6 class="text-info stroke-info-text fw-normal">Olah Fitur Default</h6>
                            </div>
                        </div>
                    </a>
                </div>
            @endif
            @if (fitur($x, 109))
                <div class="col-md-6 col-lg-2 col-xlg-3">
                    <a href="/olah-kode-budget">
                        <div class="card card-hover">
                            <div class="box e text-center">
                                <h1 class="font-light text-info">
                                    <i class="mdi mdi-cube-unfolded"></i>
                                </h1>
                                <h6 class="text-info stroke-info-text fw-normal">Olah Data Budget</h6>
                            </div>
                        </div>
                    </a>
                </div>
            @endif
            @if (fitur($x, 103))
                <div class="col-md-6 col-lg-2 col-xlg-3">
                    <a href="/olah-perusahaan">
                        <div class="card card-hover">
                            <div class="box ss text-center">
                                <h1 class="font-light text-info">
                                    <i class="mdi mdi-home-modern"></i>
                                </h1>
                                <h6 class="text-info stroke-info-text fw-normal">Olah Data Perusahaan</h6>
                            </div>
                        </div>
                    </a>
                </div>
            @endif
            @if (fitur($x, 107))
                <div class="col-md-6 col-lg-2 col-xlg-3">
                    <a href="/olah-plafon">
                        <div class="card card-hover">
                            <div class="box text-center">
                                <h1 class="font-light text-info">
                                    <i class="mdi mdi-sitemap"></i>
                                </h1>
                                <h6 class="text-info stroke-info-text fw-normal">Olah Data Plafon</h6>
                            </div>
                        </div>
                    </a>
                </div>
            @endif
            @if (fitur($x, 105))
                <div class="col-md-6 col-lg-2 col-xlg-3">
                    <a href="/olah-principal">
                        <div class="card card-hover">
                            <div class="box ss text-center">
                                <h1 class="font-light text-info">
                                    <i class="mdi mdi-pillar"></i>
                                </h1>
                                <h6 class="text-info stroke-info-text fw-normal">Olah Data Principal</h6>
                            </div>
                        </div>
                    </a>
                </div>
            @endif
            @if (fitur($x, 108))
                <div class="col-md-6 col-lg-2 col-xlg-3">
                    <a href="/olah-produk">
                        <div class="card card-hover">
                            <div class="box r text-center">
                                <h1 class="font-light text-info">
                                    <i class="mdi mdi-hamburger"></i>
                                </h1>
                                <h6 class="text-info stroke-info-text fw-normal">Olah Data Produk</h6>
                            </div>
                        </div>
                    </a>
                </div>
            @endif
            @if (fitur($x, 112))
                <div class="col-md-6 col-lg-2 col-xlg-3">
                    <a href="/olah-rute">
                        <div class="card card-hover">
                            <div class="box ng text-center">
                                <h1 class="font-light text-info">
                                    <i class="mdi mdi-google-maps"></i>
                                </h1>
                                <h6 class="text-info stroke-info-text fw-normal">Olah Data Rute</h6>
                            </div>
                        </div>
                    </a>
                </div>
            @endif
            @if (fitur($x, 104))
                <div class="col-md-6 col-lg-2 col-xlg-3">
                    <a href="/olah-sales">
                        <div class="card card-hover">
                            <div class="box text-center">
                                <h1 class="font-light text-info">
                                    <i class="mdi mdi-account-switch"></i>
                                </h1>
                                <h6 class="text-info stroke-info-text fw-normal">Olah Data Sales</h6>
                            </div>
                        </div>
                    </a>
                </div>
            @endif
            @if (fitur($x, 101))
                <div class="col-md-6 col-lg-2 col-xlg-3">
                    <a href="/olah-user">
                        <div class="card card-hover">
                            <div class="box text-center">
                                <h1 class="font-light text-info">
                                    <i class="mdi mdi-folder-account"></i>
                                </h1>
                                <h6 class="text-info stroke-info-text fw-normal">Olah Data User</h6>
                            </div>
                        </div>
                    </a>
                </div>
            @endif
            @if (fitur($x, 115))
                <div class="col-md-6 col-lg-2 col-xlg-3">
                    <a href="/olah-periode-close">
                        <div class="card card-hover">
                            <div class="box text-center">
                                <h1 class="font-light    text-info">
                                    <i class="mdi mdi-calendar-blank"></i>
                                </h1>
                                <h6 class="text-info stroke-info-text fw-normal">Olah Periode Close
                                </h6>
                            </div>
                        </div>
                    </a>
                </div>
            @endif
        </div>
    </div>
    <!-- ============================================================== -->
    <!-- End Content Container  -->
    <!-- ============================================================== -->
@endsection
