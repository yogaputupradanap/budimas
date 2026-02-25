<!DOCTYPE html>
<html dir="ltr" lang="{{ str_replace('_', '-', app()->getLocale()) }}">

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
    <link rel="stylesheet" href="{{ asset('assets-panel/assets/libs/bootstrap/dist/css/bootstrap.min.css') }}">
    <!-- Custom CSS -->
    <link rel="stylesheet" href="{{ asset('assets-panel/dist/css/style.min.css') }}">
    <link rel="stylesheet" href="{{ asset('assets-panel/dist/css/custom.css') }}">
</head>

<body>
    <!-- ============================================================== -->
    <!-- Session Data -->
    <!-- ============================================================== -->
    @if (session()->has('status'))
        <input type="hidden" id="alert-status" value="{{ session('status') }}">
    @endif
    <!-- ============================================================== -->
    <!-- End Session Data -->
    <!-- ============================================================== -->
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
    <!-- End Preloader -->
    <!-- ============================================================== -->
    <!-- ============================================================== -->
    <!-- Main wrapper - style you can find in pages.scss -->
    <!-- ============================================================== -->
    <div class="main-wrapper">
        <div class="card-fullscreen d-flex no-block justify-content-center align-items-center bg-custom">
            <div class="bg-custom login-box">
                <div>
                    <!-- ============================================================== -->
                    <!-- Header Logo -->
                    <!-- ============================================================== -->
                    <div class="text-center">
                        <span class="db">
                            <img src="{{ asset('assets-panel/assets/images/logo-budimas.png') }}" alt="logo">
                        </span>
                        <h4 class="pt-5 pb-3">Login</h4>
                    </div>
                    <!-- ============================================================== -->
                    <!-- End Header Logo -->
                    <!-- ============================================================== -->
                    <div class="row">
                        <!-- ============================================================== -->
                        <!-- Login Form -->
                        <!-- ============================================================== -->
                        <form class="form-horizontal col-12" method="POST" action="{{ route('login.proses') }}">
                            @csrf
                            <div class="alert alert-danger alert-dismissible d-none" role="alert" id="login-alert">
                                Username atau password salah.
                                <button type="button" class="btn-close" style="padding: 16px" data-bs-dismiss="alert"
                                    aria-label="Close"></button>
                            </div>
                            <div class="row pb-2">
                                <div class="col-12">
                                    <div class="input-group">
                                        <div class="form-group w-100">
                                            <label>Username</label>
                                            <input type="text" name="username"
                                                class="form-control-modal login required"
                                                placeholder="Masukkan Username Akun" required>
                                        </div>
                                    </div>
                                    <div class="input-group">
                                        <div class="form-group w-100">
                                            <label>Password</label>
                                            <input type="password" name="password"
                                                class="form-control-modal login required"
                                                placeholder="Masukkan Password Akun" required>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-12">
                                    <hr>
                                    <div class="form-group">
                                        <div class="pt-3">
                                            <button type="submit" class="btn btn-c-primary btn-lg w-100">
                                                Login
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </form>
                        <!-- ============================================================== -->
                        <!-- End Login Form -->
                        <!-- ============================================================== -->
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- ============================================================== -->
    <!-- End Wrapper -->
    <!-- ============================================================== -->
    <!-- ============================================================== -->
    <!-- All Required js -->
    <!-- ============================================================== -->
    <script src="{{ asset('assets-panel/assets/libs/jquery/dist/jquery.min.js') }}"></script>
    <!-- Bootstrap tether Core JavaScript -->
    <script src="{{ asset('assets-panel/assets/libs/bootstrap/dist/js/bootstrap.bundle.min.js') }}"></script>

    <!-- ============================================================== -->
    <!-- This page plugin js -->
    <!-- ============================================================== -->
    <script>
        $(document).ready(function() {
            $(".preloader").fadeOut();

            // Tampilkan alert jika status login gagal
            var alertStatus = $('#alert-status').val();
            if (alertStatus == 0) {
                $('#login-alert').removeClass('d-none');
            }
        });
    </script>
</body>

</html>
