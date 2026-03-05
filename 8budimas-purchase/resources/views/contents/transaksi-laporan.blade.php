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
                        <span class="card-title">Laporan Purchase</span>
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
                                    <th> Cetak </th>
                                    <th> No. <em>Transaksi</em> </th>
                                    <th> PIC <em>Penerimaan</em> </th>
                                    <th> Nama <em>Cabang</em> </th>
                                    <th> Nama <em>Principal</em> </th>
                                    <th> Tanggal <em>Purchase</em> </th>
                                    <th> Status </th>
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
                                    <input type="text" v-model="penerimaan_log.tanggal" class="datepicker"
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
                                    <input type="text" v-model="penerimaan_log.user_nama" placeholder="" readonly>
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
                            </div>
                        </div>
                    </div>
                    <div class="modal-body border-top">
                        <div class="form row">
                            <div class="col-md-4">
                                <div class="form-group">
                                    <label>PIC <em>Konfirmasi</em></label>
                                    <input type="text" v-model="konfirmasi_log.user_nama" readonly>
                                </div>
                                <div class="form-group">
                                    <label>Potongan <em>Transaksi</em></label>
                                    <input type="text" v-model="order.potongan" readonly>
                                </div>
                                <div class="form-group">
                                    <label>Status</label>
                                    <input type="text" class="form-control-modal" readonly
                                        :value="statusFormat(order.proses_id_berjalan)">
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="form-group">
                                    <label>Tanggal <em>Konfirmasi</em></label>
                                    <input type="text" v-model="konfirmasi_log.tanggal" class="datepicker"
                                        placeholder="YYYY-MM-DD" readonly>
                                </div>
                                <div class="form-group">
                                    <label>Biaya <em>Lainnya</em></label>
                                    <input type="text" v-model="order.biaya_lainnya" readonly>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="form-group">
                                    <label>Subtotal <em>Transaksi</em></label>
                                    <input type="text" :value="numberToStr(subtotalTransaksi)" placeholder="Number!"
                                        readonly>
                                </div>
                                <div class="form-group">
                                    <label>Total <em>Transaksi</em></label>
                                    <input type="text" :value="numberToStr(totalTransaksi)" placeholder="Number!"
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
                            <tbody v-for="(item, index) in order.detail" :key="index">
                                <tr>
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
                                            :value="numberToStr(itemSubtotal(item))" readonly>
                                    </td>
                                </tr>
                            </tbody>
                            <tfoot>
                                <tr>
                                    <td></td>
                                    <td colspan="5"><b>Total</b></td>
                                    <td>
                                        <input type="text" class="form-control-modal"
                                            :value="numberToStr(subtotalTransaksi)" readonly>
                                    </td>
                                </tr>
                            </tfoot>
                        </table>
                    </div>
                </div>
                {{-- <div class="modal-body border-top">
                    <div class="form row mt-3 m-0">
                        <div class="col-md-12">
                            <div class="btn-group float-end" role="group">
                                <button type="button" class="btn btn-success px-4" @click="store">
                                    <i class="mdi mdi-check"></i> Konfirmasi Order
                                </button>
                            </div>
                        </div>
                    </div>
                </div> --}}
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
                        show: req('/purchase-transaksi/daftar-laporan'),
                        edit: "penerimaan-barang/create/:id",
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
                                data: "btn_cetak"
                            },
                            {
                                data: "no_transaksi"
                            },
                            {
                                data: "penerimaan_user_nama"
                            },
                            {
                                data: "cabang_nama"
                            },
                            {
                                data: "principal_nama"
                            },
                            {
                                data: "tanggal"
                            },
                            {
                                data: "btn_status"
                            },
                        ]
                    }
                }
            },
            methods: {
                getTableRowData: function(row) {
                    let data = this.table().DataTable().row(row).data();
                    console.log('Row data:', data); // Menampilkan data baris yang dipilih
                    return data;
                },
                renderTable: function(filter = null) {
                    Table().set(this.table()).destroy().paging().rowNumber(true)
                        .serverSide(this.data.columns, this.url.show, filter)
                        .init();
                    return this;
                },
                actionDetail: function() {
                    this.table().on('click', '.btn-detail', function() {
                        app_detail.render($(this).val());
                    });
                    return this;
                },
            },
            mounted: function(vm = this) {
                this.renderTable().actionDetail();
                this.table().on('draw.dt', function() {
                    console.log('Table data:', vm.table().DataTable().data().toArray());
                });
                console.log('Component mounted'); // Log saat komponen dipasang
            }
        });

        var app_detail = new Vue({
            el: '#app-detail',
            data: function() {
                return {
                    user: {
                        id: '',
                        data: []
                    },
                    order: {
                        detail: [],
                        potongan: 0,
                        biaya_lainnya: 0,
                        penerimaan_log: {
                            tanggal: '',
                            user_nama: ''
                        },
                        konfirmasi_log: {
                            tanggal: '',
                            user_nama: ''
                        },
                    },
                }
            },
            computed: {
                subtotalTransaksi() {
                    return this.order.detail.reduce((acc, item) => acc + this.itemSubtotal(item), 0);
                },
                totalTransaksi() {
                    const subtotal = this.subtotalTransaksi;
                    const potongan = parseFloat(this.order.potongan) || 0;
                    const biayaLainnya = parseFloat(this.order.biaya_lainnya) || 0;
                    const total = subtotal - potongan + biayaLainnya;
                    const ppn = total * 0.11; // 11% PPN
                    return total + ppn;
                },
                penerimaan_log() {
                    return this.order.penerimaan_log || {};
                },
                konfirmasi_log() {
                    return this.order.konfirmasi_log || {};
                },
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
                itemSubtotal(item) {
                    return item.jumlah.reduce((acc, jumlahItem) => acc + (parseFloat(jumlahItem.subtotal) || 0), 0);
                },
                user_selected() {
                    return this.user.data.find(user => user.id == this.user.id);
                },
                user_nama() {
                    let user = this.user_selected();
                    return user ? user.nama : null;
                },
                statusFormat(status) {
                    if (status == 1) return 'Penerimaan Brg.';
                    if (status == 2) return 'Konfirmasi';
                    if (status == 3) return 'Pem. Tagihan';
                    if (status == 4) return 'Pelunasan';
                },
                render(id) {
                    this.show();
                    this.load(1);
                    $.get(req(`/purchase-transaksi/detail-riwayat/${id}`))
                        .done((res) => {
                            this.order = res.data;
                            this.load(0);
                            console.log('Order data:', this.order); // For debugging
                        })
                        .fail((err) => {
                            console.error('Failed to fetch order details:', err);
                            this.load(0);
                        });
                },
            },
            mounted: function() {
                $.get(req("/user/option"))
                    .done((res) => {
                        this.user.data = res.data;
                    })
                    .fail((err) => {
                        console.error('Failed to fetch user options:', err);
                    });
            }
        });
    </script>
@endpush
