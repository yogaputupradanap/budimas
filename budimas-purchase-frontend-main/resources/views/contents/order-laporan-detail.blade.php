@extends('layouts.main')
@section('content')
    @include('partials.breadcrumb')
    <!-- Content Container -->
    <div class="container-fluid" id="app-detail">
        <div class="row m-1">
            <div class="col-12">
                <div class="card pb-xxl-5">
                    <div class="card-header">
                        <span class="card-title">Detail Order</span>
                    </div>
                    <div class="card-body card-bar-menu">
                        <div class="btn-group" role="group">
                            <a class="btn btn-danger" onclick="window.history.back()">
                                <i class="mdi mdi-step-backward"></i>Kembali
                            </a>
                        </div>
                    </div>
                    <div class="card-body">
                        <div class="form row">
                            <div class="col-md-4">
                                <div class="form-group">
                                    <label>Kode <em>Order</em></label>
                                    <input type="hidden" name="order_id" v-model="order.id">
                                    <input type="text" v-model="order.kode" class="form-control" readonly>
                                </div>
                                <div class="form-group">
                                    <label>Tanggal <em>Request</em></label>
                                    <input type="text" v-model="request_log.tanggal" class="form-control" readonly>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="form-group">
                                    <label><em>Cabang</em></label>
                                    <select2 v-model="order.cabang_id" :options="cabang.data" :readonly="true"
                                        required></select2>
                                </div>
                                <div class="form-group">
                                    <label>PIC <em>Request</em></label>
                                    <select2 v-model="request_log.user_id" :options="user.data" :readonly="true"
                                        required></select2>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="form-group">
                                    <label><em>Principal</em></label>
                                    <select2 v-model="order.principal_id" :options="principal.data" :readonly="true"
                                        required></select2>
                                </div>
                                <div class="form-group">
                                    <label>Keterangan <em>Order</em></label>
                                    <textarea class="form-control" v-model="order.keterangan" readonly></textarea>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="card-body border-top">
                        <div class="form row">
                            <div class="col-md-4">
                                <div class="form-group">
                                    <label>Tanggal <em>Konfirmasi</em></label>
                                    <input type="text" v-model="konfirmasi_log.tanggal" class="form-control" readonly>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="form-group">
                                    <label>PIC <em>Konfirmasi</em></label>
                                    <input type="text" v-model="konfirmasi_log.user_nama" class="form-control" readonly>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="form-group">
                                    <label>Status</label>
                                    <input type="text" class="form-control" readonly
                                        :value="statusFormat(order.proses_id_berjalan)">
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="table-container h-600">
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
                            <tbody v-for="(item, index) in order.detail">
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
                                            <input class="form-control" type="text" v-model="item2.jumlah" readonly>
                                        </td>
                                    </template>
                                    <td>
                                        <br>
                                        <input type="text" class="form-control"
                                            :value="numberToStr(calculateItemSubtotal(item))" readonly>
                                    </td>
                                </tr>
                            </tbody>
                            <tfoot>
                                <tr>
                                    <td></td>
                                    <td colspan="5"><b>Total</b></td>
                                    <td>
                                        <input type="text" class="form-control" :value="numberToStr(order.total)"
                                            readonly>
                                    </td>
                                </tr>
                            </tfoot>
                        </table>
                    </div>
                </div>
            </div>
        </div>

        <!-- Purchase Table Section -->
        <div class="row m-1 mt-4" v-if="order.proses_id_berjalan >= 3">
            <div class="col-12">
                <div class="card" id="purchase-table">
                    <div class="card-header">
                        <span class="card-title">Daftar Purchase</span>
                    </div>
                    <div class="card-body">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th>#</th>
                                    <th>Detail</th>
                                    <th>Cetak</th>
                                    <th>No. <em>Transaksi</em></th>
                                    <th>PIC <em>Penerimaan</em></th>
                                    <th>Nama <em>Cabang</em></th>
                                    <th>Nama <em>Principal</em></th>
                                    <th>Tanggal <em>Purchase</em></th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

        <!-- Purchase Detail Modal -->
        <div class="modal fade" id="modal-purchase-detail">
            <div class="modal-dialog modal-xl">
                <div class="modal-content">
                    <div class="modal-load">
                        <div class="lds-ripple">
                            <div class="lds-pos"></div>
                            <div class="lds-pos"></div>
                        </div>
                    </div>
                    <div class="modal-header">
                        <span class="modal-title">Detail Purchase</span>
                        <button type="button" class="btn btn-sm btn-tool modal-close" @click="closePurchaseModal">
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
                                        <input type="text" v-model="selectedPurchase.no_transaksi"
                                            class="form-control" readonly>
                                    </div>
                                    <div class="form-group">
                                        <label>Tanggal <em>Penerimaan</em></label>
                                        <input type="text" v-model="penerimaan_log.tanggal" class="form-control"
                                            readonly>
                                    </div>
                                    <div class="form-group">
                                        <label>Kode <em>Order</em></label>
                                        <input type="text" v-model="selectedPurchase.order_kode" class="form-control"
                                            readonly>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="form-group">
                                        <label><em>Cabang</em></label>
                                        <input type="text" v-model="selectedPurchase.cabang_nama" class="form-control"
                                            readonly>
                                    </div>
                                    <div class="form-group">
                                        <label>PIC <em>Penerimaan</em></label>
                                        <input type="text" v-model="penerimaan_log.user_nama" class="form-control"
                                            readonly>
                                    </div>
                                    <div class="form-group">
                                        <label>Status</label>
                                        <input type="text" class="form-control"
                                            :value="purchaseStatusFormat(selectedPurchase.proses_id_berjalan)" readonly>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="form-group">
                                        <label><em>Principal</em></label>
                                        <input type="text" v-model="selectedPurchase.principal_nama"
                                            class="form-control" readonly>
                                    </div>
                                    <div class="form-group">
                                        <label>Keterangan <em>Penerimaan</em></label>
                                        <textarea v-model="selectedPurchase.keterangan" class="form-control" readonly></textarea>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="modal-body border-top">
                            <div class="form row">
                                <div class="col-md-4">
                                    <div class="form-group">
                                        <label>PIC <em>Konfirmasi</em></label>
                                        <input type="text" v-model="konfirmasi_log.user_nama" class="form-control"
                                            readonly>
                                    </div>
                                    <div class="form-group">
                                        <label>Potongan <em>Transaksi</em></label>
                                        <input type="text" v-model="selectedPurchase.potongan" class="form-control"
                                            readonly>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="form-group">
                                        <label>Tanggal <em>Konfirmasi</em></label>
                                        <input type="text" v-model="konfirmasi_log.tanggal" class="form-control"
                                            readonly>
                                    </div>
                                    <div class="form-group">
                                        <label>Biaya <em>Lainnya</em></label>
                                        <input type="text" v-model="selectedPurchase.biaya_lainnya"
                                            class="form-control" readonly>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="form-group">
                                        <label>Subtotal <em>Transaksi</em></label>
                                        <input type="text" :value="numberToStr(calculatePurchaseTotal())"
                                            class="form-control" readonly>
                                    </div>
                                    <div class="form-group">
                                        <label>Total <em>Transaksi</em></label>
                                        <input type="text" :value="numberToStr(totalTransaksi)" class="form-control"
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
                                        <th>#</th>
                                        <th>Deskripsi</th>
                                        <th>Harga</th>
                                        <th width="16%">Jml. <em>UOM 3</em></th>
                                        <th width="16%">Jml. <em>UOM 2</em></th>
                                        <th width="16%">Jml. <em>UOM 1</em></th>
                                        <th width="16%">Subtotal</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="(item, index) in selectedPurchase.detail" :key="index">
                                        <td>@{{ index + 1 }}</td>
                                        <td>
                                            @{{ numberToStr(item.produk_nama) }}<br>
                                            <span class="text-info">@{{ item.produk_kode }}</span>
                                        </td>
                                        <td>@{{ numberToStr(item.produk_harga_beli) }}</td>
                                        <template v-for="(jumlah, i) in item.jumlah" :key="i">
                                            <td>
                                                @{{ jumlah.uom_nama }}<br>
                                                <input class="form-control" type="text" v-model="jumlah.jumlah"
                                                    readonly>
                                            </td>
                                        </template>
                                        <td>
                                            <br>
                                            <input type="text" class="form-control"
                                                :value="numberToStr(itemSubtotal(item))" readonly>
                                        </td>
                                    </tr>
                                </tbody>
                                <tfoot>
                                    <tr>
                                        <td colspan="6"><b>Total</b></td>
                                        <td>
                                            <input type="text" class="form-control"
                                                :value="numberToStr(calculatePurchaseTotal())" readonly>
                                        </td>
                                    </tr>
                                </tfoot>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
