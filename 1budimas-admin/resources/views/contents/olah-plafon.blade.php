@extends('layouts.main')
@section('content')
    @include('partials.breadcrumb')
    <!-- ============================================================== -->
    <!-- Content Container  -->
    <!-- ============================================================== -->
    <div class="container-fluid">
        <div class="row m-md-1">
            <div class="col-md-12">
                <div class="card form" id="app-list">
                    <div class="card-header">
                        <span class="card-title">Daftar {{ $content->name }}</span>
                    </div>
                    <div class="card-body card-bar-menu">
                        <div class="btn-group" role="group">
                            <button class="btn btn-success" type="button" @click="app_form.setModal(1);">
                                <i class="stroke-white-2 mdi mdi-plus"></i>Tambah
                            </button>
                            <a class="btn btn-primary" href="/olah-plafon/week">
                                <i class="mdi mdi-table-edit"></i>Lihat Week
                            </a>
                            <a class="btn btn-danger" href="/dashboard">
                                <i class="mdi mdi-step-backward"></i>Kembali
                            </a>
                        </div>
                    </div>
                    <div class="card-body">
                        <table class="table w-120">
                            <thead>
                            <tr>
                                <th>#</th>
                                <th>Actions</th>
                                <th>Kode</th>
                                <th>Sales</th>
                                <th>Customer</th>
                                <th>Principal</th>
                                <th>Limit</th>
                                <th>Sisa Bon</th>
                                <th>Tipe Harga</th>
                                <th>Jadwal</th>
                            </tr>
                            </thead>
                            <tbody>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- ============================================================== -->
    <!-- End Content Container  -->
    <!-- ============================================================== -->
    <!-- ============================================================== -->
    <!-- Modal Form  -->
    <!-- ============================================================== -->
 <div class="modal fade" id="app-form">
    <div class="modal-dialog modal-xl">
        <div class="modal-content">
            <div class="modal-header py-3">
                <h5 class="modal-title">@{{ modal.title }} {{ $content->name }}</h5>
                <button type="button" class="btn btn-sm btn-tool modal-close">
                    <i class="mdi mdi-close"></i>
                </button>
            </div>

            <div class="modal-load">
                <div class="lds-ripple">
                    <div class="lds-pos"></div>
                    <div class="lds-pos"></div>
                </div>
            </div>

            <div class="modal-body">
                <div class="form row">
                    <div class="col-md-12 border-right">
                        <h5 class="mb-3 text-primary"><i class="mdi mdi-wallet mr-2"></i>Data Plafon</h5>
                        <hr>
                        @csrf
                        
                        <div class="form-group">
                            <label>Kode Plafon</label>
                            <input type="text" v-model="kode" class="form-control-modal" readonly>
                        </div>

                        <div class="form-group">
                            <label>Customer</label>
                            <select2-serverside :url="customer.url" v-model="customer.id"
                                                @data-loaded="onCustomerDataLoaded" required>
                            </select2-serverside>
                        </div>

                        <div class="form-group">
                            <label>Sales</label>
                            <select2 :options="uniqueSales" v-model="sales.id_sales" @change="onSalesChange" required></select2>
                        </div>

                        <div class="form-group">
                            <label>Principal (Multiple)</label>
                            <select2 :options="filteredPrincipal" v-model="principal.id" multiple="multiple" required></select2>
                        </div>

                        <div class="row">
                            <div class="col-md-6">
                                <div class="form-group">
                                    <label>Limit Bon</label>
                                    <input type="number" v-model="limit" class="form-control-modal" placeholder="0" required>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="form-group">
                                    <label>TOP (Hari)</label>
                                    <input type="number" v-model="top" class="form-control-modal" placeholder="0" required>
                                </div>
                            </div>
                        </div>

                        <div class="row">
                            <div class="col-md-6">
                                <div class="form-group">
                                    <label>Tipe Harga</label>
                                    <select2 :options="tipeHarga.data" v-model="tipeHarga.id" required></select2>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="form-group">
                                    <label>Lock Order</label>
                                    <select2 :options="lockOrder.data" v-model="lockOrder.id" required></select2>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="modal-footer bg-light">
                <button type="button" class="btn btn-secondary px-4 modal-close">
                    <i class="mdi mdi-close"></i> Batal
                </button>
                <button class="btn btn-success px-5" type="button" @click="submit">
                    <i class="mdi mdi-check"></i> Simpan Data
                </button>
            </div>
        </div>
    </div>
