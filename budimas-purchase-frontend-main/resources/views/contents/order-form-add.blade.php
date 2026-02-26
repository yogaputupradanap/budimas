@extends('layouts.main')
@section('content')
    @include('partials.breadcrumb')
    <!-- ============================================================== -->
    <!-- Content Container  -->
    <!-- ============================================================== -->
    <div class="container-fluid">
        <div class="row m-md-1">
            <div class="col-md-12">
                <form id="app" action="/purchase-order/store" method="POST">
                    @csrf
                    <div class="card form">
                        <div class="card-header">
                            <span class="card-title">Form Request Order</span>
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
                                        <label>Kode <em>Order</em></label>
                                        <input type="text" name="kode" :value="kode"
                                            placeholder="Max 50 Karakter" readonly required>
                                    </div>
                                    <div class="form-group">
                                        <label>PIC <em>Request Order</em></label>
                                        <input type="hidden" name="user_jabatan_id" :value="user_jabatan()">
                                        <select2 name="user_id" v-model="user.id" :options="user.data"
                                            :readonly="true" required></select2>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="form-group">
                                        <label>Tanggal <em>Request Order</em></label>
                                        <input type="hidden" name="waktu" value="{{ date('H:i:s') }}">
                                        <input type="text" name="tanggal" value="{{ date('Y-m-d') }}" class="datepicker"
                                            placeholder="YYYY-MM-DD" readonly required>
                                    </div>
                                    <div class="form-group">
                                        <label>Pilih <em>Principal</em></label>
                                        <select2 name="principal_id" v-model="principal.id" :options="principal.data">
                                        </select2>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="form-group">
                                        <label>Pilih <em>Cabang</em></label>
                                        <select2 name="cabang_id" v-model="cabang.id" :options="cabang.data"
                                            :readonly="true" required></select2>
                                    </div>
                                    <div class="form-group">
                                        <label>Keterangan <em>Order</em></label>
                                        <textarea type="text" name="keterangan" maxlength="100" placeholder="Max 100 Karater!"></textarea>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="card form">
                        <div class="card-body">
                            <span class="card-title">Detail Order</span>
                        </div>
                        <div class="card-body border-top p-0">
                            <div class="form row m-4">
                                <div class="col-md-4">
                                    <div class="form-group">
                                        <label>Pilih <em>Produk</em></label>
                                        <input type="hidden" v-model="produk.check" required>
                                        <select2 v-model="produk.id" :options="produk.data"></select2>
                                    </div>
                                </div>
                                <div class="col-md-8">
                                    <div class="form-group float-end">
                                        <div class="btn-group mt-4" role="group">
                                            <a href="{{ asset('assets-panel/assets/images/template-import-req-order.csv') }}"
                                                class="btn btn-success px-4 mt-1 mx-2" download>
                                                <i class="mdi mdi-download"></i> Unduh Template
                                            </a>
                                            <input type="file" ref="fileInput" @change="handleFileUpload" accept=".csv"
                                                class="d-none">
                                            <button class="btn btn-info px-4 mt-1 mx-2" type="button"
                                                @click="triggerFileUpload" :disabled="!principal.id">
                                                <i class="mdi mdi-file-import"></i> Import CSV
                                            </button>
                                            <button class="btn btn-primary px-4 mt-1" type="button"
                                                :disabled="!principal.id" @click="add">
                                                <i class="mdi mdi-plus"></i> Tambah
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="loading-overlay" v-if="isLoading">
                                <div class="lds-ripple">
                                    <div class="lds-pos"></div>
                                    <div class="lds-pos"></div>
                                </div>
                            </div>

                            <div class="table-container h-600">
                                <table class="table">
                                    <thead>
                                        <tr>
                                            <th> # </th>
                                            <th> Deskripsi </th>
                                            <th> Harga/<em>UOM 1</em> </th>
                                            <th width="13%"> Jml. <em>UOM 3</em> </th>
                                            <th width="13%"> Jml. <em>UOM 2</em> </th>
                                            <th width="13%"> Jml. <em>UOM 1</em> </th>
                                            <th width="8%"> PPN </th>
                                            <th width="12%"> Subtotal </th>
                                            <th width="12%"> Subtotal + PPN </th>
                                            <th> Hapus </th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="(item, i) in detail" :key="item.id">
                                            <td> @{{ i + 1 }} </td>
                                            <td>
                                                @{{ item.produk_nama }} <br>
                                                <span class="text-info">
                                                    @{{ item.produk_kode }}
                                                </span>
                                                <input type   = "hidden" :name="fname_detail(i, 'produk_id')"
                                                    :value="item.produk_id">
                                                <input type   = "hidden" :name="fname_detail(i, 'produk_kode')"
                                                    :value="item.produk_kode">
                                                <input type   = "hidden" :name="fname_detail(i, 'produk_nama')"
                                                    :value="item.produk_nama">
                                                <input type   = "hidden" :name="fname_detail(i, 'produk_harga_beli')"
                                                    :value="item.produk_harga_beli">
                                                <input type   = "hidden" :name="fname_detail(i, 'ppn')"
                                                    :value="item.ppn">
                                            </td>
                                            <td> @{{ numberToStr(item.produk_harga_beli) }} </td>

                                            <template v-for="(item2, i2) in item.jumlah" :key="i2">
                                                <td>
                                                    @{{ item2.uom_nama }} <br>
                                                    <input class   = "form-control-modal" type    = "number"
                                                        :name="fname_jumlah(i, i2, 'jumlah')" v-model = "item2.jumlah">
                                                    <input type   = "hidden" :name="fname_jumlah(i, i2, 'uom_id')"
                                                        :value="item2.uom_id">
                                                    <input type   = "hidden" :name="fname_jumlah(i, i2, 'uom_kode')"
                                                        :value="item2.uom_kode">
                                                    <input type   = "hidden" :name="fname_jumlah(i, i2, 'uom_nama')"
                                                        :value="item2.uom_nama">
                                                    <input type   = "hidden" :name="fname_jumlah(i, i2, 'uom_level')"
                                                        :value="item2.uom_level">
                                                    <input type   = "hidden"
                                                        :name="fname_jumlah(i, i2, 'uom_faktor_konversi')"
                                                        :value="item2.uom_faktor_konversi">
                                                    <input type   = "hidden" :name="fname_jumlah(i, i2, 'uom_harga_beli')"
                                                        :value="item2.uom_harga_beli">
                                                    <input type   = "hidden"
                                                        :name="fname_jumlah(i, i2, 'uom_harga_beli_ppn')"
                                                        :value="item2.uom_harga_beli_ppn">
                                                    <input type   = "hidden" :name="fname_jumlah(i, i2, 'subtotal')"
                                                        :value="subtotal_uom(item2)">
                                                </td>
                                            </template>
                                            <td>
                                                <br>
                                                @{{ item.ppn * 100 .toFixed(0) + '%' }}
                                            </td>
                                            <td>
                                                <br>
                                                <input type="hidden" :name="fname_detail(i, 'subtotal_asli')"
                                                    :value="subtotal_item_asli(item)">
                                                <input type="text" class="form-control-modal"
                                                    :value="numberToStr(subtotal_item_asli(item))" readonly>
                                            </td>
                                            <td>
                                                <br>
                                                <input type="hidden" :name="fname_detail(i, 'subtotal_ppn')"
                                                    :value="subtotal_item(item)">
                                                <input type="text" class="form-control-modal"
                                                    :value="numberToStr(subtotal_item(item))" readonly>
                                            </td>
                                            <td>
                                                <button type="button" class="btn btn-sm btn-danger" title="Hapus"
                                                    @click="remove(i)">
                                                    <i class="mdi mdi-delete mx-1 font-16"></i>
                                                </button>
                                            </td>
                                        </tr>
                                    </tbody>
                                    <tfoot>
                                        <tr>
                                            <td></td>
                                            <td colspan="7"><b>Total<b></td>
                                            <td>
                                                <input type="hidden" name="total" :value="total_transaksi()">
                                                <input type="text" class="form-control-modal"
                                                    :value="numberToStr(total_transaksi())" readonly>
                                            </td>
                                            <td></td>
                                        </tr>
                                    </tfoot>
                                </table>
                            </div>
                        </div>
                        <div class="card-body">
                            <button type="submit" class="btn btn-control btn-success float-end mx-1"
                                @click="validateBeforeSubmit($event, $el)">
                                <i class="mdi mdi-check"></i> Submit Order
                            </button>
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
            el: '#app',
            data: function() {
                return {
                    cabang: {
                        data: [],
                        id: '{{ user()->id_cabang }}'
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
                    user: {
                        data: [],
                        id: '{{ user()->id }}'
                    },
                    detail: [],
                    kode: null,
                    isLoading: false
                }
            },
            methods: {
                fname_detail(i, attr) {
                    return `detail[${i}][${attr}]`;
                },
                fname_jumlah(i, i2, attr) {
                    return `detail[${i}][jumlah][${i2}][${attr}]`;
                },
                fname_total(i, i2, attr) {
                    return `detail[${i}][total][${i2}][${attr}]`;
                },
                user_selected() {
                    return this.user.data.find(user => user.id == this.user.id);
                },
                user_jabatan() {
                    let user = this.user_selected();
                    return user ? user.id_jabatan : null;
                },
                add() {
                    let vm = this;
    if (!vm.produk || !vm.produk.id) return;

    let exist = this.detail.find(data => data.produk_id == this.produk.id);

    if (exist) {
        Alert().exist();
    } else {
        vm.isLoading = true;
        $.get(req(`/purchase-order/daftar-produk/${vm.produk.id}`))
            .done((res) => {
                const produkData = res.data;

                // --- PATCHING NAMA & KODE ---
                // Kita coba ambil dari berbagai kemungkinan properti
                produkData.produk_id = produkData.produk_id || vm.produk.id;
                
                // Coba ambil nama dari dropdown jika server mengirim undefined
                produkData.produk_nama = produkData.produk_nama || 
                                         vm.produk.produk_nama || 
                                         vm.produk.nama || 
                                         vm.produk.text || 
                                         vm.produk.keterangan || 
                                         "Nama Tidak Ditemukan";

                produkData.produk_kode = produkData.produk_kode || 
                                         vm.produk.produk_kode || 
                                         vm.produk.kode || 
                                         vm.produk.kode_sku || 
                                         "-";

                // --- PERBAIKAN HARGA ---
                // Pastikan harga beli diambil dari UOM jika level utama kosong (0)
                if (!produkData.produk_harga_beli || produkData.produk_harga_beli == 0) {
                    const uomTerendah = produkData.jumlah.find(u => u.uom_level == 1);
                    produkData.produk_harga_beli = uomTerendah ? uomTerendah.uom_harga_beli : 0;
                }

                // Inisialisasi angka agar reaktif
                produkData.jumlah.forEach(uom => {
                    uom.jumlah = 0; // Default awal 0 agar user yang isi
                    uom.uom_harga_beli_ppn = parseFloat(uom.uom_harga_beli_ppn) || 0;
                });

                vm.detail.push(produkData);
                console.log("BERHASIL TAMBAH:", produkData);
            })
            .fail((err) => { console.error(err); })
            .always(() => { vm.isLoading = false; });
    }
},
                remove(i) {
                    this.detail.splice(i, 1);
                },
              subtotal_uom(uom) {
    if (!uom) return 0;
    // Hitung subtotal tiap baris UOM (Harga PPN * Qty)
    const res = (parseFloat(uom.uom_harga_beli_ppn) || 0) * (parseFloat(uom.jumlah) || 0);
    uom.subtotal = res; // Simpan ke dalam object uom
    return res;
},
                // Menghitung subtotal per baris UOM tanpa PPN
    subtotal_uom_asli(uom) {
        if (!uom) return 0;
        const harga = parseFloat(uom.uom_harga_beli) || 0;
        const qty = parseFloat(uom.jumlah) || 0;
        return harga * qty;
    },

    // Menghitung total satu produk (semua UOM) tanpa PPN
    subtotal_item_asli(item) {
        if (!item || !item.jumlah) return 0;
        let total = item.jumlah.reduce((acc, uom) => {
            return acc + this.subtotal_uom_asli(uom);
        }, 0);
        return total;
    },

    // Menghitung total satu produk (semua UOM) + PPN
subtotal_item(item) {
    if (!item || !item.jumlah) return 0;
    // Total adalah penjumlahan subtotal dari UOM 1, 2, dan 3
    const total = item.jumlah.reduce((acc, uom) => {
        return acc + this.subtotal_uom(uom);
    }, 0);
    item.subtotal = total; // Update subtotal item utama
    return total;
},

    // Total Akhir Seluruh Tabel
total_transaksi() {
    if (!this.detail) return 0;
    return this.detail.reduce((acc, item) => {
        return acc + (this.subtotal_item(item) || 0);
    }, 0);
},

                total_transaksi_asli() {
                    return this.detail ? this.detail.reduce(
                        (total, item) => total + (!item ? 0 : item.subtotal_asli), 0) : 0;
                },
                validateBeforeSubmit(event, element) {
                    event.preventDefault();

                    if (this.detail.length === 0) {
                        Alert().notice('error', 'Validasi Gagal',
                            'Detail produk tidak boleh kosong. Tambahkan produk terlebih dahulu.'
                        );
                        return false;
                    }

                    let invalidSubtotal = this.detail.some(item => {
                        if (this.subtotal_item(item) <= 0) {
                            Alert().notice('error', 'Validasi Gagal',
                                `Subtotal untuk ${item.produk_nama} (${item.produk_kode}) Tidak boleh kosong. Periksa jumlah produk.`
                            );
                            return true;

                        }
                        return false;
                    });

                    if (invalidSubtotal) {
                        return false;
                    }

                    if (this.total_transaksi() <= 0) {
                        Alert().notice('error', 'Validasi Gagal',
                            'Total transaksi tidak boleh 0. Periksa produk yang ditambahkan.'
                        );
                        return false;
                    }
                    submitConfirmation(event, element);
                },
                triggerFileUpload() {
                    if (!this.principal.id) {
                        Alert().notice('error', 'Validasi Gagal',
                            'Silakan pilih Principal terlebih dahulu sebelum mengimpor data.');
                        return;
                    }
                    this.$refs.fileInput.click();
                },

                async handleFileUpload(event) {
                    const file = event.target.files[0];
                    if (!file) return;

                    // Reset file input
                    event.target.value = '';

                    if (file.type !== 'text/csv' && file.type !==
                        'application/vnd.ms-excel') { // Tambahan pengecekan tipe file
                        Alert().notice('error', 'Format File Salah', 'Mohon upload file dengan format CSV.');
                        return;
                    }

                    this.isLoading = true;
                    try {
                        const text = await this.readFileAsText(file);
                        const {
                            data,
                            errors
                        } = await this.parseCSV(text);

                        if (errors.length > 0) {
                            Alert().notice('error', 'Error pada CSV',
                                'Format CSV tidak sesuai. Pastikan kolom yang diperlukan tersedia: ' +
                                errors.join(', '));
                            return;
                        }

                        if (data.length === 0) {
                            Alert().notice('error', 'CSV Kosong', 'File CSV tidak memiliki data.');
                            return;
                        }

                        await this.processImportedData(data);
                    } catch (error) {
                        console.error('Import error:', error);
                        // Tampilkan pesan error yang lebih spesifik
                        Alert().notice('error', 'Import Gagal', error.message ||
                            'Terjadi kesalahan saat mengimpor data.');
                    } finally {
                        this.isLoading = false;
                    }
                },

                readFileAsText(file) {
                    return new Promise((resolve, reject) => {
                        const reader = new FileReader();
                        reader.onload = (e) => resolve(e.target.result);
                        reader.onerror = reject;
                        reader.readAsText(file);
                    });
                },

                async parseCSV(text) {
                    return new Promise((resolve) => {
                        Papa.parse(text, {
                            header: true,
                            skipEmptyLines: true,
                            complete: (results) => {
                                const requiredColumns = ['produk_kode', 'jumlah_uom_3',
                                    'jumlah_uom_2', 'jumlah_uom_1'
                                ];
                                const headers = results.meta.fields || [];

                                const missingColumns = requiredColumns.filter(col => !
                                    headers.includes(col));

                                resolve({
                                    data: results.data,
                                    errors: missingColumns
                                });
                            }
                        });
                    });
                },

                async processImportedData(csvData) {
                    try {
                        for (const row of csvData) {
                            // Find product in available products list
                            const matchingProduct = this.produk.data.find(p => p.kode === row.produk_kode);

                            if (!matchingProduct) {
                                throw new Error(
                                    `Produk dengan kode ${row.produk_kode} tidak ditemukan dalam Principal yang dipilih.`
                                );
                            }

                            // Fetch product details like in add() method
                            const response = await $.get(req(
                                `/purchase-order/daftar-produk/${matchingProduct.id}`));
                            const productData = response.data;

                            // Tambahkan validasi UOM di sini
                            const uomLevels = productData.jumlah.map(item => item.uom_level);
                            const hasAllLevels = [1, 2, 3].every(level => uomLevels.includes(level));

                            if (!hasAllLevels) {
                                throw new Error(
                                    `Produk ${row.produk_kode} harus memiliki semua tingkat UOM (1, 2, dan 3).`
                                );
                            }

                            // Validasi data yang diterima
                            if (!productData || !productData.jumlah) {
                                throw new Error(
                                    `Data produk ${row.produk_kode} tidak valid atau tidak lengkap.`);
                            }

                            // Update quantities based on CSV
                            productData.jumlah.forEach(item => {
                                if (item.uom_level === 3) item.jumlah = parseFloat(row.jumlah_uom_3) ||
                                    0;
                                if (item.uom_level === 2) item.jumlah = parseFloat(row.jumlah_uom_2) ||
                                    0;
                                if (item.uom_level === 1) item.jumlah = parseFloat(row.jumlah_uom_1) ||
                                    0;
                            });

                            // Check if product already exists in detail
                            const existingIndex = this.detail.findIndex(item => item.produk_id === productData
                                .produk_id);
                            if (existingIndex >= 0) {
                                this.detail.splice(existingIndex, 1, productData);
                            } else {
                                this.detail.push(productData);
                            }
                        }
                        Alert().notice('success', 'Import Berhasil', `${csvData.length} data berhasil diimpor`);
                    } catch (error) {
                        console.error('Process data error:', error);
                        throw error; // Re-throw error untuk ditangkap oleh handler di atas
                    }
                }
            },
            watch: {
                'principal.id': function(value) {
                    let vm = this;
                    vm.detail = [];
                    vm.produk.id = null;
                    
                    // Asumsi Anda punya variabel loading
                    vm.isLoading = true; 

                    if (value) {
                        $.get(req(`/produk/option/principal/${value}`))
                            .done((res) => vm.produk.data = res.data)
                            .fail((err) => console.error("Error produk:", err))
                            .always(() => vm.isLoading = false); // <--- Matikan loading di sini

                        if (vm.cabang.id) {
                            $.get(req(`/purchase-order/gen-kode/${vm.cabang.id}/${value}`))
                                .done((res) => vm.kode = res.data)
                                .fail((err) => {
                                    console.error("Gagal generate kode:", err);
                                    vm.kode = null; // Set default jika gagal
                                })
                                .always(() => vm.isLoading = false);
                        }
                    } else {
                        vm.isLoading = false;
                    }
                },
                'detail': function(value) {
                    this.produk.check = this.detail.length > 0 ? true : null;
                }
            },
            mounted: function() {
                let vm = this
                $.get(req(`/purchase-order/gen-kode/${vm.cabang.id}`))
                    .done((res) => vm.kode = res.data);
                $.get(req("/cabang/option"))
                    .done((res) => {
                        vm.cabang.data = res.data;
                        if (vm.cabang.id) {
                            $.get(req(`/purchase-order/gen-kode/${vm.cabang.id}`))
                                .done((res) => vm.kode = res.data)
                                .fail((err) => console.error("Failed to get code:", err));
                        }
                    });
                $.get(req("/user/option"))
                    .done((res) => vm.user.data = res.data);
                $.get(req("/principal/option"))
                    .done((res) => vm.principal.data = res.data);
            }
        });
    </script>
@endpush
