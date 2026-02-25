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
                                    <th>Action</th>
                                    <th>Kode</th>
                                    <th>Principal</th>
                                    <th>Departemen</th>
                                    <th>Nominal</th>
                                    <th>Limit</th>
                                    <th>Periode</th>
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
                        <div class="col-md-6">
                            @csrf
                            <div class="form-group">
                                <label>Kode</label>
                                <input type="text" v-model="kode" class="form-control-modal" maxlength="25"
                                    placeholder="Masukkan {{ $content->name }} (Max 25 Karakter)" required>
                            </div>
                            <div class="form-group">
                                <label>Principal</label>
                                <select2 :options="principal.data" v-model.sync="principal.id" required></select2>
                            </div>
                            <div class="form-group">
                                <label>Departemen</label>
                                <select2 :options="departemen.data" v-model.sync="departemen.id" required></select2>
                            </div>
                            <div class="form-group">
                                <label>Nominal</label>
                                <input type="text" v-model="nominal" value="" class="form-control-modal money"
                                    maxlength="13" placeholder="Masukkan Nominal {{ $content->name }}">
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="form-group">
                                <label>Limit</label>
                                <input type="text" v-model="limit" value="" class="form-control-modal money"
                                    maxlength="13" placeholder="Masukkan Limit {{ $content->name }}">
                            </div>
                            <div class="form-group">
                                <label>Keterangan</label>
                                <textarea v-model="keterangan" class="form-control-modal" maxlength="50"
                                    placeholder="Masukkan Keterangan {{ $content->name }} (Max 50 Karater)"></textarea>
                            </div>
                            <div class="form-group">
                                <label>Bulan</label>
                                <select2 :options="bulan.data" v-model.sync="bulan.id" required></select2>
                            </div>
                            <div class="form-group">
                                <label>Tahun</label>
                                <input type="number" v-model="tahun" value="" class="form-control-modal"
                                    maxlength="4" placeholder="Masukkan Periode Tahun {{ $content->name }}">
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
                        show: req("/getBudgetTable")
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
                                data: "actions",
                                orderable: false,
                                searchable: false
                            },
                            {
                                data: "kode",
                                orderable: true
                            },
                            {
                                data: "nama_principal",
                                orderable: true
                            },
                            {
                                data: "nama_departemen",
                                orderable: true
                            },
                            {
                                data: "nominal",
                                orderable: true,
                                render: function(data, type, row) {
                                    return formatRupiah(data);
                                }
                            },
                            {
                                data: "limit_nominal",
                                orderable: true,
                                render: function(data, type, row) {
                                    return formatRupiah(data);
                                }
                            },
                            {
                                data: "periode",
                                orderable: true,
                                render: function(data, type, row) {
                                    return formatPeriode(row.bulan, row.tahun);
                                }
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
                        show1: "/olah-principal/data/option",
                        show2: "/olah-departemen/data/option",
                        store: "/olah-kode-budget/insert",
                        edit: "/olah-kode-budget/update",
                        delete: "/olah-kode-budget/delete",
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
                    departemen: {
                        id: null,
                        data: []
                    },
                    bulan: {
                        id: null,
                        data: @json(nBulan())
                    },
                    id: '',
                    kode: '',
                    nominal: '',
                    limit: '',
                    keterangan: '',
                    tahun: '',
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
                resetData: function(data) {
                    this.principal.id = null;
                    this.departemen.id = null;
                    this.bulan.id = null;
                    this.kode = "";
                    this.nominal = "";
                    this.limit = "";
                    this.keterangan = "";
                    this.tahun = "";
                },
                /**
                 * Set Option Data.
                 * @todo Digunakan untuk Render Option
                 */
                setOption: function() {
                    let vm = this;
                    $.post(this.url.show1).done((data) => {
                        vm.principal.data = data;
                    });
                    $.post(this.url.show2).done((data) => {
                        vm.departemen.data = data;
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
                    this.principal.id = data.id_principal;
                    this.departemen.id = data.id_departemen;
                    this.bulan.id = data.bulan;
                    this.kode = data.kode;
                    this.nominal = floatToStr(data.nominal);
                    this.limit = floatToStr(data.limit_nominal);
                    this.keterangan = data.keterangan;
                    this.tahun = data.tahun;
                },
                /**
                 * Get Form Data.
                 *
                 * @todo Digunakan untuk Mendapatkan Data
                 *       yang Telah Diformat untuk Dikirim.
                 */
                getData: function(data) {
                    return {
                        idPrincipal: this.principal.id,
                        idDepartemen: this.departemen.id,
                        bulan: this.bulan.id,
                        kode: this.kode,
                        nominal: strToFloat(this.nominal),
                        limit: strToFloat(this.limit),
                        keterangan: this.keterangan,
                        tahun: this.tahun
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
@endpush
