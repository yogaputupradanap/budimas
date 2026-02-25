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
                                    <th>Nama</th>
                                    <th>Perusahaan</th>
                                    <th>Alamat</th>
                                    <th>Telepon</th>
                                    <th>NPWP</th>
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
                                <label>Perusahaan</label>
                                <select2 :options="perusahaan.data" v-model.sync="perusahaan.id" required></select2>
                            </div>
                            <div class="form-group">
                                <label>NPWP</label>
                                <input type="text" v-model="npwp" class="form-control-modal" maxlength="25"
                                    placeholder="Masukkan NPWP {{ $content->name }} (Max 25 Karakter)"
                                    oninput="filterNPWP(this)" required>
                            </div>
                            <div class="form-group">
                                <label>Telepon</label>
                                <input type="number" name="telepon" value="" class="form-control-modal"
                                    maxlength="13"
                                    placeholder="Masukkan Telepon {{ $content->name }} (Max 13 Karater) e.g. 081212341234">
                            </div>
                            <div class="form-group">
                                <label>Alamat</label>
                                <textarea type="text" v-model="alamat" class="form-control-modal" maxlength="100"
                                    placeholder="Masukkan Alamat {{ $content->name }} (Max 100 Karater)"></textarea>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <opsi-wilayah ref="opsi_wilayah" :id1.sync="idWilayah1" @input:id1="idWilayah1 = $event"
                                :id2.sync="idWilayah2" @input:id2="idWilayah2 = $event" :id3.sync="idWilayah3"
                                @input:id3="idWilayah3 = $event" :id4.sync="idWilayah4"
                                @input:id4="idWilayah4 = $event"></opsi-wilayah>
                            <div class="form-group">
                                <label>Kode</label>
                                <input type="text" v-model="kode" class="form-control-modal" maxlength="100"
                                       placeholder="Masukkan Kode {{ $content->name }} (Max 100 Karakter)"
                                       oninput="filterNPWP(this)" required>
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
                    // URL untuk Akses ke Resources
                    url: {
                        show: req("/getPrincipalTable")
                    },
                    // Instance Elemen
                    table: () => $('#app-list').find('table'),
                    // Tabel Data
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
                                orderable: true
                            },
                            {
                                data: "nama_perusahaan",
                                orderable: true
                            },
                            {
                                data: "alamat",
                                orderable: true
                            },
                            {
                                data: "telepon",
                                orderable: true
                            },
                            {
                                data: "npwp",
                                orderable: true
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
                    const rowData = this.table().DataTable().row(row).data();
                    app_form.setModal(2, rowData);
                });

                this.table().on('click', '.btn-delete', (e) => {
                    e.preventDefault();
                    const row = $(e.currentTarget).closest('tr');
                    const rowData = this.table().DataTable().row(row).data();
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
                        show1: "/olah-perusahaan/data/option",
                        store: "/olah-principal/insert",
                        edit: "/olah-principal/update",
                        delete: "/olah-principal/delete",
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
                    perusahaan: {
                        id: null,
                        data: []
                    },
                    nama: '',
                    alamat: '',
                    telepon: '',
                    npwp: '',
                    kode: '',
                    idWilayah1: null,
                    idWilayah2: null,
                    idWilayah3: null,
                    idWilayah4: null,
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
                    this.perusahaan.id = null;
                    this.alamat = "";
                    this.telepon = "";
                    this.npwp = "";
                    this.idWilayah1 = null;
                    this.idWilayah2 = null;
                    this.idWilayah3 = null;
                    this.idWilayah4 = null;
                },
                /**
                 * Set Option Data.
                 * @todo Digunakan untuk Render Option
                 */
                setOption: function() {
                    let vm = this;
                    $.post(this.url.show1).done((data) => {
                        vm.perusahaan.data = data;
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
                    this.perusahaan.id = data.id_perusahaan;
                    this.nama = data.nama;
                    this.alamat = data.alamat;
                    this.telepon = data.telepon;
                    this.npwp = data.npwp;
                    this.idWilayah1 = data.id_wilayah1;
                    this.idWilayah2 = data.id_wilayah2;
                    this.idWilayah3 = data.id_wilayah3;
                    this.idWilayah4 = data.id_wilayah4;
                    this.kode = data.kode;
                },
                /**
                 * Get Form Data.
                 *
                 * @todo Digunakan untuk Mendapatkan Data
                 *       yang Telah Diformat untuk Dikirim.
                 */
                getData: function(data) {
                    return {
                        nama: this.nama,
                        idPerusahaan: this.perusahaan.id,
                        alamat: this.alamat,
                        telepon: this.telepon,
                        npwp: this.npwp,
                        idWilayah1: this.idWilayah1,
                        idWilayah2: this.idWilayah2,
                        idWilayah3: this.idWilayah3,
                        idWilayah4: this.idWilayah4,
                        kode: this.kode
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
