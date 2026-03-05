@extends('layouts.main')
@section('content')
@include('partials.breadcrumb')
<!-- ============================================================== -->
<!-- Content Container  -->
<!-- ============================================================== -->
<div class="container-fluid">
    <div class="row m-1">
        <div class="col-12">
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
                                <th> #                        </th>
                                <th> Detail                   </th>
                                <th> Kode <em>Order</em>      </th>
                                <th> PIC <em>Request</em>     </th>
                                <th> Nama <em>Cabang</em>     </th>
                                <th> Nama <em>Principal</em>  </th>
                                <th> Tanggal <em>Request</em> </th>
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
                <span class="modal-title">Detail Konfirmasi Order</span>
                <button type="button" class="btn btn-sm btn-tool modal-close">
                    <i class="mdi mdi-close"></i>
                </button>
            </div>
            <div class="modal-body">
                <form method="" action="">
                    @csrf
                    <input type="hidden" name="id"          v-model="request.id">
                    <input type="hidden" name="idRequest"   v-model="request.id">
                    <input type="hidden" name="kodeRequest" v-model="request.kode">
                    <input type="hidden" name="idProses"    v-model="request.id_proses">
                    <input type="hidden" name="idUser2"     v-model="request.id_user2">
                    <input type="hidden" name="tanggalDikonfirmasi" value="{{ date('Y-m-d') }}">
                    <input type="hidden" name="waktuDikonfirmasi"   value="{{ date('H:i:s') }}">
                </form>
                <div class="form row">
                    <div class="col-md-4">
                        <div class="form-group">
                            <label>Kode <em>Order</em></label>
                            <input type="text" v-model="request.kode" class="form-control-modal" placeholder="Masukkan Kode Request" readonly>
                        </div>
                        <div class="form-group">
                            <label>Tanggal <em>Request</em></label>
                            <input type="text" v-model="request.tanngal" class="form-control-modal datepicker" placeholder="YYYY-MM-DD" readonly>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="form-group">
                            <label>Nama <em>Cabang</em></label>
                            <input type="text" v-model="request.nama_cabang" class="form-control-modal" placeholder="Masukkan Cabang" readonly>
                        </div>
                        <div class="form-group">
                            <label>PIC <em>Request</em></label>
                            <select2 v-model="request.id_user1" :options="user1.text" :readonly="true" required></select2>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="form-group">
                            <label>Nama <em>Principal</em></label>
                            <input type="text" v-model="request.nama_principal" class="form-control-modal" placeholder="Masukkan Principal" readonly>
                        </div>
                        <div class="form-group">
                            <label>Keterangan <em>Order</em></label>
                            <textarea type="text" v-model="request.keterangan" class="form-control-modal" maxlength="100" placeholder="Max 100 Karater!" readonly></textarea>
                        </div>
                    </div>
                </div>
            </div>
            <div class="modal-body border-top">
                <div class="form-sm row">
                    <div class="col-md-4">
                        <div class="form-group">
                            <label>PIC <em>Supervisi</em></label>
                            <select2 v-model="request.id_user2" :options="user2.text" required></select2>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="form-group">
                            <label>Tanggal <em>Konfirmasi</em></label>
                            <input type="text" value="{{ date('Y-m-d') }}" class="form-control-modal datepicker" placeholder="YYYY-MM-DD" readonly>
                        </div>
                    </div>
                </div>
            </div>
            <div class="modal-body border-top">
                <div class="form-sm row">
                    <div class="col-md-4">
                        <div class="form-group">
                            <label>PIC <em>Supervisi</em></label>
                            <select2 v-model="request.id_user2" :options="user2.text" required></select2>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="form-group">
                            <label>Tanggal <em>Konfirmasi</em></label>
                            <input type="text" value="{{ date('Y-m-d') }}" class="form-control-modal datepicker" placeholder="YYYY-MM-DD" readonly>
                        </div>
                    </div>
                </div>
            </div>
            <div class="modal-body border-top mb-2">
                <div class="form-sm row">
                    <div class="col-md-4">
                        <div class="form-group">
                            <label>PIC <em>Supervisi</em></label>
                            <select2 v-model="request.id_user2" :options="user2.text" required></select2>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="form-group">
                            <label>Tanggal <em>Konfirmasi</em></label>
                            <input type="text" value="{{ date('Y-m-d') }}" class="form-control-modal datepicker" placeholder="YYYY-MM-DD" readonly>
                        </div>
                    </div>
                </div>
            </div>
            <div class="modal-body border-top px-0 pt-0">
                <div class="table-container">
                    <table class="table">
                        <thead>
                            <tr>
                                <th> #                          </th>
                                <th> Kode <em>Produk</em>       </th>
                                <th> Nama <em>Produk</em>       </th>
                                <th> Harga Beli <em>Produk</em> </th>
                                <th> Harga Beli <em>PPN</em>    </th>
                                <th> Jumlah <em>Request</em>    </th>
                                <th> Subtotal                   </th>
                            </tr>
                        </thead>
                        <tbody v-for="(item, index) in produk.table.data">
                            <tr>
                                <td> @{{ index+1          }} </td>
                                <td> @{{ item.kode_produk }} </td>
                                <td> @{{ item.nama_produk }} </td>
                                <td class="text-center"> @{{ numberToStr(item.harga_beli_produk)     }} </td>
                                <td class="text-center"> @{{ numberToStr(item.harga_beli_produk_ppn) }} </td>
                                <td class="text-center"> @{{ item.jumlah_request                     }} </td>
                                <td class="text-center"> @{{ numberToStr(item.subtotal_request)      }} </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            <div class="modal-body border-top">
                <div class="form row mt-3 m-0">
                    <div class="col-md-12">
                        <div class="btn-group float-end" role="group">
                            <button type="button" class="btn btn-success px-4" @click="store($event.target, event)">
                                <i class="mdi mdi-check"></i> Konfirmasi Request
                            </button>
                            <button type="button" class="btn btn-primary px-4" @click="edit">
                                <i class="mdi mdi-lead-pencil"></i> Edit Request
                            </button>
                            <button type="button" class="btn btn-danger px-4" @click="destroy">
                                <i class="mdi mdi-delete"></i> Batalkan Request
                            </button>
                        </div>
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
    var app_list = new Vue({ 
        el      : '#app-list',
        data    : function() {
            return {
                url   : { show : "konfirmasi-order/data/table" },
                table : () => $('#app-list').find('table'),
                data  : {
                    columns : [ 
                        { data : ""               },
                        { data : "actions"        },
                        { data : "kode"           },
                        { data : "nama_user"      },
                        { data : "nama_cabang"    },
                        { data : "nama_principal" },
                        { data : "tanggal"        },
                    ] 
                }
            }
        },
        methods : {
            getTableRowData : function(row) {
                return this.table().DataTable().row(row).data();
            },
            renderTable : function(filter=null) {
                Table().set(this.table()).destroy().paging().rowNumber(true)
                       .serverSide(this.data.columns, this.url.show, filter)
                       .init();
                
                return this;
            },
            actionBtnDetail : function(vm = this) {
                this.table().on('click', '.btn-detail', function() {
                    let rowIndex = $(this).closest('tr');
                    let rowData  = vm.getTableRowData(rowIndex);

                    app_detail.renderData(rowData);
                    $('#app-detail').modal('show');
                });
                return this;
            },
        },
        mounted : function(vm=this){
            this.renderTable().actionBtnDetail();
        }
    });

    var app_detail = new Vue({ 
        el      : '#app-detail',
        data    : function() {
            return {
                url : { 
                    show1   : "konfirmasi-request/data",
                    show2   : "/olah-user/data/option1",
                    store   : "konfirmasi-request/store",
                    edit    : "konfirmasi-request/edit/:id",
                    destroy : "konfirmasi-request/destroy"
                },
                form    : () => $("#app-detail").find('form'),
                request : {
                    id                   : '',
                    kode                 : '',
                    keterangan           : '',
                    nama_cabang          : '',
                    nama_principal       : '',
                    nama_user            : '',
                    tanggal              : '',
                    tanggal_dibuat       : '',
                    tanggal_dikonfirmasi : '',
                    waktu_dikonfirmasi   : '',
                },
                user1     : { text  : [] },
                user2     : { text  : [] },
                produk    : { table : { data : [] } },
            }
        },
        methods : {
            loading : function(opsi) { 
                if      (opsi == 1) { $('#app-detail .modal-load').show(); } 
                else if (opsi == 0) { $('#app-detail .modal-load').hide(); }
            },
            setOption : function(vm = this) {
                $.post(this.url.show2, {display:['nik','nama']})
                 .done((data) => { 
                    vm.user1.text = data; 
                    vm.user2.text = data; 
                });
            },
            renderData : function(data, vm=this) {
                this.loading(1);
                this.request = data;

                $.post(this.url.show1, {id:this.request.id})
                 .done(function(response) {
                    vm.produk.table.data = response; 
                    vm.loading(0);
                })
            },

            /**
             * Set Form Action URL & Method
             * untuk Simpan Data dan Submit.
             */
            store : function(el, event) {
                this.request.id_proses = '3';

                // Set Form Action URL & Method
                Alert().submit().then((result) => {
                    if (result.value == true) {
                        this.$nextTick(function() {
                            this.form()
                                .attr('method', 'POST')
                                .attr("action", this.url.store)
                                .submit();
                        });
                    } else {
                        Alert().cancel();
                    }
                });
            },

            /**
             * Set Form Action URL & Method
             * untuk Simpan Data dan Submit.
             */
            destroy : function() {
                this.request.id_proses = '2';

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
                window.location.href = this.url.edit.replace(":id", this.request.id);
            }          
        },
        mounted : function(vm=this){
            this.setOption();
        }
    });
</script>
@endpush