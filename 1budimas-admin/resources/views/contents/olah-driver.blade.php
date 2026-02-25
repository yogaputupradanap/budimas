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
                        <table class="table">
                            <thead>
                                <tr>
                                    <th>#</th>
                                    <th>Action</th>
                                    <th>Nama</th>
                                    <th>NIK</th>
                                    <th>Cabang</th>
                                    <th>Area</th>
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
                        <!-- User Data Section -->
                        <div class="col-md-6">
                            <h6 class="mb-3">Data Karyawan</h6>
                            @csrf
                            <div class="form-group">
                                <label>Nama</label>
                                <input type="text" v-model="nama" class="form-control-modal" maxlength="50"
                                    placeholder="Masukkan Nama Karyawan (Max 50 Karakter)" required>
                            </div>
                            <div class="form-group">
                                <label>NIK</label>
                                <input type="number" v-model="nik" class="form-control-modal" maxlength="25"
                                    placeholder="Masukkan No Induk Karyawan (Max 25 Karakter)" required>
                            </div>
                            <div class="form-group">
                                <label>Cabang</label>
                                <select2 :options="cabang.data" v-model="cabang.id" required></select2>
                            </div>
                            <div class="form-group">
                                <label>Tanggal Lahir</label>
                                <datepicker v-model="tanggalLahir" placeholder="Masukkan Tanggal Lahir (yyyy-mm-dd)"
                                    required>
                                </datepicker>
                            </div>
                            <div class="form-group">
                                <label>Username</label>
                                <input type="text" v-model="username" class="form-control-modal"
                                    placeholder="Masukkan Username">
                            </div>
                            <div class="form-group">
                                <label>Password</label>
                                <input type="password" v-model="password" class="form-control-modal password"
                                    placeholder="Masukkan Password untuk Login">
                            </div>
                            <div class="form-group">
                                <label>Email</label>
                                <input type="email" v-model="email" class="form-control-modal"
                                    placeholder="Masukkan E-Mail">
                            </div>
                            <div class="form-group">
                                <label>Alamat</label>
                                <textarea v-model="alamat" class="form-control-modal" maxlength="100" placeholder="Masukkan Alamat (Max 100 Karater)"
                                    required></textarea>
                            </div>
                            <div class="form-group">
                                <label>Telepon</label>
                                <input type="number" v-model="telepon" class="form-control-modal" maxlength="13"
                                    placeholder="Masukkan Telepon (Max 13 Karater) e.g. 081212341234" required>
                            </div>
                        </div>

                        <!-- Driver Data Section -->
                        <div class="col-md-6">
                            <h6 class="mb-3">Data Driver</h6>
                            {{-- <div class="form-group">
                                <label>Armada</label>
                                <select2 :options="armada.data" v-model="armada.id" required></select2>
                            </div> --}}
                            <opsi-wilayah ref="opsi_wilayah" :id1.sync="idWilayah1" :id2.sync="idWilayah2"
                                @input:id1="idWilayah1 = $event" @input:id2="idWilayah2 = $event" required>
                            </opsi-wilayah>
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
                        show: req('/getDriverTable'),
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
                                orderable: true
                            },
                            {
                                data: "nik",
                                orderable: true
                            },
                            {
                                data: "nama_cabang",
                                orderable: true
                            },
                            {
                                data: "nama_wilayah2",
                                orderable: true,
                                render: function(data, type, row) {
                                    return [row.nama_wilayah2, row.nama_wilayah1].filter(Boolean).join(
                                        " - ");
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
                        // show2: "/olah-armada/data/option",
                        store: "/olah-driver/insert",
                        edit: "/olah-driver/update",
                        delete: "/olah-driver/delete",
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
                    id: '',
                    idDriver: '',
                    idUser: '',
                    // User Data
                    cabang: {
                        id: null,
                        data: []
                    },
                    jabatan: {
                        id: 6, // Driver jabatan ID
                        data: []
                    },
                    nama: '',
                    nik: '',
                    tanggalLahir: '',
                    username: '',
                    password: '',
                    email: '',
                    alamat: '',
                    telepon: '',

                    // Driver Data
                    // armada: {
                    //     id: null,
                    //     data: []
                    // },
                    idWilayah1: null,
                    idWilayah2: null,
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
                onWilayahChange: function() {
                    // Sinkronisasi data wilayah dari component
                    if (this.$refs.opsi_wilayah) {
                        this.idWilayah1 = this.$refs.opsi_wilayah.id1;
                        this.idWilayah2 = this.$refs.opsi_wilayah.id2;
                    }
                },
                /**
                 * reset Data pada Form.
                 */
                resetData: function(data) {
                    // Reset User Data
                    this.cabang.id = "";
                    this.jabatan.id = 6; // Keep driver jabatan
                    this.nama = "";
                    this.nik = "";
                    this.tanggalLahir = "";
                    this.username = "";
                    this.password = "";
                    this.email = "";
                    this.alamat = "";
                    this.telepon = "";

                    // Reset Driver Data
                    // this.armada.id = "";
                    this.idWilayah1 = null;
                    this.idWilayah2 = null;

                    // Reset wilayah component
                    this.$nextTick(() => {
                        if (this.$refs.opsi_wilayah) {
                            this.$refs.opsi_wilayah.id1 = null;
                            this.$refs.opsi_wilayah.id2 = null;
                        }
                    });
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
                    // $.post(this.url.show2).done((data) => {
                    //     vm.armada.data = data;
                    // });
                },
                /**
                 * Set Form Data.
                 *
                 * @todo Digunakan untuk Render Data
                 *       saat Membuka Edit Form.
                 */
                setData: function(data) {

                    // Set User Data
                    this.id = data.id;
                    this.idDriver = data.id;
                    this.idUser = data.id_user;
                    this.cabang.id = data.id_cabang;
                    this.nama = data.nama;
                    this.nik = data.nik;
                    this.tanggalLahir = formatDate(data.tanggal_lahir);
                    this.username = data.username;
                    this.email = data.email;
                    this.alamat = data.alamat;
                    this.telepon = data.telepon;

                    // Set Driver Data
                    // this.armada.id = data.id_armada;
                    this.idWilayah1 = data.id_wilayah1;
                    this.idWilayah2 = data.id_wilayah2;

                    // Update wilayah component setelah data di-set
                    this.$nextTick(() => {
                        if (this.$refs.opsi_wilayah) {
                            this.$refs.opsi_wilayah.id1 = data.id_wilayah1;
                            this.$refs.opsi_wilayah.id2 = data.id_wilayah2;
                        }
                    });
                },
                /**
                 * Get Form Data.
                 *
                 * @todo Digunakan untuk Mendapatkan Data
                 *       yang Telah Diformat untuk Dikirim.
                 */
                getData: function() {
                    return {
                        id: this.idUser,
                        idDriver: this.idDriver,
                        idUser: this.idUser,
                        idCabang: this.cabang.id,
                        idJabatan: 6, // Always set to driver role
                        nama: this.nama,
                        nik: this.nik,
                        tanggalLahir: this.tanggalLahir,
                        username: this.username,
                        password: this.password,
                        email: this.email,
                        alamat: this.alamat,
                        telepon: this.telepon,
                        // Driver specific data
                        // idArmada: this.armada.id,
                        idWilayah1: this.idWilayah1,
                        idWilayah2: this.idWilayah2
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
                            this.$nextTick(() => {
                                // $('.password').prop('required', true);
                            });
                            break;
                        case 2: // Set Form Edit
                            this.modal.id = 2;
                            this.modal.title = 'Edit';
                            this.setData(data);
                            this.$nextTick(() => {
                                // $('.password').prop('required', false);
                            });
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
                                        .done((response) => {
                                            app_list.renderTable();
                                            block(0);
                                            Alert().success1();
                                        })
                                        .fail((xhr) => {
                                            app_list.renderTable();
                                            block(0);
                                            Alert().error();
                                        });

                                    // Submitting Form Edit.
                                } else if (this.modal.id == 2) {
                                    $.post(this.url.edit, this.getData())
                                        .done((response) => {
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
