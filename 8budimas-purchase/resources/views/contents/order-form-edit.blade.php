@extends('layouts.main')
@section('content')
@include('partials.breadcrumb')
<!-- ============================================================== -->
<!-- Content Container  -->
<!-- ============================================================== -->
<div class="container-fluid">
    <div class="row m-md-1">
        <div class="col-md-12">
            <form id="app" action="" method="POST">
                @csrf
                <div class="card form">
                    <div class="card-header">
                        <span class="card-title">Form Edit Order</span>
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
                                    <input type="text" name="kode" value="{{ $data->kode }}" placeholder="Max 50 Karakter" readonly required>
                                </div>
                                <div class="form-group">
                                    <label>PIC <em>Request Order</em></label>
                                    <input type="hidden" name="user_jabatan_id" :value="user_jabatan()">
                                    <select2 name="user_id" v-model="user.id" :options="user.data" :readonly="true" required></select2>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="form-group">
                                    <label>Tanggal <em>Request Order</em></label>
                                    <input type="hidden" name="waktu" value="{{ date('H:i:s') }}">
                                    <input type="text" name="tanggal" value="{{ date('Y-m-d') }}" class="datepicker" placeholder="YYYY-MM-DD" readonly required>
                                </div>
                                <div class="form-group">
                                    <label>Pilih <em>Principal</em></label>
                                    <select2 name="principal_id" v-model="principal.id" :options="principal.data" required></select2>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="form-group">
                                    <label>Pilih <em>Cabang</em></label>
                                    <select2 name="cabang_id" v-model="cabang.id" :options="cabang.data" :readonly="true" required></select2>
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
                    <div class="card-body"></div>
                    <div class="card-body border-top p-0 mt-2">
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
                                        <button class="btn btn-primary px-4 mt-1" type="button" @click="add">
                                            <i class="mdi mdi-plus"></i> Tambah
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="table-container h-600">
                            <table class="table">
                                <thead>
                                    <tr>
                                        <th> #                               </th>
                                        <th> Deskripsi                       </th>
                                        <th> Harga                           </th>
                                        <th width="13%"> Jml. <em>UOM 3</em> </th>
                                        <th width="13%"> Jml. <em>UOM 2</em> </th>
                                        <th width="13%"> Jml. <em>UOM 1</em> </th>
                                        <th width="13%"> Subtotal            </th>
                                        <th> Hapus                           </th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="(item, i) in detail" :key="item.id">
                                        <td> @{{ i+1 }} </td>
                                        <td> 
                                            @{{ item.produk_nama }} <br>
                                            <span class="text-info">
                                                @{{ item.produk_kode }}
                                            </span>
                                            <input type   = "hidden" 
                                                   :name  = "fname_detail(i,'produk_id')" 
                                                   :value = "item.produk_id"
                                            >
                                            <input type   = "hidden" 
                                                   :name  = "fname_detail(i,'produk_kode')" 
                                                   :value = "item.produk_kode"
                                            >
                                            <input type   = "hidden" 
                                                   :name  = "fname_detail(i,'produk_nama')" 
                                                   :value = "item.produk_name"
                                            >
                                            <input type   = "hidden" 
                                                   :name  = "fname_detail(i,'produk_harga_beli')" 
                                                   :value = "item.produk_harga_beli"
                                            >
                                        </td>
                                        <td> @{{ numberToStr(item.produk_harga_beli) }} </td>
                                        
                                        <template v-for="(item2, i2) in item.jumlah" :key="i2">
                                            <template v-if="item2">
                                                <td> 
                                                    @{{ item2.uom_nama }} <br>
                                                    <input class   = "form-control-modal"
                                                           type    = "text"
                                                           :name   = "fname_jumlah(i,i2,'jumlah')" 
                                                           v-model = "item2.jumlah"
                                                    >
                                                    <input type   = "hidden" 
                                                           :name  = "fname_jumlah(i,i2,'uom_id')"     
                                                           :value = "item2.uom_id"
                                                    >
                                                    <input type   = "hidden" 
                                                           :name  = "fname_jumlah(i,i2,'uom_kode')"   
                                                           :value = "item2.uom_kode"
                                                    >
                                                    <input type   = "hidden" 
                                                           :name  = "fname_jumlah(i,i2,'uom_nama')"   
                                                           :value = "item2.uom_nama"
                                                    >
                                                    <input type   = "hidden" 
                                                           :name  = "fname_jumlah(i,i2,'uom_level')"  
                                                           :value = "item2.uom_level"
                                                    >
                                                    <input type   = "hidden" 
                                                           :name  = "fname_jumlah(i,i2,'uom_faktor_konversi')" 
                                                           :value = "item2.uom_faktor_konversi"
                                                    >
                                                    <input type   = "hidden" 
                                                           :name  = "fname_jumlah(i,i2,'uom_harga_beli')" 
                                                           :value = "item2.uom_harga_beli"
                                                    >
                                                    <input type   = "hidden" 
                                                           :name  = "fname_jumlah(i,i2,'uom_harga_beli_ppn')" 
                                                           :value = "item2.uom_harga_beli"
                                                    >
                                                    <input type   = "hidden" 
                                                           :name  = "fname_jumlah(i,i2,'subtotal')" 
                                                           :value = "subtotal_uom(item2)"
                                                    >
                                                    <template v-if="item2">
                                                        <input type   = "hidden" 
                                                               :name  = "fname_jumlah(i,i2,'subtotal')" 
                                                               :value = "subtotal_uom(item2)"
                                                        >
                                                    </template>
                                                </td>
                                            </template>
                                            <template v-else-if="!item2">
                                                <td class="text-center">
                                                    <em>UOM Tidak Tersedia</em>
                                                </td>
                                            </template>
                                        </template>
                                        <td> 
                                            <input type   = "hidden" 
                                                   :name  = "fname_detail(i,'subtotal')" 
                                                   :value = "subtotal_item(item)"
                                            >
                                            <input type   = "text" 
                                                   class  = "form-control-modal" 
                                                   :value = "numberToStr(subtotal_item(item))" 
                                                   readonly
                                            >
                                        </td>
                                        <td>
                                            <button type   = "button" 
                                                    class  = "btn btn-sm btn-danger" 
                                                    title  = "Hapus"
                                                    @click = "remove(i)" 
                                            >
                                                <i class="mdi mdi-delete mx-1 font-16"></i>
                                            </button>
                                        </td>
                                    </tr>
                                </tbody>
                                <tfoot>
                                    <tr>
                                        <td></td>
                                        <td colspan="5"><b>Total<b></td>
                                        <td>
                                            <input type  = "text" 
                                                   class = "form-control-modal" 
                                                   :value="numberToStr(total_transaksi())" 
                                                   readonly
                                            >
                                        </td>
                                        <td></td>
                                    </tr>
                                </tfoot>
                            </table>
                        </div>
                    </div>
                    <div class="card-body">
                        <button type="submit" class=" btn btn-control btn-success float-end mx-1" onclick="submitConfirmation(event, this)">
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
        el      : '#app',
        data    : function() {
            return {
                cabang        : { data : [], id : '{{ user()->id_cabang }}' },
                principal     : { data : [], id : ''                        },
                produk        : { data : [], id : ''                        },
                user          : { data : [], id : '{{ user()->id }}'        },
                detail        : []
            }
        },
        methods : {
            fname_detail(i, attr) {
                return `detail[i][${i}][${attr}]`;
            },
            fname_jumlah(i, i2, attr) {
                return `detail[i][${i}][jumlah][${i2}][${attr}]`;
            },
            fname_total(i, i2, attr) {
                return `detail[i][${i}][total][${i2}][${attr}]`;
            },
            user_selected() { 
                return this.user.data.find( user => user.id == this.user.id );    
            },
            user_jabatan() {
                let user = this.user_selected();
                return user ? user.id_jabatan : null;
            },
            add() {
                let vm    = this;
                let exist = this.detail.find(data => data.produk_id == this.produk.id);

                if (exist) {
                    Alert().exist();
                } else {
                    $ .get  (  req(`/purchase-order/daftar-produk/${vm.produk.id}`) )
                      .done ( (res) => vm.detail.push(res.data)                     )
                }
            },
            remove(i) {
                this.detail.splice(i, 1);
            },
            subtotal_uom(item) {
                if (item) { return item.subtotal = item.uom_harga_beli_ppn * item.jumlah; }
            },
            subtotal_item(item) {
                return item.subtotal = item.jumlah.reduce(
                    (subtotal, item2) => subtotal + (!item2 ? 0 : item2.subtotal), 0
                );
            },
            total_transaksi() {
                return this.detail ? this.detail.reduce(
                    (total, item) => total + (!item ? 0 : item.subtotal), 0) 
                : 0;
            },
        },
        watch   : {
            'principal.id' : function(value) {
                let vm       = this;
                vm.detail    = [];
                vm.produk.id = null;

                if (value) {
                    $ .get  (  req("/produk/option"), { id_principal : value } )  
                      .done ( (res) => vm.produk.data = res.data               );
                }
            }
        },
        mounted : function() {
            let vm = this
            $ .get  (  req("/cabang/option")                )    
              .done ( (res) => vm.cabang.data = res.data    );
            $ .get  (  req("/user/option")                  )      
              .done ( (res) => vm.user.data = res.data      );
            $ .get  (  req("/principal/option")             ) 
              .done ( (res) => vm.principal.data = res.data );
        }
    });
</script>
@endpush