@extends('layouts.main')
@section('content')
    @include('partials.breadcrumb')
    <!-- ============================================================== -->
    <!-- Content Container  -->
    <!-- ============================================================== -->
    <div class="container-fluid">
        <div class="row m-md-1">
            <div class="col-md-12">
                <form action="/penerimaan-barang/store" method="POST" id="app" @submit="submitForm">
                    @csrf
                    <!-- ============================================== -->
                    <!-- Card Form - Order  -->
                    <!-- ============================================== -->
                    <div class="loading-overlay" v-if="isLoading">
                        <div class="lds-ripple">
                            <div class="lds-pos"></div>
                            <div class="lds-pos"></div>
                        </div>
                    </div>
                    <div class="card form">
                        <div class="card-header">
                            <span class="card-title">Form Penerimaan Barang</span>
                        </div>
                        <div class="card-body card-bar-menu">
                            <div class="btn-group" role="group">
                                <a class="btn btn-danger" onclick="window.history.back()">
                                    <i class="mdi mdi-step-backward"></i>Kembali
                                </a>
                            </div>
                        </div>
                        <div class="card-body border-top">
                            <div class="form row">
                                <div class="col-md-4">
                                    <div class="form-group">
                                        <label>No. <em>Transaksi</em></label>
                                        <input type="text" name="no_transaksi" v-model="transaksi.no"
                                            placeholder="Max 50 Karakter" readonly required>
                                    </div>
                                    <div class="form-group">
                                        <label>Kode <em>Order</em></label>
                                        <input type="hidden" name="order_id" v-model="transaksi.order_id">
                                        <input type="text" name="order_kode" v-model="transaksi.kode_order"
                                            placeholder="Max 50 Karakter" readonly required>
                                    </div>
                                    <div class="form-group">
                                        <label>PIC <em>Supervisi</em></label>
                                        <input type="hidden" name="user_jabatan_id" :value="user_jabatan()">
                                        <select2 name="user_id" v-model="user.id" :options="user.data"
                                            :readonly="true" required></select2>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="form-group">
                                        <label>Tanggal <em>Penerimaan</em></label>
                                        <input type="hidden" name="waktu" value="{{ date('H:i:s') }}">
                                        <input type="text" name="tanggal" value="{{ date('Y-m-d') }}" class="datepicker"
                                            placeholder="YYYY-MM-DD" required>
                                    </div>
                                    <div class="form-group">
                                        <label>Pilih <em>Principal</em></label>
                                        <select2 name="principal_id" v-model="principal.id" :options="principal.data"
                                            :readonly="true" required></select2>
                                    </div>
                                    <div class="form-group">
                                        <label>Batch <em>Penerimaan</em></label>
                                        <input type="number" name="batch" v-model="transaksi.batch" placeholder="Number"
                                            readonly required>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="form-group">
                                        <label>Pilih <em>Cabang</em></label>
                                        <select2 name="cabang_id" v-model="cabang.id" :options="cabang.data"
                                            :readonly="true" required></select2>
                                    </div>
                                    <div class="form-group">
                                        <label>Keterangan <em>Penerimaan</em></label>
                                        <textarea type="text" name="keterangan" maxlength="100" placeholder="Max 100 Karater!"></textarea>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <!-- ============================================== -->
                    <!-- End Card Form - Order  -->
                    <!-- ============================================== -->
                    <!-- ============================================== -->
                    <!-- Card Form - Produk  -->
                    <!-- ============================================== -->
                    <div class="card form">
                        <div class="card-body"></div>
                        <div class="card-body border-top p-0 mt-2">
                            <div class="table-container h-600">
                                <table class="table">
                                    <thead>
                                        <tr>
                                            <th> # </th>
                                            <th> Deskripsi </th>
                                            <th> Sisa </th>
                                            <th width="10%"> Jml. <em>UOM 3</em> </th>
                                            <th width="10%"> Jml. <em>UOM 2</em> </th>
                                            <th width="10%"> Jml. <em>UOM 1</em> </th>
                                            <th width="12%"> Subtotal /UOM 1</th>
                                            <th width="12%"> Jumlah Harga</th>
                                            <th width="12%"> Tanggal Expired </th>
                                            {{-- <th width="12%"> Batch Number </th> --}}
                                            <th> Hapus </th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="(item, index) in detail" :key="item.id">
                                            <td> @{{ index + 1 }} </td>
                                            <td>
                                                @{{ item.produk_nama }} <br>
                                                <span class="text-info"> @{{ item.produk_kode }} </span>
                                                <input type="hidden" :name="'detail[' + index + '][order_detail_id]'"
                                                    :value="item.id">
                                            </td>
                                            <td> @{{ numberToStr(item.total_tersisa) }} </td>

                                            <template v-for="(j, ji) in item.jumlah" :key="ji">
                                                <td>
                                                    @{{ j.uom_nama }}<br>
                                                    <input type="number" class="form-control-modal"
                                                        :name="'detail[' + index + '][jumlah][' + ji + '][jumlah]'"
                                                        v-model="j.jumlah">
                                                    <input type="hidden"
                                                        :name="'detail[' + index + '][jumlah][' + ji +
                                                            '][order_detail_jumlah_id]'"
                                                        :value="j.id">
                                                    <input type="hidden"
                                                        :name="'detail[' + index + '][jumlah][' + ji + '][subtotal]'"
                                                        :value="hitungSubtotalUOM(j)">
                                                </td>
                                            </template>
                                            <td>
                                                <br>
                                                <input type="text" :name="'detail[' + index + '][subtotal]'"
                                                    class="form-control-modal" :value="hitungSubtotalItem(item)" readonly>
                                            </td>
                                            <td>
                                                <br>
                                                <input type="text" :name="'detail[' + index + '][jumlah_harga]'"
                                                    class="form-control-modal"
                                                    :value="numberToStrToFixed2(hitungJumlahHarga(item))" readonly>
                                                <input type="hidden" :name="'detail[' + index + '][jumlah_harga]'"
                                                    :value="hitungJumlahHarga(item)">
                                            </td>
                                            <td>
                                                <br>
                                                <input type="date" :name="'detail[' + index + '][tanggal_expired]'"
                                                    class="form-control-modal">
                                            </td>
                                            {{-- <td>
                                                <br>
                                                <input type="text" :name="'detail[' + index + '][batch_number]'"
                                                    class="form-control-modal" placeholder="Max 50 Karakter">
                                            </td> --}}
                                            <td>
                                                <button type="button" class="btn btn-sm btn-danger"
                                                    @click="removeData(index)" title="Hapus">
                                                    <i class="mdi mdi-delete mx-1 font-16"></i>
                                                </button>
                                            </td>
                                        </tr>
                                    </tbody>
                                    <tfoot>
                                        <tr>
                                            <td></td>
                                            <td colspan="6"><b>Total<b></td>
                                            <td><input type="text" name="subtotal_display" class="form-control-modal"
                                                    :value="numberToStrToFixed2(hitungTotal())" readonly>

                                                <!-- Input tersembunyi untuk nilai asli yang dikirim -->
                                                <input type="hidden" name="subtotal" :value="hitungTotal()">
                                            </td>
                                            <td colspan="2"></td>
                                        </tr>
                                    </tfoot>
                                </table>
                            </div>
                        </div>
                        <div class="card-body">
                            <button type="submit" class="btn btn-control btn-success float-end mx-1"
                                @click.prevent="submitForm">
                                <i class="mdi mdi-check"></i> Submit Penerimaan
                            </button>
                            <button type="button" class="btn btn-control btn-danger float-end mx-1" @click="closeOrder">
                                <i class="mdi mdi-close"></i> Closed Order
                            </button>
                        </div>
                    </div>
                    <!-- ============================================== -->
                    <!-- End Card Form - Produk  -->
                    <!-- ============================================== -->
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
            el: '#app',
            data: function() {
                return {
                    url: {
                        destroy: "purchase-order/destroy"
                    },
                    cabang: {
                        id: '',
                        data: []
                    },
                    principal: {
                        id: '',
                        data: []
                    },
                    user: {
                        data: [],
                        id: '{{ user()->id }}'
                    },
                    transaksi: {
                        no: null,
                        order_id: "{{ request()->route('id') }}",
                        kode_order: null,
                        batch: null,
                    },
                    isLoading: false,
                    detail: []
                }
            },
            methods: {
                user_selected() {
                    return this.user.data.find(user => user.id == this.user.id);
                },
                user_jabatan() {
                    let user = this.user_selected();
                    return user ? user.id_jabatan : null;
                },
                async setData(vm = this) {
                    try {
                        const order_id = vm.transaksi.order_id;

                        // Fetch the last batch number first
                        const lastBatch = await vm.getLastBatch(order_id);

                        // Then get the order details
                        const response = await $.get(req(`/purchase-order/detail-purchase/${order_id}`));
                        const data = response.data;
                        // console.log("respon api:", response);

                        vm.cabang.id = data.cabang_id;
                        vm.principal.id = data.principal_id;
                        vm.transaksi.kode_order = data.kode;
                        vm.transaksi.batch = lastBatch;
                        // Handle default values based on batch number
                        if (lastBatch > 1) {
                            data.detail.forEach(item => {
                                // UOM sudah terurut dari terbesar ke terkecil (UOM3 -> UOM1)
                                // Set UOM2 dan UOM3 ke 0
                                item.jumlah[0].jumlah = null; // UOM3 (BOX) = 0
                                item.jumlah[1].jumlah = null; // UOM2 (RENCENG) = 0

                                // Set UOM1 (BUNGKUS) dengan sisa quantity
                                item.jumlah[2].jumlah = item.total_tersisa;
                            });
                        }

                        vm.detail = data.detail;

                        vm.transaksi.no = "PINV{{ date('YmdHis') }}" +
                            vm.cabang.id +
                            "{{ rand(100, 1000) }}" +
                            vm.transaksi.batch;

                        console.log('Detail Purchase Data:', data);
                        console.log('Current Batch Number:', vm.transaksi.batch);
                    } catch (err) {
                        console.error('Failed to fetch purchase order details:', err);
                    }
                },
                async getLastBatch(order_id) {
                    try {
                        const response = await $.get(req(`/purchase-transaksi/last-batch/${order_id}`));
                        return response.data;
                    } catch (error) {
                        console.error('Failed to fetch last batch number:', error);
                        return 1; // Default to 1 if there's an error
                    }
                },
                closeOrder: function() {
                    Swal.fire({
                        icon: 'warning',
                        title: 'Yakin untuk Tutup Order?',
                        text: 'Order yang Ditutup, Tidak Dapat Dibuka Kembali!',
                        confirmButtonText: 'Lanjut',
                        confirmButtonColor: '#4CAF50',
                        showCancelButton: true,
                        cancelButtonText: 'Batal',
                        cancelButtonColor: '#3085D6',
                    }).then((result) => {
                        if (result.isConfirmed) {
                            this.$nextTick(() => {
                                let form = document.createElement('form');
                                form.method = 'POST';
                                form.action = '/purchase-order/destroy';

                                form.appendChild(this.createHiddenInput('order_id', this
                                    .transaksi.order_id));
                                form.appendChild(this.createHiddenInput('_token',
                                    document.querySelector('meta[name="_token"]')
                                    .getAttribute('content')));

                                document.body.appendChild(form);
                                form.submit();
                            });
                        }
                    });
                },
                createHiddenInput: function(name, value) {
                    let input = document.createElement('input');
                    input.type = 'hidden';
                    input.name = name;
                    input.value = value;
                    return input;
                },
                hitungSubtotalUOM(i) {
                    return !isNull(i) ? (i.subtotal = i.uom_harga_beli * i.jumlah) : undefined;
                },
                removeData(index) {
                    console.log('Removing item at index:', index); // Log indeks item yang akan dihapus
                    this.detail.splice(index, 1);
                },
                hitungSubtotalItem(i) {
                    i.subtotal = i.jumlah.reduce(
                        (subtotal, j) => subtotal + (isNull(j) ? 0 : (j.jumlah * j.uom_faktor_konversi)), 0
                    );
                    return i.subtotal;
                },
                hitungTotal() {
                    return this.detail ? this.detail.reduce(
                        (total, item) => total + (isNull(item) ? 0 : this.hitungJumlahHarga(item)), 0
                    ) : 0;
                },
                validateQuantities() {
                    for (let item of this.detail) {
                        if (this.hitungSubtotalItem(item) > item.total_tersisa) {
                            Alert().notice('warning', 'Penerimaan Barang',
                                `Jumlah penerimaan untuk ${item.produk_nama} (${item.produk_kode}) melebihi sisa yang tersedia. Mohon periksa kembali input Anda.`
                            );
                            return false;
                        }
                    }
                    return true;
                },

                validateTotal() {
                    const total = this.hitungTotal();
                    if (total === 0) {
                        Alert().notice('warning', 'Penerimaan Barang',
                            'Inputan tidak boleh kosong. Mohon isi jumlah penerimaan barang.'
                        );
                        return false;
                    }
                    return true;
                },
                hitungJumlahHarga(item) {
                    let jumlah_harga = 0;
                    for (let j of item.jumlah) {
                        if (!isNull(j)) {
                            jumlah_harga += j.jumlah * j.uom_harga_beli; // Kalikan jumlah dengan harga beli
                        }
                    }
                    item.jumlah_harga = jumlah_harga; // Simpan ke dalam item untuk kemudahan
                    return jumlah_harga;
                },
                validateForm() {
                    return this.validateQuantities() && this.validateTotal();
                },
                isAllItemsComplete() {
                    return this.detail.every(item => {
                        const subtotal = this.hitungSubtotalItem(item);
                        return subtotal === item.total_tersisa;
                    });
                },

                submitForm(event) {
                    event.preventDefault();
                    if (this.validateForm()) {
                        const allComplete = this.isAllItemsComplete();

                        if (allComplete) {
                            Alert().confirmation('info', 'Penerimaan Barang',
                                'Semua item telah selesai diterima. Sistem akan melakukan submit penerimaan dan close order secara otomatis. Lanjutkan?'
                            ).then((result) => {
                                if (result.isConfirmed) {
                                    this.isLoading = true;
                                    // Submit form penerimaan terlebih dahulu
                                    const formPenerimaan = document.querySelector('#app');
                                    const formData = new FormData(formPenerimaan);

                                    // Kirim form penerimaan menggunakan fetch
                                    fetch(formPenerimaan.action, {
                                            method: 'POST',
                                            body: formData
                                        })
                                        .then(response => {
                                            if (response.ok) {
                                                // Setelah penerimaan berhasil, baru close order
                                                let formClose = document.createElement('form');
                                                formClose.method = 'POST';
                                                formClose.action = '/purchase-order/destroy';

                                                formClose.appendChild(this.createHiddenInput('order_id',
                                                    this.transaksi.order_id));
                                                formClose.appendChild(this.createHiddenInput('_token',
                                                    document.querySelector(
                                                        'meta[name="_token"]').getAttribute(
                                                        'content')));

                                                document.body.appendChild(formClose);
                                                formClose.submit();
                                            }
                                        });
                                }
                            });
                        } else {
                            this.isLoading = false;
                            // Jika belum complete semua, lakukan submit biasa
                            return validateAndSubmit(event, event.target);
                        }
                    }
                    return false;
                }
            },
            mounted: function() {
                let vm = this;
                $.get(req("/cabang/option"))
                    .done((res) => {
                        vm.cabang.data = res.data;
                        console.log('Cabang data:', res.data); // Log data yang diterima
                    })
                    .fail((err) => {
                        console.error('Failed to fetch cabang data:', err); // Log error jika ada
                    });

                $.get(req("/user/option"))
                    .done((res) => {
                        vm.user.data = res.data;
                        console.log('User data:', res.data); // Log data yang diterima
                    })
                    .fail((err) => {
                        console.error('Failed to fetch user data:', err); // Log error jika ada
                    });

                $.get(req("/principal/option"))
                    .done((res) => {
                        vm.principal.data = res.data;
                        console.log('Principal data:', res.data); // Log data yang diterima
                    })
                    .fail((err) => {
                        console.error('Failed to fetch principal data:', err); // Log error jika ada
                    });
                window.validatePenerimaanBarang = this.validateForm;

                this.setData();
                console.log('Component mounted'); // Log saat komponen dipasang
            }
        });
    </script>
@endpush