</div>
    <!-- ============================================================== -->
    <!-- End Modal Form  -->
    <!-- ============================================================== -->
    <!-- ============================================================== -->
    <!-- Modal Jadwal  -->
    <!-- ============================================================== -->
    <div class="modal fade" id="app-jadwal">
        <div class="modal-dialog modal-xl">
            <div class="modal-content">
                <div class="modal-header py-3">
                    <h5 class="modal-title">Daftar Jadwal {{ $content->name }} @{{ kode }}</h5>
                    <button type="button" class="btn btn-sm btn-tool modal-close">
                        <i class="mdi mdi-close"></i>
                    </button>
                </div>
                <div class="modal-load">
                    <div class="lds-ripple">
                        <div class="lds-pos"></div>
                        <div class="lds-pos"></div>
                    </div>
                </div>
                <div class="modal-body">
                    <div class="form row">
                        <div class="col-md-6">
                            @csrf
                            <div class="form-group">
                                <label>Tipe Kunjungan</label>
                                <select2 :options="tipeKunjungan.data" v-model="tipeKunjungan.id" required></select2>
                            </div>
                            <div class="form-group">
                                <label>Minggu</label>
                                <select2 :options="minggu.data" v-model="minggu.id" required></select2>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="form-group">
                                <label>Hari</label>
                                <select2 :options="hari.data" v-model="hari.id" required></select2>
                            </div>
                            <div class="form-group">
                                <label>Status</label>
                                <select2 :options="status.data" v-model="status.id"></select2>
                            </div>
                        </div>
                        <div class="col-12">
                            <div class="form-group">
                                <div class="btn-group add" role="group">
                                    <button class="btn btn-success px-4" type="button" @click="submit">
                                        <i class="mdi mdi-plus"></i> Tambah
                                    </button>
                                </div>
                                <div class="btn-group edit" role="group">
                                    <button class="btn btn-danger cancel px-4" type="button">
                                        <i class="mdi mdi-close"></i> Batal Edit
                                    </button>
                                    <button class="btn btn-primary px-4" type="button" @click="submit">
                                        <i class="mdi mdi-pencil"></i> Edit
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-body border-top">
                    <table class="table">
                        <thead>
                        <tr>
                            <th>#</th>
                            <th>Action</th>
                            <th>Tipe Kunjungan</th>
                            <th>Hari</th>
                            <th>Minggu</th>
                            <th>Status</th>
                        </tr>
                        </thead>
                        <tbody>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
    <!-- ============================================================== -->
    <!-- End Modal Jadwal  -->
    <!-- ============================================================== -->
