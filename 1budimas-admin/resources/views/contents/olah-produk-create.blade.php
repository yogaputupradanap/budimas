@extends('layouts.main')
@section('content')
    @include('partials.breadcrumb')
    <div class="container-fluid">
        <div class="row m-md-1">
            <div class="col-md-12">
                <div class="card" id="app-create">
                    <div class="card-header">
                        <span class="card-title">Tambah <em>{{ $content->name }}</em></span>
                    </div>
                    <div class="card-body">
                        <!-- Form utama -->
                        <form @submit.prevent="submit" class="form">
                            <!-- Section Data Produk -->
                            <div class="border-bottom pb-4 mb-4">
                                <h6 class="text-primary mb-3">Data Produk <span class="text-danger">*</span></h6>
                                <div class="row">
                                    <div class="col-md-6">
                                        @csrf
                                        <div class="form-group">
                                            <label>Principal <span class="text-danger">*</span></label>
                                            <select2 :options="principal.data" v-model="principal.id" required></select2>
                                        </div>
                                        <div class="form-group">
                                            <label>Brand <span class="text-danger">*</span></label>
                                            <select2 :options="brand.data" v-model="brand.id" required></select2>
                                        </div>
                                        <div class="form-group">
                                            <label>Kategori <span class="text-danger">*</span></label>
                                            <select2 :options="kategori.data" v-model="kategori.id" required></select2>
                                        </div>
                                        <div class="form-group">
                                            <label>Kode SKU <span class="text-danger">*</span></label>
                                            <input type="text" v-model="kodeSku" class="form-control-modal"
                                                maxlength="25"
                                                placeholder="Masukkan Kode SKU {{ $content->name }} (Max 25 Karakter)"
                                                required>
                                        </div>
                                        <div class="form-group">
                                            <label>Kode EAN</label>
                                            <input type="text" v-model="kodeEan" class="form-control-modal"
                                                maxlength="25"
                                                placeholder="Masukkan Kode EAN {{ $content->name }} (Max 25 Karakter)">
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="form-group">
                                            <label>Nama <span class="text-danger">*</span></label>
                                            <input type="text" v-model="nama" class="form-control-modal" maxlength="50"
                                                placeholder="Masukkan Nama {{ $content->name }} (Max 50 Karakter)" required>
                                        </div>
                                        <div class="form-group">
                                            <label>Harga Beli <span class="text-danger">*</span></label>
                                            <input type="text" v-model="hargaBeli" class="form-control-modal money"
                                                placeholder="Masukkan Harga Beli {{ $content->name }}" required>
                                        </div>
                                        <div class="form-group">
                                            <label>Status <span class="text-danger">*</span></label>
                                            <select2 :options="status.data" v-model="status.id" required></select2>
                                        </div>
                                        <div class="form-group">
                                            <label>PPN <span class="text-danger">*</span></label>
                                            <input type="number" v-model="ppn" class="form-control-modal" maxlength="3"
                                                placeholder="Masukkan PPN {{ $content->name }} (Max 3 Karakter)" required>
                                        </div>
                                        <div class="form-group">
                                            <label>Deskripsi </label>
                                            <textarea class="form-control-modal" v-model="keterangan" maxlength="50"
                                                placeholder="Masukkan Deskripsi {{ $content->name }} (Max 50 Karater)"></textarea>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Section Harga Jual -->
                            <div class="border-bottom pb-4 mb-4">
                                <h6 class="text-primary mb-3">Harga Jual <span class="text-danger">*</span></h6>

                                <!-- Form Grid using responsive classes -->
                                <div class="row g-3 mb-3">
                                    <div class="col-12 col-md-6 col-lg-5">
                                        <div class="form-group">
                                            <label class="mb-2">Tipe Harga <span class="text-danger">*</span></label>
                                            <select2 :options="tipeHarga.data" v-model="hargaForm.idTipeHarga"
                                                class="w-100"></select2>
                                        </div>
                                    </div>
                                    <div class="col-12 col-md-5 col-lg-5">
                                        <div class="form-group">
                                            <label class="mb-2">Harga <span class="text-danger">*</span></label>
                                            <input type="text" v-model="hargaForm.harga"
                                                class="form-control-modal money w-100" placeholder="Masukkan Harga Jual">
                                        </div>
                                    </div>
                                    <div class="col-12 col-md-1 col-lg-2">
                                        <div class="form-group">
                                            <label class="d-block mb-2">&nbsp;</label>
                                            <button type="button" class="btn btn-info w-100" @click="addHarga">
                                                <i class="mdi mdi-plus me-1"></i>Tambah
                                            </button>
                                        </div>
                                    </div>
                                </div>

                                <!-- Responsive Table -->
                                <div class="table-responsive" v-if="hargaList.length > 0">
                                    <table class="table table-bordered table-hover">
                                        <thead class="table-light">
                                            <tr>
                                                <th class="text-center" style="width: 60px">No</th>
                                                <th>Tipe Harga</th>
                                                <th style="width: 200px">Harga</th>
                                                <th class="text-center" style="width: 80px">Action</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr v-for="(harga, index) in hargaList" :key="index">
                                                <td class="text-center">@{{ index + 1 }}</td>
                                                <td>@{{ getTipeHargaLabel(harga.idTipeHarga) }}</td>
                                                <td class="text-end">@{{ formatRupiah(harga.harga) }}</td>
                                                <td class="text-center">
                                                    <button type="button" class="btn btn-danger btn-sm"
                                                        @click="removeHarga(index)">
                                                        <i class="mdi mdi-delete"></i>
                                                    </button>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>

                            <!-- Section Satuan -->
                            <!-- Section Satuan -->
                            <div class="border-bottom pb-4 mb-4">
                                <h6 class="text-primary mb-3">Satuan <span class="text-danger">*</span></h6>

                                <!-- Loop through satuan levels -->
                                <div v-for="(level, index) in satuanLevels" :key="index"
                                    class="border rounded p-3 mb-4">
                                    <h6 class="text-info mb-3">Satuan Level @{{ level.level }} (@{{ level.description }})
                                    </h6>
                                    <div class="row">
                                        <div class="col-md-3">
                                            <div class="form-group">
                                                <label>Kode <em>Satuan</em> <span class="text-danger">*</span></label>
                                                <input type="text" v-model="level.kode" class="form-control-modal"
                                                    :placeholder="'Masukkan Kode Satuan Level ' + level.level" required>
                                            </div>
                                        </div>
                                        <div class="col-md-4">
                                            <div class="form-group">
                                                <label>Nama <em>Satuan</em> <span class="text-danger">*</span></label>
                                                <input type="text" v-model="level.nama" class="form-control-modal"
                                                    :placeholder="'Nama Satuan Level ' + level.level" required>
                                            </div>
                                        </div>
                                        <div class="col-md-3">
                                            <div class="form-group">
                                                <label>Faktor Konversi <span v-if="level.level !== 1"
                                                        class="text-danger">*</span></label>
                                                <input type="number" v-model="level.faktorKonversi"
                                                    class="form-control-modal"
                                                    :placeholder="'Faktor Konversi Level ' + level.level"
                                                    :readonly="level.level === 1" required>
                                            </div>
                                        </div>
                                        <div class="col-md-2">
                                            <div class="form-group">
                                                <label>Status</label>
                                                <span class="btn btn-md text-white"
                                                    :class="isLevelComplete(level) ? 'btn-success' : 'btn-danger'">
                                                    @{{ isLevelComplete(level) ? 'Terisi' : 'Belum Terisi' }}
                                                </span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Tombol Submit -->
                            <div class="d-flex justify-content-end mt-4">
                                <div class="btn-group" role="group">
                                    <a href="{{ route('olah-produk.index') }}" class="btn btn-danger px-4 me-2">
                                        <i class="mdi mdi-close"></i> Batal
                                    </a>
                                    <button type="submit" class="btn btn-success px-4">
                                        <i class="mdi mdi-check"></i> Simpan
                                    </button>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
