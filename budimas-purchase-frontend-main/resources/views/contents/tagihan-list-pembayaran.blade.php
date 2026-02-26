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
                    <span class="card-title">Daftar Purchase</span>
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
                                <th>Riwayat</th>
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
                <span class="modal-title">Detail Tagihan Faktur [ @{{ noFaktur }} ]</span>
                <button type="button" class="btn btn-sm btn-tool modal-close">
                    <i class="mdi mdi-close"></i>
                </button>
            </div>
            <form action="/pembayaran/store" method="post">
                <div class="modal-body">
                    <!-- Hidden Input Form -->
                    @csrf
                    <input type="hidden" name="id"                   v-model="id">
                    <input type="hidden" name="idOrder"              v-model="id">
                    <input type="hidden" name="idTagihan"            v-model="idTagihan">
                    <input type="hidden" name="idRequest"            v-model="idRequest">
                    <input type="hidden" name="kodeRequest"          v-model="kode">
                    <input type="hidden" name="noFaktur"             v-model="noFaktur">
                    <input type="hidden" name="idCabang"             v-model="idCabang">
                    <input type="hidden" name="waktu"                value="{{ date('H:i:s') }}">
                    <input type="hidden" name="noAngsuran"           v-model="noAngsuran">
                    <input type="hidden" name="totalTagihan"         v-model="strToInt(totalTagihan)">
                    <input type="hidden" name="totalTagihanAudit"    v-model="strToInt(totalTagihanAudit)">
                    <input type="hidden" name="nominalPembayaran"    v-model="strToInt(nominalPembayaran)">
                    <input type="hidden" name="nominalTotalSisa"     v-model="nominalTotalSisaTerhitung">
                    <input type="hidden" name="nominalTotalTerbayar" v-model="nominalTotalTerbayarTerhitung">
                    <!-- End Hidden Input Form -->
                    <div class="form row">
                        <div class="col-md-4">
                            <div class="form-group">
                                <label>No Faktur</label>
                                <input type="text" v-model="noFaktur" class="form-control-modal" placeholder="Masukkan No Faktur Order" readonly>
                            </div>
                            <div class="form-group">
                                <label>Principal</label>
                                <input type="text" v-model="principal" class="form-control-modal" placeholder="Masukkan Principal" readonly>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="form-group">
                                <label>Tanggal Angsuran Terakhir</label>
                                <input type="text" v-model="tanggalPembayaran" class="form-control-modal datepicker" placeholder="Masukkan Tanggal" readonly>
                            </div>
                            <div class="form-group">
                                <label>Total Tagihan Faktur</label>
                                <input type="text" v-model="totalTagihan" class="form-control-modal money" placeholder="Total Tagihan" readonly>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="form-group">
                                <label>Cabang</label>
                                <input type="text" v-model="cabang" class="form-control-modal" placeholder="Masukkan Cabang" readonly>
                            </div>
                            <div class="form-group">
                                <label>Total Tagihan Diaudit</label>
                                <input type="text" v-model="totalTagihanAudit" class="form-control-modal money" placeholder="Audit Total Tagihan Apabila Ada" readonly>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-body border-top">
                    <div class="form row">
                        <div class="col-md-4">
                            <div class="form-group">
                                <label>Tanggal Pembayaran</label>
                                <input type="text" name="tanggal" value="{{ date('Y-m-d') }}" class="form-control-modal datepicker" placeholder="Masukkan Tanggal Pembayaran" readonly>
                            </div>
                            <div class="form-group">
                                <label>Nominal Total Terbayar</label>
                                <input type="text" v-model="numberToStr(nominalTotalTerbayarTerhitung)" class="form-control-modal" placeholder="Masukkan Nominal Total Terbayar" readonly>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="form-group">
                                <label>No. Angsuran</label>
                                <input type="number" v-model="noAngsuran" class="form-control-modal" placeholder="Masukkan Angsuran" readonly>
                            </div>
                            <div class="form-group">
                                <label>Nominal Sisa Pembayaran</label>
                                <input type="text" v-model="numberToStr(nominalTotalSisaTerhitung)" class="form-control-modal money" placeholder="Masukkan Nominal Sisa Pembayaran" readonly>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="form-group">
                                <label>User Finance</label>
                                <select2 :options="user.data" v-model.sync="user.id" name="idUser" required></select2>
                            </div>
                            <div class="form-group">
                                <label>Nominal Pembayaran</label>
                                <input type="text" v-model="nominalPembayaran" class="form-control-modal money" placeholder="Masukkan Nominal Pembayaran">
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-body border-top">
                    <div class="my-2 mx-md-4">
                        <div class="btn-group float-end" role="group">
                            <button class="btn btn-success px-4 mb-3" :disabled="check">
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
                    show  : "pembayaran/data/table",
                    show2 : "cetak-nota/purchase/riwayat-pelunasan?idOrder=:id",
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
                    show2 : 'pembayaran/data',
                },
                // ----------------
                // Instance Elemen.
                // ----------------
                form : () => { return $("#app-detail").find('form'); },
                // -------------------
                // Form & Tabel Data.
                // -------------------
                user                          : {id : "{{ user()->id }}", data : []},
                id                            : '',
                idRequest                     : '',
                idOrder                       : '',
                idTagihan                     : '',
                idCabang                      : '',
                kode                          : '',
                noFaktur                      : '',
                totalTagihan                  : '',
                totalTagihanAudit             : '',
                cabang                        : '',
                principal                     : '',
                tanggal                       : '',
                noAngsuran                    : '',
                nominalPembayaran             : '',
                nominalTotalSisaAsli          : '',
                nominalTotalSisaTerhitung     : '',
                nominalTotalTerbayarAsli      : '',
                nominalTotalTerbayarTerhitung : '',
                tanggalPembayaran             : '',
                check                         : true,
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
                this.totalTagihanAudit = numberToStr(data.nominal_total_audit);
                
                $.post(this.url.show2,{id:this.id}).done(function(response) {
                    vm.idTagihan                     = response.id_tagihan;
                    vm.noAngsuran                    = response.no_angsuran + 1;
                    vm.nominalTotalSisaAsli          = response.nominal_total_sisa ?? 0;
                    vm.nominalTotalSisaTerhitung     = response.nominal_total_sisa ?? 0;
                    vm.nominalTotalTerbayarAsli      = response.nominal_total_terbayar ?? 0;
                    vm.nominalTotalTerbayarTerhitung = response.nominal_total_terbayar ?? 0;
                    vm.tanggalPembayaran             = response.tanggal;
                    vm.loading(0);
                });
            },   
        },
        watch : {
            nominalPembayaran : function(value) {
                this.nominalTotalSisaTerhitung     = this.nominalTotalSisaAsli - strToInt(value);
                this.nominalTotalTerbayarTerhitung = this.nominalTotalTerbayarAsli + strToInt(value);
            },
            nominalTotalSisaTerhitung : function(value) {
                this.check = value < 0 ? true : false;
            },
        },
        mounted : function() {
            this.setOption();
        }
    });
</script>
@endpush