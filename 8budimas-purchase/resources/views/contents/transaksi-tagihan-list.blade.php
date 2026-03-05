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
                        <span class="card-title">Daftar Faktur</span>
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
                                    <th> Pilih </th>
                                    <th> No. <em>Transaksi</em> </th>
                                    <th> Kode <em>Order</em> </th>
                                    <th> PIC <em>Penerimaan</em> </th>
                                    <th> Nama <em>Cabang</em> </th>
                                    <th> Nama <em>Principal</em> </th>
                                    <th> Tanggal <em>Jatuh Tempo</em> </th>
                                </tr>
                            </thead>
                            <tbody>
                            </tbody>
                        </table>
                    </div>
                    <div class="card-body border-top">
                        <div class="form row mt-3 m-0">
                            <div class="col-md-12">
                                <div class="btn-group float-end" role="group">
                                    <button type="button" class="btn btn-success px-4" @click="actionSubmit()">
                                        <i class="mdi mdi-check"></i> Buat Tagihan
                                    </button>
                                </div>
                            </div>
                        </div>
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
                    <span class="modal-title">Detail Konfirmasi Order</span>
                    <button type="button" class="btn btn-sm btn-tool modal-close">
                        <i class="mdi mdi-close"></i>
                    </button>
                </div>
                <div class="modal-body">
                    <form method="" action="">
                        @csrf
                        <input type="hidden" name="order_id" v-model="order.request.id">
                        <input type="hidden" name="kode" v-model="order.request.kode">
                        <input type="hidden" name="tanggal" value="{{ date('Y-m-d') }}">
                        <input type="hidden" name="waktu" value="{{ date('H:i:s') }}">
                        <input type="hidden" name="user_id" value="{{ user()->id }}">
                        <input type="hidden" name="user_jabatan_id" value="{{ user()->id_jabatan }}">
                    </form>
                    <div class="form row">
                        <div class="col-md-4">
                            <div class="form-group">
                                <label>No. <em>Faktur</em></label>
                                <input type="text" v-model="order.request.kode" class="form-control-modal"
                                    placeholder="Masukkan Kode Request" readonly>
                            </div>
                            <div class="form-group">
                                <label>Kode <em>Order</em></label>
                                <input type="text" v-model="order.request.kode" class="form-control-modal"
                                    placeholder="Masukkan Kode Request" readonly>
                            </div>
                            <div class="form-group">
                                <label>Tanggal <em>Penerimaan</em></label>
                                <input type="text" v-model="order.request.tanggal" class="form-control-modal datepicker"
                                    placeholder="YYYY-MM-DD" readonly>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="form-group">
                                <label>Nama <em>Cabang</em></label>
                                <input type="text" v-model="order.request.cabang_nama" class="form-control-modal"
                                    placeholder="Masukkan Cabang" readonly>
                            </div>
                            <div class="form-group">
                                <label>PIC <em>Penerimaan</em></label>
                                <input type="text" v-model="order.request.user_nama" class="form-control-modal"
                                    placeholder="Max 50 Karakter" readonly>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="form-group">
                                <label>Nama <em>Principal</em></label>
                                <input type="text" v-model="order.request.principal_nama" class="form-control-modal"
                                    placeholder="Masukkan Principal" readonly>
                            </div>
                            <div class="form-group">
                                <label>Keterangan <em>Penerimaan</em></label>
                                <textarea type="text" v-model="order.request.keterangan" class="form-control-modal" maxlength="100"
                                    placeholder="Max 100 Karater!" readonly></textarea>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-body border-top">
                    <div class="form row">
                        <div class="col-md-4">
                            <div class="form-group">
                                <label>SubTotal <em>Transaksi</em></label>
                                <input type="text" class="form-control-modal" placeholder="" readonly>
                            </div>
                            <div class="form-group">
                                <label>Total <em>Transaksi</em></label>
                                <input type="number" class="form-control-modal" placeholder="" readonly>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="form-group">
                                <label>Potongan <em>Transaksi</em></label>
                                <input type="number" class="form-control-modal" placeholder="">
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="form-group">
                                <label>Biaya <em>Lainnya</em></label>
                                <input type="number" class="form-control-modal" placeholder="">
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-body border-top px-0 pt-0">
                    <div class="table-container h-600">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th> # </th>
                                    <th> No. Transaksi </th>
                                    <th> Kode Order </th>
                                    <th width="20%"> Subtotal </th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(row, index) in selectedRows" :key="row.no_transaksi">
                                    <td> @{{ index + 1 }} </td>
                                    <td> @{{ row.no_transaksi }} </td>
                                    <td> @{{ row.order_kode }} </td>
                                    <td> @{{ row.subtotal || 0 }} </td>
                                </tr>
                            </tbody>
                            <tfoot>
                                <tr>
                                    <td></td>
                                    <td><b>Total<b></td>
                                    <td></td>
                                    <td>
                                        <input type="text" class="form-control-modal"
                                            :value="selectedRows.reduce((sum, row) => sum + (parseFloat(row.subtotal) || 0), 0)
                                                .toFixed(2)"
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
                                <button type="button" class="btn btn-success px-4" @click="store()">
                                    <i class="mdi mdi-check"></i> Konfirmasi Pembuatan Tagihan
                                </button>
                                <!-- <button type="button" class="btn btn-primary px-4" @click="edit" disabled>
                                                                                                    <i class="mdi mdi-lead-pencil"></i> Edit Order
                                                                                                </button>
                                                                                                <button type="button" class="btn btn-danger px-4" @click="destroy()">
                                                                                                    <i class="mdi mdi-delete"></i> Batalkan Order
                                                                                                </button> -->
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
                    selectedRows: [],
                    url: {
                        show: baseURL + "/purchase-transaksi/show/table/list-proses-tagihan"
                    },
                    table: () => $('#app-list').find('table'),
                    data: {
                        columns: [{
                                data: ""
                            },
                            {
                                data: "btn_check"
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
                            },
                        ]
                    }
                }
            },
            methods: {
                getTableRowData: function(row) {
                    return this.table().DataTable().row(row).data();
                },
                renderTable: function(filter = null) {
                    Table().set(this.table()).destroy().paging().rowNumber(true)
                        .serverSide(this.data.columns, this.url.show, filter)
                        .init();

                    return this;
                },
                actionBtnDetail: function(vm = this) {
                    this.table().on('click', '.btn-detail', function() {
                        let rowIndex = $(this).closest('tr');
                        let rowData = vm.getTableRowData(rowIndex);

                        app_detail.renderData(rowData);
                        $('#app-detail').modal('show');
                    });
                    return this;
                },
                actionSubmit: function() {
                    if (this.selectedRows.length === 0) {
                        Alert().notice('warning', 'required', 'Pilih data terlebih dahulu!');
                        return;
                    }
                    app_detail.renderData(this.selectedRows);
                    $('#app-detail').modal('show');
                },
                toggleSelection: function(rowData) {
                    const index = this.selectedRows.findIndex(row => row.no_transaksi === rowData.no_transaksi);
                    if (index > -1) {
                        this.selectedRows.splice(index, 1);
                    } else {
                        this.selectedRows.push(rowData);
                    }
                }
            },
            mounted: function(vm = this) {
                this.renderTable().actionBtnDetail();

                // Add event listener for checkbox changes
                this.table().on('change', 'input[type="checkbox"]', function() {
                    const rowData = vm.getTableRowData($(this).closest('tr'));
                    vm.toggleSelection(rowData);
                });
            }
        });

        var app_detail = new Vue({
            el: '#app-detail',
            data: function() {
                return {
                    url: {
                        show1: "/purchase-order/data/detail",
                        show2: "/olah-user/data/option1",
                        show3: "/olah-user/data/option5",
                        store: "konfirmasi-order/store",
                        edit: "purchase-order/edit/:id",
                        destroy: "purchase-order/destroy"
                    },
                    form: () => $("#app-detail").find('form'),
                    produk: {
                        table: {
                            data: []
                        }
                    },
                    order: {
                        request: {
                            id: '',
                            kode: '',
                            keterangan: '',
                            nama_cabang: '',
                            nama_principal: '',
                            nama_user: '',
                            tanggal: '',
                        },
                    },
                    konfirmasi1: {
                        id_proses: null,
                        user: {
                            id: '{{ user()->id }}',
                            text: [],
                            data: {
                                all: [],
                                selected: {
                                    id_jabatan: null
                                }
                            }
                        },
                    },
                    konfirmasi2: {
                        id_proses: null,
                        user: {
                            id: '',
                            text: [],
                            data: {
                                all: [],
                                selected: {
                                    id_jabatan: null
                                }
                            }
                        },
                    },
                    konfirmasi3: {
                        id_proses: null,
                        user: {
                            id: '',
                            text: [],
                            data: {
                                all: [],
                                selected: {
                                    id_jabatan: null
                                }
                            }
                        },
                    },
                    user1: {
                        text: []
                    },
                    user2: {
                        text: []
                    },
                    selectedRows: []
                }
            },
            methods: {
                loading: function(opsi) {
                    if (opsi == 1) {
                        $('#app-detail .modal-load').show();
                    } else if (opsi == 0) {
                        $('#app-detail .modal-load').hide();
                    }
                },
                setOption: function(vm = this) {
                    $.post(this.url.show2, {
                            display: ['nik', 'nama', 'nama_cabang']
                        })
                        .done((data) => {
                            vm.konfirmasi1.user.text = data;
                            vm.konfirmasi2.user.text = data;
                            vm.konfirmasi3.user.text = data;
                        });
                },
                renderData: function(data, vm = this) {
                    this.loading(1);
                    this.selectedRows = data;
                    console.log("data", data);
                    this.loading(0);
                },


                // /**
                //  * Set Form Action URL & Method
                //  * untuk Simpan Data dan Submit.
                //  */
                store: function() {
                    // this.request.id_proses = '3';

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
                destroy: function() {
                    // this.request.id_proses = '2';

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
                edit: function() {
                    window.location.href = this.url.edit.replace(":id", this.order.request.id);
                }
            },
            mounted: function(vm = this) {
                this.setOption();
            },
            computed: {
                totalSubtotal: function() {
                    return this.selectedRows.reduce((sum, row) => sum + parseFloat(row.subtotal || 0), 0);
                }
            }
        });
    </script>
@endpush
