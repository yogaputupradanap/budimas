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
                        <span class="card-title">Daftar Order</span>
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
                                    <th> Kode <em>Order</em> </th>
                                    <th> PIC <em>Request</em> </th>
                                    <th> Nama <em>Cabang</em> </th>
                                    <th> Nama <em>Principal</em> </th>
                                    <th> Tanggal <em>Request</em> </th>
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
                <form method="" action="">
                    @csrf
                    <div class="modal-body">
                        <div class="form row">
                            <div class="col-md-4">
                                <div class="form-group">
                                    <label>Kode <em>Order</em></label>
                                    <input type="hidden" name="order_id" v-model="order.id">
                                    <input type="text" v-model="order.kode" placeholder="Masukkan Kode Request" readonly>
                                </div>
                                <div class="form-group">
                                    <label>Tanggal <em>Request</em></label>
                                    <input type="text" v-model="log.tanggal" class="datepicker" placeholder="YYYY-MM-DD"
                                        readonly>
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
                                    <select2 v-model="log.user_id" :options="user.data" :readonly="true" required>
                                    </select2>
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
                                    <input type="hidden" name="user_jabatan_id" :value="user_jabatan()">
                                    <select2 name="user_id" v-model="user.id" :options="user.data" :readonly="true"
                                        required></select2>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="form-group">
                                    <label>Tanggal <em>Konfirmasi</em></label>
                                    <input type="hidden" name="waktu" value="{{ date('H:i:s') }}">
                                    <input type="text" name="tanggal" value="{{ date('Y-m-d') }}" class="datepicker"
                                        placeholder="YYYY-MM-DD" readonly>
                                </div>
                            </div>
                        </div>
                    </div>
                </form>
                <div class="modal-body border-top px-0 pt-0">
                    <div v-if="isEditing" class="form row m-4">
                        <div class="col-md-4">
                            <div class="form-group">
                                <label>Pilih <em>Produk</em></label>
                                <select2 v-model="produk.id" :options="produk.data"></select2>
                            </div>
                        </div>
                        <div class="col-md-8">
                            <div class="form-group float-end">
                                <div class="btn-group mt-4" role="group">
                                    <button class="btn btn-primary px-4 mt-1" type="button" @click="addProduct">
                                        <i class="mdi mdi-plus"></i> Tambah Produk
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="table-container">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th> # </th>
                                    <th> Deskripsi </th>
                                    <th> Harga </th>
                                    <th width="12%"> Jml. <em>UOM 3</em> </th>
                                    <th width="12%"> Jml. <em>UOM 2</em> </th>
                                    <th width="12%"> Jml. <em>UOM 1</em> </th>
                                    <th width="8%"> PPN </th>
                                    <th width="16%"> Subtotal </th>
                                    <th width="16%"> Subtotal + PPN </th>
                                    <th v-if="isEditing"> Hapus </th>
                                </tr>
                            </thead>
                            <tbody v-for="(item, index) in order.detail">
                                <tr>
                                    <td> @{{ index + 1 }} </td>
                                    <td>
                                        @{{ item.produk_nama }} <br>
                                        <span class="text-info">@{{ item.produk_kode }}</span>
                                    </td>
                                    <td> @{{ numberToStr(item.produk_harga_beli) }} </td>
                                    <template v-for="(item2, i2) in item.jumlah" :key="i2">
                                        <td>
                                            @{{ item2.uom_nama }} <br>
                                            <input class="form-control-modal" type="number" v-model="item2.jumlah"
                                                :readonly="!isEditing">
                                        </td>
                                    </template>
                                    <td>
                                        <br>
                                        @{{ (item.ppn * 100).toFixed(0) + '%' }}
                                    </td>
                                    <td>
                                        <br>
                                        <input type="text" class="form-control-modal"
                                            :value="numberToStr(subtotalAsli(item))" readonly>
                                    </td>
                                    <td>
                                        <br>
                                        <input type="text" class="form-control-modal"
                                            :value="numberToStr(subtotalPPN(item))" readonly>
                                    </td>
                                    <td v-if="isEditing">
                                        <button type="button" class="btn btn-sm btn-danger" title="Hapus"
                                            @click="removeProduct(index)">
                                            <i class="mdi mdi-delete mx-1 font-16"></i>
                                        </button>
                                    </td>
                                </tr>
                            </tbody>
                            <tfoot>
                                <tr>
                                    <td></td>
                                    <td colspan="7"><b>Total</b></td>
                                    <td>
                                        <input type="text" class="form-control-modal" :value="numberToStr(totalPPN())"
                                            readonly>
                                    </td>
                                    <td v-if="isEditing"></td>
                                </tr>
                            </tfoot>
                        </table>
                    </div>
                </div>
                <div class="modal-body border-top">
                    <div class="form row mt-3 m-0">
                        <div class="col-md-12">
                            <div class="btn-group float-end" role="group">
                                <template v-if="!isEditing">
                                    <button type="button" class="btn btn-success px-4" @click="store">
                                        <i class="mdi mdi-check"></i> Konfirmasi Order
                                    </button>
                                    <button type="button" class="btn btn-primary px-4" @click="startEdit">
                                        <i class="mdi mdi-lead-pencil"></i> Edit Order
                                    </button>
                                    <button type="button" class="btn btn-danger px-4" @click="destroy">
                                        <i class="mdi mdi-delete"></i> Close Order
                                    </button>
                                </template>
                                <template v-else>
                                    <button type="button" class="btn btn-success px-4" @click="submitEdit">
                                        <i class="mdi mdi-check"></i> Selesai Edit
                                    </button>
                                    <button type="button" class="btn btn-danger px-4" @click="cancelEdit">
                                        <i class="mdi mdi-close"></i> Batal Edit
                                    </button>
                                </template>
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
                        show: req("/purchase-order/daftar-konfirmasi")
                    },
                    table: () => $('#app-list').find('table'),
                    user_cabang_id: null,
                    data: {
                        columns: [{
                                data: ""
                            },
                            {
                                data: "btn_detail"
                            },
                            {
                                data: "kode"
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
                renderTable(filter = null) {
                    let url = this.url.show;
                    if (this.user_cabang_id) {
                        const separator = url.includes('?') ? '&' : '?';
                        url += `${separator}cabang_id=${this.user_cabang_id}`;
                    }
                    Table().set(this.table()).destroy().paging().rowNumber(true).setDefaultOrder(6, 'desc')
                        .serverSide(this.data.columns, url, filter)
                        .init();
                    return this;
                },
                actionDetail() {
                    this.table().on('click', '.btn-detail', function() {
                        app_detail.render($(this).val());
                    });
                    return this;
                },
            },
            mounted: function() {
                const user = @json(Auth::user());

                if (user && user.response && user.response.result.length > 0) {
                    this.user_cabang_id = user.response.result.id_cabang;
                }

                console.log('Cabang Id', user);
                this.renderTable().actionDetail();
            }
        });

        var app_detail = new Vue({
            el: '#app-detail',
            data: function() {
                return {
                    url: {
                        store: "konfirmasi-order/store",
                        destroy: "purchase-order/destroy"
                    },
                    form: () => $("#app-detail").find('form'),
                    user: {
                        data: [],
                        id: '{{ user()->id }}'
                    },
                    cabang: {
                        data: [],
                        id: ''
                    },
                    principal: {
                        data: [],
                        id: ''
                    },
                    produk: {
                        data: [],
                        id: '',
                        check: null
                    },
                    order: {
                        id: null,
                        kode: '',
                        detail: [], // Initialize as empty array
                        total: 0
                    },
                    log: [],
                    isEditing: false,
                    originalOrder: null
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
                user_selected() {
                    return this.user.data.find(user => user.id == this.user.id);
                },
                user_jabatan() {
                    let user = this.user_selected();
                    return user ? user.user_jabatan_id : null;
                },
                render(id, vm = this) {
                    vm.show();
                    $.get(req(`/purchase-order/detail-riwayat/${id}`))
                        .done((res) => {
                            vm.order = res.data;
                            vm.originalOrder = JSON.parse(JSON.stringify(res.data));
                            vm.log = res.data.log;
                            vm.load(0);
                            vm.isEditing = false;
                            console.log('Order data:', vm.order); // Log data yang diterima
                        })
                        .fail((err) => {
                            console.error('Failed to fetch order data:', err); // Log error jika ada
                            vm.load(0);
                        });
                },
                // Di dalam methods Vue component:
                store: function() {
                    // Get form data dasar
                    const formData = new FormData(this.form()[0]);

                    // Deklarasikan variabel di luar blok if
                    let deletedDetails = [];
                    let addedDetails = [];
                    let editedDetails = [];

                    // Cek apakah ada perubahan pada order
                    const hasChanges = this.isOrderChanged();

                    if (hasChanges) {
                        // Mencari order_detail yang dihapus
                        deletedDetails = this.originalOrder.detail.filter(originalDetail =>
                            !this.order.detail.some(currentDetail =>
                                currentDetail.id === originalDetail.id
                            )
                        ).map(detail => ({
                            order_detail_id: detail.id,
                            produk_id: detail.produk_id,
                            produk_nama: detail.produk_nama,
                            produk_kode: detail.produk_kode
                        }));

                        // Mencari order_detail yang ditambahkan
                        addedDetails = this.order.detail.filter(currentDetail =>
                            !this.originalOrder.detail.some(originalDetail =>
                                originalDetail.id === currentDetail.id
                            )
                        ).map(detail => ({
                            order_id: this.order.id,
                            produk_id: detail.produk_id,
                            produk_nama: detail.produk_nama,
                            produk_kode: detail.produk_kode,
                            jumlah: detail.jumlah.map(uom => ({
                                ...uom,
                                order_id: this.order.id
                            }))
                        }));

                        // Mencari order_detail yang diedit
                        editedDetails = this.order.detail.map(currentDetail => {
                            const originalDetail = this.originalOrder.detail.find(d =>
                                d.id === currentDetail.id
                            );

                            if (originalDetail) {
                                const changes = currentDetail.jumlah.map((uom, index) => {
                                    const originalUom = originalDetail.jumlah.find(u => u.id ===
                                        uom.id);
                                    if (originalUom && originalUom.jumlah !== uom.jumlah) {
                                        return {
                                            order_detail_jumlah_id: uom.id,
                                            uom_id: uom.uom_id,
                                            uom_nama: uom.uom_nama,
                                            nilai_lama: originalUom.jumlah || 0,
                                            nilai_baru: uom.jumlah || 0,
                                            subtotal_lama: originalUom.subtotal || 0,
                                            subtotal_baru: uom.subtotal || 0
                                        };
                                    }
                                    return null;
                                }).filter(Boolean);

                                if (changes.length > 0) {

                                    const total_order_konversi = currentDetail.jumlah.reduce((total,
                                        uom) => {
                                        // Konversi ke unit terkecil dan tambahkan ke total
                                        return total + ((uom.jumlah || 0) * uom
                                            .uom_faktor_konversi);
                                    }, 0);

                                    return {
                                        order_detail_id: currentDetail.id,
                                        produk_id: currentDetail.produk_id,
                                        produk_nama: currentDetail.produk_nama,
                                        produk_kode: currentDetail.produk_kode,
                                        total_order: total_order_konversi,
                                        subtotal: currentDetail.subtotal,
                                        perubahan: changes
                                    };
                                }
                            }
                            return null;
                        }).filter(Boolean);

                        // Tambahkan ke formData jika ada perubahan
                        if (deletedDetails.length > 0) {
                            formData.append('deleted_details', JSON.stringify(deletedDetails));
                        }
                        if (addedDetails.length > 0) {
                            formData.append('added_details', JSON.stringify(addedDetails));
                        }
                        if (editedDetails.length > 0) {
                            formData.append('edited_details', JSON.stringify(editedDetails));
                        }
                        // Tambahkan total
                        formData.append('total', this.order.total);
                    }

                    // Untuk debugging - log data yang akan dikirim
                    const dataToSend = {};
                    for (let [key, value] of formData.entries()) {
                        dataToSend[key] = value;
                    }
                    console.log('Data yang akan dikirim ke server:', dataToSend);
                    // console.log(this.url.store);

                    // Submit form dengan konfirmasi
                    Alert().submit().then((result) => {
                        if (result.value === true) {
                            this.$nextTick(() => {
                                const form = this.form();
                                form.attr('method', 'POST')
                                    .attr('action', this.url.store);
                                    

                                // Jika ada perubahan, tambahkan hidden inputs
                                if (hasChanges) {
                                    if (deletedDetails.length > 0) {
                                        this.appendHiddenInput(form, 'deleted_details', JSON
                                            .stringify(deletedDetails));
                                    }
                                    if (addedDetails.length > 0) {
                                        this.appendHiddenInput(form, 'added_details', JSON
                                            .stringify(addedDetails));
                                    }
                                    if (editedDetails.length > 0) {
                                        this.appendHiddenInput(form, 'edited_details', JSON
                                            .stringify(editedDetails));
                                    }
                                    this.appendHiddenInput(form, 'total', this.order.total);
                                }

                                form.submit();
                            });
                        } else {
                            Alert().cancel();
                        }
                    });
                },
                // Tambahkan method untuk cek perubahan
                isOrderChanged() {
                    // Cek apakah ada produk yang dihapus
                    const hasDeletedProducts = this.originalOrder.detail.some(originalProduct =>
                        !this.order.detail.some(currentProduct =>
                            currentProduct.id === originalProduct.id
                        )
                    );
                    if (hasDeletedProducts) return true;

                    // Cek apakah ada produk yang ditambahkan
                    const hasAddedProducts = this.order.detail.some(currentProduct =>
                        !this.originalOrder.detail.some(originalProduct =>
                            originalProduct.id === currentProduct.id
                        )
                    );
                    if (hasAddedProducts) return true;

                    // Cek apakah ada perubahan jumlah
                    const hasEditedProducts = this.order.detail.some(currentProduct => {
                        const originalProduct = this.originalOrder.detail.find(p =>
                            p.id === currentProduct.id
                        );

                        if (originalProduct) {
                            return currentProduct.jumlah.some((uom, index) => {
                                const originalUom = originalProduct.jumlah.find(u => u.id === uom
                                    .id);
                                return originalUom && originalUom.jumlah !== uom.jumlah;
                            });
                        }
                        return false;
                    });
                    if (hasEditedProducts) return true;

                    return false;
                },
                appendHiddenInput: function(form, name, value) {
                    $('<input>').attr({
                        type: 'hidden',
                        name: name,
                        value: value
                    }).appendTo(form);
                },
                destroy: function() {
                    Alert().delete().then((result) => {
                        if (result.value == true) {
                            this.$nextTick(function() {
                                console.log('Deleting order:', this
                                    .order); // Log data yang akan dihapus
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
                startEdit() {
                    this.isEditing = true;
                    this.originalOrder = JSON.parse(JSON.stringify(this.order));
                    // Load produk options saat mulai edit
                    this.loadProdukOptions();
                },
                loadProdukOptions() {
                    if (this.order.principal_id) {
                        $.get(req(`/produk/option/principal/${this.order.principal_id}`))
                            .done((res) => {
                                this.produk.data = res.data;
                            });
                    }
                },
                // Fungsi untuk menambah produk baru
                addProduct() {
                    if (!this.produk.id) {
                        Alert().notice('error', 'Validasi',
                            'Silakan pilih produk terlebih dahulu');
                        return;
                    }

                    // Cek apakah produk sudah ada
                    let exist = this.order.detail.find(item => item.produk_id == this.produk
                        .id);
                    if (exist) {
                        Alert().exist();
                        return;
                    }

                    // Ambil detail produk dan tambahkan ke order
                    $.get(req(`/purchase-order/daftar-produk/${this.produk.id}`))
                        .done((res) => {
                            this.order.detail.push(res.data);
                            this.recalculateTotal();
                        });
                },

                // Fungsi untuk menghapus produk
                removeProduct(index) {
                    this.order.detail.splice(index, 1);
                    this.recalculateTotal();
                },

                // Fungsi untuk menghitung ulang subtotal
                recalculateTotal() {
                    if (!this.order || !this.order.detail) return;
                    this.order.detail.forEach(item => {
                        item.subtotal = this.subtotalPPN(item);
                    });
                    this.order.total = this.totalPPN();
                },

                calculateItemSubtotal(item) {
                    let subtotal = 0;
                    item.jumlah.forEach(uom => {
                        uom.subtotal = uom.jumlah * uom.uom_harga_beli_ppn;
                        subtotal += uom.subtotal;
                    });
                    return subtotal;
                },
                cancelEdit() {
                    // Kembalikan ke data sebelum diedit
                    this.order = JSON.parse(JSON.stringify(this.originalOrder));
                    this.isEditing = false;
                },
                isDataChanged() {
                    // Mengubah data menjadi string untuk membandingkan
                    const originalString = JSON.stringify(this.originalOrder);
                    const currentString = JSON.stringify(this.order);

                    return originalString !== currentString;
                },
                submitEdit() {
                    if (!this.isDataChanged()) {
                        Alert().notice('warning', 'Peringatan',
                            'Tidak ada perubahan data yang dilakukan');
                        return;
                    }

                    if (this.validateEdit()) {
                        Alert().submit().then((result) => {
                            if (result.value) {
                                // Hanya mengubah state editing dan memperbarui data di modal
                                this.isEditing = false;

                                // Tampilkan notifikasi sukses
                                Alert().success2();

                                // Data order sudah berubah dan siap untuk dikirim saat konfirmasi
                            } else {
                                Alert().cancel();
                            }
                        });
                    }

                },
                // Validasi sebelum submit edit
                validateEdit() {
                    if (this.order.detail.length === 0) {
                        Alert().notice('error', 'Validasi Gagal',
                            'Detail produk tidak boleh kosong');
                        return false;
                    }

                    let isValid = true;
                    this.order.detail.forEach(item => {
                        let subtotal = this.calculateItemSubtotal(item);
                        if (subtotal <= 0) {
                            Alert().notice('error', 'Validasi Gagal',
                                `Subtotal untuk ${item.produk_nama} tidak boleh 0. Periksa jumlah produk.`
                            );
                            isValid = false;
                        }
                    });

                    if (!isValid) return false;

                    if (this.order.total <= 0) {
                        Alert().notice('error', 'Validasi Gagal',
                            'Total transaksi tidak boleh 0');
                        return false;
                    }

                    return true;
                },
                subtotalAsli(item) {
                    if (!item || !item.jumlah) return 0;
                    let subtotal = 0;
                    item.jumlah.forEach(uom => {
                        const jumlahValue = parseFloat(uom.jumlah) || 0;
                        subtotal += jumlahValue * uom.uom_harga_beli;
                    });
                    return subtotal;
                },

                // Calculate subtotal with PPN for a single item
                subtotalPPN(item) {
                    if (!item || !item.jumlah) return 0;
                    let subtotal = 0;
                    item.jumlah.forEach(uom => {
                        const jumlahValue = parseFloat(uom.jumlah) || 0;
                        subtotal += jumlahValue * uom.uom_harga_beli_ppn;
                    });
                    return subtotal;
                },

                // Calculate total without PPN
                totalAsli() {
                    if (!this.order || !this.order.detail) return 0;
                    return this.order.detail.reduce((total, item) => {
                        return total + this.subtotalAsli(item);
                    }, 0);
                },

                // Calculate total with PPN
                totalPPN() {
                    if (!this.order || !this.order.detail) return 0;
                    return this.order.detail.reduce((total, item) => {
                        return total + this.subtotalPPN(item);
                    }, 0);
                },


            },
            watch: {
                'order.detail': {
                    deep: true,
                    handler(newVal) {
                        if (this.isEditing) {
                            this.recalculateTotal();
                        }
                    }
                }
            },
            mounted: function(vm = this) {
                $.get(req("/cabang/option"))
                    .done((res) => {
                        vm.cabang.data = res.data;
                        console.log('Cabang data:', res.data); // Log data yang diterima
                    })
                    .fail((err) => console.error('Failed to fetch cabang data:',
                        err)); // Log error jika ada

                $.get(req("/user/option"))
                    .done((res) => {
                        vm.user.data = res.data;
                        console.log('User data:', res.data); // Log data yang diterima
                    })
                    .fail((err) => console.error('Failed to fetch user data:',
                        err)); // Log error jika ada

                $.get(req("/principal/option"))
                    .done((res) => {
                        vm.principal.data = res.data;
                        console.log('Principal data:', res.data); // Log data yang diterima
                    })
                    .fail((err) => console.error('Failed to fetch principal data:',
                        err)); // Log error jika ada
            }
        });
    </script>
@endpush
