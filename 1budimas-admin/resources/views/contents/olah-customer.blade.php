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
                            <a class="btn btn-primary" href="/olah-customer/tipe">
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
                                    <th>Action</th>
                                    <th>Kode</th>
                                    <th>Nama</th>
                                    <th>Tipe</th>
                                    <th>Cabang</th>
                                    <th>Rute</th>
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
                                <input type="text" v-model="kode" class="form-control-modal" maxlength="30"
                                    placeholder="Masukkan Kode {{ $content->name }} (Max 30 Karakter)" required>
                            </div>
                            <div class="form-group">
                                <label>Nama</label>
                                <input type="text" v-model="nama" class="form-control-modal" maxlength="50"
                                    placeholder="Masukkan Nama {{ $content->name }} (Max 50 Karakter)" required>
                            </div>
                            <div class="form-group">
                                <label>PIC</label>
                                <input type="text" v-model="pic" class="form-control-modal" maxlength="50"
                                    placeholder="Masukkan PIC {{ $content->name }} (Max 50 Karakter)" required>
                            </div>
                            <div class="form-group">
                                <label>Email</label>
                                <input type="email" v-model="email" class="form-control-modal" maxlength="100"
                                    placeholder="Masukkan Email {{ $content->name }} (Max 100 Karakter)">
                            </div>
                            <div class="form-group">
                                <label>Cabang</label>
                                <select2 :options="cabang.data" v-model.sync="cabang.id" required @change="onCabangChange">
                                </select2>
                            </div>
                            <div class="form-group">
                                <label>Rute</label>
                                <select2 :options="filteredRuteData" v-model.sync="rute.id" :disabled="!cabang.id" required>
                                    <option v-if="!cabang.id" disabled>Pilih cabang terlebih dahulu</option>
                                    <option v-else-if="filteredRuteData.length === 0" disabled>Tidak ada rute untuk cabang
                                        ini</option>
                                </select2>
                            </div>
                            <div class="form-group">
                                <label>Tipe</label>
                                <select2 :options="tipe.data" v-model.sync="tipe.id" required></select2>
                            </div>
                            {{-- <div class="form-group">
                                <label>Tipe Harga</label>
                                <select2 :options="tipeHarga.data" v-model="tipeHarga.id"></select2>
                            </div> --}}
                            <div class="form-group">
                                <label>NPWP</label>
                                <input type="text" v-model="npwp" class="form-control-modal" maxlength="25"
                                    placeholder="Masukkan NPWP {{ $content->name }} (Max 25 Karakter)"
                                    oninput="filterNPWP(this)" required>
                            </div>
                            <div class="form-group">
                                <label>Nama Wajib Pajak</label>
                                <input type="text" v-model="namaWajibPajak" class="form-control-modal" maxlength="100"
                                    placeholder="Masukkan Nama Wajib Pajak {{ $content->name }} (Max 100 Karakter)"
                                    required>
                            </div>
                            <div class="form-group">
                                <label>Alamat Wajib Pajak</label>
                                <textarea v-model="alamatWajibPajak" class="form-control-modal" maxlength="200"
                                    placeholder="Masukkan Alamat Wajib Pajak {{ $content->name }} (Max 200 Karakter)" required></textarea>
                            </div>
                            <div class="form-group">
                                <label>No. Rekening</label>
                                <input type="number" v-model="noRek" class="form-control-modal" maxlength="20"
                                    placeholder="Masukkan No. Rek {{ $content->name }} (Max 20 Karakter)">
                            </div>

                        </div>
                        <div class="col-md-6">
                            <div class="form-group">
                                <label>Telepon</label>
                                <input type="number" v-model="telepon" value="" class="form-control-modal   "
                                    maxlength="13"
                                    placeholder="Masukkan Telepon {{ $content->name }} e.g. (021)55955975">
                            </div>
                            <div class="form-group">
                                <label>Telepon2</label>
                                <input type="number" v-model="telepon2" value="" class="form-control-modal"
                                    maxlength="13" placeholder="Masukkan Telepon {{ $content->name }} e.g. 081212341234">
                            </div>
                            <opsi-wilayah ref="opsi_wilayah" :id1.sync="idWilayah1" @input:id1="idWilayah1 = $event"
                                :id2.sync="idWilayah2" @input:id2="idWilayah2 = $event" :id3.sync="idWilayah3"
                                @input:id3="idWilayah3 = $event" :id4.sync="idWilayah4"
                                @input:id4="idWilayah4 = $event"></opsi-wilayah>
                            <div class="form-group" :required="true">
                                <label>Longitude</label>
                                <input type="number" step="0.000001" min="-180" max="180" v-model="longitude"
                                    class="form-control-modal" maxlength="25"
                                    placeholder="Masukkan Longitude {{ $content->name }} (Max 25 Karakter)">
                            </div>
                            <div class="form-group">
                                <label>Latitude</label>
                                <input type="number" v-model="latitude" step="0.000001" min="-90" max="90"
                                    class="form-control-modal" maxlength="25"
                                    placeholder="Masukkan Latitude {{ $content->name }} (Max 25 Karakter)">
                            </div>
                            <div class="form-group">
                                <label>Alamat</label>
                                <textarea type="text" v-model="alamat" class="form-control-modal" maxlength="100"
                                    placeholder="Masukkan Alamat {{ $content->name }} (Max 100 Karater)" required></textarea>
                            </div>
                            <div class="form-group">
                                <label>PPN</label>
                                <select2 :options="ppnOptions" v-model.sync="isPpn" required></select2>
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
                        show: req("/getCustomer")
                    },
                    // Instance Elemen.
                    table: () => $('#app-list').find('table'),
                    // Tabel Data.
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
                                data: "kode",
                                orderable: true
                            },
                            {
                                data: "nama",
                                orderable: true
                            },
                            {
                                data: "tipe",
                                orderable: true
                            },
                            {
                                data: "nama_cabang",
                                orderable: true
                            },
                            {
                                data: "nama_rute",
                                orderable: true
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
                        show1: "/olah-customer/tipe/data/option",
                        show2: "/olah-cabang/data/option",
                        show3: "/olah-rute/data/option",
                        store: "/olah-customer/insert",
                        edit: "/olah-customer/update",
                        delete: "/olah-customer/delete",
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
                    rute: {
                        id: null,
                        data: []
                    },
                    tipe: {
                        id: null,
                        data: []
                    },
                    kode: '',
                    nama: '',
                    pic: '',
                    email: '',
                    alamat: '',
                    telepon: '',
                    telepon2: '',
                    npwp: '',
                    namaWajibPajak: '',
                    alamatWajibPajak: '',
                    noRek: '',
                    longitude: '',
                    latitude: '',
                    isPpn: '',
                    ppnOptions: [{
                            id: '0',
                            text: 'Tidak'
                        },
                        {
                            id: '1',
                            text: 'Ya'
                        }
                    ],
                    idWilayah1: null,
                    idWilayah2: null,
                    idWilayah3: null,
                    idWilayah4: null,
                }
            },
            computed: {
                filteredRuteData() {
                    if (!this.cabang.id || !this.rute.data.length) {
                        return [];
                    }
                    return this.rute.data.filter(rute => rute.id_cabang == this.cabang.id);
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
                    this.cabang.id = null;
                    this.rute.id = null;
                    this.tipe.id = null;
                    this.kode = '';
                    this.nama = '';
                    this.pic = '';
                    this.email = '';
                    this.alamat = '';
                    this.telepon = '';
                    this.telepon2 = '';
                    this.npwp = '';
                    this.namaWajibPajak = '';
                    this.alamatWajibPajak = '';
                    this.noRek = '';
                    this.longitude = '';
                    this.latitude = '';
                    this.isPpn = '0';
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
                        vm.tipe.data = data;
                    });
                    $.post(this.url.show2).done((data) => {
                        vm.cabang.data = data;
                    });
                    $.post(this.url.show3).done((data) => {
                        vm.rute.data = data;
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
                    this.cabang.id = data.id_cabang;
                    this.rute.id = data.id_rute;
                    this.tipe.id = data.id_tipe;
                    this.kode = data.kode;
                    this.nama = data.nama;
                    this.pic = data.pic;
                    this.email = data.email;
                    this.alamat = data.alamat;
                    this.telepon = data.telepon;
                    this.telepon2 = data.telepon2;
                    this.npwp = data.npwp;
                    this.namaWajibPajak = data.nama_wajib_pajak;
                    this.alamatWajibPajak = data.alamat_wajib_pajak;
                    this.noRek = data.no_rekening;
                    this.longitude = data.longitude;
                    this.latitude = data.latitude;
                    this.isPpn = data.is_ppn;
                    this.idWilayah1 = data.id_wilayah1;
                    this.idWilayah2 = data.id_wilayah2;
                    this.idWilayah3 = data.id_wilayah3;
                    this.idWilayah4 = data.id_wilayah4;
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
                        idRute: this.rute.id,
                        idTipe: this.tipe.id,
                        kode: this.kode,
                        nama: this.nama,
                        pic: this.pic,
                        email: this.email,
                        alamat: this.alamat,
                        telepon: this.telepon,
                        telepon2: this.telepon2,
                        npwp: this.npwp,
                        namaWajibPajak: this.namaWajibPajak,
                        alamatWajibPajak: this.alamatWajibPajak,
                        noRek: this.noRek,
                        longitude: this.longitude,
                        latitude: this.latitude,
                        isPpn: this.isPpn,
                        idWilayah1: this.idWilayah1,
                        idWilayah2: this.idWilayah2,
                        idWilayah3: this.idWilayah3,
                        idWilayah4: this.idWilayah4,
                    };
                },
                onCabangChange: function() {
                    // Reset rute selection when cabang changes
                    this.rute.id = null;
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
                                            app_list
                                                .renderTable();
                                            block(0);
                                            Alert().success1();
                                        })
                                        .fail(() => {
                                            app_list.renderTable();
                                            block(0);
                                            Alert().error();
                                        });
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
