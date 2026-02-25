/*
 |--------------------------------------------------------------------------
 | Functions.
 |--------------------------------------------------------------------------
 |
 | Global Functions & Configurations Collection.
 |
 */
window.baseURL = window.baseURL || "";
window.req = function (endpoint) {
    return `${window.baseURL}/api/extra${endpoint}`;
};

/**
 * Setting up Intial JQuery AJAX Request.
 * Adding CSRF Token which Applied on Every Request.
 *
 * @requires JQuery `$`.
 */
$.ajaxSetup({
    headers: { Authorization: `Bearer ${window.userToken}` },
    data: { _token: $("#csrf").attr("content") },
    dataType: "JSON",
    beforeSend: function (xhr) {
        if (xhr && xhr.overrideMimeType) {
            xhr.overrideMimeType("application/json;charset=UTF-8");
        }
    },
});
/**
 * Validasi Apakah Value Konsong atau Tidak.
 *
 * @param {*} val The value to check.
 * @param {boolean} number If true, also check if the value is 0.
 * @return {boolean}
 */
function isNull(value, number = false) {
    if (value === null || value === undefined) {
        return true;
    }
    if (typeof value === "string" && value.trim() === "") {
        return true;
    }
    if (Array.isArray(value) && value.length === 0) {
        return true;
    }
    if (typeof value === "object" && Object.keys(value).length === 0) {
        return true;
    }
    if (number === true && typeof value === "number" && value === 0) {
        return true;
    }

    return false;
}
/**
 * Validasi Apakah Variable Ada atau Tidak.
 *
 * @param {*} variable The value to check.
 * @return {boolean}
 */
function isExist(variable) {
    if (variable !== undefined) {
        return true;
    }

    return false;
}
/**
 * Generate Angka secara Acak.
 *
 * @param {integer} min
 * @param {integer} max
 */
function rand(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}
/**
 * Mendapatkan Timestamp saat Ini.
 * @return {number} Timestamp.
 */
function time() {
    return Math.floor(Date.now() / 1000);
}
/**
 * Format Date ke Bentuk Y-m-d.
 *
 * @param {text} date.
 * @return {text} Tanggal.
 */
function date(date) {
    if (!isNull(date)) {
        date = new Date(date);
        year = date.getFullYear();
        day = date.getDate().toString().padStart(2, "0");
        month = (date.getMonth() + 1).toString().padStart(2, "0");

        return year + "-" + month + "-" + day;
    }
}
/**
 * Mendapatkan Waktu dalam Format AM/PM.
 * @return {text} Jam.
 */
function clock() {
    let date = new Date();
    let hours = date.getHours();
    let minutes = String(date.getMinutes()).padStart(2, "0");
    // let seconds = String(date.getSeconds()).padStart(2, '0');

    // Format Waktu ke AM/PM.
    let ampm = hours >= 12 ? "PM" : "AM";

    // Format Jam AM/PM.
    hours = hours % 12;
    hours = hours ? hours : 12;
    hours = String(hours).padStart(2, "0");

    // return hours+" : "+minutes+" : "+seconds+" "+ampm;
    return hours + " : " + minutes + " " + ampm;
}
/**
 * Konversi String ke Float.
 *
 * @param {text} value yang akan Diformat.
 * @returns {number} Float Value.
 */
function strToFloat(value) {
    return isNull(value) || !isExist(value)
        ? null
        : parseFloat(value.replace(/\./g, "").replace(",", "."));
}
/**
 * Konversi String ke Integer.
 *
 * @param {text} value yang akan Diformat.
 * @returns {number} Integer Value.
 */
function strToInt(value) {
    return isNull(value) || !isExist(value)
        ? null
        : parseInt(value.replace(/\./g, "").replace(",", "."));
}
/**
 * Konversi Number ke String.
 *
 * @param {number} value yang akan Diformat.
 * @returns {text} Text/String Value.
 */
function numberToStr(value) {
    if (!isNull(value)) {
        var parts = value.toString().split(".");
        parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ".");

        return parts.join(",");
    } else {
        return null;
    }
}
/**
 * Simplified Block UI.
 * @param {number} opsi 1 : block | 0 : unblock
 */
