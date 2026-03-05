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
                        <span class="card-title">Form Request Order</span>
                    </div>
                    <div class="card-body card-bar-menu">
                        <div class="btn-group" role="group">
                            <a class="btn btn-danger" onclick="window.history.back()">
                                <i class="mdi mdi-step-backward"></i>Kembali
                            </a>
                        </div>
                    </div>
                    <div class="card-body">
                        <div class="form row">
                            <div class="col-md-4">
                                <div class="form-group">
                                    <label>Kode <em>Order</em></label>
                                    <input type="hidden" name="idProsesBerjalan"     value="2">
                                    <input type="hidden" name="idProsesDiselesaikan" value="1">
                                    <input type="text" name="kodeOrder" value="{{ $data->kode }}" placeholder="Max 50 Karakter" readonly required>
                                </div>
                                <div class="form-group">
                                    <label>PIC Request <em>Order</em></label>
                                    <input type="hidden" name="idUserJabatan" v-model="user.data.selected.id_jabatan">
                                    <select2 name="idUser" v-model="user.id" :options="user.text" :readonly="true" required></select2>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="form-group">
                                    <label>Tanggal Request <em>Order</em></label>
                                    <input type="hidden" name="waktu" value="{{ date('H:i:s') }}">
                                    <input type="text" name="tanggal" value="{{ date('Y-m-d') }}" class="datepicker" placeholder="YYYY-MM-DD" readonly required>
                                </div>
                                <div class="form-group">
                                    <label>Pilih <em>Principal</em></label>
                                    <select2 name="idPrincipal" v-model="principal.id" :options="principal.text" required></select2>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="form-group">
                                    <label>Pilih <em>Cabang</em></label>
                                    <select2 name="idCabang" v-model="cabang.id" :options="cabang.text" :readonly="true" required></select2>
                                </div>
                                <div class="form-group">
                                    <label>Keterangan <em>Order</em></label>
                                    <textarea type="text" name="keterangan" maxlength="100" placeholder="Max 100 Karater!"></textarea>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- ============================================== -->
                <!-- End Card Form - Order  -->
                <!-- ============================================== -->
                <div id="app_produk">
                    <!-- ============================================== -->
                    <!-- Card Form - Add Produk  -->
                    <!-- ============================================== -->
                    <div class="card form">
                        <div class="card-body">
                            <div class="form row">
                                <div class="col-md-4">
                                    <div class="form-group">
                                        <label>Pilih <em>Produk</em></label>
                                        <input type="hidden" v-model="produk.check" required>
                                        <select2 v-model="produk.option.id" :options="produk.option.text"></select2>
                                    </div>
                                    <div class="form-group">
                                        <label>Harga Beli <em>Produk</em></label>
                                        <input type="number" placeholder="Pilih Satuan Produk Terlebih Dahulu!" v-model="produk.option.data.selected.harga_beli_produk_dikonversi"  readonly>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="form-group">
                                        <label>Pilih Satuan <em>Produk</em></label>
                                        <select2 v-model="satuan.id" :options="satuan.text"></select2>
                                    </div>
                                    <div class="form-group">
                                        <label>Harga Beli + PPN</label>
                                        <input type="number" v-model="produk.option.data.selected.harga_beli_produk_ppn" placeholder="Pilih Satuan Produk Terlebih Dahulu!" readonly>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="form-group">
                                        <label>Jumlah <em>Order</em></label>
                                        <input type="number" v-model="produk.option.data.selected.jumlah_order" placeholder="Number">
                                    </div>
                                    <div class="form-group">
                                        <label>Subtotal <em>Order</em></label>
                                        <input type="number" v-model="produk.option.data.selected.subtotal_order" placeholder="Number" readonly>
                                    </div>
                                    <div class="form-group">
                                        <div class="btn-group float-end" role="group">
                                            <button class="btn btn-primary px-4 mt-3" type="button" @click="addData">
                                                <i class="mdi mdi-plus"></i> Tambah
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <!-- ============================================== -->
                    <!-- End Card List - Produk  -->
                    <!-- ============================================== -->
                    <div class="card form">
                        <div class="card-body p-0 mt-2">
                            <div class="table-container">
                                <table class="table">
                                    <thead>
                                        <tr>
                                            <th> #                              </th>
                                            <th> Kode <br><em>Produk</em>       </th>
                                            <th> Nama <br><em>Produk</em>       </th>
                                            <th> Satuan <br><em>Produk</em>     </th>
                                            <th> Harga Beli <br><em>Produk</em> </th>
                                            <th> Harga Beli <br>+ PPN           </th>
                                            <th> Jumlah <br><em>Order</em>      </th>
                                            <th> Subtotal <br><em>Order</em>    </th>
                                            <th> Hapus <br><em>Item</em>        </th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="(item, index) in produk.table.data" :key="item.id">
                                            <td> @{{ index+1 }}                                             </td>
                                            <td> @{{ item.kode_produk }}                                    </td>
                                            <td> @{{ item.nama_produk }}                                    </td>
                                            <td> [@{{ item.level_produk_uom }}] @{{ item.nama_produk_uom }} </td>
                                            <td> @{{ item.harga_beli_produk_dikonversi }}                   </td>
                                            <td> @{{ item.harga_beli_produk_ppn }}                          </td>
                                            <td> @{{ item.jumlah_order }}                                   </td>
                                            <td> @{{ item.subtotal_order }}                                 </td>
                                            <td>
                                                <input type="hidden" name="idProduk[]"                  :value="item.id_produk">
                                                <input type="hidden" name="namaProduk[]"                :value="item.nama_produk">
                                                <input type="hidden" name="kodeProduk[]"                :value="item.kode_produk">
                                                <input type="hidden" name="hargaBeliProduk[]"           :value="item.harga_beli_produk">
                                                <input type="hidden" name="hargaBeliProdukDikonversi[]" :value="item.harga_beli_produk_dikonversi">
                                                <input type="hidden" name="hargaBeliProdukPPN[]"        :value="item.harga_beli_produk_ppn">
                                                <input type="hidden" name="idProdukUOM[]"               :value="item.id_produk_uom">
                                                <input type="hidden" name="namaProdukUOM[]"             :value="item.nama_produk_uom">
                                                <input type="hidden" name="kodeProdukUOM[]"             :value="item.kode_produk_uom">
                                                <input type="hidden" name="levelProdukUOM[]"            :value="item.level_produk_uom">
                                                <input type="hidden" name="faktorKonversiProdukUOM[]"   :value="item.faktor_konversi_produk_uom">
                                                <input type="hidden" name="jumlahOrder[]"               :value="item.jumlah_order">
                                                <input type="hidden" name="jumlahTersisa[]"             :value="item.jumlah_order">
                                                <input type="hidden" name="subtotalOrder[]"             :value="item.subtotal_order">

                                                <button type="button" class="btn btn-sm btn-danger" @click="removeData(index)" title="Hapus">
                                                    <i class="mdi mdi-delete mx-1 font-16"></i>
                                                </button>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                        <div class="card-body">
                            <button type="submit" class=" btn btn-control btn-success float-end mx-1" onclick="submitConfirmation(event, this)">
                                <i class="mdi mdi-check"></i> Submit Order
                            </button>
                        </div>
                    </div>
                    <!-- ============================================== -->
                    <!-- End Card List - Produk  -->
                    <!-- ============================================== -->
                </div>
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
        el      : '#app_form',
        data    : function() {
            return {
                url : { 
                    show1 : "/olah-cabang/data/option",
                    show2 : "/olah-principal/data/option",
                    show3 : "/olah-user/data/option4",
                },
                table     : () => Table().set($('#app-list').find('table')),
                cabang    : { text : [], id : '{{ user()->id_cabang }}'   },
                principal : { text : [], id : ''                          },
                user      : { 
                    id   : '{{ user()->id }}', 
                    text : [], 
                    data : {all:[], selected:{ id_jabatan : null }}
                },
            }
        },
        methods : {
            setOption : function(vm = this) {
                $.post(this.url.show1).done((data) => { 
                    vm.cabang.text = data; 
                });
                $.post(this.url.show2).done((data) => { 
                    vm.principal.text = data; 
                });
                $.post(this.url.show3, {display:['nik','nama']})
                 .done((data) => { 
                    vm.user.text          = data.options; 
                    vm.user.data.all      = data.collections; 
                    vm.user.data.selected = vm.user.data.all.filter( 
                        data => data.id == this.user.id
                    )[0];
                });
            },
        },
        watch   : {
            'principal.id' : function(value) {
                app_produk.resetData();
                app_produk.resetSatuan();
                app_produk.setData(value);
            }
        },
        mounted : function() {
            this.setOption();
        }
    });

    var app_produk = new Vue({ 
        el      : '#app_produk',
        data    : function() {
            return {
                url : { 
                    show1  : "/olah-produk/data/option2",
                    show2  : "/olah-produk/satuan/data/option3",
                },
                table  : () => { return Table().set($('#app-produk').find('table')); },
                satuan : { 
                    id   : '', 
                    text : '', 
                    data : {
                        all      : [],
                        selected : {
                            dikonversi : null, // Satuan Dikonversi      (A).
                            target     : null, // Satuan Target Konversi (B).
                        }
                    },
                },
                produk : {
                    table  : { data : [] },
                    option : { 
                        id    : '',
                        text  : [],
                        data  : { 
                            all      : [], 
                            selected : {
                                id_produk                    : null,
                                nama_produk                  : null,
                                kode_produk                  : null,
                                harga_beli_produk            : null,
                                id_produk_uom                : null,
                                nama_produk_uom              : null,
                                kode_produk_uom              : null,
                                level_produk_uom             : null,
                                harga_beli_produk_dikonversi : null,
                                id                           : null,
                                kode_order                   : null,
                                jumlah_order                 : null,
                                jumlah_terpenuhi             : null,
                                jumlah_tersisa               : null,
                                subtotal_order               : null,
                                harga_beli_produk_ppn        : null,
                            } 
                        },
                    },
                    check : '',
                },
            }
        },
        methods : {
            setSatuan   : function(id, vm = this){
                $.post(this.url.show2, {idProduk:id}).done((data) => { 
                    vm.satuan.text     = data.options; 
                    vm.satuan.data.all = data.collections;
                    vm.setSatuanA();
                    vm.satuan.id       = vm.satuan.data.selected.dikonversi.id
                });
            },
            setSatuanA  : function(){
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
            setSatuanB  : function(id){
                console.log(id);
                // Satuan Target Konversi/Terpilih (B).
                let produk = this.produk.option.data.selected;
                let satuan = this.satuan.data.selected;

                satuan.target                     = this.satuan.data.all.find(data => data.id == id);
                produk.id_produk_uom              = satuan.target.id;
                produk.nama_produk_uom            = satuan.target.nama;
                produk.kode_produk_uom            = satuan.target.kode;
                produk.level_produk_uom           = satuan.target.level;
                produk.faktor_konversi_produk_uom = satuan.target.level;
            },
            resetSatuan : function() {
                this.satuan.id                       = '';
                this.satuan.text                     = [];
                this.satuan.data.all                 = [];
                this.satuan.data.selected.dikonversi = null;
                this.satuan.data.selected.target     = null;
            },
            setData     : function(id, vm = this) {
                if (!isNull(id)) {
                    $.post(this.url.show1, {idPrincipal:id}).done((data) => { 
                        vm.produk.option.text     = data.options; 
                        vm.produk.option.data.all = data.collections; 
                    });
                }
            },
            getData     : function() {
                return this.produk.option.data.all.filter( 
                    data => data.id_produk == this.produk.option.id
                )[0];
            },
            resetData   : function() {
                this.produk.option.id       = '';
                this.produk.table.text      = [];
                this.produk.table.data      = [];
                this.produk.option.data.all = [];

                for (let key in this.produk.option.data.selected) { 
                    this.produk.option.data.selected[key] = null; 
                }
            },
            removeData  : function(index) {
                this.produk.table.data.splice(index, 1);
            },
            addData     : function() {
                let item  = { ...this.produk.option.data.selected };
                let exist = this.produk.table.data.find(data => data.id_produk == item.id_produk);
                exist ? Alert().exist() : this.produk.table.data.push(item);
            },
        },
        watch   : {
            'produk.option.id'  : function(value) {
                if (!isNull(value)) { 
                    this.produk.option.data.selected.jumlah_order = null;
                    this.produk.option.data.selected = this.getData(); 
                    this.setSatuan(value);
                }
            },
            'produk.option.data.selected.jumlah_order' : function(value) {
                let produk = this.produk.option.data.selected;
                produk.subtotal_order = produk.harga_beli_produk_ppn * produk.jumlah_order;
                produk.subtotal_order = produk.subtotal_order == 0 ? null : produk.subtotal_order;
            },
            'produk.table.data' : function(value) {
                this.produk.check = this.produk.table.data.length > 0 ? "true" : "";
            },
            'satuan.id'         : function(value) {
                if(!isNull(value)){
                    let ppn    = 0.11;
                    let produk = this.produk.option.data.selected;
                    let satuan = this.satuan.data.selected;

                    this.setSatuanB(value);

                    // Konversi Harga Sesuai dengan Satuan Terpilih
                    produk.harga_beli_produk_dikonversi = produk.harga_beli_produk * 
                    (satuan.target.faktor_konversi / satuan.dikonversi.faktor_konversi);

                    produk.harga_beli_produk_dikonversi = Number.isInteger(produk.harga_beli_produk_dikonversi)
                    ? produk.harga_beli_produk_dikonversi : Math.round(produk.harga_beli_produk_dikonversi * 100) / 100;

                    // Menghitung Harga Beli Produk PPN.
                    produk.harga_beli_produk_ppn = produk.harga_beli_produk_dikonversi + 
                    (produk.harga_beli_produk_dikonversi * ppn);

                    produk.harga_beli_produk_ppn = Number.isInteger(produk.harga_beli_produk_ppn)
                    ? produk.harga_beli_produk_ppn : Math.round(produk.harga_beli_produk_ppn * 100) / 100;

                    // Hitung Subtotal
                    produk.subtotal_order = produk.harga_beli_produk_ppn * produk.jumlah_order;
                    produk.subtotal_order = produk.subtotal_order == 0 ? null : produk.subtotal_order;
                }
            },
        }
    });
</script>
@endpush