@endsection
@push('page_scripts')
    <script>
        /**
         * Tabel Data
         */
        var app_list = new Vue({
            el: '#app-list',
            data: function () {
                return {
                    // URL untuk Akses ke Resources.
                    url: {
                        show: req("/getPlafon")
                    },
                    // Instance Elemen.
                    table: () => $('#app-list').find('table'),
                    // Tabel Data.
                    data: {
                        columns: [{
                            data: "",
                            orderable: false,
                            searchable: false
                        },
                            {
                                data: 'actions',
                                orderable: false,
                                searchable: false
                            },
                            {
                                data: 'kode',
                                orderable: true
                            },
                            {
                                data: 'nama_user',
                                orderable: true
                            },
                            {
                                data: 'nama_customer',
                                orderable: true
                            },
                            {
                                data: 'nama_principal',
                                orderable: true
                            },
                            {
                                data: 'limit_bon',
                                orderable: true,
                                render: function (data, type, row) {
                                    return formatRupiah(data);
                                }
                            },
                            {
                                data: 'sisa_bon',
                                orderable: true,
                                render: function (data, type, row) {
                                    return formatRupiah(data);
                                }
                            },
                            {
                                data: 'tipe_harga',
                                orderable: true
                            },
                            {
                                data: 'detail_jadwal',
                                orderable: false,
                                searchable: false
                            }
                        ]
                    }
                }
            },
            methods: {
                /**
                 * Inisialisasi DataTable
                 */
                renderTable: function () {
                    const table = Table1()
                        .set(this.table())
                        .debounce()
                        .destroy()
                        .paging()
                        .rowNumber(true)
                        .setDefaultOrder(2, 'asc')
                        .serverSide(this.data.columns, this.url.show);

                    table.init();


                    return table;
                }
            },
            mounted: function () {
                this.renderTable();

                // Event listener untuk tombol edit dan delete
                this.table().on('click', '.btn-edit', (e) => {
                    e.preventDefault();
                    const row = $(e.currentTarget).closest('tr');
                    const rowData = this.table().DataTable().row(row)
                        .data();
                    app_form.setModal(2, rowData);
                });

                this.table().on('click', '.btn-delete', (e) => {
                    e.preventDefault();
                    const row = $(e.currentTarget).closest('tr');
                    const rowData = this.table().DataTable().row(row)
                        .data();
                    app_form.delete(rowData.id);
                });
                this.table().on('click', '.btn-detail', (e) => {
                    e.preventDefault();
                    const row = $(e.currentTarget).closest('tr');
                    const rowData = this.table().DataTable().row(row)
                        .data();
                    app_jadwal.show(rowData);
                });
            }
        });
    </script>
    <script>
        /**
         * Modal Form Add & Edit Data
         */
        var app_form = new Vue({
            el: '#app-form',
            components: {
                'infinite-select': InfiniteSelect
            },
            data: function () {
                return {
                    url: {
                        show1: "/olah-user/data/option2",
                        show2: req("/getCustomerOpt"),
                        show3: "/olah-principal/data/option",
                        show4: "/olah-produk/tipe-harga/data/option",
                        show5: "/olah-sales/data/option",
                        show6: "/olah-sales/multiple-principal/data",
                        showCabang: "/olah-cabang/data/option",
                        store: "/olah-plafon/insert",
                        edit: "/olah-plafon/update",
                        delete: "/olah-plafon/delete",
                    },
                    form: () => {
                        return Form().set($('#app-form').find('.form.row'));
                    },
                    modal: {
                        id: '',
                        title: ''
                    },
                    sales: {
                        id: null,
                        id_user: null,
                        id_sales: null,
                        data: []
                    },
                    customer: {
                        id: null,
                        url: '/getCustomerOpt',
                        data: []
                    },
                    cabang: {
                        data: []
                    },
                    principal: {
                        id: [],
                        data: []
                    },
                    tipeHarga: {
                        id: null,
                        data: []
                    },
                    dataMultiplePrincipal: [],
                    lockOrder: {
                        id: null,
                        data: @json(nStatus())
                    },
                    jadwal: {
                    idTipeKunjungan: '',
                    idMinggu: '',
                    idHari: '',
                    idStatus: '1',
                    tipeKunjunganData: @json(nTipeKunjungan()),
                    mingguData: @json(nMinggu()),
                    hariData: @json(nHari()),
                    statusData: @json(nStatus())
                },
                    id: '',
                    kode: 'PL{{ time() . rand(100, 1000) }}',
                    limit: '',
                    originalLimit: 0,
                    originalSisaBon: 0,
                    top: '',
                }
            },
            computed: {
                // 1. Menghasilkan daftar Sales yang unik (Tanpa Duplikat)
                uniqueSales() {
                    let baseSales = this.sales.data || [];
                    
                    // Ambil data sales yang ada di multiple principal juga
                    const additionalSales = this.dataMultiplePrincipal.map(mp => {
                        return baseSales.find(s => s.id_sales === mp.id_sales);
                    }).filter(item => item != null);

                    const allSales = [...baseSales, ...additionalSales];

                    const map = new Map();
                    const result = [];
                    for (const item of allSales) {
                        if(!map.has(item.id_sales)){
                            map.set(item.id_sales, true);
                            result.push(item);
                        }
                    }
                    return result;
                },

                // 2. Filter Principal berdasarkan Sales yang dipilih
                filteredPrincipal() {
                    // Jika sales belum dipilih, tampilkan semua (atau kosongkan jika ingin lebih ketat)
                    if (!this.sales.id_sales) {
                        return this.principal.data; 
                    }

                    // Cari ID Principal dari master sales
                    const principalIdsFromMaster = this.sales.data
                        .filter(s => s.id_sales == this.sales.id_sales)
                        .map(s => s.id_principal);

                    // Cari ID Principal dari data multiple principal
                    const principalIdsFromMulti = this.dataMultiplePrincipal
                        .filter(mp => mp.id_sales == this.sales.id_sales)
                        .map(mp => mp.id_principal);

                    // Gabungkan dan hapus duplikat ID
                    const allowedIds = [...new Set([...principalIdsFromMaster, ...principalIdsFromMulti])];

                    // Kembalikan data principal yang sesuai dengan ID yang di-handle sales
                    return this.principal.data.filter(p => allowedIds.includes(p.id));
                },

                selectedCustomerCabang() {
                    if (!this.customer.id || !this.customer.data.length) return null;
                    const selectedCustomer = this.customer.data.find(c => c.id == this.customer.id);
                    if (!selectedCustomer || !selectedCustomer.id_cabang) return 'Tidak ada cabang';
                    const cabang = this.cabang.data.find(c => c.id == selectedCustomer.id_cabang);
                    return cabang ? cabang.text : 'Tidak ada cabang';
                },

                selectedSalesCabang() {
                    if (!this.sales.id_sales || !this.sales.data.length) return null;
                    const selectedSales = this.sales.data.find(s => s.id_sales == this.sales.id_sales);
                    if (!selectedSales || !selectedSales.id_cabang) return 'Tidak ada cabang';
                    const cabang = this.cabang.data.find(c => c.id == selectedSales.id_cabang);
                    return cabang ? cabang.text : 'Tidak ada cabang';
                },
            },
            watch: {
                // Otomatisasi saat customer dipilih
                'customer.id': function (newVal) {
                    if (!newVal) {
                        this.principal.id = []; // Reset ke array kosong
                        return;
                    }
                    const selectedCustomer = this.customer.data.find(c => c.id == newVal);
                    if (selectedCustomer && selectedCustomer.id_principal) {
                        // UBAH: Masukkan ke dalam array jika hanya satu dari customer
                        this.principal.id = [selectedCustomer.id_principal];
                        
                        if (selectedCustomer.id_tipe_harga) {
                            this.tipeHarga.id = selectedCustomer.id_tipe_harga;
                        }
                    }
                },
                // Pastikan id_user selalu sinkron dengan sales terpilih
                'sales.id_sales': function (newVal) {
                    const selectedSales = this.sales.data.find(s => s.id_sales == newVal);
                    if (selectedSales) {
                        this.sales.id_user = selectedSales.id_user;
                    }
                }
            },
            methods: {
                loading: function (opsi) {
                    if (opsi == 1) $('#app-form .modal-load').show();
                    else $('#app-form .modal-load').hide();
                },

                // TRIGER UTAMA: Saat Sales diubah
                onSalesChange: function () {
                    // UBAH: Reset ke array kosong saat sales ganti
                    this.principal.id = [];

                    const selectedSales = this.sales.data.find(s => s.id_sales == this.sales.id_sales);
                    if (selectedSales) {
                        this.sales.id_user = selectedSales.id_user;
                    }
                },

                onCustomerDataLoaded: function (data) {
                    if (data && data.length > 0) {
                        data.forEach(newCustomer => {
                            const existingIndex = this.customer.data.findIndex(c => c.id == newCustomer.id);
                            if (existingIndex >= 0) {
                                this.$set(this.customer.data, existingIndex, newCustomer);
                            } else {
                                this.customer.data.push(newCustomer);
                            }
                        });
                    }
                },

                validateCabang: function () {
                    if (!this.sales.id_sales || !this.customer.id) {
                        Alert().notice('error', 'Validasi Error', 'Sales dan Customer harus dipilih!');
                        return false;
                    }
                    const selectedSales = this.sales.data.find(s => s.id_sales == this.sales.id_sales);
                    const selectedCustomer = this.customer.data.find(c => c.id == this.customer.id);

                    if (!selectedSales || selectedSales.id_cabang != selectedCustomer.id_cabang) {
                        Alert().notice('error', 'Validasi Error', 'Sales dan Customer harus dalam cabang yang sama!');
                        return false;
                    }
                    return true;
                },

                resetData: function () {
                    this.id = "";
                    this.sales.id_sales = "";
                    this.sales.id_user = "";
                    this.customer.id = null;
                    this.customer.data = [];
                    this.principal.id = [];
                    this.tipeHarga.id = "";
                    this.lockOrder.id = "";
                    this.kode = "PL" + new Date().getTime() + Math.floor(Math.random() * 1000);
                    this.limit = "";
                    this.top = "";
                    this.originalLimit = 0;
                    this.originalSisaBon = 0;

                    this.jadwal.idTipeKunjungan = "";
                    this.jadwal.idMinggu = "";
                    this.jadwal.idHari = "";
                    this.jadwal.idStatus = "1";
                },

                setData: function (data) {
                    this.id = data.id;
                    this.sales.id_sales = data.id_sales;
                    this.sales.id_user = data.id_user;
                    this.customer.id = data.id_customer;
                    
                    // UBAH: Jika data dari server berupa string (misal: "1,2,3"), pecah jadi array
                    if (typeof data.id_principal === 'string') {
                        this.principal.id = data.id_principal.split(',');
                    } else {
                        this.principal.id = Array.isArray(data.id_principal) ? data.id_principal : [data.id_principal];
                    }

                    this.tipeHarga.id = data.id_tipe_harga;
                    this.lockOrder.id = data.lock_order;
                    this.kode = data.kode;
                    this.limit = floatToStr(data.limit_bon);
                    this.top = data.top;
                    this.originalLimit = parseFloat(data.limit_bon) || 0;
                    this.originalSisaBon = parseFloat(data.sisa_bon) || 0;
                },

                setOption: function () {
                    let vm = this;
                    $.post(this.url.show5).done((data) => {
                        vm.sales.data = data.map(item => ({
                            id_sales: item.id_sales,
                            id: item.id_sales,
                            text: item.text,
                            id_user: item.id_user,
                            id_cabang: item.id_cabang,
                            id_principal: item.id_principal
                        }));
                    });
                    $.post(this.url.showCabang).done((data) => { vm.cabang.data = data; });
                    $.post(this.url.show3).done((data) => { vm.principal.data = data; });
                    $.post(this.url.show4).done((data) => { vm.tipeHarga.data = data; });
                    $.post(this.url.show6).done((data) => { vm.dataMultiplePrincipal = data; });
                },

                getData: function () {
                    let sisaBonBaru = (this.modal.id == 2) 
                        ? (this.originalSisaBon + (strToFloat(this.limit) - this.originalLimit))
                        : strToFloat(this.limit);

                    return {
                        idSales: this.sales.id_sales,
                        idUser: this.sales.id_user,
                        idCustomer: this.customer.id,
                        // Pastikan ini dikirim sebagai string gabungan
                        idPrincipal: Array.isArray(this.principal.id) ? this.principal.id.join(',') : this.principal.id,
                        idTipeHarga: this.tipeHarga.id,
                        lockOrder: this.lockOrder.id,
                        kode: this.kode,
                        limit: strToFloat(this.limit),
                        sisaBon: sisaBonBaru,
                        top: this.top,
                        jadwal: {
                            idTipeKunjungan: this.jadwal.idTipeKunjungan,
                            idMinggu: this.jadwal.idMinggu,
                            idHari: this.jadwal.idHari,
                            idStatus: this.jadwal.idStatus
                        }
                    };
                },

                setModal: function (type, data = null) {
                    this.loading(1);
                    this.form().validate(0);
                    if (type == 1) {
                        this.modal.id = 1; this.modal.title = 'Tambah'; this.resetData();
                    } else {
                        this.modal.id = 2; this.modal.title = 'Edit'; this.setData(data);
                    }
                    this.loading(0);
                    $('#app-form').modal('show');
                },

                submit: function () {
                    if (!this.validateCabang()) return;

                    this.form().validate(1).confirm().then((result) => {
                        if (!result.value) return;

                        block(1);
                        $('#app-form').modal('hide');

                        const targetUrl = this.modal.id === 1 ? this.url.store : this.url.edit;

                        // Pastikan id_principal selalu array
                        const principalIds = Array.isArray(this.principal.id) 
                            ? this.principal.id 
                            : [this.principal.id];

                        // Siapkan payload
                        const payload = {
                            _token: $('meta[name="csrf-token"]').attr('content'),
                            id: this.id ?? null,
                            kode: this.kode ?? null,
                            id_customer: this.customer?.id ?? null,
                            id_sales: this.sales?.id_sales ?? null,
                            id_principal: principalIds,
                            id_tipe_harga: this.tipeHarga?.id ?? null,
                            lock_order: Number(this.lockOrder?.id) || 0,
                            limit: Number(this.limit) || 0,
                            top: Number(this.top) || 0,
                            jadwal: {
                                id_tipe_kunjungan: Number(this.jadwal?.idTipeKunjungan) || 0,
                                id_hari: Number(this.jadwal?.idHari) || 0,
                                id_minggu: Number(this.jadwal?.idMinggu) || 0,
                            },
                        };

                        $.post(targetUrl, payload)
                            .done((res) => {
                                block(0);

                                // update table & alert
                                app_list.renderTable();

                                if (this.modal.id === 1) {
                                    Alert().success1();
                                } else {
                                    Alert().success2();
                                }
                            })
                            .fail((err) => {
                                block(0);
                                console.error("Response Error:", err.responseJSON);
                                Alert().error();
                            });
                    });
                },


                delete: function (id) {
                    Alert().delete().then((result) => {
                        if (result.value) {
                            block(1);
                            $.post(this.url.delete, { id: id }).done(() => {
                                app_list.renderTable();
                                block(0);
                                Alert().success3();
                            }).fail(() => { block(0); Alert().error(); });
                        }
                    });
                },
            },
            mounted: function () {
                this.setOption();
                $('#app-form').on('hidden.bs.modal', () => {
                    if (this.$refs.customerSelect) {
                        this.$refs.customerSelect.reset();
                        this.customer.id = null;
                    }
                });
            }
        });
        </script>
    <script>
        /**
         * Modal Plafon Jadwal
         */
        var app_jadwal = new Vue({
            el: '#app-jadwal',
            data: function () {
                return {
                    // URL untuk Akses ke Resources.
                    url: {
                        show: "/olah-plafon/jadwal/data/table",
                        store: "/olah-plafon/jadwal/insert",
                        edit: "/olah-plafon/jadwal/update",
                        delete: "/olah-plafon/jadwal/delete",
                    },
                    // Instance Elemen.
                    table: () => {
                        return Table().set($('#app-jadwal').find('table'));
                    },
                    rowData: (el) => {
                        return this.table().getRowData(el.closest('tr'));
                    },
                    form: () => {
                        return Form().set($('#app-jadwal').find('.form.row'));
                    },
                    // Tabel Data.
                    data: {
                        columns: [{
                            data: ""
                        },
                            {
                                data: "actions"
                            },
                            {
                                data: "e_tipe_kunjungan"
                            },
                            {
                                data: "e_hari"
                            },
                            {
                                data: "e_minggu"
                            },
                            {
                                data: "e_status"
                            },
                        ]
                    },
                    modal: {
                        id: ''
                    },
                    hari: {
                        id: '',
                        data: @json(nHari())
                    },
                    tipeKunjungan: {
                        id: '',
                        data: @json(nTipeKunjungan())
                    },
                    minggu: {
                        id: '',
                        data: @json(nMinggu())
                    },
                    status: {
                        id: '1',
                        data: @json(nStatus())
                    },
                    id: '',
                    idPlafon: '',
                    kode: '',
                }
            },
            methods: {
                /**
                 * Memperlihatkan Animasi Loading.
                 * @param opsi 1 : aktif | 0 : mati.
                 */
                loading: function (opsi) {
                    if (opsi == 1) {
                        $('#app-jadwal .modal-load').show();
                    } else if (opsi == 0) {
                        $('#app-jadwal .modal-load').hide();
                    }
                },
                /**
                 * Render Tabel dengan Data.
                 * Inisiasi Kembali Datatable Instance dengan
                 * Data Baru.
                 *
                 * @param filter Filter Data yang Akan
                 *               Dirender oleh Tabel.
                 */
                renderTable: function (filter = null) {
                    if (!isNull(this.idPlafon)) {
                        filter = {
                            idPlafon: this.idPlafon
                        };
                    }

                    this.table().destroy().paging().rowNumber().scrollY('350')
                        .serverSide(this.data.columns, this.url.show, filter)
                        .throw().init();
                },
                /**
                 * reset Data pada Form.
                 */
                resetData: function () {
                    this.tipeKunjungan.id = "";
                    this.minggu.id = "";
                    this.hari.id = "";
                    this.status.id = "1";
                },
                /**
                 * Set Form Data.
                 *
                 * @todo Digunakan untuk Render Data
                 *       saat Membuka Edit Form.
                 */
                setData: function (data) {
                    this.id = data.id
                    this.tipeKunjungan.id = data.id_tipe_kunjungan;
                    this.minggu.id = data.id_minggu;
                    this.hari.id = data.id_hari;
                    this.status.id = data.id_status;
                },
                /**
                 * Get Form Data.
                 *
                 * @todo Digunakan untuk Mendapatkan Data
                 *       yang Telah Diformat untuk Dikirim.
                 */
                getData: function () {
                    return {
                        idTipeKunjungan: this.tipeKunjungan.id,
                        idMinggu: this.minggu.id,
                        idHari: this.hari.id,
                        idStatus: this.status.id,
                        idPlafon: this.idPlafon,
                    };
                },
                /**
                 * Show Modal dan Intial Render Table Action.
                 */
                show: function (data) {
                    if (!isNull(data)) {
                        this.idPlafon = data.id;
                        this.kode = data.kode;
                    }

                    this.renderTable();
                    this.setModal(1);
                    $("#app-jadwal").modal('show');
                },
                /**
                 * Modal Handler.
                 * Render Modal dan Set Form Data Berdasarkan
                 * Tipe yang Dipilih.
                 *
                 * @param type 1 : Tambah | 2 : Edit.
                 * @param data yang Diambil dari RowData pada
                 *             Tabel. Digunakan untuk Set Data
                 *             pada Form Edit.
                 */
                setModal: function (type, data = null) {
                    this.loading(1);
                    this.form().validate(0);

                    switch (type) {
                        case 1: // Set Form Tambah
                            this.modal.id = 1;
                            this.form().el.find(".btn-group.edit").hide();
                            this.form().el.find(".btn-group.add").show();
                            this.resetData();
                            break;
                        case 2: // Set Form Edit
                            this.modal.id = 2;
                            this.form().el.find(".btn-group.edit").show();
                            this.form().el.find(".btn-group.add").hide();
                            this.form().el.find("input, select, textarea").focus();
                            this.setData(data);
                            break;
                    }

                    this.loading(0);
                },
                /**
                 * Form Submit Handler.
                 * Submit Form Berdasarkan Tipe Form dari `modal.id`.
                 * `modal.id` => 1 : Tambah | 2 : Edit.
                 */
                submit: function () {
                    this.form().validate(0).validate(1).confirm()
                        .then((result) => {
                            if (result.value == true) {
                                // Before Submitting Actions.
                                this.loading(1);

                                // Submitting Form Tambah.
                                if (this.modal.id == 1) {
                                    $.post(this.url.store, this.getData())
                                        .done(() => {
                                            this.renderTable();
                                            this.setModal(1);
                                            Alert().success1();
                                        })
                                        .fail(() => {
                                            this.renderTable();
                                            this.setModal(1);
                                            Alert().error();
                                        });

                                    // Submitting Form Edit.
                                } else if (this.modal.id == 2) {
                                    $.post(this.url.edit, {
                                        ...this.getData(),
                                        id: this.id
                                    })
                                        .done(() => {
                                            this.renderTable();
                                            this.setModal(1);
                                            Alert().success2();
                                        })
                                        .fail(() => {
                                            this.renderTable();
                                            this.setModal(1);
                                            Alert().error();
                                        });
                                }
                            } else {
                                Alert().cancel();
                            }
                        });
                },
                delete: function (id) {
                    Alert().delete().then((result) => {
                        if (result.value == true) {
                            // Before Submitting Actions.
                            this.loading(1);

                            // Submitting Delete Action.
                            $.post(this.url.delete, {
                                id: id
                            })
                                .done(() => {
                                    this.renderTable();
                                    this.loading(0);
                                    Alert().success3();
                                })
                                .fail(() => {
                                    this.renderTable();
                                    this.loading(0);
                                    Alert().error();
                                });

                        } else {
                            Alert().cancel();
                        }
                    });
                }
            },
            mounted: function () {
                let vm = this;
                this.loading(0);

                /**
                 * Handler Modal Form untuk Button Batal Edit.
                 */
                this.form().el.on('click', '.btn.cancel', function () {
                    vm.setModal(1);
                });
                /**
                 * Handler Modal Form untuk Button Edit.
                 */
                this.table().el.on('click', '.btn-edit', function () {
                    vm.setModal(2, vm.rowData($(this)));
                });
                /**
                 * Handler Button Delete.
                 */
                this.table().el.on('click', '.btn-delete', function () {
                    vm.delete($(this).val());
                });
            }
        });
    </script>
@endpush