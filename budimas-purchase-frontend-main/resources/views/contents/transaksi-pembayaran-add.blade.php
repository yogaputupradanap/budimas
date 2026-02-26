@extends('layouts.main')
@section('content')
    @include('partials.breadcrumb')
    <!-- ============================================================== -->
    <!-- Content Container  -->
    <!-- ============================================================== -->
    <div class="container-fluid">
        <div class="row m-md-1">
            <div class="col-md-12">
                <form action="/purchase-order/store" method="POST">
                    @csrf
                    <!-- ============================================== -->
                    <!-- Card Form - Order  -->
                    <!-- ============================================== -->
                    <div class="card form" id="app_form">
                        <div class="card-header">
                            <span class="card-title">Form Pembayaran</span>
                        </div>
                        <div class="card-body card-bar-menu">
                            <div class="btn-group" role="group">
                                <a class="btn btn-danger" onclick="window.history.back()">
                                    <i class="mdi mdi-step-backward"></i>Kembali
                                </a>
                            </div>
                        </div>
                        <div class="card-body border-top">
                            <div class="form row">
                                <div class="col-md-4">
                                    <div class="form-group">
                                        <label>No. <em>Tagihan</em></label>
                                        <input type="text" name="kode" value="" placeholder="Max 50 Karakter"
                                            readonly required>
                                    </div>
                                    <div class="form-group">
                                        <label>PIC <em>Pembayaran</em></label>
                                        <input type="hidden" name="user_jabatan_id"
                                            v-model="user.data.selected.id_jabatan">
                                        <select2 name="user_id" v-model="user.id" :options="user.text"
                                            :readonly="true" required></select2>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="form-group">
                                        <label>Tanggal <em>Pembayaran</em></label>
                                        <input type="hidden" name="waktu" value="{{ date('H:i:s') }}">
                                        <input type="text" name="tanggal" value="{{ date('Y-m-d') }}" class="datepicker"
                                            placeholder="YYYY-MM-DD" readonly required>
                                    </div>
                                    <div class="form-group">
                                        <label><em>Principal</em></label>
                                        <select2 name="principal_id" v-model="principal.id" :options="principal.text"
                                            required></select2>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="form-group">
                                        <label><em>Cabang</em></label>
                                        <select2 name="cabang_id" v-model="cabang.id" :options="cabang.text"
                                            :readonly="true" required></select2>
                                    </div>
                                    <div class="form-group">
                                        <label>Keterangan <em>Pembayaran</em></label>
                                        <textarea type="text" name="keterangan" maxlength="100" placeholder="Max 100 Karater!"></textarea>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <!-- ============================================== -->
                    <!-- End Card Form - Order  -->
                    <!-- ============================================== -->
                    <!-- ============================================== -->
                    <!-- Card Form - Produk  -->
                    <!-- ============================================== -->
                    <div id="app_produk" class="card form">
                        <div class="card-body"></div>
                        <div class="card-body border-top p-0 mt-2">
                            <!-- <div class="form row m-4">
                                <div class="col-md-4">
                                    <div class="form-group">
                                        <label>Pilih <em>Produk</em></label>
                                        <input type="hidden" v-model="produk.check" required>
                                        <select2 v-model="produk.option.id" :options="produk.option.text"></select2>
                                    </div>
                                </div>
                                <div class="col-md-8">
                                    <div class="form-group float-end">
                                        <div class="btn-group mt-4" role="group">
                                            <button class="btn btn-primary px-4 mt-1" type="button" @click="addData">
                                                <i class="mdi mdi-plus"></i> Tambah
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div> -->
                            <div class="table-container h-600">
                                <table class="table">
                                    <thead>
                                        <tr>
                                            <th> # </th>
                                            <th> No. Transaksi </th>
                                            <th> Kode Order </th>
                                            <th width="20%"> Subtotal </th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="i in 4" :key="i">
                                            <td> @{{ i + 1 }} </td>
                                            <td> PINV-20240119191471-@{{ i }} </td>
                                            <td> PO-20240119191471-@{{ i }} </td>
                                            <td> 0 </td>
                                        </tr>
                                    </tbody>
                                    <tfoot>
                                        <tr>
                                            <td></td>
                                            <td><b>Total<b></td>
                                            <td></td>
                                            <td><input type="text" class="form-control-modal" value="0" readonly>
                                            </td>
                                        </tr>
                                    </tfoot>
                                </table>
                            </div>
                        </div>
                        <div class="card-body">
                            <button type="submit" class=" btn btn-control btn-success float-end mx-1"
                                onclick="submitConfirmation(event, this)">
                                <i class="mdi mdi-check"></i> Submit Pembayaran
                            </button>
                        </div>
                    </div>
                    <!-- ============================================== -->
                    <!-- End Card Form - Produk  -->
                    <!-- ============================================== -->
                </form>
            </div>
        </div>
    </div>
    <!-- ============================================================== -->
    <!-- End Content Container  -->
    <!-- ============================================================== -->
