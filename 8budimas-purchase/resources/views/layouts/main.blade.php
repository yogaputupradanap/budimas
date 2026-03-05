<!DOCTYPE html>
<html dir="ltr" lang="en">

<head>
    <meta charset="utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="_token" id="csrf" content="{{ csrf_token() }}">
    <!-- Tell the browser to be responsive to screen width -->
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="keywords" content="PT. BUDIMAS MAKMUR MULIA" />
    <meta name="description" content="PT. BUDIMAS MAKMUR MULIA" />
    <meta name="robots" content="noindex,nofollow" />
    <title>PT. BUDIMAS MAKMUR MULIA</title>
    <!-- Favicon icon -->
    <link rel="icon" type="image/png" sizes="16x16"
        href="{{ asset('assets-panel/assets/images/icon-budimas.png') }}" />
    <link rel="stylesheet" href="{{ asset('assets-panel/assets/libs/flot/css/float-chart.css') }}">
    <!-- <link rel="stylesheet" href="{{ asset('assets-panel/assets/libs/datatables.net-bs4/css/dataTables.bootstrap4.css') }}" > -->
    <link rel="stylesheet" href="{{ asset('assets-panel/assets/libs/select2/dist/css/select2.min.css') }}">
    <!-- Bootstrap -->
    <link rel="stylesheet" href="{{ asset('assets-panel/assets/libs/bootstrap/dist/css/bootstrap.min.css') }}">
    <!-- Datepicker -->
    <link rel="stylesheet"
        href="{{ asset('assets-panel/assets/libs/bootstrap-datepicker/dist/css/bootstrap-datepicker.min.css') }}">
    <!-- Custom CSS -->
    <link rel="stylesheet" href="{{ mix('css/vendor.css') }}">
    <link rel="stylesheet" href="{{ asset('assets-panel/dist/css/style.min.css') }}">
    <link rel="stylesheet" href="{{ asset('assets-panel/dist/css/custom.css') }}">
    <!-- Daterangepicker -->
    <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/daterangepicker/daterangepicker.css" />
</head>

