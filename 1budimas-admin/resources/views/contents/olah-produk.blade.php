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
                        <span class="card-title">Daftar <em>{{ $content->name }}</em></span>
                    </div>
                    <div class="card-body card-bar-menu">
                        <div class="btn-group" role="group">
                            <a href="{{ route('olah-produk.create') }}" class="btn btn-success">
                                <i class="stroke-white-2 mdi mdi-plus"></i>Tambah
                            </a>
                            <a class="btn btn-primary" href="/olah-produk/brand">
                                <i class="mdi mdi-table-edit"></i>Lihat Brand
                            </a>
                            <a class="btn btn-primary" href="/olah-produk/kategori">
                                <i class="mdi mdi-table-edit"></i>Lihat Kategori
                            </a>
                            <a class="btn btn-primary" href="/olah-produk/tipe-harga">
                                <i class="mdi mdi-table-edit"></i>Lihat Tipe Harga
                            </a>
                            <a class="btn btn-danger" href="{{ route('dashboard.index') }}">
                                <i class="mdi mdi-step-backward"></i>Kembali
                            </a>
                        </div>
                    </div>
                    <div class="card-body">
                        <table class="table w-150">
                            <thead>
                                <tr>
                                    <th>#</th>
                                    <th>Action</th>
                                    <th>Nama</th>
                                    <th>Kode SKU</th>
                                    <th>Kode EAN</th>
                                    <th>Principal</th>
                                    <th>Brand</th>
                                    <th>Kategori</th>
                                    <th>Status</th>
                                    <th>PPN</th>
                                    <th>Harga Beli*</th>
                                    <th>Harga Jual*</th>
                                    <th>Satuan</th>
                                </tr>
                            </thead>
                            <tbody>
                            </tbody>
                        </table>
                    </div>
                    <div class="card-body border-top">
                        <div class="form row m-0">
                            <div class="col-md-12">
                                <div class="form-group px-0 mt-1 mb-0">
                                    <label><em>*) Harga Beli dan Harga Jual yang Tersimpan adalah dari Satuan yang
                                            Terbesar</em></label>
                                </div>
                            </div>
                        </div>
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
                        <div class="col-md-6">
                            @csrf
                            <div class="form-group">
                                <label>Principal</label>
                                <select2 :options="principal.data" v-model.sync="principal.id" required></select2>
                            </div>
                            <div class="form-group">
                                <label>Brand</label>
                                <select2 :options="brand.data" v-model="brand.id"></select2>
                            </div>
                            <div class="form-group">
                                <label>Kategori</label>
                                <select2 :options="kategori.data" v-model.sync="kategori.id"></select2>
                            </div>
                            <div class="form-group">
                                <label>Kode SKU</label>
                                <input type="text" v-model="kodeSku" class="form-control-modal" maxlength="25"
                                    placeholder="Masukkan Kode SKU {{ $content->name }} (Max 25 Karakter)">
                            </div>
                            <div class="form-group">
                                <label>Kode EAN</label>
                                <input type="text" v-model="kodeEan" class="form-control-modal" maxlength="25"
                                    placeholder="Masukkan Kode EAN {{ $content->name }} (Max 25 Karakter)">
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="form-group">
                                <label>Nama</label>
                                <input type="text" v-model="nama" class="form-control-modal" maxlength="50"
                                    placeholder="Masukkan Nama {{ $content->name }} (Max 50 Karakter)" required>
                            </div>
                            <div class="form-group">
                                <label>Harga Beli</label>
                                <input type="text" v-model="hargaBeli" class="form-control-modal money"
                                    placeholder="Masukkan Harga Beli {{ $content->name }}">
                            </div>
                            <div class="form-group">
                                <label>Status</label>
                                <select2 :options="status.data" v-model.sync="status.id" required></select2>
                            </div>
                            <div class="form-group">
                                <label>PPN</label>
                                <input type="number" v-model="ppn" class="form-control-modal" maxlength="3"
                                    placeholder="Masukkan PPN {{ $content->name }} (Max 3 Karakter)">
                            </div>
                            <div class="form-group">
                                <label>Deskripsi</label>
                                <textarea class="form-control-modal" v-model="keterangan" maxlength="50"
                                    placeholder="Masukkan Deskripsi {{ $content->name }} (Max 50 Karater)"></textarea>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-body border-top">
                    <div class="btn-group float-end mx-md-4" role="group">
                        <button class="btn btn-success px-4" type="button" @click="submit">
                            <i class="mdi mdi-check"></i> Submit
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- ============================================================== -->
    <!-- End Modal Form  -->
    <!-- ============================================================== -->
    <!-- ============================================================== -->
    <!-- Modal Harga Jual  -->
    <!-- ============================================================== -->
    <div class="modal fade" id="app-harga">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header py-3">
                    <h5 class="modal-title">Daftar Harga Jual {{ $content->name }} @{{ kodeSku }}</h5>
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
                        <div class="col-6">
                            @csrf
                            <div class="form-group">
                                <label>Tipe Harga</label>
                                <select2 :options="tipeHarga.data" v-model="tipeHarga.id" required></select2>
                            </div>
                        </div>
                        <div class="col-6">
                            <div class="form-group">
                                <label>Harga</label>
                                <input type="text" v-model="harga" class="form-control-modal money"
                                    placeholder="Masukkan Harga Jual {{ $content->name }}" required>
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
                                <th>Harga</th>
                                <th>Tipe Harga</th>
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
    <!-- End Modal Harga Jual  -->
    <!-- ============================================================== -->
    <!-- ============================================================== -->
    <!-- Modal Satuan -->
    <!-- ============================================================== -->
    <div class="modal fade" id="app-satuan">
        <div class="modal-dialog modal-xl">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Detail Satuan <em>Produk</em></h5>
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
                <div class="modal-body border-bottom">
                    <div class="form-sm row">
                        <div class="col-md-3">
                            <div class="form-group">
                                <label>Kode SKU <em>Produk</em></label>
                                <input type="text" v-model="kodeSku" class="form-control-modal"
                                    placeholder="Max 50 Karakter" readonly>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="form-group">
                                <label>Kode EAN <em>Produk</em></label>
                                <input type="text" v-model="kodeEan" class="form-control-modal"
                                    placeholder="Max 50 Karakter" readonly>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="form-group">
                                <label>Nama <em>Produk</em></label>
                                <input type="text" v-model="namaProduk" class="form-control-modal"
                                    placeholder="Max 50 Karakter" readonly>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-body border-bottom">
                    <div class="form-sm row">
                        <div class="col-md-3">
                            <div class="form-group">
                                <label>Kode <em>Satuan</em></label>
                                <input type="text" v-model="kode" class="form-control-modal"
                                    placeholder="Masukkan Kode Satuan {{ $content->name }}" required>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="form-group">
                                <label>Nama <em>Satuan</em></label>
                                <input type="text" v-model="nama" class="form-control-modal"
                                    placeholder="Max 50 Karakter" required>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="form-group">
                                <label>Level <em>Satuan</em></label>
                                <select2 :readonly="level.readonly" :options="level.data" v-model="level.id" required>
                                </select2>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="form-group">
                                <label>Faktor Konversi</label>
                                <input type="number" v-model="faktorKonversi" class="form-control-modal"
                                    placeholder="Masukkan Berat Kotor {{ $content->name }}" required
                                    :readonly="inputFaktorKonversi">
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-body border-bottom">
                    <div class="form-sm row">
                        <div class="col-md-3">
                            <div class="form-group">
                                <label>Satuan <em>Packing</em></label>
                                <input type="text" v-model="packingSatuan" class="form-control-modal"
                                    placeholder="Masukkan Satuan Packing {{ $content->name }} e.g. Meter">
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="form-group">
                                <label>Panjang <em>Packing</em></label>
                                <input type="number" v-model="packingPanjang" class="form-control-modal"
                                    placeholder="Masukkan Panjang Packing {{ $content->name }}">
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="form-group">
                                <label>Tinggi <em>Packing</em></label>
                                <input type="number" v-model="packingTinggi" class="form-control-modal"
                                    placeholder="Masukkan Tinggi Packing {{ $content->name }}">
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="form-group">
                                <label>Lebar <em>Packing</em></label>
                                <input type="number" v-model="packingLebar" class="form-control-modal"
                                    placeholder="Masukkan Lebar Packing {{ $content->name }}">
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-body border-bottom">
                    <div class="form-sm row">
                        <div class="col-md-3">
                            <div class="form-group">
                                <label>Satuan <em>Berat</em></label>
                                <input type="text" v-model="beratSatuan" class="form-control-modal"
                                    placeholder="Masukkan Satuan Berat {{ $content->name }}">
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="form-group">
                                <label><em>Berat</em> Bersih</label>
                                <input type="number" v-model="beratBersih" class="form-control-modal"
                                    placeholder="Masukkan Berat Bersih {{ $content->name }}">
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="form-group">
                                <label><em>Berat</em> Kotor</label>
                                <input type="number" v-model="beratKotor" class="form-control-modal"
                                    placeholder="Masukkan Berat Kotor {{ $content->name }}">
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-body">
                    <div class="form-sm row">
                        <div class="col-md-8">
                            <div class="form-group px-0 mt-md-2">
                                <label><em>*) Faktor Konversi adalah Jumlah Produk Jika Dikonversi ke dalam Satuan
                                        Terkecil</em></label>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="form-group float-end">
                                <div class="btn-group add " role="group">
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
                                <th>Kode</th>
                                <th>Nama</th>
                                <th>Level</th>
                                <th>Faktor Konversi</th>
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
    <!-- End Modal Satuan -->
    <!-- ============================================================== -->
