@extends('layouts.main')
@section('content')
@include('partials.breadcrumb')
<!-- ============================================================== -->
<!-- Container fluid  -->
<!-- ============================================================== -->
<div class="container-fluid">
    <div class="row m-1">
        <div class="col-12">
            <!-- =================================== -->
            <!-- Informasi Request -->
            <!-- =================================== -->
            <div class="card form" id="app-list">
                <div class="card-header">
                    <span class="card-title">Daftar Order</span>
                </div>
                <div class="card-body card-bar-menu">
                    <div class="btn-group" role="group">
                        <a class="btn btn-danger" onclick="window.history.back()">
                            <i class="mdi mdi-step-backward"></i>Kembali
                        </a>
                    </div>
                </div>
                <div class="card-body">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Detail</th>
                                <th>Kode Request</th>
                                <th>Kode Penerimaan</th>
                                <th>No Batch</th>
                                <th>Nama Cabang</th>
                                <th>Nama Principal</th>
                                <th>Tanggal Penerimaan</th>
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
<!-- End Container fluid  -->
<!-- ============================================================== -->
<!-- ============================================================== -->
<!-- Modal Filter  -->
<!-- ============================================================== -->
<div class="modal fade" id="app-detail">
    <div class="modal-dialog modal-xl">
        <div class="modal-content">
            <div class="modal-load">
                <div class="lds-ripple">
                    <div class="lds-pos"></div>
                    <div class="lds-pos"></div>
                </div>
            </div>
            <div class="modal-header">
                <span class="modal-title">Detail Order [ @{{ noFaktur }} ]</span>
                <button type="button" class="btn btn-sm btn-tool modal-close">
                    <i class="mdi mdi-close"></i>
                </button>
            </div>
            <form action="/konfirmasi-order/store" method="post">
                <div class="modal-body">
                    <!-- Hidden Input Form -->
                    @csrf
                    <input type="hidden" name="id"          v-model="id">
                    <input type="hidden" name="idOrder"     v-model="id">
                    <input type="hidden" name="idRequest"   v-model="idRequest">
                    <input type="hidden" name="kodeRequest" v-model="kode">
                    <input type="hidden" name="noFaktur"    v-model="noFaktur">
                    <input type="hidden" name="idCabang"    v-model="idCabang">
                    <input type="hidden" name="tanggal"     value="{{ date('Y-m-d') }}">
                    <input type="hidden" name="waktu"       value="{{ date('H:i:s') }}">
                    <!-- End Hidden Input Form -->
                    <div class="form row">
                        <div class="col-md-4">
                            <div class="form-group">
                                <label>Kode Request</label>
                                <input type="text" v-model="kode" class="form-control-modal" placeholder="Masukkan Kode Request" readonly>
                            </div>
                            <div class="form-group">
                                <label>Principal</label>
                                <input type="text" v-model="principal" class="form-control-modal" placeholder="Masukkan Principal" readonly>
                            </div>
                            <div class="form-group">
                                <label>User Penerima</label>
                                <select2 :options="user1.data" v-model.sync="user1.id" name="idUser1" required></select2>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="form-group">
                                <label>No Faktur</label>
                                <input type="text" v-model="noFaktur" class="form-control-modal" placeholder="Masukkan No Faktur Order" readonly>
                            </div>
                            <div class="form-group">
                                <label>Tanggal Order</label>
                                <input type="text" v-model="tanggal" class="form-control-modal datepicker" placeholder="Masukkan Tanggal" readonly>
                            </div>
                            <div class="form-group">
                                <label>User Supervisi</label>
                                <select2 :options="user2.data" v-model.sync="user2.id" name="idUser" required></select2>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="form-group">
                                <label>Cabang</label>
                                <input type="text" v-model="cabang" class="form-control-modal" placeholder="Masukkan Cabang" readonly>
                            </div>
                            <div class="form-group">
                                <label>Keterangan</label>
                                <input type="text" v-model="keterangan" class="form-control-modal" placeholder="Masukkan Keterangan" readonly>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-body border-top px-0">
                    <div class="table-container">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th>#</th>
                                    <th>Kode Produk</th>
                                    <th>Nama Produk</th>
                                    <th>Total Request</th>
                                    <th>Total Request Diterima</th>
                                    <th>Jumlah Order</th>
                                    <th>Jumlah Datang</th>
                                </tr>
                            </thead>
                            <tbody v-for="(collection, index) in collections">
                                <tr>
                                    <td>@{{ index+1 }}</td>
                                    <td>@{{ collection.kode_produk }}</td>
                                    <td>@{{ collection.nama_produk }}</td>
                                    <td>@{{ collection.jumlah_pesan }}</td>
                                    <td>@{{ collection.jumlah_diterima ?? 0 }}</td>
                                    <td>@{{ collection.jumlah_order }}</td>
                                    <td>
                                        <input type="hidden" name="idProduk[]"        :value="collection.id_produk">
                                        <input type="hidden" name="namaProduk[]"      :value="collection.nama_produk">
                                        <input type="hidden" name="kodeProduk[]"      :value="collection.kode_produk">
                                        <input type="hidden" name="hargaBeliProduk[]" :value="collection.harga_beli_produk">
                                        <input type="hidden" name="idRequestDetail[]" :value="collection.id">
                                        <input type="hidden" name="jumlahOrder[]"     :value="collection.jumlah_order">
                                        <input type="hidden" name="jumlahDiterima[]"  :value="collection.jumlah_diterima">
                                        <input type="text"   name="jumlahDatang[]" v-model="collection.jumlah_datang" class="form-control-modal w-50" placeholder="Masukkan Jumlah">
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
                <div class="modal-body border-top">
                    <div class="my-2 mx-md-4">
                        <div class="btn-group float-end" role="group">
                            <button class="btn btn-success px-4 mb-3">
                                <i class="mdi mdi-check"></i> Konfirmasi Kedatangan
                            </button>
                        </div>
                    </div>
                </div>
            </form>
        </div>
    </div>
