/*
 |--------------------------------------------------------------------------
 | Functions.
 |--------------------------------------------------------------------------
 |
 | Global Functions & Configurations Collection.
 |
 */
/**
 * Setting up Intial JQuery AJAX Request.
 * Adding CSRF Token which Applied on Every Request.
 * 
 * @requires JQuery `$`.
 */
$.ajaxSetup({
    data		: {'_token': $('#csrf').attr('content')},
    dataType	: "JSON",
    beforeSend	: function(xhr) {
        if (xhr && xhr.overrideMimeType) { 
            xhr.overrideMimeType("application/json;charset=UTF-8"); 
        }
    }
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
    if (typeof value === 'string' && value.trim() === '') { 
        return true; 
    } 
    if (Array.isArray(value) && value.length === 0) { 
        return true; 
    } 
    if (typeof value === 'object' && Object.keys(value).length === 0) { 
        return true; 
    } 
    if (number === true && (typeof value === 'number' && value === 0)) { 
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
        date  = new Date(date);
        year  = date.getFullYear();
        day   = date.getDate().toString().padStart(2, '0');
        month = (date.getMonth() + 1).toString().padStart(2, '0');
    
        return year+"-"+month+"-"+day;
	}
}
/**
 * Mendapatkan Waktu dalam Format AM/PM.
 * @return {text} Jam.
 */
function clock() {
    let date    = new Date();
    let hours   = date.getHours();
    let minutes = String(date.getMinutes()).padStart(2, '0');
    // let seconds = String(date.getSeconds()).padStart(2, '0');

    // Format Waktu ke AM/PM.
    let ampm    = hours >= 12 ? 'PM' : 'AM';
    
    // Format Jam AM/PM.
    hours = hours % 12;
    hours = hours ? hours : 12;
    hours = String(hours).padStart(2, '0');

    // return hours+" : "+minutes+" : "+seconds+" "+ampm;
    return hours+" : "+minutes+" "+ampm;
}
/** 
 * Konversi String ke Float.
 * 
 * @param {text} value yang akan Diformat.
 * @returns {number} Float Value.
 */
function strToFloat(value) {
    return isNull(value) || !isExist(value) ? null : parseFloat(value.replace(/\./g, "").replace(",", "."));
}
/** 
 * Konversi String ke Integer.
 * 
 * @param {text} value yang akan Diformat.
 * @returns {number} Integer Value.
 */
function strToInt(value) {
    return isNull(value) || !isExist(value) ? null : parseInt(value.replace(/\./g, "").replace(",", "."));
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
        parts[0]  = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ".");
        
        return parts.join(",");
    } else {
        return null;
    }
}
/**
 * Simplified Block UI.
 * @param {number} opsi 1 : block | 0 : unblock
 */
function block(opsi){
    switch (opsi) {
        case 1 :
            $.blockUI({ css : {
                color                   : '#fff',
                border                  : 'none',
                opacity                 : .5,
                padding                 : '15px',
                backgroundColor         : '#000',
                '-webkit-border-radius' : '10px',
                '-moz-border-radius'    : '10px'
            }});
        break;
        case 0 :
            $.unblockUI();
        break;
    }
}