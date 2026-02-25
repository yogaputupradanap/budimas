@extends('layouts.main')
@section('content')
    @include('partials.breadcrumb')
    <!-- ============================================================== -->
    <!-- Content Container  -->
    <!-- ============================================================== -->
    <div class="container-fluid" id="container-fluid">
        <div class="row m-md-1">
            <div class="col-md-12">
                <form action="" method="post" id="form-export" class="form-horizontal" enctype="multipart/form-data">
                    <div class="card form">
                        <div class="card-header">
                            <span class="card-title">{{ $content->name }}</span>
                        </div>
                        <div class="card-body card-bar-menu">
                            <div class="btn-group" role="group">
                                <a class="btn btn-danger" href="/olah-data/import">
                                    <i class="mdi mdi-step-backward"></i>Kembali
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
                                                    <li>Mohon untuk <strong>pilih data</strong> terlebih dahulu sebelum
                                                        melakukan export.</li>
                                                    <li>Setelah memilih data, klik button <strong>Unduh *CSV</strong>.</li>
                                                    <li>Format dari file hasil export adalah <strong>csv</strong>.</li>
                                                    <li>Harap menunggu hingga file Terunduh.</li>
                                                    <li>Apabila file berhasil diunduh, akan ada <strong>notifikasi dari
                                                            browser</strong>.</li>
                                                    <li>Apabila tidak ada notifikasi dengan rentan waktu yang cukup lama,
                                                        silahkan <strong>refresh kembali</strong> halaman dan melakukan
                                                        export ulang.</li>
                                                    <li>Untuk data dengan ukuran yang besar, waktu unduh akan <strong>lebih
                                                            lama</strong>, sehingga dimohon untuk dapat menunggu.</li>
                                                </ul>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-12 px-md-3">
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
                                                    <option value="5"> Data Produk - Brand </option>
                                                    <option value="6"> Data Produk - Kategori</option>
                                                    <option value="7"> Data Produk - Satuan</option>
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
                            </div>
                        </div>
                        <div class="card-body card-bar-menu border-top">
                            <div class="btn-group float-end" role="group">
                                <button type="button" id="csv-download" class="btn btn-success mb-1" @click="submit"><i
                                        class="mdi mdi-check"></i> Unduh *CSV</button>
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
                    opsi: '',
                }
            },
            methods: {
                submit: function(event) {
                    console.log("Submit Export CSV with Opsi:", this.opsi);
                    const $form = $(this.$el).find('form');
                    if (!validateContainer($form)) {
                        return;
                    }
                    block(1);
                    $.post("", {
                        opsi: this.opsi,
                    }).done((response) => {
                        console.log("CSV Download Response:", response);
                        csvDownload(response);
                        block(0);
                        Alert().notice('success', 'Berhasil!', 'Proses unduh CSV berhasil.');
                    }).fail((xhr, status, error) => {
                        console.error("CSV Download Error:", error);
                        block(0);
                        // Alert().custom('error', 'Gagal!', 'Terjadi kesalahan saat unduh CSV.');
                        Alert().notice('error', 'Keslaahan', 'Gagal mengunduh CSV. Silahkan coba lagi.');
                    });
                }
            }
        });

        $("#opsi-data").change(function() {
            let opsi = $(this).val();
            app.opsi = opsi ? Number(opsi) : '';
            console.log("opsi (from DOM change):", opsi);
        });
    </script>
@endpush
