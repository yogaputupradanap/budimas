@extends('layouts.main')
@section('content')
@include('partials.breadcrumb')
<!-- ============================================================== -->
<!-- Container fluid  -->
<!-- ============================================================== -->
<div class="container-fluid">
    <div class="row m-md-1">
        <div class="col-md-12">
            <form action="/purchase-order/store" target="_blank" method="POST">
                <div class="card form" id="app_form">
                    <div class="card-header">
                        <span class="card-title">Form Penerimaan Barang</span>
                    </div>
                    <div class="card-body card-bar-menu">
                        <div class="btn-group" role="group">
                            <a class="btn btn-danger" href="/purchase-order">
                                <i class="mdi mdi-step-backward"></i>Kembali
                            </a>
                        </div>
                    </div>
                    <div class="card-body">
                        <div class="form row">
                            @csrf
                            <input type="hidden" name="statusProses"     value="1">
                            <input type="hidden" name="statusPembayaran" value="1">
                            <input type="hidden" name="idUser"           value="{{ user()->id }}">
                            <input type="hidden" name="waktu"            value="{{ date('H:i:s') }}">
                            <input type="hidden" name="idRequest"        value="{{ request()->id }}">
                            <div class="col-md-4">
                                <div class="form-group">
                                    <label>Kode Request</label>
                                    <input type="text" name="kodeRequest" value="{{ $purchaseRequest->kode }}" class="form-control-modal" placeholder="Masukkan Kode {{ $content->name }}" readonly required>
                                </div>
                                <div class="form-group">
                                    <label>User (PIC)</label>
                                    <input type="text" value="{{ user()->nama }}" class="form-control-modal" maxlength="50" placeholder="Max 50 Karakter" readonly>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="form-group">
                                    <label>Tanggal Request</label>
                                    <input type="text" name="tanggalRequest" value="{{ $purchaseRequest->tanggal }}" class="form-control-modal datepicker" placeholder="YYYY-MM-DD" readonly required>
                                </div>
                                <div class="form-group">
                                    <label>Cabang</label>
                                    <select2 :mute="cabang.mute" :options="cabang.data" v-model="cabang.id" name="idCabang" readonly required></select2>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="form-group">
                                    <label>Tanggal Diterima</label>
                                    <input type="text" name="tanggal" value="{{ date('Y-m-d') }}" class="form-control-modal datepicker" placeholder="YYYY-MM-DD" required>
                                </div>
                                <div class="form-group">
                                    <label>Principal</label>
                                    <select2 :mute="principal.mute" :options="principal.data" v-model="principal.id" name="idPrincipal" readonly required></select2>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div id="app_produk">
                    <div class="card form">
                        <div class="card-body">
                            <div class="form row">
                                <div class="col-md-4">
                                    <div class="form-group">
                                        <label>Pilih Produk</label>
                                        <input type="hidden" v-model="produk.check" required>
                                        <select2 :options="produk.option.text" v-model.sync="produk.option.id"></select2>
                                    </div>
                                    <div class="form-group">
                                        <label>Jumlah Fulfillment <small><em>Sebelumnya</em></small></label>
                                        <input type="text" :value="numberToStr(produk.option.data.selected.jumlah_diterima)" class="form-control-modal money" placeholder="Masukan Jumlah Fulfillment" readonly>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="form-group">
                                        <label>Jumlah Datang</label>
                                        <input type="number" v-model="produk.jumlah_datang" max="produk.option.data.selected.jumlah_sisa" class="form-control-modal" placeholder="Masukan Jumlah Datang Produk">
                                    </div>
                                    <div class="form-group">
                                        <label>Jumlah Sisa <small><em>Sebelumnya</em></small></label>
                                        <input type="text" :value="numberToStr(produk.option.data.selected.jumlah_sisa)" class="form-control-modal money" placeholder="Masukan Jumlah Sisa" readonly>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="form-group">
                                        <label>Jumlah Request <small><em>Keseluruhan</em></small></label>
                                        <input type="text" :value="numberToStr(produk.option.data.selected.jumlah)" class="form-control-modal money" placeholder="Masukan Jumlah Request" readonly>
                                    </div>
                                    <div class="form-group">
                                        <div class="btn-group mt-4" role="group">
                                            <button class="btn btn-primary px-4 mt-1" type="button" @click="addProduk">
                                                <i class="mdi mdi-plus"></i> Tambah
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="card form">
                        <div class="card-body p-0 mt-2">
                            <div class="table-container">
                                <table class="table">
                                    <thead>
                                        <tr>
                                            <th>#</th>
                                            <th>Kode Produk</th>
                                            <th>Nama Produk</th>
                                            <th>Jumlah Datang</th>
                                            <th>Jumlah Fulfillment</th>
                                            <th>Jumlah Sisa</th>
                                            <th>Hapus</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="(item, index) in produk.table.data" :key="item.id">
                                            <td>@{{ index+1 }}</td>
                                            <td>@{{ item.kode_sku }}</td>
                                            <td>@{{ item.nama }}</td>
                                            <td>@{{ item.jumlah_datang }}</td>
                                            <td>@{{ item.jumlah_diterima }}</td>
                                            <td>@{{ item.jumlah_sisa }}</td>
                                            <td>
                                                <input type="hidden" name="idProduk[]"        :value="item.id">
                                                <input type="hidden" name="namaProduk[]"      :value="item.nama">
                                                <input type="hidden" name="kodeProduk[]"      :value="item.kode_sku">
                                                <input type="hidden" name="hargaBeliProduk[]" :value="item.harga_beli">
                                                <input type="hidden" name="jumlahDatang[]"    :value="item.jumlah_datang">
                                                <input type="hidden" name="jumlahSisa[]"      :value="item.jumlah_sisa">
                                                <input type="hidden" name="jumlahDiterima[]"  :value="item.jumlah_diterima">
                                                <input type="hidden" name="idRequestDetail[]" :value="item.id_detail_request">
                                                <input type="hidden" name="subtotalProduk[]"  :value="item.subtotal">
                                                <button type="button" class="btn btn-sm btn-danger" @click="removeProduk(index)" title="Hapus">
                                                    <i class="mdi mdi-delete mx-1 font-16"></i>
                                                </button>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                        <div class="card-body">
                            <div class="btn-group float-end" role="group">
                                <button type="submit" class=" btn btn-success px-4 mt-2" onclick="submitConfirmation(event, this, '/purchase-order')">
                                    <i class="mdi mdi-check"></i> Submit
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </form>
        </div>
    </div>
