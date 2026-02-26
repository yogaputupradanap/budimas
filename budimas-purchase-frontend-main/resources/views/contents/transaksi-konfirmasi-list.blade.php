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
                        <span class="card-title">Daftar Penerimaan Barang</span>
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
                                    <th> # </th>
                                    <th> Detail </th>
                                    <th> No. <em>Transaksi</em> </th>
                                    <th> Kode <em>Order</em> </th>
                                    <th> PIC <em>Penerimaan</em> </th>
                                    <th> Nama <em>Cabang</em> </th>
                                    <th> Nama <em>Principal</em> </th>
                                    <th> Tanggal <em>Penerimaan</em> </th>
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
    <!-- Modal Form  -->
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
                    <span class="modal-title">Detail Konfirmasi Purchase</span>
                    <button type="button" class="btn btn-sm btn-tool modal-close">
                        <i class="mdi mdi-close"></i>
                    </button>
                </div>
                <form method="" action="">
                    @csrf
                    <div class="modal-body">
                        <div class="form row">
                            <div class="col-md-4">
                                <div class="form-group">
                                    <label>No. <em>Transaksi</em></label>
                                    <input type="hidden" name="order_id" v-model="order.id">
                                    <input type="text" v-model="order.no_transaksi" placeholder="" readonly>
                                </div>
                                <div class="form-group">
                                    <label>Tanggal <em>Penerimaan</em></label>
                                    <input type="text" v-model="order.tanggal" class="datepicker"
                                        placeholder="YYYY-MM-DD" readonly>
                                </div>
                                <div class="form-group">
                                    <label>Kode <em>Order</em></label>
                                    <input type="text" v-model="order.order_kode" placeholder="" readonly>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="form-group">
                                    <label><em>Cabang</em></label>
                                    <input type="text" v-model="order.cabang_nama" placeholder="" readonly>
                                </div>
                                <div class="form-group">
                                    <label>PIC <em>Penerimaan</em></label>
                                    <input type="text" v-model="order.user_nama" placeholder="" readonly>
                                </div>
                                <div class="form-group">
                                    <label>Jatuh Tempo <em>Pembayaran</em></label>
                                    <input type="text" name="jatuh_tempo" v-model="order.jatuh_tempo" class="datepicker"
                                        placeholder="YYYY-MM-DD" required>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="form-group">
                                    <label><em>Principal</em></label>
                                    <input type="text" v-model="order.principal_nama" placeholder="" readonly>
                                </div>
                                <div class="form-group">
                                    <label>Keterangan <em>Penerimaan</em></label>
                                    <textarea type="text" v-model="order.keterangan" maxlength="100" placeholder="Max 100 Karater!" readonly></textarea>
                                </div>
                                <div class="form-group">
                                    <label><em>Batch</em></label>
                                    <input type="text" v-model="order.batch" placeholder="" readonly>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="modal-body border-top">
                        <div class="form row">
                            <div class="col-md-4">
                                <div class="form-group">
                                    <label>PIC <em>Konfirmasi</em></label>
                                    <input type="hidden" name="user_jabatan_id" :value="user_jabatan()">
                                    <select2 name="user_id" v-model="user.id" :options="user.data" :readonly="true"
                                        required></select2>
                                </div>
                                <div class="form-group">
                                    <label>Potongan <em>Transaksi</em></label>
                                    <input type="number" name="potongan" v-model="order.potongan" placeholder="Number!">
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="form-group">
                                    <label>Tanggal <em>Konfirmasi</em></label>
                                    <input type="hidden" name="waktu" value="{{ date('H:i:s') }}">
                                    <input type="text" name="tanggal" value="{{ date('Y-m-d') }}" class="datepicker"
                                        placeholder="YYYY-MM-DD" readonly>
                                </div>

                                <div class="form-group" hidden>
                                    <label>Biaya <em>Lainnya</em></label>
                                    <input type="number" name="biaya_lainnya" v-model="order.biaya_lainnya"
                                        placeholder="Number!">
                                </div>
                                <div class="form-group">
                                    <label>Subtotal <em>Transaksi</em></label>
                                    <input type="text" :value="numberToStr(totalAll())" placeholder="Number!" readonly>
                                </div>
                            </div>
                            <div class="col-md-4">

                                <div class="form-group">
                                    <label>Total <em>Transaksi</em></label>
                                    <input type="text" :value="numberToStr(total_transaksi())" placeholder="Number!"
                                        readonly>
                                </div>
                            </div>
                        </div>
                    </div>
                </form>
                <div class="modal-body border-top px-0 pt-0">
                    <div class="table-container">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th> # </th>
                                    <th> Deskripsi </th>
                                    <th> Harga </th>
                                    <th width="16%"> Jml. <em>UOM 3</em> </th>
                                    <th width="16%"> Jml. <em>UOM 2</em> </th>
                                    <th width="16%"> Jml. <em>UOM 1</em> </th>
                                    <th width="16%"> Subtotal </th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(item, index) in filteredDetails" :key="item.id">
                                    <td> @{{ index + 1 }} </td>
                                    <td>
                                        @{{ numberToStr(item.produk_nama) }} <br>
                                        <span class="text-info"> @{{ item.produk_kode }} </span>
                                    </td>
                                    <td> @{{ numberToStr(item.produk_harga_beli) }} </td>
                                    <template v-for="(item2, i2) in item.jumlah" :key="i2">
                                        <td>
                                            @{{ item2.uom_nama }} <br>
                                            <input class="form-control-modal" type="text" v-model="item2.jumlah"
                                                readonly>
                                        </td>
                                    </template>
                                    <td>
                                        <br>
                                        <input type="text" class="form-control-modal"
                                            :value="numberToStr(totalSubtotal[index])" readonly>
                                    </td>
                                </tr>
                            </tbody>
                            <tfoot>
                                <tr>
                                    <td></td>
                                    <td colspan="5"><b>Total<b></td>
                                    <td>
                                        <input type="text" class="form-control-modal" :value="numberToStr(totalAll())"
                                            readonly>
                                    </td>
                                </tr>
                            </tfoot>
                        </table>
                    </div>
                </div>
                <div class="modal-body border-top">
                    <div class="form row mt-3 m-0">
                        <div class="col-md-12">
                            <div class="btn-group float-end" role="group">
                                <button type="button" class="btn btn-success px-4" @click="store">
                                    <i class="mdi mdi-check"></i> Konfirmasi Purchase
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- ============================================================== -->
    <!-- End Modal Form  -->
    <!-- ============================================================== -->