function block(opsi) {
    switch (opsi) {
        case 1:
            $.blockUI({
                css: {
                    color: "#fff",
                    border: "none",
                    opacity: 0.5,
                    padding: "15px",
                    backgroundColor: "#000",
                    "-webkit-border-radius": "10px",
                    "-moz-border-radius": "10px",
                },
            });
            break;
        case 0:
            $.unblockUI();
            break;
    }
}
/*
 |--------------------------------------------------------------------------
 | Alert.
 |--------------------------------------------------------------------------
 |
 | Global Alert Functions & Configurations Collection.
 |
 */
/**
 * Class of Alert Collections Utilizing
 * SweetAlert Lib.
 *
 * @requires SweetAlert2 `swal`.
 */
class Alerts {
    /** Firing Swal Alert dengan Opsi Untuk Notifikasi. */
    notice(icon, title, text) {
        Swal.fire({
            icon: icon,
            text: text,
            title: title,
            timer: 1500,
            showConfirmButton: false,
        });
    }
    /** Firing Swal Alert dengan Opsi Untuk Konfirmasi. */
    confirmation(icon, title, text) {
        return Swal.fire({
            icon: icon,
            text: text,
            title: title,
            confirmButtonText: "Lanjut",
            confirmButtonColor: "#4CAF50",
            showCancelButton: true,
            cancelButtonText: "Batal",
            cancelButtonColor: "#3085D6",
        });
    }
    /** Menampilkan Session Alert (Jika Ada) */
    session() {
        switch (parseInt($("#session-alert").val())) {
            case 1:
                this.success1();
                break;
            case 2:
                this.success2();
                break;
            case 3:
                this.success3();
                break;
            case 4:
                this.error();
                break;
        }
    }
    /** Menampilkan Alert Sukses Insert. */
    success1() {
        this.notice("success", "Berhasil", "Data Berhasil Ditambah.");
    }
    /** Menampilkan Alert Sukses Update. */
    success2() {
        this.notice("success", "Berhasil", "Data Berhasil Diubah.");
    }
    /** Menampilkan Alert Sukses Delete. */
    success3() {
        this.notice("success", "Berhasil", "Data Berhasil Dihapus.");
    }
    /** Menampilkan Pesan Error/Gagal. */
    error() {
        this.notice("error", "Kesalahan", "Silahkan Coba Kembali!");
    }
    /** Menampilkan Pesan Pembatalan Aksi. */
    cancel() {
        this.notice("warning", "Batal", "Aksi telah Dibatalkan!");
    }
    /** Menampilkan Pesan Peringatan Required Form Fill. */
    required1() {
        this.notice("warning", "Required", "Data Belum Lengakap!");
    }
    /** Menampilkan Pesan Peringatan Required Filter Form Fill. */
    required2() {
        this.notice("warning", "Required", "Isi Data Filter Terlebih Dahulu!");
    }
    /** Menampilkan Pesan Peringatan Exist Form Fill. */
    exist() {
        this.notice(
            "warning",
            "Data Sudah Ada",
            "Untuk Input Ulang, Hapus Data Terlebih Dahulu"
        );
    }
    /** Menampilkan Pesan Peringatan Exist Form Fill. */
    exist2() {
        this.notice(
            "warning",
            "Data Sudah Ada",
            "Data tidak dapat Ditambahkan, Silahkan melakukan Edit"
        );
    }
    /** Menampilkan Konfirmasi Submit Form. */
    submit() {
        return this.confirmation(
            "question",
            "Yakin untuk Submit?",
            "Pastikan Inputan Telah Sesuai!"
        );
    }
    /** Menampilkan Konfirmasi Delete Form. */
    delete() {
        return this.confirmation(
            "warning",
            "Yakin untuk Hapus?",
            "Data yang Dihapus, Tidak Dapat Dikembalikan!"
        );
    }
}

// Instantiate Alert Class.
Alert = () => {
    return new Alerts();
};

// Run Session Alert.
Alert().session();
/*
 |--------------------------------------------------------------------------
 | File Handler.
 |--------------------------------------------------------------------------
 |
 | Global File Handler Functions & Configurations Collection.
 |
 */
/**
 * CSV Handler (CSV to JSON)
 * CSV Downloader (Otomatis Mengunduh Resource/File)
 *
 * @param data `json` dengan konten {header:<val>, data:<val>, filename:<val>}
 * @param data `data.header` baris pertama dari data yang berisi nama kolom.
 * @param data `data.data` baris lainnya dari data yang berisi nilai untuk tiap kolom.
 * @param data `data.file_name` nama dari file csv yang akan dibuat.
 */