@endsection

@push('page_scripts')
    <script>
        var app_create = new Vue({
            el: '#app-create',
            data: function() {
                return {
                    url: {
                        show1: "/olah-produk/brand/data/option",
                        show2: "/olah-produk/kategori/data/option",
                        show3: "/olah-principal/data/option",
                        show4: "/olah-produk/tipe-harga/data/option",
                        store: "/olah-produk/insert"
                    },
                    // Data produk
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
                        id: "1",
                        data: @json(nStatus())
                    },
                    ppn: 11,
                    kodeSku: '',
                    kodeEan: '',
                    nama: '',
                    hargaBeli: '',
                    keterangan: '',

                    // Data harga
                    tipeHarga: {
                        data: []
                    },
                    hargaForm: {
                        idTipeHarga: '',
                        harga: ''
                    },
                    hargaList: [],
                    satuanLevels: [{
                            level: 1,
                            description: 'Terkecil',
                            kode: '',
                            nama: '',
                            faktorKonversi: 1
                        },
                        {
                            level: 2,
                            description: 'Menengah',
                            kode: '',
                            nama: '',
                            faktorKonversi: ''
                        },
                        {
                            level: 3,
                            description: 'Terbesar',
                            kode: '',
                            nama: '',
                            faktorKonversi: ''
                        }
                    ],
                }
            },
            methods: {
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
                    $.post(this.url.show4).done((data) => {
                        console.log('Tipe Harga Data:', data); // Debug tipe harga
                        vm.tipeHarga.data = data;
                    });

                },

                // Method untuk harga
                addHarga: function() {
                    if (!this.hargaForm.idTipeHarga || !this.hargaForm.harga) {
                        Alert().required1();
                        return;
                    }

                    // Cek duplikasi tipe harga
                    if (this.hargaList.find(h => h.idTipeHarga === this.hargaForm.idTipeHarga)) {
                        Alert().exist2();
                        return;
                    }

                    this.hargaList.push({
                        idTipeHarga: this.hargaForm.idTipeHarga,
                        harga: strToFloat(this.hargaForm.harga)
                    });

                    // Reset form
                    this.hargaForm.idTipeHarga = '';
                    this.hargaForm.harga = '';
                },

                removeHarga: function(index) {
                    this.hargaList.splice(index, 1);
                },
                isLevelComplete: function(level) {
                    if (level.level === 1) {
                        return level.kode && level.nama;
                    }
                    return level.kode && level.nama && level.faktorKonversi;
                },

                getTipeHargaLabel: function(id) {
                    if (!this.tipeHarga.data || this.tipeHarga.data.length === 0) {
                        return '';
                    }
                    const tipe = this.tipeHarga.data.find(t => t.id == id);
                    return tipe ? tipe.text : ''; // Changed to text since that's the property name in your data
                },

                getData: function() {
                    return {
                        // Data produk
                        idPrincipal: this.principal.id,
                        idBrand: this.brand.id,
                        idKategori: this.kategori.id,
                        idStatus: this.status.id,
                        ppn: this.ppn,
                        kodeSku: this.kodeSku,
                        kodeEan: this.kodeEan,
                        nama: this.nama,
                        hargaBeli: strToFloat(this.hargaBeli),
                        keterangan: this.keterangan,
                        // Data harga jual
                        hargaList: this.hargaList,
                        // Data satuan
                        satuanList: this.satuanLevels.map(level => ({
                            kode: level.kode,
                            nama: level.nama,
                            faktorKonversi: level.faktorKonversi,
                            level: level.level
                        }))
                    };
                },
                validateForm: function() {
                    // Validate all satuan levels
                    for (let level of this.satuanLevels) {
                        if (!this.isLevelComplete(level)) {
                            Alert().notice('warning', 'Required',
                                `Mohon lengkapi data Satuan Level ${level.level}`);
                            return false;
                        }
                    }

                    // Validasi minimal 1 harga
                    if (this.hargaList.length === 0) {
                        Alert().notice('warning', 'Required', 'Mohon tambahkan minimal 1 data harga');
                        return false;
                    }

                    return true;
                },

                submit: function() {

                    if (!this.validateForm()) {
                        return;
                    }
                    Alert().submit().then((result) => {
                        if (result.value) {
                            block(1);
                            $.post(this.url.store, this.getData())
                                .done((response) => {
                                    block(0);
                                    window.location.href =
                                        "/olah-produk";
                                    if (response.success) {
                                        Alert().success1();
                                    }
                                })
                                .fail(() => {
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
