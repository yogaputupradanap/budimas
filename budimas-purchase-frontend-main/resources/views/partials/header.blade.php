<header class="topbar" data-navbarbg="skin5">
    <nav class="navbar top-navbar navbar-expand-md navbar-dark">
        <div class="navbar-header" data-logobg="skin5">
            <!-- ============================================================== -->
            <!-- Logo -->
            <!-- ============================================================== -->
            <a class="navbar-brand" href="javascript:void(0)">
                <!-- Logo icon -->
                <span class="logo-icon ps-2"> 
                    <img src="{{ asset('assets-panel/assets/images/logo-budimas.png') }}" alt="homepage" class="light-logo" width="30" />
                </span>
                <!-- Logo text -->
                <span class="logo-text ms-2"> 
                    <img src="{{ asset('assets-panel/assets/images/logo-text-budimas.png') }}" alt="homepage" class="light-logo w-100" />
                </span>
            </a>
            <!-- ============================================================== -->
            <!-- End Logo -->
            <!-- ============================================================== -->
            <!-- ============================================================== -->
            <!-- Mobile Toggle -->
            <!-- ============================================================== -->
            <a class="nav-toggler waves-effect waves-light d-block d-md-none" href="javascript:void(0)">
                <i class="mdi mdi-dots-horizontal font-24"></i>
            </a>
            <!-- ============================================================== -->
            <!-- End Mobile Toggle -->
            <!-- ============================================================== -->
        </div>
        <!-- ============================================================== -->
        <!-- Toggle and Navbar Items -->
        <!-- ============================================================== -->
        <div class="navbar-collapse collapse" id="navbarSupportedContent" data-navbarbg="skin5">
            <!-- ============================================================== -->
            <!-- Left Side -->
            <!-- ============================================================== -->
            <ul class="navbar-nav float-start me-auto">
                <!-- Sidebar Toggle -->
                <li class="nav-item d-none d-lg-block">
                    <a class="nav-link sidebartoggler waves-effect waves-light" href="javascript:void(0)" data-sidebartype="mini-sidebar"><i class="mdi mdi-menu font-24"></i></a>
                </li>
                <!-- Module/Fiture Name -->
                <li class="nav-item display dropdown">
                    <div class="nav-link font-14 text-info" href="javascript:void(0)">
                        <span class="mx-1">
                            <i class="mdi mdi-clock stroke-info-text"></i>
                            <span id="timer" class="mx-1 stroke-info-text"></span>
                        </span>
                        <!-- <span class="mx-1">
                            <span class="mx-1 stroke-info-text">Purchase</span>
                        </span> -->
                    </div>
                </li>
            </ul>
            <!-- ============================================================== -->
            <!-- End Left Side -->
            <!-- ============================================================== -->
            <!-- ============================================================== -->
            <!-- Right Side -->
            <!-- ============================================================== -->
            <ul class="navbar-nav float-end">
                <!-- User Info -->
                <li class="nav-item display dropdown">
                    <div class="nav-link font-14 text-info" href="javascript:void(0)">
                        <span class="mx-1" title="User">
                            <i class="mdi mdi-account"></i>
                            <span class="mx-1 stroke-info-text">{{ user()->nama }}</span>
                        </span>
                        <span class="mx-1" title="Jabatan">
                            <i class="mdi mdi-tag"></i>
                            <span class="mx-1 stroke-info-text">{{ user()->nama_jabatan }}</span>
                        </span>
                        <span class="mx-1" title="Cabang">
                            <i class="mdi mdi-store"></i>
                            <span class="mx-1 stroke-info-text">{{ user()->nama_cabang }}</span> 
                        </span>
                    </div>
                </li>
                <!-- ============================================================== -->
                <!-- User Edit Profile and Notifications -->
                <!-- ============================================================== -->
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle waves-effect waves-dark" href="#" id="2" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                        <img src="{{ asset('assets-panel/assets/images/users/1.jpg') }}" alt="user" class="rounded-circle" width="31"/>
                    </a>
                    <ul class="dropdown-menu dropdown-menu-end mailbox animated bounceInDown "aria-labelledby="2">
                        <ul class="list-style-none">
                            <li>
                                <!-- User Profile -->
                                <a href="/profile" class="link border-top">
                                    <div class="d-flex no-block align-items-center p-10 mx-3">
                                        <span class="btn btn-info pills d-flex align-items-center justify-content-center">
                                            <i class="mdi mdi-account fs-4"></i>
                                        </span>
                                        <div class="ms-3">
                                            <h5 class="mb-0 font-normal">Profile</h5>
                                        </div>
                                    </div>
                                </a>
                                <a href="{{ route('logout') }}" class="link border-top" onclick="logoutConfirmation(event, this)">
                                    <div class="d-flex no-block align-items-center p-10 mx-3">
                                        <span class="btn btn-danger pills d-flex align-items-center justify-content-center">
                                            <i class="mdi mdi-power text-white fs-4"></i>
                                        </span>
                                        <div class="ms-3">
                                            <h5 class="mb-0 font-normal">Logout</h5>
                                        </div>
                                    </div>
                                </a>
                            </li>
                        </ul>
                    </ul>
                </li>
                <!-- ============================================================== -->
                <!-- End User Edit Profile and Notifications -->
                <!-- ============================================================== -->
            </ul>
        </div>
        <!-- ============================================================== -->
        <!-- End Toggle and Navbar Items -->
        <!-- ============================================================== -->
    </nav>
</header>