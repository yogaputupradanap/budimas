@extends('layouts.main')
@section('content')
    @include('partials.breadcrumb')
    <!-- Content Container -->
    <div class="container-fluid">
        <div class="row m-1">
            <div class="col-12">
                <div class="card form" id="app_filter">
                    <div class="card-header">
                        <span class="card-title">Form Filter Laporan</span>
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
                                    <label>Nama Principal</label>
                                    <select2 name="principal_id" v-model="principal.id" :options="principal.data">
                                    </select2>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="form-group">
                                    <label>Status</label>
                                    <select2 name="status" v-model="status.id" :options="status.data">
                                    </select2>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="form-group">
                                    <label>Rentang Tanggal</label>
                                    <div class="form-group position-relative p-0 m-0" style="cursor: pointer;">
                                        <i class="mdi mdi-calendar position-absolute"
                                            style="top: 50%; transform: translateY(-50%); left: 10px;"></i>
                                        <input type="text" id="date-range" class="form-control"
                                            placeholder="Masukkan Rentang Tanggal" readonly
                                            style="padding-left: 35px; cursor: pointer;">
                                        <input type="hidden" name="start_date" v-model="dateRange.start">
                                        <input type="hidden" name="end_date" v-model="dateRange.end">
                                    </div>

                                </div>
                            </div>
                            <div class="col-12 d-flex justify-content-end mt-2">
                                <div class="form-group d-flex gap-2">
                                    <button class="btn btn-danger px-4" type="button" @click="resetFilter">
                                        <i class="mdi mdi-refresh"></i> Reset
                                    </button>
                                    <button class="btn btn-primary px-4" type="button" @click="applyFilter">
                                        <i class="mdi mdi-magnify"></i> Filter
                                    </button>
                                </div>
                            </div>

                        </div>
                    </div>
                </div>
                <div class="card form" id="app-list">
                    <div class="card-header">
                        <span class="card-title">Laporan Order</span>
                    </div>
                    <div class="card-body">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th> # </th>
                                    <th> Detail </th>
                                    <th> Cetak </th>
                                    <th> Kode <em>Order</em> </th>
                                    <th> Nama <em>Cabang</em> </th>
                                    <th> Nama <em>Principal</em> </th>
                                    <th> Tanggal <em>Order</em> </th>
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
@endsection

@push('page_scripts')
    <script>
        var app_list = new Vue({
            el: '#app-list',
            data: function() {
                return {
                    url: {
                        show: req('/purchase-order/daftar-laporan'),
                        detail: '/laporan-order/',
                    },
                    table: () => $('#app-list').find('table'),
                    data: {
                        columns: [{
                                data: "",
                                orderable: false
                            },
                            {
                                data: "btn_detail",
                                orderable: false
                            },
                            {
                                data: "btn_cetak",
                                orderable: false
                            },
                            {
                                data: "kode",
                                orderable: true
                            },
                            {
                                data: "cabang_nama",
                                orderable: true
                            },
                            {
                                data: "principal_nama",
                                orderable: true
                            },
                            {
                                data: "tanggal",
                                orderable: true
                            },
                            {
                                data: "btn_status",
                                orderable: true
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
                    const table = Table()
                        .set(this.table())
                        .destroy()
                        .paging()
                        .rowNumber(true)
                        .setDefaultOrder(6, 'asc')
                        .serverSide(this.data.columns, this.url.show, filter);

                    table.init();

                    // Tambahkan event listener untuk btn-detail
                    this.table().on('click', '.btn-detail', (e) => {
                        e.preventDefault();
                        const row = $(e.currentTarget).closest('tr');
                        const data = this.getTableRowData(row);
                        window.location.href = this.url.detail + data.id;
                    });

                    return table;
                }
            },
            mounted: function() {
                this.renderTable();
                console.log('List component mounted');
            }
        });

        var app_filter = new Vue({
            el: '#app_filter',
            data: function() {
                return {
                    principal: {
                        data: [],
                        id: ''
                    },
                    status: {
                        data: [{
                                id: 1,
                                text: 'Request'
                            },
                            {
                                id: 2,
                                text: 'Need Confirm'
                            },
                            {
                                id: 3,
                                text: 'In Transit'
                            },
                            {
                                id: 4,
                                text: 'Closed'
                            }
                        ],
                        id: ''
                    },
                    dateRange: {
                        start: '', // Changed to empty string
                        end: '' // Changed to empty string
                    }
                }
            },
            methods: {
                initDateRangePicker() {
                    const vm = this;
                    $('#date-range').daterangepicker({
                        autoUpdateInput: false, // Set to false to prevent auto-update
                        buttonClasses: 'btn',
                        applyClass: 'btn-primary',
                        cancelClass: 'btn-default',
                        locale: {
                            format: 'DD/MM/YYYY',
                            separator: ' - ',
                            applyLabel: 'Pilih',
                            cancelLabel: 'Batal',
                            customRangeLabel: 'Rentang Kustom',
                        },
                        ranges: {
                            'Hari Ini': [moment(), moment()],
                            'Kemarin': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
                            'Minggu Ini': [moment().startOf('week'), moment().endOf('week')],
                            'Bulan Ini': [moment().startOf('month'), moment().endOf('month')],
                            'Bulan Lalu': [moment().subtract(1, 'month').startOf('month'), moment()
                                .subtract(1, 'month').endOf('month')
                            ]
                        },
                        alwaysShowCalendars: true,
                        opens: 'left'
                    });

                    // Handle the apply event
                    $('#date-range').on('apply.daterangepicker', function(ev, picker) {
                        $(this).val(picker.startDate.format('DD/MM/YYYY') + ' - ' + picker.endDate.format(
                            'DD/MM/YYYY'));
                        vm.dateRange.start = picker.startDate.format('YYYY-MM-DD');
                        vm.dateRange.end = picker.endDate.format('YYYY-MM-DD');
                    });

                    // Handle the cancel event
                    $('#date-range').on('cancel.daterangepicker', function(ev, picker) {
                        $(this).val('');
                        vm.dateRange.start = '';
                        vm.dateRange.end = '';
                    });
                },
                resetFilter() {
                    // Reset all filter values
                    this.principal.id = '';
                    this.status.id = '';
                    this.dateRange.start = '';
                    this.dateRange.end = '';

                    // Reset daterangepicker display
                    $('#date-range').val('');

                    // Reset select2 components
                    $('select[name="principal_id"]').val(null).trigger('change');
                    $('select[name="status"]').val(null).trigger('change');

                    // Render table without filters
                    app_list.renderTable();
                },
                applyFilter() {
                    const filters = {
                        principal_id: this.principal.id,
                        status: this.status.id,
                        start_date: this.dateRange.start,
                        end_date: this.dateRange.end
                    };

                    app_list.renderTable(filters);
                }
            },
            mounted: function() {
                const vm = this;
                // Mengambil data principal saat komponen dimuat
                $.get(req("/principal/option"))
                    .done((res) => vm.principal.data = res.data);

                this.$nextTick(() => {
                    this.initDateRangePicker();
                });
            }
        });
    </script>
@endpush
