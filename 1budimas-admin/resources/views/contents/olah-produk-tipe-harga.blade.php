@extends('layouts.main')
@section('content')
@include('partials.breadcrumb')
<!-- ============================================================== -->
<!-- Content Container  -->
<!-- ============================================================== -->
<div class="container-fluid">
    <div class="row m-md-1">
        <div class="col-md-12">
            <div class="card form" id="app">
                <div class="card-header">
                    <span class="card-title">Daftar {{ $content->name }}</span>
                </div>
                <div class="card-body card-bar-menu">
                    <div class="btn-group" role="group">
                        <a class="btn btn-danger" href="/olah-produk">
                            <i class="mdi mdi-step-backward"></i>Kembali
                        </a>
                    </div>
                </div>
                <div class="card-body border-bottom">
                    <div class="form row">
                        <div class="col-6">
                            <div class="form-group">
                                <label>Kode</label>
                                <input type="text" v-model="kode" class="form-control-modal" maxlength="50" placeholder="Masukkan Nama {{ $content->name }} (Max 50 Karakter)" required>
                            </div>
                        </div>
                        <div class="col-6">
                            <div class="form-group">
                                <label>Nama</label>
                                <input type="text" v-model="nama" class="form-control-modal" maxlength="50" placeholder="Masukkan Nama {{ $content->name }} (Max 50 Karakter)" required>
                            </div>
                        </div>
                        <div class="col-12">
                            <div class="form-group">
                                <div class="btn-group add" role="group">
                                    <button class="btn btn-success px-4" type="button" @click="submit">
                                        <i class="mdi mdi-plus"></i> Tambah
                                    </button>
                                </div>
                                <div class="btn-group edit" role="group">
                                    <button class="btn btn-danger cancel px-4" type="button">
                                        <i class="mdi mdi-close"></i> Batal Edit
                                    </button>
                                    <button class="btn btn-primary px-4" type="button" @click="submit">
                                        <i class="mdi mdi-pencil"></i> Edit
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="card-body">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Actions</th>
                                <th>Kode</th>
                                <th>Nama</th>
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
@endsection
@push('page_scripts')
<script>
    /** 
     * Modal Produk Brand 
     */
    var app = new Vue({ 
        el      : '#app',
        data    : function() {
            return {
                // URL untuk Akses ke Resources.
                url   : { 
                    show   : "/olah-produk/tipe-harga/data/table",
                    store  : "/olah-produk/tipe-harga/insert",
                    edit   : "/olah-produk/tipe-harga/update",
                    delete : "/olah-produk/tipe-harga/delete",
                },
                // Instance Elemen.
                table  : () => { return Table().set($('#app').find('table')); },
                form   : () => { return Form().set($('#app').find('.form.row')); },
                // Tabel Data.
                data  : {
                    columns : [ 
                        { data : "" },
                        { data : "actions" },
                        { data : "kode" },
                        { data : "nama" },
                    ] 
                },
                modal : {id : ''},
                id    : '',
                kode  : '',
                nama  : '',
            }
        },
        methods : {
            /**
             * Render Tabel dengan Data.
             * Inisiasi Kembali Datatable Instance dengan
             * Data Baru.
             * 
             * @param filter Filter Data yang Akan 
             *               Dirender oleh Tabel.
             */
            renderTable : function(filter=null) {
                this.table().destroy().paging().rowNumber()
                    .serverSide(this.data.columns, this.url.show, filter)
                    .init();
            },
            /**
             * reset Data pada Form.
             */
            resetData : function() {
                this.kode = "";
                this.nama = "";
            },
            /**
             * Set Form Data.
             * 
             * @todo Digunakan untuk Render Data
             *       saat Membuka Edit Form.
             */
            setData : function(data) {
                this.id   = data.id
                this.kode = data.kode;
                this.nama = data.nama;
            },
            /**
             * Get Form Data.
             * 
             * @todo Digunakan untuk Mendapatkan Data
             *       yang Telah Diformat untuk Dikirim.
             */
            getData : function() {
                return {
                    kode : this.kode,
                    nama : this.nama
                };
            },
            /**
             * Form Handler.
             * Render Modal dan Set Form Data Berdasarkan 
             * Tipe yang Dipilih.
             * 
             * @param type 1 : Tambah | 2 : Edit.
             * @param data yang Diambil dari RowData pada
             *             Tabel. Digunakan untuk Set Data
             *             pada Form Edit.
             */
            setForm : function(type, data=null) {
                this.form().validate(0);

                switch (type) {
                    case 1 : // Set Form Tambah
                        this.modal.id = 1;
                        this.form().el.find(".btn-group.edit").hide();
                        this.form().el.find(".btn-group.add").show();
                        this.resetData();
                    break;
                    case 2 : // Set Form Edit
                        this.modal.id = 2;
                        this.form().el.find(".btn-group.edit").show();
                        this.form().el.find(".btn-group.add").hide();
                        this.form().el.find("input, select, textarea").focus();
                        this.setData(data);
                    break;
                }
            },
            /**
             * Form Submit Handler.
             * Submit Form Berdasarkan Tipe Form dari `modal.id`.
             * `modal.id` => 1 : Tambah | 2 : Edit.
             */
            submit : function() {
                this.form().validate(0).validate(1).confirm()
                    .then((result) => {
                        if (result.value == true) {
                            // Before Submitting Actions.
                            block(1);

                            // Submitting Form Tambah.
                            if (this.modal.id == 1) { 
                                $.post(this.url.store, this.getData())
                                 .done(() => { this.renderTable(); block(0); Alert().success1(); })
                                 .fail(() => { this.renderTable(); block(0); Alert().error(); });
                            
                            // Submitting Form Edit.
                            } else if (this.modal.id == 2) { 
                                $.post(this.url.edit, { ...this.getData(), id:this.id })
                                 .done(() => { this.renderTable(); block(0); Alert().success2();  })
                                 .fail(() => { this.renderTable(); block(0); Alert().error(); });
                            }

                            this.setForm(1);

                        } else {
                            Alert().cancel();
                        }
                    });
            },
            delete : function(id) {
                Alert().delete().then((result) => {
                    if (result.value == true) {
                        // Before Submitting Actions.
                        block(1);
                        
                        // Submitting Delete Action.
                        $.post(this.url.delete, {id:id})
                         .done(() => { this.renderTable(); block(0); Alert().success3(); })
                         .fail(() => { this.renderTable(); block(0); Alert().error(); });

                    } else { 
                        Alert().cancel(); 
                    }
                });
            }
        },
        mounted : function() {
            let vm = this;
            this.renderTable();
            this.setForm(1);

            /** 
             * Handler Modal Form untuk Button Batal Edit.
             */ 
            this.form().el.on('click', '.btn.cancel', function() { 
                vm.setForm(1); 
            });
            /** 
             * Handler Modal Form untuk Button Edit.
             */ 
            this.table().el.on('click', '.btn-edit', function() { 
                let rowData = vm.table().getRowData($(this).closest('tr'));
                vm.setForm(2, rowData); 
            });
            /** 
             * Handler Button Delete.
             */ 
            this.table().el.on('click', '.btn-delete', function() { 
                vm.delete($(this).val()); 
            });
        }
    });
</script>
@endpush