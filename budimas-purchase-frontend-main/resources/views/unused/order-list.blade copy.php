@extends('layouts.main')
@section('content')
@include('partials.breadcrumb')
<!-- ============================================================== -->
<!-- Container fluid  -->
<!-- ============================================================== -->
<div class="container-fluid">
    <div class="row m-1">
        <div class="col-12">
            <div class="card form" id="app-list">
                <div class="card-header">
                    <span class="card-title">Daftar Request</span>
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
                                <th>Konfirmasi</th>
                                <th>Batalkan</th>
                                <th>Kode <em>Request</em></th>
                                <th>PIC <em>Request</em></th>
                                <th>Nama <em>Principal</em></th>
                                <th>Tanggal <em>Request</em></th>
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
                <span class="modal-title">Detail Request [ @{{ kode }} ]</span>
                <button type="button" class="btn btn-sm btn-tool modal-close">
                    <i class="mdi mdi-close"></i>
                </button>
            </div>
            <div class="modal-body">
                <form method="" action="">
                    @csrf
                    <input type="hidden" name="id" v-model="id">
                </form>
                <div class="form row">
                    <div class="col-md-4">
                        <div class="form-group">
                            <label>Kode Request</label>
                            <input type="text" v-model="kode" class="form-control-modal" placeholder="Masukkan Kode Request" readonly>
                        </div>
                        <div class="form-group">
                            <label>Tanggal Request</label>
                            <input type="text" v-model="tanggal" class="form-control-modal datepicker" placeholder="Masukkan Tanggal" readonly>
                        </div>
                    </div>
                    <div class="col-md-4 px-3">
                        <div class="form-group">
                            <label>Cabang</label>
                            <input type="text" v-model="cabang" class="form-control-modal" placeholder="Masukkan Cabang" readonly>
                        </div>
                        <div class="form-group">
                            <label>Keterangan</label>
                            <input type="text" v-model="keterangan" class="form-control-modal" placeholder="Masukkan Keterangan" readonly>
                        </div>
                    </div>
                    <div class="col-md-4 px-3">
                        <div class="form-group">
                            <label>Principal</label>
                            <input type="text" v-model="principal" class="form-control-modal" placeholder="Masukkan Principal" readonly>
                        </div>
                        <div class="form-group">
                            <label>User (PIC)</label>
                            <input type="text" v-model="user" class="form-control-modal" placeholder="Masukkan User" readonly>
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
                                <th>Jumlah Request</th>
                                <th>Jumlah Diterima</th>
                                <th>Jumlah Sisa Request</th>
                            </tr>
                        </thead>
                        <tbody v-for="(collection, index) in collections">
                            <tr>
                                <td>@{{ index+1 }}</td>
                                <td>@{{ collection.kode_produk }}</td>
                                <td>@{{ collection.nama_produk }}</td>
                                <td>@{{ collection.jumlah_pesan }}</td>
                                <td>@{{ collection.jumlah_diterima ?? 0 }}</td>
                                <td>@{{ collection.jumlah_sisa }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            <div class="modal-body border-top">
                <div class="my-2 mx-md-4">
                    <div class="btn-group float-end" role="group">
                        <button type="button" class="btn btn-primary px-4" @click="edit" :disabled="!checkOrder">
                            <i class="mdi mdi-receipt"></i> Buat Faktur Order
                        </button>
                        <button type="button" class="btn btn-danger px-4" @click="destroy">
                            <i class="mdi mdi-close"></i> Closed Request
                        </button>
                    </div>
                </div>
            </div>
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
     * Table Handler.
     */  
    var app_list = new Vue({ 
        el      : '#app-list',
        data    : function() {
            return {
                // Elements/DOM Wrapper.
                table : () => $('#app-list').find('table'),
                // URL untuk Akses ke Resources.
                url   : { show : "purchase-order/data/table" },
                // Instances Data.
                data  : {
                    // Table Columns Data.
                    columns : [ 
                        { data : ""               },
                        { data : "action_form"    },
                        { data : "action_delete"  },
                        { data : "kode"           },
                        { data : "nama_user"      },
                        { data : "nama_principal" },
                        { data : "tanggal"        },
                    ] 
                }
            }
        },
        methods : {
            /**
             * Mendapatkan Data dari Index Row Terpilih.
             * @param {number} row Index dari Row.
             */
            getTableRowData : function(row) {
                return this.table().DataTable().row(row).data();
            },
            /**
             * Re-inisiasi dan Render Tabel Kembali.
             * @param {object} filter Filter Data dari Tabel.
             */
            renderTable : function(filter=null) {
                Table().set(this.table()).destroy().paging().rowNumber(true)
                       .serverSide(this.data.columns, this.url.show, filter)
                       .init();
                return this;
            },
            /**
             * Action Handler dari Button Form.
             * @param data Row Data dari Button.
             */
            actionBtnForm : function(vm=this) {
                this.table().on('click', '.btn-form', function() {
                    let rowData = vm.getTableRowData($(this).closest('tr'));
                    app_detail.renderData(rowData);
                    app_detail.edit();
                });
                return this;
            },
            /**
             * Action Handler dari Button Delete.
             * @param data Row Data dari Button.
             */
            actionBtnDelete : function(vm=this) {
                this.table().on('click', '.btn-delete', function() {
                    let rowData = vm.getTableRowData($(this).closest('tr'));
                    app_detail.renderData(rowData);
                    app_detail.destroy();
                });
                return this;
            },
        },
        mounted : function(){
            this.renderTable().actionBtnForm().actionBtnDelete();
        }
    });

    /**
     * Form Handler
     */
    var app_detail = new Vue({ 
        el      : '#app-detail',
        data    : function() {
            return {
                // Elements/DOM Wrapper.
                form  : () => { return $("#app-detail").find('form'); },
                // URL untuk Akses ke Resources.
                url   : { 
                    show    : "purchase-order/data",
                    edit    : "purchase-order/create/:id",
                    destroy : "purchase-order/destroy",
                },
                // Form Data.
                id          : '',
                kode        : '',
                cabang      : '',
                user        : '',
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
             * Render Tabel dengan Data.
             * Inisiasi Kembali Datatable Instance dengan
             * Data Baru.
             * 
             * @param data Row Data dari Tabel Draft Request.
             */
            renderData : function(data, vm=this) {
                this.loading(1);
                this.id         = data.id;
                this.kode       = data.kode;
                this.cabang     = data.nama_cabang;
                this.user       = data.nama_user;
                this.principal  = data.nama_principal;
                this.tanggal    = data.tanggal;
                this.keterangan = data.keterangan;

                $.post(this.url.show, {id:this.id}).done(function(response) {
                    vm.collections = response;
                    vm.loading(0);
                })
            },

            /**
             * Set Form Action URL & Method
             * untuk Simpan Data dan Submit.
             */
            destroy : function() {
                this.proses = '10';

                // Set Form Action URL & Method
                Alert().delete().then((result) => {
                    if (result.value == true) {
                        this.$nextTick(function() {
                            this.form()
                                .attr('method', 'POST')
                                .attr("action", this.url.destroy)
                                .submit();
                        });
                    } else {
                        Alert().cancel();
                    }
                });
            },

            /**
             * Set Form Action URL & Method
             * untuk Redirect ke Form Edit.
             */
            edit : function() {
                // Set Form Action URL & Redirect
                window.location.href = this.url.edit.replace(":id", this.id);
            }          
        },
        computed: {
            checkOrder: function() { return this.collections.some(i => i.jumlah_sisa != 0); },
        },
    });
</script>
@endpush