@endsection

@push('page_scripts')
    <script>
        var app_detail = new Vue({
            el: '#app-detail',
            data: function() {
                return {
                    user: {
                        data: [],
                        id: ''
                    },
                    cabang: {
                        data: [],
                        id: ''
                    },
                    principal: {
                        data: [],
                        id: ''
                    },
                    order: {},
                    request_log: {},
                    konfirmasi_log: {},
                    selectedPurchase: {
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
                    penerimaan_log: {},
                    konfirmasi_log: {},
                    url: {
                        show: req('/purchase-transaksi/daftar-laporan')
                    },
                    purchaseTable: () => $('#purchase-table').find('table'),
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
            },
            computed: {
                subtotalTransaksi() {
                    return this.selectedPurchase.detail.reduce((acc, item) => acc + this.itemSubtotal(item), 0);
                },
                totalTransaksi() {
                    const subtotal = this.subtotalTransaksi;
                    const potongan = parseFloat(this.selectedPurchase.potongan) || 0;
                    const biayaLainnya = parseFloat(this.selectedPurchase.biaya_lainnya) || 0;
                    const total = subtotal - potongan;
                    const ppn = total * 0.11; // 11% PPN
                    return total + ppn + biayaLainnya;
                }
            },
            methods: {
                loadData() {
                    const id = window.location.pathname.split('/').pop();
                    $.get(req(`/purchase-order/detail-purchase-laporan/${id}`))
                        .done((res) => {
                            this.order = res.data;
                            this.request_log = res.data.request_log || {};
                            this.konfirmasi_log = res.data.konfirmasi_log || {};

                            if (this.order.proses_id_berjalan >= 3) {
                                this.$nextTick(() => {
                                    this.renderPurchaseTable(id);
                                });
                            }
                        })
                        .fail((err) => {
                            console.error('Failed to fetch order data:', err);
                        });
                },
                calculateItemSubtotal(item) {
                    if (!item.jumlah) return 0;
                    return item.jumlah.reduce((acc, jumlahItem) => acc + (parseFloat(jumlahItem.subtotal) || 0), 0);
                },

                renderPurchaseTable(orderId) {
                    Table()
                        .set(this.purchaseTable())
                        .destroy()
                        .paging()
                        .rowNumber(true)
                        .serverSide(
                            this.columns,
                            `${this.url.show}/${orderId}`,
                            null
                        )
                        .init();

                    this.actionDetail();
                    return this;
                },

                actionDetail() {
                    this.purchaseTable().on('click', '.btn-detail', (e) => {
                        e.preventDefault();
                        let row = $(e.currentTarget).closest('tr');
                        let data = this.getTableRowData(row);
                        this.showPurchaseDetail(data);
                    });
                    return this;
                },

                getTableRowData(row) {
                    return this.purchaseTable().DataTable().row(row).data();
                },
                showPurchaseDetail(purchase) {
                    this.loadModalData(1);
                    $.get(req(`/purchase-transaksi/detail-riwayat/${purchase.id}`))
                        .done((res) => {
                            this.selectedPurchase = res.data;
                            this.penerimaan_log = res.data.penerimaan_log || {};
                            this.konfirmasi_log = res.data.konfirmasi_log || {};
                            this.loadModalData(0);
                            $('#modal-purchase-detail').modal('show');
                        })
                        .fail((err) => {
                            console.error('Failed to fetch purchase details:', err);
                            this.loadModalData(0);
                        });
                },

                loadModalData(opsi) {
                    if (opsi == 1) {
                        $('#modal-purchase-detail .modal-load').show();
                    } else if (opsi == 0) {
                        $('#modal-purchase-detail .modal-load').hide();
                    }
                },

                closePurchaseModal() {
                    $('#modal-purchase-detail').modal('hide');
                    this.selectedPurchase = {
                        detail: [],
                        potongan: 0,
                        biaya_lainnya: 0
                    };
                    this.penerimaan_log = {};
                    this.konfirmasi_log = {};
                },

                statusFormat(status) {
                    const statusMap = {
                        1: 'Request',
                        2: 'Need Confirm',
                        3: 'In Transit',
                        4: 'Closed'
                    };
                    return statusMap[status] || '';
                },

                purchaseStatusFormat(status) {
                    if (status == 1) return 'Penerimaan Brg.';
                    if (status == 2) return 'Konfirmasi';
                    if (status == 3) return 'Pem. Tagihan';
                    if (status == 4) return 'Pelunasan';
                    if (status == 5) return 'Lunas';
                    return '';
                },

                itemSubtotal(item) {
                    if (!item.jumlah) return 0;
                    return item.jumlah.reduce((acc, jumlahItem) => acc + (parseFloat(jumlahItem.subtotal) || 0), 0);
                },

                calculatePurchaseTotal() {
                    if (!this.selectedPurchase.detail) return 0;
                    return this.selectedPurchase.detail.reduce((total, item) => total + this.itemSubtotal(item), 0);
                },
            },
            mounted: function() {
                // Load initial data
                $.get(req("/cabang/option"))
                    .done((res) => {
                        this.cabang.data = res.data;
                        console.log('Cabang data:', res.data);
                    })
                    .fail((err) => console.error('Failed to fetch cabang data:', err));

                $.get(req("/user/option"))
                    .done((res) => {
                        this.user.data = res.data;
                        console.log('User data:', res.data);
                    })
                    .fail((err) => console.error('Failed to fetch user data:', err));

                $.get(req("/principal/option"))
                    .done((res) => {
                        this.principal.data = res.data;
                        console.log('Principal data:', res.data);
                    })
                    .fail((err) => console.error('Failed to fetch principal data:', err));

                this.loadData();

                // Initialize modal events
                $('#modal-purchase-detail').on('hidden.bs.modal', () => {
                    this.closePurchaseModal();
                });

                // Initialize DataTable events
                this.purchaseTable().on('draw.dt', () => {
                    console.log('Purchase table data:', this.purchaseTable().DataTable().data()
                        .toArray());
                });
            }
        });
    </script>
@endpush