</div>
<!-- ============================================================== -->
<!-- End Modal Filter  -->
<!-- ============================================================== -->
@endsection
@push('page_scripts')
<script>
    /**
     * ---------------------------------------------------------------------------------------
     * Draft Request List
     * ---------------------------------------------------------------------------------------
     */
    var app_list = new Vue({ 
        el      : '#app-list',
        data    : function() {
            return {
                // -----------------------------
                // URL untuk Akses ke Resources.
                // -----------------------------
                url : {
                    show  : "konfirmasi-order/data/table",
                    show2 : "cetak-nota/purchase/faktur?idOrder=:id",
                },
                // ----------------
                // Instance Elemen.
                // ----------------
                table : () => { return $('#app-list').find('table'); },
                // -------------------
                // Form & Tabel Data.
                // -------------------
                data : {
                    columns : [ 
                        { data : ""                },
                        { data : "actions"         },
                        { data : "kode_request"    },
                        { data : "no_faktur"       },
                        { data : "no_batch_faktur" },
                        { data : "nama_cabang"  },
                        { data : "nama_principal"  },
                        { data : "tanggal"         },
                    ] 
                }
            }
        },
        methods : {
            /**
             * Mendapatkan row data dari Instance DataTable.
             * @param row Index dari Row.
             */
            getRowData : function(row) {
                return this.table().DataTable().row(row).data();
            },

            /**
             * Handler untuk Action dari Button Detail.
             * @param data Row Data dari Row Tabel Button.
             */
            showDetail : function(data) {
                $('#app-detail').modal('show');
                app_detail.renderData(data);
            },

            /**
             * Render Tabel dengan Data.
             * Inisiasi Kembali Datatable Instance dengan
             * Data Baru.
             * 
             * @param filter Data FIlter untuk Filter Data
             *               yang Akan Dirender Oleh Tabel.
             */
            renderTable : function(filter=null) {
                Table().set(this.table()).destroy().paging().rowNumber(true)
                  .serverSide(this.data.columns, this.url.show, filter)
                  .init();
                
                return this;
            }
        },
        mounted : function(vm=this){
            this.renderTable();

            // Trigger Action dari Button Detail Jika Diklik.
            this.table().on('click', '.btn-detail', function() {
                let row = $(this).closest('tr');
                let rowData = vm.getRowData(row);
                vm.showDetail(rowData);
            });

            // Trigger Action dari Button Print Jika Diklik.
            this.table().on('click', '.btn-print', function() {
                window.open(vm.url.show2.replace(":id", $(this).val()), "_blank");
            });
        }
    });

    /**
     * ---------------------------------------------------------------------------------------
     * Detail Request (Modal)
     * ---------------------------------------------------------------------------------------
     */
    var app_detail = new Vue({ 
        el      : '#app-detail',
        data    : function() {
            return {
                // -----------------------------
                // URL untuk Akses ke Resources.
                // -----------------------------
                url : { 
                    show  : "olah-user/data/option4",
                    show2 : 'konfirmasi-order/data',
                },
                // ----------------
                // Instance Elemen.
                // ----------------
                form : () => { return $("#app-detail").find('form'); },
                // -------------------
                // Form & Tabel Data.
                // -------------------
                user1       : {id : null, data : []},
                user2       : {id : null, data : []},
                id          : '',
                idRequest   : '',
                idCabang    : '',
                kode        : '',
                noFaktur    : '',
                cabang      : '',
                principal   : '',
                tanggal     : '',
                keterangan  : '',
                collections : []
            }
        },
        methods : {
            /** 
             * @summary Memperlihatkan Animasi Loading. 
             * @todo Digunakan saat Memuat Data pada Form Editing.
             * @opsi 1:aktif | 0:mati.
             */
            loading : function(opsi) { 
                if      (opsi == 1) { $('#app-detail .modal-load').show(); } 
                else if (opsi == 0) { $('#app-detail .modal-load').hide(); }
            },
            
            /**
             * Set Option Data.
             * @todo Digunakan untuk Render Option
             */
            setOption : function() {
                let vm = this;

                $.post(this.url.show).done((data) => { 
                    vm.user1.data = data; 
                    vm.user2.data = data; 
                });
            },

            /**
             * Render Tabel dengan Data.
             * Inisiasi Kembali Datatable Instance dengan
             * Data Baru.
             * 
             * @param data Row Data dari Tabel Draft Request.
             */
            renderData : function(data, vm=this) {
                this.loading(1);
                this.id         = data.id;
                this.idRequest  = data.id_request;
                this.kode       = data.kode_request;
                this.noFaktur   = data.no_faktur;
                this.cabang     = data.nama_cabang;
                this.idCabang   = data.id_cabang;
                this.principal  = data.nama_principal;
                this.tanggal    = data.tanggal;
                this.keterangan = data.keterangan;

                $.post(this.url.show2,{id:this.id}).done(function(response) {
                    vm.collections = response;
                    vm.collections.forEach((i) => { i.jumlah_datang = null; });
                    vm.loading(0);
                });
            },   
        },
        mounted : function() {
            this.setOption();
        }
    });
</script>
@endpush