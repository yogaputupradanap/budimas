@extends('layouts.main')
@section('content')
@include('partials.breadcrumb')
<div class="container-fluid">
    <div class="row m-md-1">
        <div class="col-md-12">
            <div class="card form" id="app-list">
                <div class="card-header">
                    <span class="card-title">Daftar {{ $content->name }}</span>
                </div>
                <div class="card-body card-bar-menu">
                    <div class="btn-group" role="group">
                        <button class="btn btn-success" type="button" @click="tambahJabatan">
                            <i class="stroke-white-2 mdi mdi-plus"></i>Tambah Jabatan Baru
                        </button>
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
                                <th>Jabatan</th>
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

<div class="modal fade" id="app-fitur">
    <div class="modal-dialog modal-lg">
        <div class="modal-content">
            <div class="modal-header py-3">
                <h5 class="modal-title">Setting Fitur Untuk Jabatan: @{{ nama }}</h5>
                <button type="button" class="btn btn-sm btn-tool modal-close" data-dismiss="modal">
                    <i class="mdi mdi-close"></i>
                </button>
            </div>
            <div class="modal-load" style="display: none;">
                <div class="lds-ripple">
                    <div class="lds-pos"></div>
                    <div class="lds-pos"></div>
                </div>
            </div>
            <div class="modal-body">
                <div class="form row">
                    <div class="col-md-12">
                        <div class="form-group">
                            <label>Pilih Fitur yang Tersedia</label>
                            <select2 :options="fitur.data" v-model="fitur.id" required></select2>
                        </div>
                    </div>
                    <div class="col-12">
                        <div class="form-group">
                            <div class="btn-group add" role="group">
                                <button class="btn btn-success px-4" type="button" @click="submit">
                                    <i class="mdi mdi-plus"></i> Tambahkan Fitur
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="modal-body border-top">
                <h6 class="mb-3">Fitur yang Sudah Dimiliki:</h6>
                <table class="table table-sm">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Action</th>
                            <th>Nama Fitur</th>
                        </tr>
                    </thead>
                    <tbody>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
@endsection

@push('page_scripts')
<script>
    /** * Tabel Utama (Daftar Jabatan)
     */
    var app_list = new Vue({ 
        el      : '#app-list',
        data    : function() {
            return {
                url     : { show : "/olah-fitur/jabatan/data/table" },
                table   : () => { return Table().set($('#app-list').find('table'));   },
                rowData : (el) => { return this.table().getRowData(el.closest('tr')); },
                data    : {
                    columns : [ 
                        { data : "" }, 
                        { data : "details" }, // Kolom tombol untuk buka modal
                        { data : "nama" },
                    ] 
                }
            }
        },
        methods : {
            renderTable : function(filter=null) {
                this.table().destroy().paging().rowNumber()
                    .serverSide(this.data.columns, this.url.show, filter)
                    .init();
            },
            tambahJabatan : function() {
                // Logika jika ingin tambah jabatan baru (bukan fitur)
                Alert().info("Fitur tambah jabatan ada di Master Jabatan");
            }
        },
        mounted : function() {
            let vm = this;
            this.renderTable();

            // Handler klik tombol detail di tabel utama
            this.table().el.on('click', '.btn-detail', function() {
                app_fitur.show(vm.rowData($(this)));
            });
        }
    });

    /** * Modal Management (Setting Fitur per Jabatan)
     */
    var app_fitur = new Vue({ 
        el      : '#app-fitur',
        data    : function() {
            return {
                url   : { 
                    show   : "/olah-fitur/jabatan/data/table2",
                    show2  : "/olah-fitur/jabatan/data/option2",
                    store  : "/olah-fitur/jabatan/insert",
                    delete : "/olah-fitur/jabatan/delete",
                },
                table   : ()   => { return Table().set($('#app-fitur').find('table')); },
                rowData : (el) => { return this.table().getRowData(el.closest('tr')); },
                form    : ()   => { return Form().set($('#app-fitur').find('.form.row')); },
                data    : {
                    columns : [ 
                        { data : "" },
                        { data : "actions" },
                        { data : "nama_fitur" },
                    ] 
                },
                modal     : {id : ''},
                fitur     : {id : '',  data : []},
                nama      : '',
                idJabatan : '',
            }
        },
        methods : {
            loading : function(opsi) { 
                if (opsi == 1) { $('#app-fitur .modal-load').show(); } 
                else { $('#app-fitur .modal-load').hide(); }
            },
            renderTable : function() {
                let filter = null;
                if (!isNull(this.idJabatan)) {
                    filter = { idJabatan : this.idJabatan };
                }
                this.table().destroy().paging().rowNumber().scrollY('350')
                    .serverSide(this.data.columns, this.url.show, filter)
                    .init();
            },
            setOption : function(id) {
                let vm = this;
                // Tambahkan CSRF Token jika dibutuhkan oleh middleware
                $.post(this.url.show2, { id: id, _token: "{{ csrf_token() }}" })
                 .done((data) => { vm.fitur.data = data; });
            },
            getData : function() {
                return {
                    // Jangan kirim _token ke API Python jika API tersebut tidak memvalidasinya
                    id_fitur   : parseInt(this.fitur.id), 
                    id_jabatan : parseInt(this.idJabatan),
                };
            },
            show : function(data){
                if (!isNull(data)) { 
                    this.idJabatan = data.id; 
                    this.nama      = data.nama; 
                    this.setOption(data.id);
                }
                this.renderTable();
                this.modal.id = 1; 
                $("#app-fitur").modal('show');
            },
            submit : function() {
                this.form().confirm().then((result) => {
                    if (result.value == true) {
                        this.loading(1);

                        // Gunakan axios atau ubah setting $.ajax agar mengirim JSON
                        $.ajax({
                            url: this.url.store,
                            type: 'POST',
                            contentType: 'application/json', // Set konten sebagai JSON
                            data: JSON.stringify(this.getData()), // Ubah objek ke string JSON
                            success: (res) => {
                                this.loading(0);
                                Alert().success1();
                                this.renderTable();
                                this.setOption(this.idJabatan);
                                this.fitur.id = "";
                            },
                            error: (err) => {
                                this.loading(0);
                                Alert().error("Gagal menyimpan data");
                            }
                        });
                    }
                });
            },
            delete : function(id) {
                Alert().delete().then((result) => {
                    if (result.value == true) {
                        this.loading(1);
                        $.post(this.url.delete, { id: id, _token: "{{ csrf_token() }}" })
                         .done(() => { 
                             this.loading(0); 
                             Alert().success3(); 
                             this.renderTable(); 
                             this.setOption(this.idJabatan);
                         })
                         .fail(() => { 
                             this.loading(0); 
                             Alert().error(); 
                         });
                    }
                });
            }
        },
        mounted : function() {
            let vm = this;
            // Handler klik tombol hapus di dalam modal
            this.table().el.on('click', '.btn-delete', function() { 
                vm.delete($(this).val()); 
            });
        }
    });
</script>
@endpush