<body>
    <!-- ============================================================== -->
    <!-- Preloader - style you can find in spinners.css -->
    <!-- ============================================================== -->
    <div class="preloader">
        <div class="lds-ripple">
            <div class="lds-pos"></div>
            <div class="lds-pos"></div>
        </div>
    </div>
    <!-- ============================================================== -->
    <!-- Main wrapper - style you can find in pages.scss -->
    <!-- ============================================================== -->
    <div id="main-wrapper" data-layout="vertical" data-navbarbg="skin5" data-sidebartype="full"
        data-sidebar-position="absolute" data-header-position="absolute" data-boxed-layout="full">
        <!-- ============================================================== -->
        <!-- Session Data -->
        <!-- ============================================================== -->
        @if (session()->has('status'))
            <input type="hidden" id="session-alert" value="{{ session('status') }}">
        @endif
        <!-- ============================================================== -->
        <!-- End Session Data -->
        <!-- ============================================================== -->
        <!-- ============================================================== -->
        <!-- Topbar header - style you can find in pages.scss -->
        <!-- ============================================================== -->
        @include('partials.header')
        <!-- ============================================================== -->
        <!-- End Topbar header -->
        <!-- ============================================================== -->
        <!-- ============================================================== -->
        <!-- Left Sidebar - style you can find in sidebar.scss  -->
        <!-- ============================================================== -->
        @include('partials.sidebar')
        <!-- ============================================================== -->
        <!-- End Left Sidebar - style you can find in sidebar.scss  -->
        <!-- ============================================================== -->
        <!-- ============================================================== -->
        <!-- Page wrapper  -->
        <!-- ============================================================== -->
        <div class="page-wrapper">
            @yield('content')
            <!-- ============================================================== -->
            <!-- footer -->
            <!-- ============================================================== -->
            <footer class="footer text-center">
                <div class="mb-2">
                    Copyright&copy;
                    <script>
                        document.write(new Date().getFullYear());
                    </script>
                    PT. BUDIMAS MAKMUR MULIA
                    <br>
                    Designed and Developed by <a href="https://www.horus.co.id" target="_blank">HORUS TECHNOLOGY</a>
                </div>
            </footer>
            <!-- ============================================================== -->
            <!-- End footer -->
            <!-- ============================================================== -->
        </div>
        <!-- ============================================================== -->
        <!-- End Page wrapper  -->
        <!-- ============================================================== -->
    </div>
    <!-- ============================================================== -->
    <!-- End Wrapper -->
    <!-- ============================================================== -->
    <!-- ============================================================== -->
    <!-- Javascript Plugins Import -->
    <!-- ============================================================== -->
    <!-- <script src="{{ asset('assets-panel/assets/libs/jquery/dist/jquery.min.js') }}"></script> -->
    <!-- Bootstrap tether Core JavaScript -->
    <script>
        window.baseURL = @json(App\Models\Model::getBaseURL());
        window.userToken = @json(Auth::user()->getRememberToken());
    </script>

    <script src="{{ mix('js/vendor.js') }}"></script>
    <script src="{{ mix('js/main.js') }}?v={{ time() }}"></script>
    <script src="{{ asset('assets-panel/assets/libs/bootstrap/dist/js/bootstrap.bundle.min.js') }}"></script>
    <script src="{{ asset('assets-panel/assets/libs/perfect-scrollbar/dist/perfect-scrollbar.jquery.min.js') }}"></script>
    <script src="{{ asset('assets-panel/assets/extra-libs/sparkline/sparkline.js') }}"></script>
    <!--Wave Effects -->
    <script src="{{ asset('assets-panel/dist/js/waves.js') }}"></script>
    <!--Menu sidebar -->
    <script src="{{ asset('assets-panel/dist/js/sidebarmenu.js') }}"></script>
    <!--Custom JavaScript -->
    <script src="{{ asset('assets-panel/dist/js/custom.js') }}"></script>
    <!--This page JavaScript -->
    <!-- <script src="dist/js/pages/dashboards/dashboard1.js"></script> -->
    <!-- Select 2 -->
    <script src="{{ asset('/assets-panel/assets/libs/select2/dist/js/select2.min.js') }}"></script>
    <!-- Block UI -->
    <script src="{{ asset('/assets-panel/assets/libs/jquery-blockUI/blockUI-2.70.js') }}"></script>
    <!-- Charts js Files -->
    <script src="{{ asset('assets-panel/assets/libs/flot/excanvas.js') }}"></script>
    <script src="{{ asset('assets-panel/assets/libs/flot/jquery.flot.js') }}"></script>
    <script src="{{ asset('assets-panel/assets/libs/flot/jquery.flot.pie.js') }}"></script>
    <script src="{{ asset('assets-panel/assets/libs/flot/jquery.flot.time.js') }}"></script>
    <script src="{{ asset('assets-panel/assets/libs/flot/jquery.flot.stack.js') }}"></script>
    <script src="{{ asset('assets-panel/assets/libs/flot/jquery.flot.crosshair.js') }}"></script>
    <script src="{{ asset('assets-panel/assets/libs/flot.tooltip/js/jquery.flot.tooltip.min.js') }}"></script>
    <script src="{{ asset('assets-panel/dist/js/pages/chart/chart-page-init.js') }}"></script>
    <!-- <script src="{{ asset('assets-panel/assets/extra-libs/DataTables/datatables.min.js') }}"></script> -->
    <script src="//cdn.jsdelivr.net/npm/sweetalert2@11"></script>
    <script src="{{ asset('assets-panel/assets/libs/bootstrap-datepicker/dist/js/bootstrap-datepicker.min.js') }}">
    </script>
    <script src="{{ asset('assets-panel/assets/libs/vue/dist/vue.min.js') }}"></script>
    <script src="{{ asset('assets-panel/dist/js/pages/vue-apps/components/select2.vue') }}"></script>
    <script src="{{ asset('assets-panel/dist/js/pages/vue-apps/components/datepicker.vue') }}"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.3.0/papaparse.min.js"></script>
    <script type="text/javascript" src="https://cdn.jsdelivr.net/momentjs/latest/moment.min.js"></script>
    <script type="text/javascript" src="https://cdn.jsdelivr.net/npm/daterangepicker/daterangepicker.min.js"></script>
    <script></script>
    <!-- ============================================================== -->
    <!-- End Javascript Plugins Import -->
    <!-- ============================================================== -->
    <!-- ============================================================== -->
    <!-- Page Spesific Javascript -->
    <!-- ============================================================== -->
    @stack('page_scripts')
    <!-- ============================================================== -->
    <!-- End Page Spesific Javascript -->
    <!-- ============================================================== -->
</body>

</html>