function csvDownload(data) {
    console.log("Show CSV Download Data: ", data);

    // Baris Pertama dari Data Berisi Nama Kolom.
    let header = data.header;

    // Baris Lainnya Berisi Nilai/Value dari Tiap Kolom.
    let items = data.data.map((item) => {
        return Object.values(item)
            .map(value => {
                if (typeof value === 'string') {
                    // Ganti koma dalam teks menjadi titik koma
                    return value.replace(/,/g, ' ');
                }
                return value;
            })
            .toString();
    });
    console.log("CSV Items: ", items);

    // Join Header dan Items ke Dalam satu Array.
    let rows = [header, ...items].join("\n");

    // Membuat Objek Blob (File) dengan Konten Csv.
    let blob = new Blob([rows], { type: "application/csv" });

    // Membuat Temporary Storage untuk File Csv.
    let url = URL.createObjectURL(blob);

    // Membuat Perintah Download Otomatis dengan Menggunakan Tag Anchor
    let a = document.createElement("a");
    a.href = url; // Lokasi (Temporary Storage) dari File.
    a.download = data.file_name;
    a.style.display = "none";

    document.body.appendChild(a);
    a.click();
    a.remove();

    // Menghapus File dari Temporary Storage.
    URL.revokeObjectURL(url);
}
/*
 |--------------------------------------------------------------------------
 | Form Handler.
 |--------------------------------------------------------------------------
 |
 | Global Form Handler Functions & Configurations Collection.
 |
 */
/**
 * Class of Form Control Handler Collections.
 * @requires JQuery `$`.
 */
class Forms {
    /**
     * Initialize Properties and Methods.
     */
    constructor() {
        this.valid = true;
        this.el = null; // Element of Form (Optional).
        this.errMsg1 = `<small class="form-error-info">Mohon Lengkapi Data!</small>`;
        this.errMsg2 = `<small class="form-error-info">Format E-mail Tidak Sesuai!</small>`;
    }
    /**
     * Memformat `Value` dari Input Money ke Bentuk `Uang`.
     * @todo Digunakan saat Selesai Submit/Request Form.
     */
    setMoneyFormat() {
        // Mencari Input Money.
        let inputs = this.el ? this.el.find(".money") : $(".money");

        // Memformat Value dari Input.
        if (inputs.length > 0) {
            inputs.each(function () {
                if (!isNull(this.value)) {
                    this.value = numberToStr(this.value);
                }
            });
        }
    }
    /**
     * Memformat `Value` dari Input Money ke Bentuk `Angka`.
     * @todo Digunakan saat Submit/Request Form.
     */
    resetMoneyFormat() {
        // Mencari Input Money.
        let inputs = this.el ? this.el.find(".money") : $(".money");

        // Memformat Value dari Input.
        if (inputs.length > 0) {
            inputs.each(function () {
                if (!isNull(this.value)) {
                    this.value = strToFloat(this.value);
                }
            });
        }
    }
    /**
     * Validation Checker Handler.
     * @param {number} option 0 : Reset | 1 : Check.
     */
    validate(option) {
        // Mencari Input, Text Area, dan Select.
        let inputs = this.el
            ? this.el.find("input,textarea,select").filter("[required]")
            : $("input,textarea,select").filter("[required]");

        if (inputs.length > 0) {
            switch (option) {
                case 0: // Reset Form Validasi.
                    inputs.each(function (i, input) {
                        // Remove Error Message.
                        $(input)
                            .closest(".form-group")
                            .find(".form-error-info")
                            .remove();

                        // Remove Form Error Styling Border Class.
                        $(input).is("select")
                            ? $(input)
                                  .next()
                                  .find(".select2-selection--single")
                                  .removeClass("form-error")
                            : $(input).removeClass("form-error");
                    });
                    break;
                case 1: // Check Form Validasi.
                    this.valid = true;
                    let instance = this;

                    inputs.each(function (i, input) {
                        if (isNull(input.value)) {
                            // Menandai Jika Form Tidak Valid.
                            if (instance.valid == true) {
                                instance.valid = false;
                            }

                            // Add Form Error Message.
                            $(input)
                                .closest(".form-group")
                                .find("label")
                                .append(instance.errMsg1);

                            // Add Form Error Styling Border Class.
                            $(input).is("select")
                                ? $(input)
                                      .next()
                                      .find(".select2-selection--single")
                                      .addClass("form-error")
                                : $(input).addClass("form-error");
                        }
                    });
                    break;
            }
        }
        return this;
    }
    /**
     * Show Confirmation of a Form Action.
     */
    confirm() {
        if (this.valid) {
            return Alert().submit();
        }
    }
    /**
     * Set the Element where Form/Inputs are Located.
     * @param {object} el Element with JQuery Selector.
     */
    set(el) {
        this.el = el;
        return this;
    }
}