@endsection
@push('page_scripts')
    <script>
        var app_form = new Vue({
            el: '#app_form',
            data: function() {
                return {
                    url: {
                        show1: "/olah-cabang/data/option",
                        show2: "/olah-principal/data/option",
                        show3: "/olah-user/data/option4",
                    },
                    table: () => Table().set($('#app-list').find('table')),
                    cabang: {
                        text: [],
                        id: '{{ user()->id_cabang }}'
                    },
                    principal: {
                        text: [],
                        id: ''
                    },
                    user: {
                        id: '{{ user()->id }}',
                        text: [],
                        data: {
                            all: [],
                            selected: {
                                id_jabatan: null
                            }
                        }
                    },
                }
            },
            methods: {
                setOption: function(vm = this) {
                    $.post(this.url.show1).done((data) => {
                        vm.cabang.text = data;
                        console.log('Cabang options:', data); // Log data cabang
                    }).fail((err) => {
                        console.error('Failed to fetch cabang options:', err); // Log error jika ada
                    });
                    $.post(this.url.show2).done((data) => {
                        vm.principal.text = data;
                        console.log('Principal options:', data); // Log data principal
                    }).fail((err) => {
                        console.error('Failed to fetch principal options:', err); // Log error jika ada
                    });
                    $.post(this.url.show3, {
                            display: ['nik', 'nama']
                        })
                        .done((data) => {
                            vm.user.text = data.options;
                            vm.user.data.all = data.collections;
                            vm.user.data.selected = vm.user.data.all.filter(data => data.id == this.user
                                .id)[0];
                            console.log('User options:', data); // Log data user
                        }).fail((err) => {
                            console.error('Failed to fetch user options:', err); // Log error jika ada
                        });
                },
            },
            watch: {
                'principal.id': function(value) {
                    console.log('Principal ID changed:', value); // Log perubahan ID principal
                    app_produk.resetData();
                    app_produk.resetSatuan();
                    app_produk.setData(value);
                }
            },
            mounted: function() {
                this.setOption();
                console.log('Component mounted'); // Log saat komponen dipasang
            }
        });

        var app_produk = new Vue({
            el: '#app_produk',
            data: function() {
                return {
                    url: {
                        show1: "/olah-produk/data/option2",
                        show2: "/olah-produk/satuan/data/option3",
                        show3: "/olah-produk/satuan/data1",
                    },
                    table: () => Table().set($('#app-produk').find('table')),
                    satuan: {
                        id: '',
                        text: '',
                        data: {
                            all: [],
                            selected: {
                                dikonversi: null, // Satuan Dikonversi      (A).
                                target: null, // Satuan Target Konversi (B).
                            }
                        },
                    },
                    satuan2: [],
                    produk: {
                        table: {
                            data: []
                        },
                        option: {
                            id: '',
                            text: [],
                            data: {
                                all: [],
                                selected: {
                                    id_produk: null,
                                    nama_produk: null,
                                    kode_produk: null,
                                    harga_beli_produk: null,
                                    id_produk_uom: null,
                                    nama_produk_uom: null,
                                    kode_produk_uom: null,
                                    level_produk_uom: null,
                                    harga_beli_produk_dikonversi: null,
                                    id: null,
                                    kode_order: null,
                                    jumlah_order: null,
                                    jumlah_terpenuhi: null,
                                    jumlah_tersisa: null,
                                    subtotal_order: null,
                                    harga_beli_produk_ppn: null,
                                }
                            },
                        },
                        check: '',
                    },
                }
            },
            methods: {
                setSatuan: function(id, vm = this) {
                    $.post(this.url.show2, {
                        idProduk: id
                    }).done((data) => {
                        vm.satuan.text = data.options;
                        vm.satuan.data.all = data.collections;
                        vm.setSatuanA();
                        vm.satuan.id = vm.satuan.data.selected.dikonversi.id;
                        console.log('Satuan options:', data); // Log data satuan
                    }).fail((err) => {
                        console.error('Failed to fetch satuan options:', err); // Log error jika ada
                    });
                },
                setSatuanA: function() {
                    // Satuan Dikonversi/Awal (A).
                    // Purchasing Satuan Awal yang Terbesar.
                    this.satuan.data.selected.dikonversi =
                        this.satuan.data.all.reduce((maxData, currentData) => {
                            if (currentData.hasOwnProperty('level')) {
                                if (!maxData || currentData.level > maxData.level) {
                                    maxData = currentData;
                                }
                            }
                            return maxData;
                        }, null);
                },
                setSatuanB: function(id) {
                    console.log('Setting Satuan B with ID:', id); // Log ID Satuan B
                    // Satuan Target Konversi/Terpilih (B).
                    let produk = this.produk.option.data.selected;
                    let satuan = this.satuan.data.selected;

                    satuan.target = this.satuan.data.all.find(data => data.id == id);
                    produk.id_produk_uom = satuan.target.id;
                    produk.nama_produk_uom = satuan.target.nama;
                    produk.kode_produk_uom = satuan.target.kode;
                    produk.level_produk_uom = satuan.target.level;
                    produk.faktor_konversi_produk_uom = satuan.target.level;
                },
                resetSatuan: function() {
                    this.satuan.id = '';
                    this.satuan.text = [];
                    this.satuan.data.all = [];
                    this.satuan.data.selected.dikonversi = null;
                    this.satuan.data.selected.target = null;
                },
                setData: function(id, vm = this) {
                    if (!isNull(id)) {
                        $.post(this.url.show1, {
                            idPrincipal: id
                        }).done((data) => {
                            vm.produk.option.text = data.options;
                            vm.produk.option.data.all = data.collections;
                            console.log('Produk options:', data); // Log data produk
                        }).fail((err) => {
                            console.error('Failed to fetch produk options:', err); // Log error jika ada
                        });
                    }
                },
                getData: function() {
                    return this.produk.option.data.all.filter(data => data.id_produk == this.produk.option.id)[
                        0];
                },
                resetData: function() {
                    this.produk.option.id = '';
                    this.produk.table.text = [];
                    this.produk.table.data = [];
                    this.produk.option.data.all = [];

                    for (let key in this.produk.option.data.selected) {
                        this.produk.option.data.selected[key] = null;
                    }
                },
                removeData: function(index) {
                    console.log('Removing item at index:', index); // Log indeks item yang dihapus
                    this.produk.table.data.splice(index, 1);
                },
                hitungSubtotalItem: function(i) {
                    return i.harga_beli_uom * i.jumlah_order;
                },
                hitungSubtotalTransaksi: function(i) {
                    subtotal = 0;
                    i.uom.forEach(function(value) {
                        if (!isNull(value)) {
                            subtotal += value.harga_beli_uom * value.jumlah_order;
                        }
                    });
                    i.subtotal_order = subtotal;
                    return subtotal;
                },
                hitungTotalTransaksi: function() {
                    total = 0;
                    produk = this.produk.table.data;
                    produk.forEach(function(value) {
                        if (!isNull(value)) {
                            total += value.subtotal_order;
                        }
                    });
                    console.log('Total transaksi:', total); // Log total transaksi
                    return total;
                },
                addData: function() {
                    $.post(this.url.show3, {
                        idProduk: this.produk.option.data.selected.id_produk
                    }).done((data) => {
                        console.log('Data satuan produk:', data); // Log data satuan produk

                        let produk = this.produk.option.data.selected;

                        // Sort the array based on the level property
                        data.sort((a, b) => a.level - b.level);

                        let satuan_konversi = data.reduce((maxData, currentData) => {
                            if (currentData.hasOwnProperty('level')) {
                                if (!maxData || currentData.level > maxData.level) {
                                    maxData = currentData;
                                }
                            }
                            return maxData;
                        }, null);

                        data.forEach(item => {
                            item.jumlah_order = null;
                            item.harga_beli_uom = produk.harga_beli_produk * (
                                item.faktor_konversi / satuan_konversi.faktor_konversi
                            );

                            item.harga_beli_uom = Number.isInteger(item.harga_beli_uom) ?
                                item.harga_beli_uom : Math.round(item.harga_beli_uom * 100) /
                                100;

                            item.harga_beli_ppn = item.harga_beli_uom + (item.harga_beli_uom *
                                0.11);
                        });

                        // Determine the minimum and maximum levels in the data
                        const minLevel = Math.min(...data.map(item => item.level), 1);
                        const maxLevel = Math.max(...data.map(item => item.level), 3);

                        // Create a new array with entries for levels minLevel, minLevel + 1, ..., maxLevel
                        const resultArray = Array.from({
                            length: maxLevel - minLevel + 1
                        }, (_, index) => {
                            const matchingItem = data.find(item => item.level === minLevel +
                                index);
                            return matchingItem || null;
                        });

                        let item = {
                            ...this.produk.option.data.selected,
                            uom: resultArray
                        };
                        console.log('Item to add:', item); // Log item yang akan ditambahkan
                        let exist = this.produk.table.data.find(data => data.id_produk == item
                            .id_produk);
                        exist ? Alert().exist() : this.produk.table.data.push(item);
                    }).fail((err) => {
                        console.error('Failed to fetch product data:', err); // Log error jika ada
                    });
                },
            },
            watch: {
                'produk.option.id': function(value) {
                    if (!isNull(value)) {
                        this.produk.option.data.selected.jumlah_order = null;
                        this.produk.option.data.selected = this.getData();
                        this.setSatuan(value);
                    }
                },
                'produk.option.data.selected.jumlah_order': function(value) {
                    let produk = this.produk.option.data.selected;
                    produk.subtotal_order = produk.harga_beli_produk_ppn * produk.jumlah_order;
                    produk.subtotal_order = produk.subtotal_order == 0 ? null : produk.subtotal_order;
                },
                'produk.table.data': function(value) {
                    this.produk.check = this.produk.table.data.length > 0 ? "true" : "";
                    console.log('Produk table data changed:', value); // Log perubahan data tabel produk
                },
                'satuan.id': function(value) {
                    if (!isNull(value)) {
                        let ppn = 0.11;
                        let produk = this.produk.option.data.selected;
                        let satuan = this.satuan.data.selected;

                        this.setSatuanB(value);

                        // Konversi Harga Sesuai dengan Satuan Terpilih
                        produk.harga_beli_produk_dikonversi = produk.harga_beli_produk *
                            (satuan.target.faktor_konversi / satuan.dikonversi.faktor_konversi);

                        produk.harga_beli_produk_dikonversi = Number.isInteger(produk
                                .harga_beli_produk_dikonversi) ?
                            produk.harga_beli_produk_dikonversi : Math.round(produk
                                .harga_beli_produk_dikonversi * 100) / 100;

                        // Menghitung Harga Beli Produk PPN.
                        produk.harga_beli_produk_ppn = produk.harga_beli_produk_dikonversi +
                            (produk.harga_beli_produk_dikonversi * ppn);

                        produk.harga_beli_produk_ppn = Number.isInteger(produk.harga_beli_produk_ppn) ?
                            produk.harga_beli_produk_ppn : Math.round(produk.harga_beli_produk_ppn * 100) / 100;

                        // Hitung Subtotal
                        produk.subtotal_order = produk.harga_beli_produk_ppn * produk.jumlah_order;
                        produk.subtotal_order = produk.subtotal_order == 0 ? null : produk.subtotal_order;

                        console.log('Produk setelah konversi:', produk); // Log produk setelah konversi
                    }
                },
            }
        });
    </script>
@endpush