@endsection
@push('page_scripts')
    <script>
        /**
         * Tabel Data
         */
        var app_list = new Vue({
            el: '#app-list',
            data: function() {
                return {
                    // URL untuk Akses ke Resources.
                    url: {
                        show: req("/getProdukTable")
                    },
                    // Instance Elemen.
                    table: () => $('#app-list').find('table'),
                    data: {
                        columns: [{
                                data: "",
                                orderable: false
                            },
                            {
                                data: "actions",
                                orderable: false,
                                searchable: false
                            },
                            {
                                data: "nama",
                                orderable: true
                            },
                            {
                                data: "kode_sku",
                                orderable: true
                            },
                            {
                                data: "kode_ean",
                                orderable: true
                            },
                            {
                                data: "nama_principal",
                                orderable: true
                            },
                            {
                                data: "brand",
                                orderable: true
                            },
                            {
                                data: "kategori",
                                orderable: true
                            },
                            {
                                data: "id_status",
                                orderable: true,
                                render: function(data, type, row) {
                                    return data == 1 ?
                                        '<span class="btn btn-sm btn-info pills def-point">Aktif</span>' :
                                        '<span class="btn btn-sm btn-danger pills def-point text-nowrap">Non Aktif</span>';
                                }
                            },
                            {
                                data: "ppn",
                                orderable: true,
                                render: function(data, type, row) {
                                    // Memastikan angka valid
                                    if (data === null || data === undefined) {
                                        return '0%';
                                    }
                                    // Mengubah ke format angka dengan 0 desimal
                                    return data.toFixed(0) + '%';
                                }
                            },
                            {
                                data: "harga_beli",
                                orderable: true,
                                render: function(data, type, row) {
                                    return formatRupiah(data);
                                }
                            },
                            {
                                data: "harga",
                                orderable: false,
                                searchable: false
                            },
                            {
                                data: "satuan",
                                orderable: false,
                                searchable: false
                            },
                        ]
                    }
                }
            },
            methods: {
                /**
                 * Inisialisasi DataTable
                 */
                renderTable: function() {
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
            mounted: function() {
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

                this.table().on('click', '.btn-detail-harga', (e) => {
                    e.preventDefault();
                    const row = $(e.currentTarget).closest('tr');
                    const rowData = this.table().DataTable().row(row)
                        .data();
                    app_harga.show(rowData);
                });

                this.table().on('click', '.btn-detail-satuan', (e) => {
                    e.preventDefault();
                    const row = $(e.currentTarget).closest('tr');
                    const rowData = this.table().DataTable().row(row)
                        .data();
                    app_satuan.show(rowData);
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
            data: function() {
                return {
                    // URL untuk Akses ke Resources.
                    url: {
                        show1: "/olah-produk/brand/data/option",
                        show2: "/olah-produk/kategori/data/option",
                        show3: "/olah-principal/data/option",
                        store: "/olah-produk/insert",
                        edit: "/olah-produk/update",
                        delete: "/olah-produk/delete",
                    },
                    // Instance Elemen.
                    form: () => {
                        return Form().set($('#app-form').find('.form.row'));
                    },
                    // Form Data.
                    modal: {
                        id: '',
                        title: ''
                    },
                    principal: {
                        id: null,
                        data: []
                    },
                    brand: {
                        id: null,
                        data: []
                    },
                    kategori: {
                        id: null,
                        data: []
                    },
                    status: {
                        id: null,
                        data: @json(nStatus())
                    },
                    ppn: '',
                    id: '',
                    kodeSku: '',
                    kodeEan: '',
                    nama: '',
                    hargaBeli: '',
                    keterangan: '',
                }
            },
            methods: {
                /**
                 * Memperlihatkan Animasi Loading.
                 * @param opsi 1 : aktif | 0 : mati.
                 */
                loading: function(opsi) {
                    if (opsi == 1) {
                        $('#app-form .modal-load').show();
                    } else if (opsi == 0) {
                        $('#app-form .modal-load').hide();
                    }
                },
                /**
                 * reset Data pada Form.
                 */
                resetData: function() {
                    this.principal.id = null;
                    this.brand.id = null;
                    this.kategori.id = null;
                    this.status.id = "1";
                    this.ppn = 11;
                    this.kodeSku = "";
                    this.kodeEan = "";
                    this.nama = "";
                    this.hargaBeli = "";
                    this.keterangan = "";
                },
                /**
                 * Set Option Data.
                 * @todo Digunakan untuk Render Option
                 */
                setOption: function() {
                    let vm = this;
                    $.post(this.url.show1).done((data) => {
                        vm.brand.data = data;
                    });
                    $.post(this.url.show2).done((data) => {
                        vm.kategori.data = data;
                    });
                    $.post(this.url.show3).done((data) => {
                        vm.principal.data = data;
                    });
                },
                /**
                 * Set Form Data.
                 *
                 * @todo Digunakan untuk Render Data
                 *       saat Membuka Edit Form.
                 */
                setData: function(data) {
                    this.id = data.id
                    this.principal.id = data.id_principal;
                    this.brand.id = data.id_brand;
                    this.kategori.id = data.id_kategori;
                    this.status.id = data.id_status;
                    this.ppn = data.ppn;
                    this.kodeSku = data.kode_sku;
                    this.kodeEan = data.kode_ean;
                    this.nama = data.nama;
                    this.hargaBeli = floatToStr(data.harga_beli);
                    this.keterangan = data.keterangan;



                },
                /**
                 * Get Form Data.
                 *
                 * @todo Digunakan untuk Mendapatkan Data
                 *       yang Telah Diformat untuk Dikirim.
                 */
                getData: function() {
                    return {
                        idPrincipal: this.principal.id,
                        idBrand: this.brand.id,
                        idKategori: this.kategori.id,
                        idStatus: this.status.id,
                        ppn: this.ppn,
                        kodeSku: this.kodeSku,
                        kodeEan: this.kodeEan,
                        nama: this.nama,
                        hargaBeli: strToFloat(this.hargaBeli),
                        keterangan: this.keterangan
                    };
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
                setModal: function(type, data = null) {
                    this.loading(1);
                    this.form().validate(0);

                    switch (type) {
                        case 1: // Set Form Tambah
                            this.modal.id = 1;
                            this.modal.title = 'Tambah';
                            this.resetData();
                            break;
                        case 2: // Set Form Edit
                            this.modal.id = 2;
                            this.modal.title = 'Edit';
                            this.setData(data);
                            break;
                    }

                    this.loading(0);
                    $('#app-form').modal('show');
                },
                /**
                 * Form Submit Handler.
                 * Submit Form Berdasarkan Tipe Form dari `modal.id`.
                 * `modal.id` => 1 : Tambah | 2 : Edit.
                 */
                submit: function() {
                    this.form().validate(0).validate(1).confirm()
                        .then((result) => {
                            if (result.value == true) {
                                // Before Submitting Actions.
                                block(1);
                                $('#app-form').modal('hide');

                                // Submitting Form Tambah.
                                if (this.modal.id == 1) {
                                    $.post(this.url.store, this.getData())
                                        .done(() => {
                                            app_list.renderTable();
                                            block(0);
                                            Alert().success1();
                                        })
                                        .fail(() => {
                                            app_list.renderTable();
                                            block(0);
                                            Alert().error();
                                        });

                                    // Submitting Form Edit.
                                } else if (this.modal.id == 2) {
                                    $.post(this.url.edit, {
                                            ...this.getData(),
                                            id: this.id
                                        })
                                        .done(() => {
                                            app_list.renderTable();
                                            block(0);
                                            Alert().success2();
                                        })
                                        .fail(() => {
                                            app_list.renderTable();
                                            block(0);
                                            Alert().error();
                                        });
                                }
                            } else {
                                Alert().cancel();
                            }
                        });
                },
                delete: function(id) {
                    Alert().delete().then((result) => {
                        if (result.value == true) {
                            // Before Submitting Actions.
                            block(1);

                            // Submitting Delete Action.
                            $.post(this.url.delete, {
                                    id: id
                                })
                                .done(() => {
                                    app_list.renderTable();
                                    block(0);
                                    Alert().success3();
                                })
                                .fail(() => {
                                    app_list.renderTable();
                                    block(0);
                                    Alert().error();
                                });

                        } else {
                            Alert().cancel();
                        }
                    });
                }
            },
            mounted: function() {
                this.setOption();
            }
        });
    </script>
    <script>
        /**
         * Modal Produk Harga Jual
         */
        var app_harga = new Vue({
            el: '#app-harga',
            data: function() {
                return {
                    // URL untuk Akses ke Resources.
                    url: {
                        show: "/olah-produk/harga/data/table",
                        show2: "/olah-produk/tipe-harga/data/option",
                        store: "/olah-produk/harga/insert",
                        edit: "/olah-produk/harga/update",
                        delete: "/olah-produk/harga/delete",
                    },
                    // Instance Elemen.
                    table: () => {
                        return Table().set($('#app-harga').find('table'));
                    },
                    rowData: (el) => {
                        return this.table().getRowData(el.closest('tr'));
                    },
                    form: () => {
                        return Form().set($('#app-harga').find('.form.row'));
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
                                data: "e_harga"
                            },
                            {
                                data: "tipe_harga"
                            }
                        ]
                    },
                    modal: {
                        id: ''
                    },
                    tipeHarga: {
                        id: '',
                        data: []
                    },
                    kodeSku: '',
                    id: '',
                    idProduk: '',
                    harga: '',
                }
            },
            methods: {
                /**
                 * Memperlihatkan Animasi Loading.
                 * @param opsi 1 : aktif | 0 : mati.
                 */
                loading: function(opsi) {
                    if (opsi == 1) {
                        $('#app-harga .modal-load').show();
                    } else if (opsi == 0) {
                        $('#app-harga .modal-load').hide();
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
                renderTable: function(filter = null) {
                    if (!isNull(this.idProduk)) {
                        filter = {
                            idProduk: this.idProduk
                        };
                    }

                    this.table().destroy().paging().rowNumber()
                        .serverSide(this.data.columns, this.url.show, filter)
                        .throw().init();
                },
                /**
                 * reset Data pada Form.
                 */
                resetData: function() {
                    this.harga = "";
                    this.tipeHarga.id = "";
                },
                /**
                 * Set Option Data.
                 * @todo Digunakan untuk Render Option
                 */
                setOption: function() {
                    let vm = this;
                    $.post(this.url.show2).done((data) => {
                        vm.tipeHarga.data = data
                    });
                },
                /**
                 * Set Form Data.
                 *
                 * @todo Digunakan untuk Render Data
                 *       saat Membuka Edit Form.
                 */
                setData: function(data) {
                    this.id = data.id;
                    this.harga = floatToStr(data.harga);
                    this.tipeHarga.id = data.id_tipe_harga;
                },
                /**
                 * Get Form Data.
                 *
                 * @todo Digunakan untuk Mendapatkan Data
                 *       yang Telah Diformat untuk Dikirim.
                 */
                getData: function() {
                    return {
                        idProduk: this.idProduk,
                        idTipeHarga: this.tipeHarga.id,
                        harga: strToFloat(this.harga),

                    };
                },
                /**
                 * Show Modal dan Intial Render Table Action.
                 */
                show: function(data) {
                    if (!isNull(data)) {
                        this.idProduk = data.id;
                        this.kodeSku = data.kode_sku;
                    }

                    this.renderTable();
                    this.setModal(1);
                    $("#app-harga").modal('show');
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
                setModal: function(type, data = null) {
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
                submit: function() {
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
                                            this.loading(0);
                                            Alert().success1();
                                        })
                                        .fail(() => {
                                            this.renderTable();
                                            this.loading(0);
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
                                            this.loading(0);
                                            Alert().success2();
                                        })
                                        .fail(() => {
                                            this.renderTable();
                                            this.loading(0);
                                            Alert().error();
                                        });
                                }
                            } else {
                                Alert().cancel();
                            }
                        });
                },
                delete: function(id) {
                    Alert().delete().then((result) => {
                        if (result.value == true) {
                            // Before Submitting Actions.
                            this.loading(1);

                            // Submitting Delete Action.
                            $.post(this.url.delete, {
                                    id: id
                                })
                                .done((response) => {
                                    console.log("Delete response:",
                                        response); // Log the server response
                                    if (response.success) {
                                        this.renderTable();
                                        Alert().success3();
                                    } else {
                                        Alert().error();
                                    }
                                    this.loading(0);
                                })
                                .fail((error) => {
                                    console.log("Delete error:", error); // Log the error response
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
            mounted: function() {
                let vm = this;
                this.setOption();
                this.loading(0);

                /**
                 * Handler Modal Form untuk Button Batal Edit.
                 */
                this.form().el.on('click', '.btn.cancel', function() {
                    vm.setModal(1);
                });
                /**
                 * Handler Modal Form untuk Button Edit.
                 */
                this.table().el.on('click', '.btn-edit', function() {
                    vm.setModal(2, vm.rowData($(this)));
                });
                /**
                 * Handler Button Delete.
                 */
                this.table().el.on('click', '.btn-delete', function() {
                    vm.delete($(this).val());
                });
            }
        });
    </script>
    <script>
        /**
         * Modal Produk Satuan
         */
        var app_satuan = new Vue({
            el: '#app-satuan',
            data: function() {
                return {
                    // URL untuk Akses ke Resources.
                    url: {
                        show: "/olah-produk/satuan/data/table",
                        store: "/olah-produk/satuan/insert",
                        edit: "/olah-produk/satuan/update",
                        delete: "/olah-produk/satuan/delete",
                    },
                    // Instance Elemen.
                    table: () => {
                        return Table().set($('#app-satuan').find('table'));
                    },
                    rowData: (el) => {
                        return this.table().getRowData(el.closest('tr'));
                    },
                    form: () => {
                        return Form().set($('#app-satuan').find('.form-sm.row'));
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
                                data: "kode"
                            },
                            {
                                data: "nama"
                            },
                            {
                                data: "level"
                            },
                            {
                                data: "faktor_konversi"
                            },
                        ]
                    },
                    modal: {
                        id: ''
                    },
                    level: {
                        id: '',
                        data: @json(nLevelSatuan()),
                        readonly: false
                    },
                    id: '',
                    idProduk: '',
                    kodeSku: '',
                    kodeEan: '',
                    namaProduk: '',
                    kode: '',
                    nama: '',
                    beratSatuan: '',
                    beratBersih: '',
                    beratKotor: '',
                    packingSatuan: '',
                    packingPanjang: '',
                    packingTinggi: '',
                    packingLebar: '',
                    faktorKonversi: '',
                    inputFaktorKonversi: false,
                }
            },
            methods: {
                /**
                 * Memperlihatkan Animasi Loading.
                 * @param opsi 1 : aktif | 0 : mati.
                 */
                loading: function(opsi) {
                    if (opsi == 1) {
                        $('#app-satuan .modal-load').show();
                    } else if (opsi == 0) {
                        $('#app-satuan .modal-load').hide();
                    }
                },
                /**
                 * Mengunci Faktor Konversi untuk Data dengan Level 1.
                 * Saat dikunci Input Faktor Konversi akan Menjadi Readonly.
                 */
                levelDataHandler: function() {
                    // Mengubah Nilai dari Faktor Konversi.
                    this.faktorKonversi = this.level.id == 1 ? 1 :
                        this.modal.id == 1 ? "" : this.faktorKonversi;

                    // Setting Atribut Readonly dari Input Faktor Konversi.
                    this.inputFaktorKonversi = this.level.id == 1 ? true : false;
                },
                /**
                 * Submit Cheker untuk Form.
                 * Form tidak boleh menginput data level yang sama.
                 */
                submitChecker: function() {
                    let exist = this.table().getRowsData().find(data => data.level == this.level.id);
                    return exist;
                },
                /**
                 * Render Tabel dengan Data.
                 * Inisiasi Kembali Datatable Instance dengan
                 * Data Baru.
                 *
                 * @param filter Filter Data yang Akan
                 *               Dirender oleh Tabel.
                 */
                renderTable: function(filter = null) {
                    if (!isNull(this.idProduk)) {
                        filter = {
                            idProduk: this.idProduk
                        };
                    }

                    this.table().destroy().paging().rowNumber().scrollY(250)
                        .serverSide(this.data.columns, this.url.show, filter)
                        .throw().init();
                },
                /**
                 * reset Data pada Form.
                 */
                resetData: function() {
                    this.kode = "";
                    this.nama = "";
                    this.level.id = "";
                    this.beratSatuan = "";
                    this.beratBersih = "";
                    this.beratKotor = "";
                    this.packingSatuan = "";
                    this.packingPanjang = "";
                    this.packingTinggi = "";
                    this.packingLebar = "";
                    this.faktorKonversi = "";
                },
                /**
                 * Set Form Data.
                 *
                 * @todo Digunakan untuk Render Data
                 *       saat Membuka Edit Form.
                 */
                setData: function(data) {
                    this.id = data.id;
                    this.kode = data.kode;
                    this.nama = data.nama;
                    this.level.id = data.level;
                    this.beratSatuan = data.berat_satuan;
                    this.beratBersih = data.berat_bersih;
                    this.beratKotor = data.berat_kotor;
                    this.packingSatuan = data.packing_satuan;
                    this.packingPanjang = data.packing_panjang;
                    this.packingTinggi = data.packing_tinggi;
                    this.packingLebar = data.packing_lebar;
                    this.faktorKonversi = data.faktor_konversi;
                },
                /**
                 * Get Form Data.
                 *
                 * @todo Digunakan untuk Mendapatkan Data
                 *       yang Telah Diformat untuk Dikirim.
                 */
                getData: function() {
                    return {
                        idProduk: this.idProduk,
                        kode: this.kode,
                        nama: this.nama,
                        level: this.level.id,
                        beratSatuan: this.beratSatuan,
                        beratBersih: this.beratBersih,
                        beratKotor: this.beratKotor,
                        packingSatuan: this.packingSatuan,
                        packingPanjang: this.packingPanjang,
                        packingTinggi: this.packingTinggi,
                        packingLebar: this.packingLebar,
                        faktorKonversi: this.faktorKonversi,
                    };
                },
                /**
                 * Show Modal dan Intial Render Table Action.
                 */
                show: function(data) {
                    if (!isNull(data)) {
                        this.idProduk = data.id;
                        this.kodeSku = data.kode_sku;
                        this.kodeEan = data.kode_ean;
                        this.namaProduk = data.nama;
                    }

                    this.renderTable();
                    this.setModal(1);
                    $("#app-satuan").modal('show');
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
                setModal: function(type, data = null) {
                    this.loading(1);
                    this.form().validate(0);

                    switch (type) {
                        case 1: // Set Form Tambah
                            this.modal.id = 1;
                            this.level.readonly = false;
                            this.form().el.find(".btn-group.edit").hide();
                            this.form().el.find(".btn-group.add").show();
                            this.resetData();
                            break;
                        case 2: // Set Form Edit
                            this.modal.id = 2;
                            this.level.readonly = true;
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
                submit: function() {
                    this.form().validate(0).validate(1).confirm()
                        .then((result) => {
                            if (result.value == true) {
                                // Before Submitting Actions.
                                this.loading(1);

                                // Submitting Form Tambah.
                                if (this.modal.id == 1) {
                                    if (!this.submitChecker()) {
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
                                    } else {
                                        Alert().exist2();
                                        this.setModal(1);
                                    }

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
                delete: function(id) {
                    console.log("Deleting data with ID:", id);
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
            mounted: function() {
                let vm = this;
                this.loading(0);

                /**
                 * Handler Modal Form untuk Button Batal Edit.
                 */
                this.form().el.on('click', '.btn.cancel', function() {
                    vm.setModal(1);
                });
                /**
                 * Handler Modal Form untuk Button Edit.
                 */
                this.table().el.on('click', '.btn-edit', function() {
                    vm.setModal(2, vm.rowData($(this)));
                });
                /**
                 * Handler Button Delete.
                 */
                this.table().el.on('click', '.btn-delete', function() {
                    vm.delete($(this).val());
                });
            },
            watch: {
                'level.id': function(value) {
                    this.levelDataHandler();
                }
            }
        });
    </script>
@endpush