// Instantiate Form Class.
var Form = () => {
    return new Forms();
};
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
        this.el = null; // Elements / Selector of Table.
        this.p = {
            // DataTable Intial Properties.
            searching: true,
            lengthChange: true,
            autoWidth: false,
            scrollX: true,
            scrollY: 400,
            info: true,
            paging: false,
            language: { zeroRecords: "Tidak Ada Data Ditemukan" },
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
    serverSide(columns, url, data = null) {
        this.p.processing = true;
        this.p.serverSide = true;
        this.p.deferRender = true;
        this.p.columns = columns;
        this.p.ajax = {
            url: url,
            type: "POST",
            data: (d) => {
                $.extend(d, data);
            },
        };
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
        this.p.paging = true;
        this.p.pageLength = len;
        this.p.lengthMenu = [
            [10, 25, 50, 75, 100],
            [10, 25, 50, 75, 100],
        ];

        return this;
    }
    /**
     * Throw Default Error.
     */
    throw() {
        $.fn.dataTable.ext.errMode = "none";
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
            ? (this.p.fnRowCallback = (row, data, index) => {
                  $("td:eq(0)", row).html(index + 1);
              })
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
}

// Instantiate DataTable Class.
var Table = () => {
    return new DataTables();
};

// Remove White Background at Loading Animation.
$(".dataTables_processing.card").removeClass("card");

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
class DataTables1 {
    /**
     * Set Element of DataTable Instance.
     * Preaping The Properties.
     *
     * @param el The Selected Element (Table).
     */
    constructor() {
        this.el = null; // Elements / Selector of Table.
        this.p = {
            // DataTable Intial Properties.
            searching: true,
            lengthChange: true,
            autoWidth: false,
            scrollX: true,
            scrollY: 400,
            info: true,
            paging: false,
            ordering: true,
            language: { zeroRecords: "Tidak Ada Data Ditemukan" },
            select: true,
        };
        this.defaultOrder = [[0, "asc"]];
        this.searchTimeout = null;
    }
    /**
     * Add debounce functionality to search
     * @param {number} delay - Delay in milliseconds (default: 500)
     */
    debounce(delay = 500) {
        this.searchDelay = delay;
        return this;
    }
    setDefaultOrder(column, direction = "asc") {
        this.defaultOrder = [[column, direction]];
        return this;
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
    serverSide(columns, url, data = null, type = "GET") {
        this.p.processing = true;
        this.p.serverSide = true;
        this.p.deferRender = true;
        this.p.columns = columns;
        this.p.order = this.defaultOrder;
        this.p.ajax = {
            url: url,
            type: type,
            data: (d) => {
                $.extend(d, data);
                if (d.order && d.order.length > 0) {
                    d.order_column = d.columns[d.order[0].column].data;
                    d.order_dir = d.order[0].dir;
                }
            },
        };

        return this;
    }
    /**
     * Add Pagination Properties.
     *
     * @param {number} len Pagination Data Length. Default 10.
     * @see https://datatables.net/reference/option/paging
     */
    paging(len = 10) {
        this.p.paging = true;
        this.p.pageLength = len;
        this.p.lengthMenu = [
            [10, 25, 50, 75, 100],
            [10, 25, 50, 75, 100],
        ];

        return this;
    }
    /**
     * Throw Default Error.
     */
    throw() {
        $.fn.dataTable.ext.errMode = "none";
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
            ? (this.p.fnRowCallback = (row, data, index) => {
                  $("td:eq(0)", row).html(index + 1);
              })
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
        const table = this.el.DataTable(this.p);

        // Add debounced search if delay is set
        if (this.searchDelay) {
            // Disable default search
            this.el.off("keyup.DT search.DT input.DT paste.DT cut.DT");

            // Custom search with debounce
            $(table.table().container())
                .find('input[type="search"]')
                .off("keyup search input paste cut")
                .on("input keyup paste cut", (e) => {
                    const searchValue = e.target.value;

                    clearTimeout(this.searchTimeout);
                    this.searchTimeout = setTimeout(() => {
                        if (table.search() !== searchValue) {
                            table.search(searchValue).draw();
                        }
                    }, this.searchDelay);
                });
        }

        return this;
    }
    /**
     * Getting Row Data.
     * @param {object} row Row Element with JQuery Masked.
     */
    getRowData(row) {
        return this.el.DataTable().row(row).data();
    }
}

// Instantiate DataTable Class.
var Table1 = () => {
    return new DataTables1();
};

// Remove White Background at Loading Animation.
$(".dataTables_processing.card").removeClass("card");

/**
 * Format periode dari bulan dan tahun
 *
 * @param {string|number|null} bulan - Nomor bulan (1-12)
 * @param {string|number|null} tahun - Tahun
 * @returns {string} Periode dalam format "[Bulan] [Tahun]"
 */
function formatPeriode(bulan, tahun) {
    const namaBulan = [
        "Januari",
        "Februari",
        "Maret",
        "April",
        "Mei",
        "Juni",
        "Juli",
        "Agustus",
        "September",
        "Oktober",
        "November",
        "Desember",
    ];

    // Jika keduanya kosong, return strip
    if (isNull(bulan) && isNull(tahun)) {
        return "-";
    }

    // Format bulan jika ada
    const textBulan = !isNull(bulan) ? namaBulan[parseInt(bulan) - 1] : "";
    const textTahun = !isNull(tahun) ? tahun : "";

    // Gabungkan sesuai data yang tersedia
    if (textBulan && textTahun) {
        return `${textBulan} ${textTahun}`;
    } else if (textBulan) {
        return textBulan;
    } else {
        return textTahun;
    }
}

/**
 * Format angka ke dalam format mata uang Rupiah Indonesia
 *
 * @param {number|string|null} nominal - Nilai yang akan diformat
 * @param {boolean} withSymbol - Tampilkan simbol mata uang (default: true)
 * @returns {string} Nominal dalam format Rupiah
 */
function formatRupiah(nominal, withSymbol = true) {
    // Jika null atau undefined, return strip
    if (isNull(nominal)) {
        return "-";
    }

    // Konversi ke number jika string dan ambil 2 digit tanpa pembulatan
    let num;
    if (typeof nominal === "string") {
        num = parseFloat(nominal);
    } else {
        num = nominal;
    }

    // Mengambil 2 digit tanpa pembulatan
    const strNum = num.toString();
    if (strNum.includes(".")) {
        const [whole, decimal] = strNum.split(".");
        num = parseFloat(whole + "." + decimal.substring(0, 2));
    }

    // Format menggunakan Intl.NumberFormat
    const formatter = new Intl.NumberFormat("id-ID", {
        style: withSymbol ? "currency" : "decimal",
        currency: "IDR",
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
    });

    return formatter.format(num);
}

/**
 * Format tanggal ke Y-m-d
 * @param {string} date - Tanggal yang akan diformat
 * @returns {string} Tanggal dalam format Y-m-d atau string kosong jika date null/undefined
 */
function formatDate(date) {
    if (date) {
        var d = new Date(date);
        var year = d.getFullYear();
        var month = String(d.getMonth() + 1).padStart(2, "0");
        var day = String(d.getDate()).padStart(2, "0");
        return `${year}-${month}-${day}`;
    }
    return "";
}
function floatToStr(floatValue) {
    // Pastikan nilai float dan batasi 2 digit desimal
    var number = parseFloat(floatValue || 0).toFixed(2);
    // Pisahkan bagian desimal
    var parts = number.split(".");
    // Format ribuan untuk bagian integer
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    // Gabungkan dengan koma sebagai separator desimal
    return parts.join(",");
}
function renderBadges(data, badgeClass = "bg-primary") {
    if (!data) return "";

    const items = data.split(",").map((item) => item.trim());
    let badges = "";

    items.forEach((item) => {
        badges += `<span class="badge px-3 rounded-pill ${badgeClass} me-2 mb-2">${item}</span>`;
    });

    return badges;
}

/**
 * Memfilter input NPWP agar hanya menerima angka, titik, dan strip
 *
 * @param {string} value - Input NPWP
 * @returns {string} - NPWP yang sudah difilter
 */
function filterNPWP(value) {
    return value.replace(/[^0-9.-]/g, "");
}

/**
 * Safe Parse JSON String
 */
function safeJSONParse(jsonString) {
    try {
        return JSON.parse(jsonString);
    } catch (e) {
        return jsonString;
    }
}
