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
                                <th>Faktur</th>
                                <th>No Faktur</th>
                                <th>No Batch</th>
                                <th>Cabang</th>
                                <th>Principal</th>
                                <th>Tanggal Order</th>
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
            <form action="/konfirmasi-tagihan/store" method="post">
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
                    <input type="hidden" name="noAngsuran"  value="0">
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
                                <label>User Finance</label>
                                <select2 :options="user.data" v-model.sync="user.id" name="idUser" required></select2>
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
                                <label>Total Tagihan Faktur</label>
                                <input type="hidden" name="totalTagihan" v-model="strToInt(totalTagihan)">
                                <input type="text" v-model="totalTagihan" class="form-control-modal money" placeholder="Total Tagihan" readonly>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="form-group">
                                <label>Cabang</label>
                                <input type="text" v-model="cabang" class="form-control-modal" placeholder="Masukkan Cabang" readonly>
                            </div>
                            <div class="form-group">
                                <label>Keterangan</label>
                                <textarea type="text" name="keterangan" class="form-control-modal" placeholder="Masukkan Keterangan"></textarea>
                            </div>
                            <div class="form-group">
                                <label>Total Tagihan Diaudit</label>
                                <input type="hidden" name="totalSisa" v-model="strToInt(totalTagihanAudit)">
                                <input type="hidden" name="totalTagihanAudit" v-model="strToInt(totalTagihanAudit)">
                                <input type="text" v-model="totalTagihanAudit" class="form-control-modal money" placeholder="Audit Total Tagihan Apabila Ada">
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
                                    <th>Harga Beli Produk</th>
                                    <th>Jumlah Order</th>
                                    <th>Jumlah Datang</th>
                                    <th>Valuasi</th>
                                </tr>
                            </thead>
                            <tbody v-for="(collection, index) in collections">
                                <tr>
                                    <td>@{{ index+1 }}</td>
                                    <td>@{{ collection.kode_produk }}</td>
                                    <td>@{{ collection.nama_produk }}</td>
                                    <td>@{{ numberToStr(collection.harga_beli_produk) }}</td>
                                    <td>@{{ collection.jumlah_order }}</td>
                                    <td>@{{ collection.jumlah_datang ?? 0 }}</td>
                                    <td>@{{ numberToStr(collection.jumlah_datang * collection.harga_beli_produk) }}
                                        <input type="hidden" name="idProduk[]"        :value="collection.id_produk">
                                        <input type="hidden" name="namaProduk[]"      :value="collection.nama_produk">
                                        <input type="hidden" name="kodeProduk[]"      :value="collection.kode_produk">
                                        <input type="hidden" name="hargaBeliProduk[]" :value="collection.harga_beli_produk">
                                        <input type="hidden" name="idRequestDetail[]" :value="collection.id">
                                        <input type="hidden" name="jumlahOrder[]"     :value="collection.jumlah_order">
                                        <input type="hidden" name="jumlahDiterima[]"  :value="collection.jumlah_diterima">
                                        <input type="hidden"   name="jumlahDatang[]"  :value="collection.jumlah_datang">
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
                                <i class="mdi mdi-check"></i> Konfirmasi Tagihan
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
                    show  : "konfirmasi-tagihan/data/table",
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
                        { data : "print"           },
                        { data : "no_faktur"       },
                        { data : "no_batch_faktur" },
                        { data : "nama_cabang"     },
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
                console.log(rowData);
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
                    show  : "olah-user/data/option1",
                    show2 : 'konfirmasi-order/data',
                },
                // ----------------
                // Instance Elemen.
                // ----------------
                form : () => { return $("#app-detail").find('form'); },
                // -------------------
                // Form & Tabel Data.
                // -------------------
                user              : {id : null, data : []},
                id                : '',
                idRequest         : '',
                idCabang          : '',
                kode              : '',
                noFaktur          : '',
                totalTagihan      : '',
                totalTagihanAudit : '',
                cabang            : '',
                principal         : '',
                tanggal           : '',
                keterangan        : '',
                collections       : []
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
                $.post(this.url.show).done((data) => { vm.user.data = data; });
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
                this.id                = data.id;
                this.idRequest         = data.id_request;
                this.kode              = data.kode_request;
                this.noFaktur          = data.no_faktur;
                this.cabang            = data.nama_cabang;
                this.idCabang          = data.id_cabang;
                this.principal         = data.nama_principal;
                this.tanggal           = data.tanggal;
                this.keterangan        = data.keterangan;
                this.totalTagihan      = numberToStr(data.total_tagihan);
                this.totalTagihanAudit = numberToStr(data.total_tagihan);
                
                $.post(this.url.show2,{id:this.id}).done(function(response) {
                    vm.collections = response;
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