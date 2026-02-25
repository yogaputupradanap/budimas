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
                            <a class="btn btn-primary" href="/olah-armada/tipe">
                                <i class="mdi mdi-table-edit"></i>Lihat Tipe
                            </a>
                            <a class="btn btn-danger" href="/dashboard">
                                <i class="mdi mdi-step-backward"></i>Kembali
                            </a>
                        </div>
                    </div>
                    <div class="card-body">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th>#</th>
                                    <th>Actions</th>
                                    <th>Kendaraan</th>
                                    <th>Cabang</th>
                                    <th>Tipe</th>
                                    <th>CBM</th>
                                    <th>Exp. STNK</th>
                                    <th>Exp. Uji</th>
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
                                <label>Nama</label>
                                <input type="text" v-model="nama" class="form-control-modal" maxlength="50"
                                    placeholder="Masukkan Nama {{ $content->name }} (Max 50 Karakter)" required>
                            </div>
                            <div class="form-group">
                                <label>Cabang</label>
                                <select2 :options="cabang.data" v-model="cabang.id" required></select2>
                            </div>
                            <div class="form-group">
                                <label>Tipe</label>
                                <select2 :options="tipe.data" v-model="tipe.id" required></select2>
                            </div>
                            <div class="form-group">
                                <label>Status</label>
                                <select2 :options="status.data" v-model="status.id" required></select2>
                            </div>
                            <div class="form-group">
                                <label>Pelat Nomor</label>
                                <input type="text" v-model="noPelat" class="form-control-modal" maxlength="11"
                                    placeholder="Masukkan Pelat Nomor {{ $content->name }} (Max 11 Karakter)"
                                    style="text-transform: uppercase;" required>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="form-group">
                                <label>Tanggal Expired STNK</label>
                                <datepicker v-model="tanggalStnk"
                                    placeholder="Masukkan Tanggal Expired STNK {{ $content->name }} (yyyy-mm-dd)">
                                </datepicker>
                            </div>
                            <div class="form-group">
                                <label>Tanggal Expired Uji</label>
                                <datepicker v-model="tanggalUji"
                                    placeholder="Masukkan Tanggal Expired Uji {{ $content->name }} (yyyy-mm-dd)">
                                </datepicker>
                            </div>
                            <div class="form-group">
                                <label>CBM</label>
                                <input type="number" v-model="kubikasi" class="form-control-modal"
                                    placeholder="Masukkan CBM (Kubikas/Volume) {{ $content->name }}" required>
                            </div>
                            <div class="form-group">
                                <label>Keterangan</label>
                                <textarea v-model="keterangan" class="form-control-modal" maxlength="25"
                                    placeholder="Masukkan Keterangan {{ $content->name }} (Max 25 Karater)"></textarea>
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
    <script src="{{ asset('assets-panel/dist/js/pages/vue-apps/option-wilayah.vue') }}"></script>
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
                        show: req('/getArmadaTable')
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
                                data: "nama",
                                orderable: true,
                                render: function(data, type, row) {
                                    return row.nama + '<br><small class="text-primary">' + row
                                        .no_pelat + '</small>'
                                }
                            },
                            {
                                data: "nama_cabang",
                                orderable: true,
                                render: function(data, type, row) {
                                    return renderBadges(data);
                                }
                            },
                            {
                                data: "tipe",
                                orderable: true
                            },
                            {
                                data: "kubikasi",
                                orderable: true
                            },
                            {
                                data: "tanggal_stnk",
                                orderable: true,
                                render: function(data, type, row) {
                                    return formatDate(data);
                                }
                            },
                            {
                                data: "tanggal_uji",
                                orderable: true,
                                render: function(data, type, row) {
                                    return formatDate(data);
                                }
                            },
                            {
                                data: "id_status",
                                orderable: true,
                                render: function(data, type, row) {
                                    return data == 1 ?
                                        '<span class="btn btn-sm btn-info pills def-point">Aktif</span>' :
                                        '<span class="btn btn-sm btn-danger pills def-point text-nowrap">Non Aktif</span>';
                                }
                            }
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
                        show1: "/olah-cabang/data/option",
                        show2: "/olah-armada/tipe/data/option",
                        store: "/olah-armada/insert",
                        edit: "/olah-armada/update",
                        delete: "/olah-armada/delete",
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
                    cabang: {
                        id: null,
                        data: []
                    },
                    tipe: {
                        id: null,
                        data: []
                    },
                    status: {
                        id: 1,
                        data: @json(nStatus())
                    },
                    id: '',
                    nama: '',
                    noPelat: '',
                    tanggalStnk: '',
                    tanggalUji: '',
                    kubikasi: '',
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
                resetData: function(data) {
                    this.nama = "";
                    this.cabang.id = null;
                    this.tipe.id = "";
                    this.status.id = "1";
                    this.noPelat = "";
                    this.tanggalStnk = "";
                    this.tanggalUji = "";
                    this.kubikasi = "";
                    this.keterangan = "";
                },
                /**
                 * Set Form Data.
                 *
                 * @todo Digunakan untuk Render Data
                 *       saat Membuka Edit Form.
                 */
                setData: function(data) {
                    this.id = data.id;
                    this.cabang.id = data.id_cabang;
                    this.tipe.id = data.id_tipe;
                    this.status.id = data.id_status;
                    this.nama = data.nama;
                    this.noPelat = data.no_pelat;
                    this.tanggalStnk = formatDate(data.tanggal_stnk);
                    this.tanggalUji = formatDate(data.tanggal_uji);
                    this.kubikasi = data.kubikasi;
                    this.keterangan = data.keterangan;
                },
                /**
                 * Set Option Data.
                 * @todo Digunakan untuk Render Option
                 */
                setOption: function() {
                    let vm = this;
                    $.post(this.url.show1).done((data) => {
                        vm.cabang.data = data;
                    });
                    $.post(this.url.show2).done((data) => {
                        vm.tipe.data = data;
                    });
                },
                /**
                 * Get Form Data.
                 *
                 * @todo Digunakan untuk Mendapatkan Data
                 *       yang Telah Diformat untuk Dikirim.
                 */
                getData: function(data) {
                    return {
                        idCabang: this.cabang.id,
                        idTipe: this.tipe.id,
                        idStatus: this.status.id,
                        nama: this.nama,
                        noPelat: this.noPelat,
                        tanggalStnk: this.tanggalStnk,
                        tanggalUji: this.tanggalUji,
                        kubikasi: this.kubikasi,
                        keterangan: this.keterangan,
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
                },
            },
            mounted: function() {
                this.setOption();
            }
        });
    </script>
@endpush