@endsection
@push('page_scripts')
    <script>
        var app_list = new Vue({
            el: '#app-list',
            data: function() {
                return {
                    url: {
                        show: req("/purchase-transaksi/daftar-konfirmasi")
                    },
                    table: () => $('#app-list').find('table'),
                    data: {
                        columns: [{
                                data: ""
                            },
                            {
                                data: "btn_detail"
                            },
                            {
                                data: "no_transaksi"
                            },
                            {
                                data: "order_kode"
                            },
                            {
                                data: "user_nama"
                            },
                            {
                                data: "cabang_nama"
                            },
                            {
                                data: "principal_nama"
                            },
                            {
                                data: "tanggal"
                            }
                        ]
                    }
                }
            },
            methods: {
                renderTable: function(filter = null) {
                    Table().set(this.table()).destroy().paging().rowNumber(true).setDefaultOrder(7, 'desc')
                        .serverSide(this.data.columns, this.url.show, filter)
                        .init();

                    // Tambahkan console.log untuk menampilkan data tabel setelah diinisialisasi
                    this.table().on('xhr.dt', function(e, settings, json, xhr) {
                        console.log('Data yang ditampilkan di tabel:', json.data);
                    });

                    return this;
                },
                actionDetail: function() {
                    this.table().on('click', '.btn-detail', function() {
                        app_detail.render($(this).val());
                    });
                    return this;
                },
            },
            mounted: function() {
                this.renderTable().actionDetail();
            }
        });

        var app_detail = new Vue({
            el: '#app-detail',
            data: function() {
                return {
                    url: {
                        store: "konfirmasi-purchase/store",
                        edit: "purchase-order/edit/:id",
                        destroy: "purchase-order/destroy"
                    },
                    form: () => $("#app-detail").find('form'),
                    user: {
                        data: [],
                        id: '{{ user()->id }}'
                    },
                    order: {
                        jatuh_tempo: '', // Tambahkan ini
                        potongan: 0,
                        biaya_lainnya: 0,
                        detail: []
                    },
                }
            },
            methods: {
                show() {
                    $('#app-detail').modal('show');
                    return this;
                },
                load(opsi) {
                    if (opsi == 1) {
                        $('#app-detail .modal-load').show();
                    } else if (opsi == 0) {
                        $('#app-detail .modal-load').hide();
                    }
                },
                total_transaksi() {
                    const subtotal = this.totalAll();

                    const potongan = parseFloat(this.order.potongan || 0);

                    const ppn = (subtotal - potongan) * 0.11;

                    const biayaLainnya = parseFloat(this.order.biaya_lainnya || 0);

                    return (subtotal - potongan + ppn) + biayaLainnya;
                },
                user_selected() {
                    return this.user.data.find(user => user.id == this.user.id);
                },
                totalAll() {
                    // Pastikan order.detail ada dan berupa array
                    if (!this.order.detail || !Array.isArray(this.order.detail)) {
                        return 0; // Jika tidak ada detail, kembalikan nilai 0
                    }

                    // Penjumlahan subtotal dari semua item di order.detail
                    return this.order.detail.reduce((acc, item) => {
                        // Pastikan item.jumlah ada dan berupa array
                        if (!item.jumlah || !Array.isArray(item.jumlah)) {
                            return acc; // Jika jumlah tidak ada, lanjutkan ke item berikutnya
                        }

                        // Tambahkan subtotal dari setiap item.jumlah
                        return acc + item.jumlah.reduce((subtotalAcc, jumlahItem) => {
                            return subtotalAcc + parseFloat(jumlahItem.subtotal || 0);
                        }, 0);
                    }, 0);
                },
                user_jabatan() {
                    let user = this.user_selected();
                    return user ? user.id_jabatan : null;
                },
                render: function(id, vm = this) {
                    vm.show();
                    vm.load(1);
                    $.get(req(`/purchase-transaksi/detail-riwayat/${id}`))
                        .done((res) => {
                            vm.order = {
                                ...res.data,
                                jatuh_tempo: res.data.jatuh_tempo || '' // Tambahkan ini
                            };
                            console.log('Data yang diambil dari server:', vm.order);
                            vm.load(0);
                            this.$nextTick(() => {
                                $('.datepicker').datepicker({
                                    format: 'yyyy-mm-dd',
                                    autoclose: true,
                                    todayHighlight: true
                                });
                            });
                        })
                        .fail((err) => {
                            console.error('Failed to fetch order details:', err);
                            vm.load(0);
                        });
                },
                initDatepicker: function() {
                    $('.datepicker').not('[readonly]').datepicker({
                        format: 'yyyy-mm-dd',
                        autoclose: true,
                        todayHighlight: true,
                        startDate: new Date()
                    }).on('changeDate', (e) => {
                        if (e.target.name === 'jatuh_tempo') {
                            this.order.jatuh_tempo = e.format('yyyy-mm-dd');
                            console.log('Jatuh Tempo updated:', this.order.jatuh_tempo);
                        }
                    });
                },
                store: function() {
                    const totalTransaksi = this.total_transaksi();

                    // Debug untuk melihat nilai jatuh_tempo
                    console.log('Jatuh Tempo value:', this.order.jatuh_tempo);

                    // Validasi jatuh tempo
                    if (!this.order.jatuh_tempo) {
                        Alert().notice('error', 'gagal', 'Tanggal Jatuh Tempo Pembayaran wajib diisi!');
                        return;
                    }

                    // Validasi tanggal jatuh tempo harus lebih besar dari hari ini
                    const today = new Date();
                    today.setHours(0, 0, 0, 0);
                    const jatuhTempo = new Date(this.order.jatuh_tempo);
                    if (jatuhTempo <= today) {
                        Alert().notice('error', 'gagal',
                            'Tanggal Jatuh Tempo harus lebih besar dari tanggal hari ini!');
                        return;
                    }

                    // Validasi jika Total Transaksi <= 0
                    if (totalTransaksi <= 0) {
                        Alert().notice('error', 'gagal',
                            'Total Transaksi tidak boleh bernilai 0 atau negatif!');
                        console.error('Validasi gagal: Total Transaksi =', totalTransaksi);
                        return;
                    }
                    console.log('Data yang akan dikirim:', this.order);
                    Alert().submit().then((result) => {
                        if (result.value == true) {
                            this.$nextTick(function() {
                                // Pastikan jatuh_tempo termasuk dalam form data
                                const form = this.form();
                                if (!form.find('input[name="jatuh_tempo"]').length) {
                                    form.append(
                                        `<input type="hidden" name="jatuh_tempo" value="${this.order.jatuh_tempo}">`
                                    );
                                }
                                form.attr('method', 'POST')
                                    .attr("action", this.url.store)
                                    .submit();
                            });
                        } else {
                            Alert().cancel();
                        }
                    });
                },
            },
            computed: {
                totalSubtotal() {
                    return this.order.detail.map(item => {
                        return item.jumlah.reduce((acc, jumlahItem) => acc + parseFloat(jumlahItem
                            .subtotal || 0), 0);
                    });
                },

                filteredDetails() {
                    if (!this.order.detail || !Array.isArray(this.order.detail)) {
                        return []
                    }
                    return this.order.detail.filter(item => {
                        if (!item.jumlah || !Array.isArray(item.jumlah)) {
                            return false;
                        }
                        return item.jumlah.some(uomItem => {
                            const value = parseFloat(uomItem.jumlah || 0);
                            return value > 0;
                        });
                    })
                },
            },
            mounted: function(vm = this) {
                $.get(req("/user/option"))
                    .done((res) => {
                        vm.user.data = res.data;
                        console.log('User options:', res.data);
                    })
                    .fail((err) => {
                        console.error('Failed to fetch user options:', err);
                    });
                this.$nextTick(() => {
                    this.initDatepicker();
                });
            }
        });
    </script>
@endpush
