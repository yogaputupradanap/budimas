<aside class="left-sidebar" data-sidebarbg="skin5">
    <!-- Sidebar scroll-->
    <div class="scroll-sidebar">
        <!-- Sidebar navigation-->
        <nav class="sidebar-nav">
            <ul id="sidebarnav" class="pt-4">
                <li class="sidebar-item">
                    <a class="sidebar-link waves-effect waves-dark sidebar-link" href="{{ route('dashboard.index') }}" aria-expanded="false"><i class="mdi mdi-view-dashboard"></i><span class="hide-menu mx-2">Dashboard</span></a>
                </li>
            @php $x = userFitur(); @endphp
            @if (fitur($x, 111))
                <li class="sidebar-item">
                    <a class="sidebar-link waves-effect waves-dark sidebar-link" href="/olah-armada" aria-expanded="false"><i class="mdi mdi-truck"></i><span class="hide-menu mx-2">Olah Armada</span></a>
                </li>
            @endif
            @if (fitur($x, 102))
                <li class="sidebar-item">
                    <a class="sidebar-link waves-effect waves-dark sidebar-link" href="/olah-cabang" aria-expanded="false"><i class="mdi mdi-source-branch"></i><span class="hide-menu mx-2">Olah Cabang</span></a>
                </li>
            @endif
            @if (fitur($x, 106))
                <li class="sidebar-item">
                    <a class="sidebar-link waves-effect waves-dark sidebar-link" href="/olah-customer" aria-expanded="false"><i class="mdi mdi-store"></i><span class="hide-menu mx-2">Olah Customer</span></a>
                </li>
            @endif
            @if (fitur($x, 114))
                <li class="sidebar-item">
                    <a class="sidebar-link waves-effect waves-dark sidebar-link" href="/olah-data/import" aria-expanded="false"><i class="mdi mdi-file"></i><span class="hide-menu mx-2">Operasi Data</span></a>
                </li>
            @endif
            @if (fitur($x, 110))
                <li class="sidebar-item">
                    <a class="sidebar-link waves-effect waves-dark sidebar-link" href="/olah-driver" aria-expanded="false"><i class="mdi mdi-account-settings"></i><span class="hide-menu mx-2">Olah Driver</span></a>
                </li>
            @endif
            @if (fitur($x, 113))
                <li class="sidebar-item">
                    <a class="sidebar-link waves-effect waves-dark sidebar-link" href="/olah-fitur/jabatan" aria-expanded="false"><i class="mdi mdi-apps"></i><span class="hide-menu mx-2">Olah Fitur Default</span></a>
                </li>
            @endif
            @if (fitur($x, 109))
                <li class="sidebar-item">
                    <a class="sidebar-link waves-effect waves-dark sidebar-link" href="/olah-kode-budget" aria-expanded="false"><i class="mdi mdi-cube-unfolded"></i><span class="hide-menu mx-2">Olah Budget</span></a>
                </li>
            @endif
            @if (fitur($x, 103))
                <li class="sidebar-item">
                    <a class="sidebar-link waves-effect waves-dark sidebar-link" href="/olah-perusahaan" aria-expanded="false"><i class="mdi mdi-home-modern"></i><span class="hide-menu mx-2">Olah Perusahaan</span></a>
                </li>
            @endif
            @if (fitur($x, 107))
                <li class="sidebar-item">
                    <a class="sidebar-link waves-effect waves-dark sidebar-link" href="/olah-plafon" aria-expanded="false"><i class="mdi mdi-sitemap"></i><span class="hide-menu mx-2">Olah Plafon</span></a>
                </li>
            @endif
            @if (fitur($x, 108))
                <li class="sidebar-item">
                    <a class="sidebar-link waves-effect waves-dark sidebar-link" href="/olah-produk" aria-expanded="false"><i class="mdi mdi-hamburger"></i><span class="hide-menu mx-2">Olah Produk</span></a>
                </li>
            @endif
            @if (fitur($x, 105))
                <li class="sidebar-item">
                    <a class="sidebar-link waves-effect waves-dark sidebar-link" href="/olah-principal" aria-expanded="false"><i class="mdi mdi-pillar"></i><span class="hide-menu mx-2">Olah Principal</span></a>
                </li>
            @endif
            @if (fitur($x, 112))
                <li class="sidebar-item">
                    <a class="sidebar-link waves-effect waves-dark sidebar-link" href="/olah-rute" aria-expanded="false"><i class="mdi mdi-google-maps"></i><span class="hide-menu mx-2">Olah Rute</span></a>
                </li>
            @endif
            @if (fitur($x, 104))
                <li class="sidebar-item">
                    <a class="sidebar-link waves-effect waves-dark sidebar-link" href="/olah-sales" aria-expanded="false"><i class="mdi mdi-account-switch"></i><span class="hide-menu mx-2">Olah Sales</span></a>
                </li>
            @endif
            @if (fitur($x, 101))
                <li class="sidebar-item">
                    <a class="sidebar-link waves-effect waves-dark sidebar-link" href="/olah-user" aria-expanded="false"><i class="mdi mdi-folder-account"></i><span class="hide-menu mx-2">Olah User</span></a>
                </li>
            @endif
            @if (fitur($x, 115))
                <li class="sidebar-item">
                    <a class="sidebar-link waves-effect waves-dark sidebar-link" href="/olah-periode-close" aria-expanded="false"><i class="mdi mdi-calendar-blank"></i><span class="hide-menu mx-2">Olah Periode Close</span></a>
                </li>
            @endif
                <li class="sidebar-item">
                    <a class="sidebar-link waves-effect waves-dark sidebar-link logout" href="{{ route('logout') }}" aria-expanded="false" onclick="logoutConfirmation(event, this)"><i class="mdi mdi-logout"></i><span class="hide-menu mx-2">Log Out</span></a>
                </li>
            </ul>
        </nav>
        <!-- End Sidebar navigation -->
    </div>
    <!-- End Sidebar scroll-->
</aside>
