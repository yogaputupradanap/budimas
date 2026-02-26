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
                        <span class="card-title">Daftar Tagihan</span>
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
                                    <th> No. <em>Surat Tagihan</em></th>
                                    <th> PIC <em>Penerimaan</em> </th>
                                    <th> Nama <em>Cabang</em> </th>
                                    <th> Nama <em>Principal</em> </th>
                                    <th> Tanggal <em>Tagihan</em> </th>
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
                    <span class="modal-title">Detail Konfirmasi Order</span>
                    <button type="button" class="btn btn-sm btn-tool modal-close">
                        <i class="mdi mdi-close"></i>
                    </button>
                </div>
                <div class="modal-body">
                    <form method="" action="">
                        @csrf
                    </form>
                    <div class="form row">
                        <div class="col-md-4">
                            <div class="form-group">
                                <label>No. <em>Transaksi</em></label>
                                <input type="text" v-model="transaksi.no_transaksi" class="form-control-modal"
                                    placeholder="Masukkan Kode Request" readonly>
                            </div>
                            <div class="form-group">
                                <label>Kode <em>Order</em></label>
                                <input type="text" v-model="transaksi.kode_order" class="form-control-modal"
                                    placeholder="Masukkan Kode Request" readonly>
                            </div>
                            <div class="form-group">
                                <label>Tanggal <em>Penerimaan</em></label>
                                <input type="text" v-model="transaksi.tanggal" class="form-control-modal datepicker"
                                    placeholder="YYYY-MM-DD" readonly>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="form-group">
                                <label>Nama <em>Cabang</em></label>
                                <input type="text" v-model="transaksi.cabang_nama" class="form-control-modal"
                                    placeholder="Masukkan Cabang" readonly>
                            </div>
                            <div class="form-group">
                                <label>PIC <em>Penerimaan</em></label>
                                <input type="text" v-model="transaksi.user_nama" class="form-control-modal"
                                    placeholder="Max 50 Karakter" readonly>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="form-group">
                                <label>Nama <em>Principal</em></label>
                                <input type="text" v-model="transaksi.principal_nama" class="form-control-modal"
                                    placeholder="Masukkan Principal" readonly>
                            </div>
                            <div class="form-group">
                                <label>Keterangan <em>Penerimaan</em></label>
                                <textarea type="text" v-model="transaksi.keterangan" class="form-control-modal" maxlength="100"
                                    placeholder="Max 100 Karater!" readonly></textarea>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-body border-top">
                    <div class="form row">
                        <div class="col-md-4">
                            <div class="form-group">
                                <label>Subtotal <em>Transaksi</em></label>
                                <input type="text" class="form-control-modal" v-model="transaksi.subtotal"
                                    placeholder="Number" readonly>
                            </div>
                            <div class="form-group">
                                <label>Total <em>Transaksi</em></label>
                                <input type="number" class="form-control-modal" :value="hitungTotal()" placeholder="Number"
                                    readonly>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="form-group">
                                <label>Potongan <em>Transaksi</em></label>
                                <input type="number" class="form-control-modal" v-model="transaksi.potongan"
                                    placeholder="Number">
                            </div>
                            <div class="form-group">
                                <label>Tanggal <em>Jatuh Tempo</em></label>
                                <input type="number" class="datepicker" placeholder="YYYY-MM-DD">
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="form-group">
                                <label>Biaya <em>Lainnya</em></label>
                                <input type="number" class="form-control-modal" v-model="transaksi.biaya_lainnya"
                                    placeholder="Number">
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-body border-top px-0 pt-0">
                    <div class="table-container">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th> # </th>
                                    <th> Deskripsi </th>
                                    <th> Harga </th>
                                    <th width="10%"> Jml. <em>UOM 3</em> </th>
                                    <th width="10%"> Jml. <em>UOM 2</em> </th>
                                    <th width="10%"> Jml. <em>UOM 1</em> </th>
                                    <th width="12%"> Subtotal </th>
                                    <th width="12%"> Tanggal Expired </th>
                                    <th width="12%"> Batch Number </th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(item, index) in detail" :key="item.id">
                                    <td> @{{ index + 1 }} </td>
                                    <td>
                                        @{{ item.produk_nama }} <br>
                                        <span class="text-info"> @{{ item.produk_kode }} </span>
                                        <input type="hidden" :name="'detail[i][' + index + '][order_detail_id]'"
                                            :value="item.id">
                                    </td>
                                    <td> @{{ numberToStr(item.produk_harga_beli) }} </td>

                                    <template v-for="(j, ji) in item.jumlah" :key="ji">
                                        <template v-if="j !== null">
                                            <td>
                                                @{{ j.uom_nama }}<br>
                                                <input type="number" class="form-control-modal"
                                                    :name="'detail[i][' + index + '][jumlah][' + ji + '][jumlah_per_uom]'"
                                                    v-model="j.jumlah_per_uom" placeholder="Number!" readonly>
                                            </td>
                                        </template>
                                        <template v-else>
                                            <td class="text-center"><em>UOM Tidak Tersedia</em></td>
                                        </template>
                                    </template>
                                    <td>
                                        <input type="text" :name="'detail[i][' + index + '][subtotal]'"
                                            class="form-control-modal" :value="item.subtotal_per_uom"
                                            placeholder="Number!" readonly>
                                    </td>
                                    <td>
                                        <input type="text" :name="'detail[i][' + index + '][tanggal_expired]'"
                                            class="form-control-modal" :value="item.tanggal_expired"
                                            placeholder="YYYY-MM-DD" readonly>
                                    </td>
                                    <td>
                                        <input type="text" :name="'detail[i][' + index + '][batch_number]'"
                                            class="form-control-modal" :value="item.batch_number"
                                            placeholder="Max 50 Karakter" readonly>
                                    </td>
                                </tr>
                            </tbody>
                            <tfoot>
                                <tr>
                                    <td></td>
                                    <td colspan="5"><b>Total<b></td>
                                    <td><input type="text" name="subtotal" class="form-control-modal"
                                            :value="hitungTotal()" readonly></td>
                                    <td colspan="3"></td>
                                </tr>
                            </tfoot>
                        </table>
                    </div>
                    <div class="modal-body border-top">
                        <div class="form row mt-3 m-0">
                            <div class="col-md-12">
                                <div class="btn-group float-end" role="group">
                                    <button type="button" class="btn btn-success px-4" @click="store()">
                                        <i class="mdi mdi-check"></i> Konfirmasi Purchase
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
                        url: {
                            show: baseURL + "/purchase-transaksi/daftar-konfirmasi"
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
                },
                mounted: function(vm = this) {
                    this.renderTable().actionBtnDetail();
                }
            });

            var app_detail = new Vue({
                el: '#app-detail',
                data: function() {
                    return {
                        url: {
                            show1: `${baseURL}/purchase-transaksi/detail-riwayat/:id`,
                            show2: "/olah-user/data/option1",
                            show3: "/olah-user/data/option5",
                            store: "konfirmasi-order/store",
                            edit: "purchase-order/edit/:id",
                            destroy: "purchase-order/destroy"
                        },
                        form: () => $("#app-detail").find('form'),
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
                        produk: {
                            table: {
                                data: []
                            }
                        },
                        transaksi: [],
                        detail: []
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
                                vm.user.text = data;
                            });
                    },
                    renderData: function(data, vm = this) {
                        this.loading(1);
                        var url = this.url.show1.replace(':id', data.id);
                        $.get(url, {
                                //  transaksi_id: data.id
                            })
                            .done(function(response) {
                                data = response.data;
                                console.log(data);
                                vm.transaksi = data;
                                vm.detail = data.detail;
                                console.log(response);
                                console.log(data);
                                vm.produk.table.data = response;
                                vm.loading(0);
                            })
                    },
                    hitungTotal: function() {
                        if (!isNull(this.transaksi)) {
                            return this.transaksi.biaya_lainnya - this.transaksi.potongan + this.transaksi.subtotal;
                        }
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
                }
            });
        </script>
    @endpush
