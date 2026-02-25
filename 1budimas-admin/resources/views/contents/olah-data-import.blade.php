@extends('layouts.main')
@section('content')
    @include('partials.breadcrumb')
    <!-- ============================================================== -->
    <!-- Content Container  -->
    <!-- ============================================================== -->
    <div class="container-fluid" id="container-fluid">
        <div class="row m-md-1">
            <div class="col-md-12">
                <form action="" method="POST" class="form-horizontal" enctype="multipart/form-data" id="app-form">
                    <div class="card form">
                        <div class="card-header">
                            <span class="card-title">{{ $content->name }}</span>
                        </div>
                        <div class="card-body card-bar-menu">
                            <div class="btn-group" role="group">
                                <a class="btn btn-danger" href="/dashboard">
                                    <i class="mdi mdi-step-backward"></i>Kembali
                                </a>
                                <a class="btn btn-primary" href="/olah-data/export">
                                    <i class="mdi mdi-table-edit"></i>Export
                                </a>
                            </div>
                        </div>
                        <div class="card-body">
                            <div class="row m-md-2">
                                <div class="col-12 px-md-3">
                                    <div class="input-group">
                                        <div class="form-group w-100">
                                            <label class="text-info">
                                                <i class="mdi mdi-information-outline"></i>
                                                Catatan Penggunaan
                                            </label>
                                            <div class="form-control-modal" style="height:200px; overflow: scroll;">
                                                <ul class="mt-1">
                                                    <li>Panduan lengkap tentang tata cara penggunaan, <strong><a
                                                                href="https://docs.google.com/document/d/1gg2-JkeG7THgdwMlMGUTKeVxUWMoAdMaBk1CmWaqU3k/edit?usp=sharing"
                                                                target="_blank">Baca Di Sini!</a></strong></li>
                                                    <li>Data diupload hanya dalam format <strong>csv</strong></li>
                                                    <li><strong>Karakter spesial</strong> yang dapat diinputkan pada data
                                                        adalah <strong>-, _, +, dan :</strong></li>
                                                    <li>Format yang digunakan untuk data dengan tipe <strong>date</strong>
                                                        adalah <strong>yyyy-mm-dd</strong></li>
                                                    <li>Format yang digunakan untuk data dengan tipe <strong>time</strong>
                                                        adalah <strong>hh:mm:ss</strong></li>
                                                    <li>Data dengan tipe <strong>string</strong> dapat menerima input
                                                        <strong>alfanumerik</strong>
                                                    </li>
                                                    <li>Data dengan tipe <strong>string</strong> memiliki <strong>batas
                                                            maksimal karakter</strong> yang perlu diperhatikan.</li>
                                                    <li>Data dengan tipe <strong>integer</strong> hanya dapat menerima input
                                                        <strong>numerik</strong> saja
                                                    </li>
                                                    <li>Harap <em>menyesuaikan</em> <strong>input data</strong> dengan
                                                        <strong>tipe data</strong> sebelum melakukan upload file
                                                    </li>
                                                    <li>Untuk kolom apa saja yang dapat diupload, dapat dilihat pada bagian
                                                        <strong>kolom atribut</strong> di bawah setelah memilih data.
                                                    </li>
                                                    <li>Nama - nama kolom harus disertakan pada baris pertama dalam file.
                                                    </li>
                                                </ul>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-12 px-md-3">
                                    <div class="input-group">
                                        <div class="form-group w-100">
                                            <label class="text-orange">
                                                <i class="mdi mdi-information-outline"></i>
                                                Kolom Atribut Data
                                            </label>
                                            <div id="list-attr" class="form-control-modal"
                                                style="height:200px; overflow: scroll;">
                                                <ul class="mt-1">
                                                    <li v-for="item in selected">
                                                        <a href="#" v-if="item.length > 1 && item[2]"
                                                            :href="item[2]" target="_blank">
                                                            <b>@{{ item[0] }}</b>
                                                            @{{ item[1] }}
                                                        </a>
                                                        <span v-else><b>@{{ item[0] }}</b>
                                                            @{{ item[1] }}</span>
                                                    </li>
                                                </ul>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6 px-md-3">
                                    @csrf
                                    <div class="input-group">
                                        <div class="form-group w-100">
                                            <label>Data</label>
                                            <div>
                                                <select id="opsi-data" v-model.number="opsi" class="select2 shadow-none"
                                                    name="opsi" required>
                                                    <option value="" selected disabled> Pilih Data </option>
                                                    <option value="1"> Data Cabang </option>
                                                    <option value="2"> Data Perusahaan </option>
                                                    <option value="3"> Data Principal </option>
                                                    <option value="4"> Data Customer - Tipe </option>
                                                    <option value="5"> Data Customer </option>
                                                    <option value="6"> Data Produk - Brand </option>
                                                    <option value="7"> Data Produk - Kategori</option>
                                                    <option value="8"> Data Produk</option>
                                                    <option value="9"> Data Armada</option>
                                                    <option value="10"> Data Plafon</option>
                                                    <option value="11"> Data Sales</option>
                                                    <option value="12"> Data User</option>
                                                </select>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6 px-md-3">
                                    <div class="input-group">
                                        <div class="form-group w-100">
                                            <label>Upload <em>*csv</em></label>
                                            <input type="file" accept=".csv" name="file" value=""
                                                class="form-control-modal" placeholder="Masukkan Username Untuk Login"
                                                id="file_upload" required>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="card-body card-bar-menu border-top">
                            <div class="btn-group float-end" role="group">
                                <button class="btn btn-success mb-1" type="button" @click="submit">
                                    <i class="mdi mdi-check"></i>Submit
                                </button>
                            </div>
                        </div>
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
        var app = new Vue({
            el: '#container-fluid',
            data: function() {
                return {
                    selected: null,
                    file: null,
                    opsi: '',
                    url: 'import'
                }
            },
            methods: {
                fetch: function(opsi) {
                    return new Promise((resolve, reject) => {
                        $.post("import/show", {
                                opsi: opsi
                            })
                            .done(response => {
                                console.log(response);
                                resolve(response);
                            })
                            .fail(error => {
                                reject(error);
                            });
                    });
                },
                load: async function(opsi) {
                    this.selected = await this.fetch(opsi);
                },
                submit: function(event) {
                    const $form = $(this.$el).find('form');
                    if (!validateContainer($form)) {
                        return;
                    }

                    Swal.fire({
                        title: 'Apakah anda yakin?',
                        text: "Data akan diimport ke dalam sistem!",
                        icon: 'warning',
                        showCancelButton: true,
                        confirmButtonColor: '#3085d6',
                        cancelButtonColor: '#d33',
                        confirmButtonText: 'Ya, import data!'
                    }).then((result) => {
                        if (result.isConfirmed) {
                            const fd = new FormData();
                            fd.append('file', this.file);
                            fd.append('_token', $('#csrf').attr('content'));
                            fd.append('opsi', this.opsi);
                            console.log("Submitting form with opsi:", this.opsi);
                            console.log("File to upload:", this.file);
                            $.ajax({
                                url: this.url,
                                method: 'POST',
                                data: fd,
                                processData: false, // PENTING untuk FormData
                                contentType: false, // PENTING agar browser set Content-Type + boundary
                                success: (response) => {
                                    this.resetData();
                                    Alert().success1();
                                    window.location.reload();
                                },
                                error: (xhr, status, error) => {
                                    console.log('Terjadi error!');
                                    console.log('Status:',
                                        status); // contoh: "error" atau "timeout"
                                    console.log('Error message:',
                                        error); // contoh: "Internal Server Error"
                                    console.log('get type of responseJSON:',
                                        typeof xhr.responseJSON);
                                    let msg = safeJSONParse(xhr.responseJSON);

                                    msg = typeof msg === 'object' ? msg.error : msg;
                                    console.log('Get type:', typeof msg);
                                    console.log('Get message:', msg);
                                    Alert().notice('error', 'Gagal mengimport data', msg);
                                }
                            });
                        } else {
                            Alert().cancel();
                        }
                    });
                },
                resetData: function() {
                    this.selected = null;
                    this.file = null;
                    this.opsi = '';
                }
            }
        });

        $("#opsi-data").change(function() {
            let opsi = $(this).val();
            app.opsi = opsi;
            console.log(opsi);
            app.load(opsi);
        })

        $("#file_upload").change(function(event) {
            const file = event.target.files[0];
            app.file = file;
            console.log("File selected:", file);
        });
    </script>
@endpush
