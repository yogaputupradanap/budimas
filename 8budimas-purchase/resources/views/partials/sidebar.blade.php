<aside class="left-sidebar" data-sidebarbg="skin5">
    <!-- Sidebar scroll-->
    <div class="scroll-sidebar">
        <!-- Sidebar navigation-->
        <nav class="sidebar-nav">
            <ul id="sidebarnav" class="pt-4">
                <li class="sidebar-item">
                    <a class="sidebar-link waves-effect waves-dark sidebar-link" href="{{ route('dashboard.index') }}" aria-expanded="false"><i class="mdi mdi-view-dashboard"></i><span class="hide-menu mx-2">Dashboard</span></a>
                </li>
                <li class="sidebar-item">
                    <a class="sidebar-link waves-effect waves-dark sidebar-link" href="{{ route('purchase-order.create') }}" aria-expanded="false"><i class="mdi mdi-file-document"></i><span class="hide-menu mx-2">Request Order</span></a>
                </li>
                <li class="sidebar-item">
                    <a class="sidebar-link waves-effect waves-dark sidebar-link" href="{{ route('konfirmasi-order.index') }}" aria-expanded="false"><i class="mdi mdi-file-check"></i><span class="hide-menu mx-2">Konf. Order</span></a>
                </li>
                <li class="sidebar-item">
                    <a class="sidebar-link waves-effect waves-dark sidebar-link" href="{{ route('penerimaan-barang.index') }}" aria-expanded="false"><i class="mdi mdi-clipboard-text"></i><span class="hide-menu mx-2">Penerimaan Barang</span></a>
                </li>
                <li class="sidebar-item">
                    <a class="sidebar-link waves-effect waves-dark sidebar-link" href="{{ route('transaksi-konfirmasi.index') }}" aria-expanded="false"><i class="mdi mdi-clipboard-check"></i><span class="hide-menu mx-2">Konf. Purchase</span></a>
                </li>
                {{-- <li class="sidebar-item">
                    <a class="sidebar-link waves-effect waves-dark sidebar-link" href="{{ route('transaksi-tagihan.index') }}" aria-expanded="false"><i class="mdi mdi-credit-card"></i><span class="hide-menu mx-2">Pembuatan Tagihan</span></a>
                </li>
                <li class="sidebar-item">
                    <a class="sidebar-link waves-effect waves-dark sidebar-link" href="{{ route('transaksi-pembayaran.index') }}" aria-expanded="false"><i class="mdi mdi-cash-multiple"></i><span class="hide-menu mx-2">Pembayaran</span></a>
                </li> --}}
                <li class="sidebar-item">
                    <a class="sidebar-link waves-effect waves-dark sidebar-link" href="{{ route('laporan-order') }}" aria-expanded="false"><i class="mdi mdi-book-open"></i><span class="hide-menu mx-2">Laporan</span></a>
                </li> 
                {{-- <li class="sidebar-item">
                    <a class="sidebar-link waves-effect waves-dark sidebar-link" href="{{ route('laporan-purchase') }}" aria-expanded="false"><i class="mdi mdi-book-open"></i><span class="hide-menu mx-2"><em>Lap.</em> Purchase</span></a>
                </li> --}}
                <li class="sidebar-item">
                    <a class="sidebar-link waves-effect waves-dark sidebar-link logout" href="{{ route('logout') }}" aria-expanded="false" onclick="logoutConfirmation(event, this)"><i class="mdi mdi-logout"></i><span class="hide-menu mx-2">Log Out</span></a>
                </li>
            </ul>
        </nav>
        <!-- End Sidebar navigation -->
    </div>
    <!-- End Sidebar scroll-->
</aside>