</div>
<!-- ============================================================== -->
<!-- End Container fluid  -->
<!-- ============================================================== -->
@endsection
@push('page_scripts')
<script>
    var app_form = new Vue({ 
        el      : '#app_form',
        data    : function() {
            return {
                // URL untuk Akses ke Resources.
                url : { 
                    show1  : "/olah-cabang/data/option",
                    show2  : "/olah-principal/data/option",
                },
                // Instance Elemen.
                table : () => { return Table().set($('#app-list').find('table')); },
                // Form Data.
                cabang    : { id : '{{ $purchaseRequest->id_cabang }}',     data : [], mute : true },
                principal : { id : '{{ $purchaseRequest->id_principal }}',  data : [], mute : true },
            }
        },
        methods : {
            /**
             * Set Option Data.
             * @todo Digunakan untuk Render Option
             */
            setOption : function() {
                let vm = this;
                $.post(this.url.show1).done((data) => { vm.cabang.data = data;    });
                $.post(this.url.show2).done((data) => { vm.principal.data = data; });
            },
        },
        mounted : function() {
            this.setOption();
        }
    });
    
    var app_produk = new Vue({ 
        el      : '#app_produk',
        data    : function() {
            return {
                // URL untuk Akses ke Resources.
                url : { 
                    show1  : "/olah-produk/data/option2",
                    show2  : "/olah-produk/satuan/data/option",
                },
                // Instance Elemen.
                table : () => { return Table().set($('#app-produk').find('table')); },
                // Form Data.
                id     : '',
                satuan : { id : '', data : [] },
                produk : {
                    table  : { data : [] },
                    option : { 
                        id    : '',
                        text  : [],
                        data  : { 
                            all      : [], 
                            selected : {
                                id                : null,
                                id_detail_request : null,
                                harga_beli        : null,
                                jumlah            : null,
                                jumlah_diterima   : null,
                                jumlah_sisa       : null,
                                kode_sku          : null,
                                nama              : null,
                            } 
                        },
                    },
                    check         : '',
                    jumlah_datang : null,
                },
            }
        },
        methods : {
            setSatuan : function(id) {
                let vm = this;
                if (!isNull(id)) {
                    $.post(this.url.show2, {idProduk:id}).done((data) => { 
                        vm.satuan.data = data; 
                    });
                }
            },
            setProduk : function() {
                this.produk.option.text     = @json($nProduk).options; 
                this.produk.option.data.all = @json($nProduk).collections; 
            },
            getProduk : function() {
                return this.produk.option.data.all.filter( 
                    data => data.id == this.produk.option.id
                );
            },
            removeProduk : function(index) {
                this.produk.table.data.splice(index, 1);
            },
            addProduk : function() {
                let item  = { ...this.produk.option.data.selected };
                let exist = this.produk.table.data.find(data => data.id == item.id);
                
                if (exist) { 
                    Alert().exist(); 

                } else {
                    item.jumlah_datang    = strToInt(this.produk.jumlah_datang);
                    item.jumlah_sisa     -= item.jumlah_datang;    
                    item.jumlah_diterima += item.jumlah_datang;
                    item.subtotal         = item.jumlah_datang * item.harga_beli

                    this.produk.table.data.push(item);
                }
            },
        },
        watch   : {
            'produk.option.id' : function(value) {
                if (!isNull(value)) {
                    this.setSatuan(value);
                    this.produk.option.data.selected = this.getProduk()[0];
                }
            },
            'produk.table.data' : function(value) {
                // Set Produk Check Pass
                if (this.produk.table.data.length > 0) {
                    this.produk.check = "true";
                }
            },
        },
        mounted : function() {
            this.setProduk();
        }
    });
</script>
@endpush