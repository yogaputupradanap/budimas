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
                                    <th> Form </th>
                                    <th> Kode <em>Order</em> </th>
                                    <th> PIC <em>Order</em> </th>
                                    <th> Nama <em>Cabang</em> </th>
                                    <th> Nama <em>Principal</em> </th>
                                    <th> Tanggal <em>Order</em> </th>
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
@endsection
@push('page_scripts')
    <script>
        var app_list = new Vue({
            el: '#app-list',
            data: function() {
                return {
                    url: {
                        show: req("/purchase-order/daftar-purchase"),
                        edit: "penerimaan-barang/create/:id",
                    },
                    table: () => $('#app-list').find('table'),
                    data: {
                        columns: [{
                                data: ""
                            },
                            {
                                data: "btn_form"
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
                render(filter = null) {
                    Table().set(this.table()).destroy().paging().rowNumber(true).setDefaultOrder(6, 'desc')
                        .serverSide(this.data.columns, this.url.show, filter)
                        .init();
                    console.log('Rendering table with filter:', filter); // Log filter
                    return this;
                },
                actionForm(vm = this) {
                    this.table().on('click', '.btn-form', function() {
                        const id = $(this).val();
                        console.log('Navigating to edit form with ID:', id); // Log ID
                        window.location.href = vm.url.edit.replace(":id", id);
                    });
                    return this;
                },
            },
            mounted: function(vm = this) {
                this.render().actionForm();
                console.log('Component mounted'); // Log saat komponen dipasang
            }
        });
    </script>
@endpush
