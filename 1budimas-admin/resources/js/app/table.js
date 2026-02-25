/*
 |--------------------------------------------------------------------------
 | Table.
 |--------------------------------------------------------------------------
 |
 | Table Configurations Collection.
 | Some of Configurations Requiring JQuery DataTable Package.
 |
 */
/** 
 * DataTables Configuration and Comand Class.
 * @requires DataTable JQuery.
 * @see https://datatables.net/manual/options
 */ 
class DataTables {
    /**
     * Set Element of DataTable Instance.
     * Preaping The Properties.
     * 
     * @param el The Selected Element (Table).
     */
    constructor() {
        this.el = null;     // Elements / Selector of Table.
        this.p  = {         // DataTable Intial Properties.
            searching     : true,
            lengthChange  : true,
            autoWidth     : false,
            scrollX       : true,
            scrollY       : 400,
            info          : true,
            paging        : false,
            language      : { zeroRecords : "Tidak Ada Data Ditemukan" },
        };
    }
    /** 
     * Add Server Side Processing Properties. 
     * Need Serverside Extension.
     * 
     * @param {object} columns List dari Kolom yang ingin Ditampilkan
     *                         pada Tabel.
     * @param {text} url URL untuk Requesting Data menggunakan AJAX.
     * @param {object} data Data Filter untuk Requesting Data menggunakan AJAX.
     */ 
    serverSide(columns, url, data=null) {
        this.p.processing          = true;
        this.p.serverSide          = true;
        this.p.deferRender         = true;
        this.p.columns             = columns;
        this.p.ajax                = { url: url, type: 'POST', data: (d) => { $.extend(d, data); } };
        // this.p.language.processing =  `<div class="lds-ripple">
        //                                     <div class="lds-pos"></div>
        //                                     <div class="lds-pos"></div>
        //                                </div>`;
        return this;
    }
    /** 
     * Add Pagination Properties.
     * 
     * @param {number} len Pagination Data Length. Default 10.
     * @see https://datatables.net/reference/option/paging
     */ 
    paging(len = 10) {
        this.p.paging     = true;
        this.p.pageLength = len;
        this.p.lengthMenu = [[10, 25, 50, 75, 100, -1], [10, 25, 50, 75, 100, "Semua"]];

        return this;
    }
    /** 
     * Throw Default Error.
     */
    throw() {
        $.fn.dataTable.ext.errMode = 'none';
        return this;
    }
    /** 
     * Add Order Property for Ordering Columns.
     * 
     * @param {Array} order List of Default Sorting.
     * @see https://datatables.net/examples/basic_init/table_sorting.html
     */
    order(order) {
        this.p.order = order; 
        return this;
    }
    /**
     * Set Custom Value of Vertical Scroll Height.
     * @param {number} value Desired Value of The Scroll Height.
     */
    scrollY(value) {
        this.p.scrollY = value;
        return this;
    }
    /**
     * Set Custom Value of Vertical Scroll Height.
     * @param {boolean} option true : Active | false : Deactive.
     */
    rowNumber(option = true) {
        option 
            ? this.p.fnRowCallback = (row, data, index) => { $('td:eq(0)', row).html(index +1); }
            : delete this.p.fnRowCallback;
        
      return this;
    }
    /**
     * Set Element of DataTable Instance.
     * @param el The Selected Element (Table).
     */
    set(el) {
        this.el = el;
        return this;
    }
    /**
     * Destroy Existing DataTable API
     */
    destroy() {
        this.el.DataTable().clear().destroy();
        return this;
    }
    /**
     * Initialize DataTable API
     */
    init() {
        this.el.DataTable(this.p);
        return this;
    }
    /**
     * Getting Row Data.
     * @param {object} row Row Element with JQuery Masked.
     */
    getRowData(row) {
        return this.el.DataTable().row(row).data();
    }
    /**
     * Getting Row Data.
     */
    getRowsData() {
        return this.el.DataTable().rows().data().toArray();
    }
};

// Instantiate DataTable Class.
var Table = () => { return new DataTables(); }

// Remove White Background at Loading Animation.
$(".dataTables_processing.card").removeClass("card");