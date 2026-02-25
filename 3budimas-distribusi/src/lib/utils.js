import axios from "axios";
import CryptoJS from "crypto-js";
import html2pdf from "html2pdf.js";

const API_URL = process.env.VUE_APP_API_URL;
const APP_SECRET = process.env.VUE_APP_SECRETS;

class encryption {
    encrypt(item) {
        const encrypt = CryptoJS.AES.encrypt(item, APP_SECRET).toString();

        return encrypt;
    }

    decrypt(item) {
        const decrypt = CryptoJS.AES.decrypt(item, APP_SECRET);
        const text = decrypt.toString(CryptoJS.enc.Utf8);

        return text;
    }
}

class session {
    constructor() {
        this.enc = new encryption();
    }

    setSession(cname, cvalue) {
        const d = new Date();
        d.setTime(d.getTime() + 7 * 24 * 60 * 60 * 1000);
        let expires = "expires=" + d.toUTCString();

        let encryptedValue = this.enc.encrypt(JSON.stringify(cvalue));

        document.cookie = cname + "=" + encryptedValue + ";" + expires + ";path=/";
    }

    getSession(cname) {
        let name = cname + "=";
        let decodedCookie = decodeURIComponent(document.cookie);
        let ca = decodedCookie.split(";");
        for (let i = 0; i < ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) == " ") {
                c = c.substring(1);
            }
            if (c.indexOf(name) == 0) {
                let decryptValue = this.enc.decrypt(c.substring(name.length, c.length));

                return JSON.parse(decryptValue);
            }
        }

        return null;
    }

    deleteSession(cname) {
        document.cookie =
            cname + "=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    }

    clearSession() {
        var cookies = document.cookie.split(";");

        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i];
            var eqPos = cookie.indexOf("=");
            var name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
            document.cookie =
                name + "=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
        }
    }
}

class localstorageDisk {
  constructor() {
    this.enc = new encryption();
  }

  setLocalStorage(key, item) {
    if (item === undefined || item === null) {
      localStorage.removeItem(key);
      return;
    }

    const value =
      typeof item === "string" ? item : JSON.stringify(item);

    localStorage.setItem(key, this.enc.encrypt(value));
  }

  getLocalStorage(key) {
    try {
      const local = localStorage.getItem(key);

      if (!local) return null;

      const decrypted = this.enc.decrypt(local);

      try {
        return JSON.parse(decrypted);
      } catch {
        return decrypted;
      }
    } catch (err) {
      console.warn("localStorage decrypt failed:", key);
      localStorage.removeItem(key);
      return null;
    }
  }

  removeLocalStorage(items) {
    items.forEach((item) => localStorage.removeItem(item));
  }

  clearLocalStorage() {
    localStorage.clear();
  }
}

export const localDisk = new localstorageDisk();

export const sessionDisk = new session();

export const apiUrl = API_URL;

export const axiosPostFetch = (url, body) =>
    axios.post(url, body, {
        headers: {
            Authorization: `Bearer ${
                sessionDisk.getSession("authUser_distribusi").token
            }`,
        },
    });

export const getClock = () => {
    let clock = new Date();

    const formatClock = new Intl.DateTimeFormat("default", {
        hour12: true,
        hour: "numeric",
        minute: "numeric",
    }).format(clock);

    const formatString =
        formatClock[0].length < 2 ? formatClock.padStart(8, "0") : formatClock;
    return formatString;
};

export const parseCurrency = (number) =>
    new Intl.NumberFormat("de-DE").format(number);

export const authFetch = (method, url, body) => {
    return new Promise(async (resolve, reject) => {
        let res;
        try {
            let params = {
                method,
                url,
                headers: {
                    Authorization: `Bearer ${
                        sessionDisk.getSession("authUser_distribusi").token
                    }`,
                },
            };

            if (method === "POST" || method === "PUT" || method == "PATCH")
                params["data"] = body || {};

            res = await axios(params);

            resolve(res);
        } catch (error) {
            reject(error?.response?.data || "");
        }
    });
};

export const fetchWithAuth = async (method, url, body) => {
    return new Promise(async (resolve, reject) => {
        let retryCount = 0;
        let error = "";
        console.log("try fetching in auth fetch");
        try {
            while (retryCount < 2) {
                const res = await authFetch(method, url, body).catch((err) => {
                    error = err;
                });
                if (res?.status === 200) {
                    resolve(res.data);
                    return;
                } else {
                    console.log("An error occurred, retrying to fetch data...");
                    retryCount++;
                }
            }

            throw error;
        } catch (error) {
            reject(error);
        }
    });
};

export const checkNaN = (value) => (isNaN(value) ? 0 : value);

export const deepCopy = (value) => {
    return JSON.parse(JSON.stringify(value));
};

export const logout = () => {
    sessionDisk.clearSession();

    window.location.reload();
};

export const formatLongNumberToString = (num, threshold = 2) => {
    var stringNum = "";
    const abbreviations = {
        Ribu: 1000,
        Juta: 1000000,
        Miliar: 1000000000,
    };

    for (const key in abbreviations) {
        if (num >= abbreviations[key]) {
            stringNum = (num / abbreviations[key]).toFixed(threshold) + " " + key;
        }
    }

    return stringNum;
};

export const getMonthString = (month) => {
    const monthStrings = {
        1: "Januari",
        2: "Februari",
        3: "Maret",
        4: "April",
        5: "Mei",
        6: "Juni",
        7: "Juli",
        8: "Agustus",
        9: "September",
        10: "Oktober",
        11: "November",
        12: "Desember",
    };

    return monthStrings[parseInt(month)];
};

export const getDayString = (day) => {
    const dayString = {
        0: "minggu",
        1: "senin",
        2: "selasa",
        3: "rabu",
        4: "kamis",
        5: "jumat",
        6: "sabtu",
    };

    return dayString[parseInt(day)];
};

export const downloadPdf = (
    id,
    filename,
    orientation = "portrait",
    format = "a4"
) => {
    let opt = {
        margin: 0,
        filename: `${filename || "file"}.pdf`,
        image: {type: "jpeg", quality: 0.7},
        html2canvas: {scale: 2.5},
        jsPDF: {
            unit: "in",
            format: "letter",
            orientation,
            compress: true,
            format,
        },
    };
    const element = document.getElementById(id);
    const cloneElement = element.cloneNode(true);
    cloneElement.removeAttribute("style");
    html2pdf().set(opt).from(cloneElement).save();
};

export const trimText = (text = "", treshold = 0) => {
    return text.length > treshold ? `${text.substring(0, treshold)} ....` : text;
};

export const getDateNow = (
    now = new Date(),
    useSlash = true,
    timeOnly = false
) => {
    const date = now.getDate().toString();
    const month = (now.getMonth() + 1).toString();
    const year = now.getFullYear();

    const formatDate = date.length > 1 ? date : "0" + date;
    const formatMonth = month.length > 1 ? month : "0" + month;

    const isUseSlash = useSlash ? "/" : "-";

    if (timeOnly) {
        const nowTime = getClock();

        if (/(pm)/gi.test(nowTime)) {
            let o = parseInt(nowTime.substring(0, 2)) + 12;
            return o + nowTime.substring(2, 5);
        }

        return nowTime.substring(0, 5);
    }

    return `${formatDate}${isUseSlash}${formatMonth}${isUseSlash}${year}`;
};

export const simpleDateNow = (date = Date.now()) => {
    return new Date(date).toISOString().split("T")[0];
};

export const numberToWords = (numStr) => {
    // Cek jika input adalah string yang berformat mata uang seperti "461.056,49"
    if (typeof numStr === "string") {
        // Pisahkan angka utama dan angka desimal
        const parts = numStr.split(",");
        const mainNumber = parts[0].replace(/\./g, ""); // Hapus titik pemisah ribuan
        const decimal = parts.length > 1 ? parts[1] : "";

        // Konversi bagian utama ke angka
        const mainInt = parseInt(mainNumber);

        // Konversi bagian utama ke kata-kata
        const mainWords = convertToWords(mainInt) + " rupiah";

        // Jika tidak ada desimal, kembalikan hasil langsung
        if (!decimal || decimal === "00") {
            return mainWords;
        }

        // Konversi bagian desimal ke kata-kata (sebagai dua digit)
        const decimalInt = parseInt(decimal);
        const decimalWords = convertToWords(decimalInt) + " sen";

        // Gabungkan hasil
        return `${mainWords} ${decimalWords}`;
    } else {
        // Jika input adalah angka, gunakan logika yang ada
        return convertToWords(numStr);
    }
};

// Fungsi untuk mengkonversi angka utama ke kata-kata
const convertToWords = (num) => {
    if (num === 0) return "nol";

    const belowTwenty = [
        "",
        "satu",
        "dua",
        "tiga",
        "empat",
        "lima",
        "enam",
        "tujuh",
        "delapan",
        "sembilan",
        "sepuluh",
        "sebelas",
        "dua belas",
        "tiga belas",
        "empat belas",
        "lima belas",
        "enam belas",
        "tujuh belas",
        "delapan belas",
        "sembilan belas",
    ];
    const tens = [
        "",
        "sepuluh",
        "dua puluh",
        "tiga puluh",
        "empat puluh",
        "lima puluh",
        "enam puluh",
        "tujuh puluh",
        "delapan puluh",
        "sembilan puluh",
    ];
    const thousands = ["", "ribu", "juta", "miliar", "triliun"];

    const helper = (n) => {
        if (n === 0) return "";
        else if (n < 20) return belowTwenty[n] + " ";
        else if (n < 100) return tens[Math.floor(n / 10)] + " " + helper(n % 10);
        else if (n < 1000) {
            if (Math.floor(n / 100) === 1) {
                return "seratus " + helper(n % 100);
            } else {
                return belowTwenty[Math.floor(n / 100)] + " ratus " + helper(n % 100);
            }
        }
        return "";
    };

    let result = "";
    let i = 0;

    // Handle special case for 0
    if (num === 0) return "nol";

    while (num > 0) {
        const chunk = num % 1000;

        if (chunk !== 0) {
            let chunkStr = helper(chunk);

            // Special case for 1000
            if (i === 1 && chunk === 1) {
                chunkStr = "seribu ";
            }
            // Special case for thousands: "satu ribu" -> "seribu"
            else if (i === 1 && chunk === 1) {
                chunkStr = "seribu ";
            }
            // Add the scale word (ribu, juta, etc)
            else if (chunk !== 0) {
                chunkStr += thousands[i] + " ";
            }

            result = chunkStr + result;
        }

        num = Math.floor(num / 1000);
        i++;
    }

    return result.trim();
};

export const getVoucherDiscount = (vouchers, tipe_voucher, harga_jual) => {
    const getValueDiscount1 = vouchers.filter((item) => {
        let splitString = String(item.kode).split("-");
        let lastIndexValue = splitString[splitString.length - 1];
        return lastIndexValue == tipe_voucher;
    });

    const hargaJualProduk = harga_jual;
    const getDiscount = getValueDiscount1
        .map((item) => {
            let discount = (item.nilai_diskon / hargaJualProduk) * 100;
            return discount;
        })
        .reduce((acc, val) => val + acc, 0);

    return getDiscount;
};

export const parse = (item) => JSON.parse(item);

export const parseNumberFromCurrency = (value) => {
    const removedDots = value.replace(/[a-zA-Z.]/g, "");
    return parseInt(removedDots);
};

/**
 * Format angka untuk menampilkan mata uang dengan format Indonesia
 * - Menggunakan titik (.) sebagai pemisah ribuan
 * - Menggunakan koma (,) sebagai pemisah desimal
 * - Contoh: 1000000.5 -> 1.000.000,5
 *
 * @param {number} value - Nilai yang akan diformat
 * @param {number} decimalPlaces - Jumlah digit desimal (default: 0 untuk non-desimal, null untuk menampilkan semua digit desimal yang ada)
 * @return {string} - String angka yang sudah diformat
 */
export const formatCurrency = (value, decimalPlaces = null) => {
    if (value === null || value === undefined) return "0";

    // Convert to number if it's a string
    const numValue = typeof value === "string" ? parseFloat(value) : value;

    // Check if the value has decimals
    const hasDecimal =
        String(numValue).includes(".") &&
        parseFloat(String(numValue).split(".")[1]) > 0;

    // If no decimals or decimalPlaces = 0, don't show decimals
    if (!hasDecimal || decimalPlaces === 0) {
        return Math.floor(numValue)
            .toString()
            .replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    }

    // If decimalPlaces is null, show all existing decimal digits
    if (decimalPlaces === null) {
        const parts = String(numValue).split(".");
        const integerPart = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ".");
        return `${integerPart},${parts[1]}`;
    }

    // Format with specified number of decimal places
    // First convert to fixed number of decimals
    const fixed = numValue.toFixed(decimalPlaces);
    const parts = fixed.split(".");

    // Format the integer part with periods as thousand separators
    const integerPart = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ".");

    // Return with comma as decimal separator
    return `${integerPart},${parts[1]}`;
};

/**
 * Format angka untuk menampilkan mata uang dengan format Indonesia
 * dan otomatis menampilkan digit desimal jika ada
 *
 * @param {number} value - Nilai yang akan diformat
 * @return {string} - String angka yang sudah diformat
 */
export const formatCurrencyAuto = (value) => {
    if (value === null || value === undefined) return "0";

    // Convert to number if it's a string
    const numValue = typeof value === "string" ? parseFloat(value) : value;

    // Cek apakah nilai memiliki desimal
    const hasDecimal =
        String(numValue).includes(".") &&
        parseFloat(String(numValue).split(".")[1]) > 0;

    // Jika tidak memiliki desimal, tidak tampilkan desimal
    if (!hasDecimal) {
        return Math.floor(numValue).toLocaleString("id-ID").replace(/,/g, ".");
    }

    // Jika ada desimal, tampilkan dengan format Indonesia dan maksimal 2 digit desimal
    const formattedNumber = numValue.toFixed(2); // Bulatkan ke 2 digit desimal
    const parts = formattedNumber.split(".");
    const integerPart = parseInt(parts[0])
        .toLocaleString("id-ID")
        .replace(/,/g, ".");
    return `${integerPart},${parts[1]}`;
};

/**
 * Format angka untuk menampilkan mata uang dengan format Indonesia
 * dan selalu menampilkan 1 digit desimal
 *
 * @param {number} value - Nilai yang akan diformat
 * @return {string} - String angka yang sudah diformat
 */
export const formatCurrencyWithDecimal = (value) => {
    return formatCurrency(value, 1);
};

export function stringToNumber(str) {
    // Remove all thousand separators (periods)
    let cleanStr = str.replace(/\./g, "");

    // Replace decimal separator (comma) with a period
    cleanStr = cleanStr.replace(",", ".");

    // Convert to number
    return parseFloat(cleanStr);
}

/**
 * Menghitung subtotal berdasarkan harga jual dan jumlah produk
 * @param {Object} product - Data produk
 * @returns {number} Subtotal produk
 */
export const calculateProductSubtotal = (product, mode = "order") => {
    // Mode realisasi - menggunakan field realisasi yang sudah dihitung dalam pieces
    if (mode === "realisasi") {
        const totalRealisasi = product.realisasi || 0;
        return totalRealisasi * (product.harga_jual || 0);
    }

    // Ambil nilai-nilai yang diperlukan
    const hargaJual = product.harga_jual || 0;
    const konversiLevel2 = product.konversi_level2 || 1; // Konversi box ke pieces
    const konversiLevel3 = product.konversi_level3 || 1; // Konversi karton ke pieces

    // Jumlah produk di setiap level berdasarkan mode
    let karton, box, pieces;

    if (mode === "delivered") {
        karton = product.karton_delivered;
        box = product.box_delivered;
        pieces = product.pieces_delivered;
    } else if (mode === "picked") {
        karton = product.karton_picked;
        box = product.box_picked;
        pieces = product.pieces_picked;
    } else {
        // mode === "order"
        karton = product.karton_order;
        box = product.box_order;
        pieces = product.pieces_order;
    }

    // Hitung total pieces
    const totalPieces = karton * konversiLevel3 + box * konversiLevel2 + pieces;

    // Hitung subtotal berdasarkan harga jual dan total pieces
    const subtotal = hargaJual * totalPieces;

    return subtotal;
};
/**
 * Menghitung diskon untuk Voucher Reguler 1 (v1r)
 * @param {Object} product - Data produk dan voucher
 * @param {boolean} isActive - Status voucher aktif atau tidak
 * @param {number} totalOrderSubtotal - Total subtotal seluruh pesanan
 * @returns {number} Nilai diskon
 */
export const calculateVoucher1rDiscount = (
    product,
    isActive = true,
    totalOrderSubtotal = 0,
    mode = "order"
) => {
    if (!isActive || !product.v1r_persen) return 0;

    // Hitung subtotal produk dengan parameter mode
    const subtotal = calculateProductSubtotal(product, mode);

    // Periksa syarat minimal subtotal pembelian terhadap TOTAL pesanan
    if (
        product.v1r_minimal_subtotal_pembelian &&
        totalOrderSubtotal < product.v1r_minimal_subtotal_pembelian
    ) {
        return 0;
    }

    // Hitung diskon berdasarkan persentase
    return (product.v1r_persen / 100) * subtotal;
};

// Untuk voucher reguler v2r
export const calculateVoucher2rDiscount = (
    product,
    hargaSetelahDiskon,
    isActive = true,
    totalOrderSubtotal = 0,
    mode = "order"
) => {
    if (!isActive || !product.v2r_persen) return 0;

    // Periksa syarat minimal subtotal pembelian terhadap TOTAL pesanan
    if (
        product.v2r_minimal_subtotal_pembelian &&
        totalOrderSubtotal < product.v2r_minimal_subtotal_pembelian
    ) {
        return 0;
    }

    // Hitung diskon berdasarkan persentase
    return (product.v2r_persen / 100) * hargaSetelahDiskon;
};

// Untuk voucher reguler v3r
export const calculateVoucher3rDiscount = (
    product,
    hargaSetelahDiskon,
    isActive = true,
    totalOrderSubtotal = 0,
    mode = "order"
) => {
    if (!isActive || !product.v3r_persen) return 0;

    // Periksa syarat minimal subtotal pembelian terhadap TOTAL pesanan
    if (
        product.v3r_minimal_subtotal_pembelian &&
        totalOrderSubtotal < product.v3r_minimal_subtotal_pembelian
    ) {
        return 0;
    }

    // Hitung diskon berdasarkan persentase
    return (product.v3r_persen / 100) * hargaSetelahDiskon;
};

/**
 * Menghitung diskon untuk Voucher Produk 2 (v2p)
 * @param {Object} product - Data produk dan voucher
 * @param {number} hargaSetelahDiskon - Harga setelah diskon voucher sebelumnya
 * @param {boolean} isActive - Status voucher aktif atau tidak
 * @param {string} mode - Mode perhitungan: "order", "delivered", "picked", "realisasi"
 * @returns {number} Nilai diskon
 */
export const calculateVoucher2pDiscount = (
    product,
    hargaSetelahDiskon,
    isActive = true,
    mode = "order"
) => {
    if (!isActive) return 0;

    // Cek syarat minimal jumlah produk
    if (product.v2p_minimal_jumlah_produk && product.v2p_level_uom) {
        let totalJumlahUOM = 0;

        if (mode === "realisasi") {
            // Untuk mode realisasi, gunakan total pieces dari field realisasi
            const totalPieces = product.realisasi || 0;

            // Konversi ke level UOM yang diminta oleh voucher
            const piecesPerBox = product.konversi_level2 || 1;
            const piecesPerKarton = product.konversi_level3 || 1;

            switch (product.v2p_level_uom) {
                case 1: // pieces
                    totalJumlahUOM = totalPieces;
                    break;
                case 2: // box
                    totalJumlahUOM = totalPieces / piecesPerBox;
                    break;
                case 3: // karton
                    totalJumlahUOM = totalPieces / piecesPerKarton;
                    break;
            }
        } else {
            // Logic yang sudah ada untuk mode lainnya
            const piecesPerBox = product.konversi_level2 || 1;
            const piecesPerKarton = product.konversi_level3 || 1;

            // Pilih field yang sesuai berdasarkan mode
            const pieces =
                mode === "order" ? product.pieces_order : product.pieces_picked;
            const box = mode === "order" ? product.box_order : product.box_picked;
            const karton =
                mode === "order" ? product.karton_order : product.karton_picked;

            const totalPieces =
                (pieces || 0) +
                (box || 0) * piecesPerBox +
                (karton || 0) * piecesPerKarton;

            // Konversi ke level UOM yang diminta oleh voucher
            switch (product.v2p_level_uom) {
                case 1: // pieces
                    totalJumlahUOM = totalPieces;
                    break;
                case 2: // box
                    totalJumlahUOM = totalPieces / piecesPerBox;
                    break;
                case 3: // karton
                    totalJumlahUOM = totalPieces / piecesPerKarton;
                    break;
            }
        }

        if (totalJumlahUOM < product.v2p_minimal_jumlah_produk) {
            return 0;
        }
    }

    // Hitung diskon
    let discount = 0;

    if (product.v2p_kategori_voucher === 1 && product.v2p_persen) {
        // Kategori 1: diskon persentase
        discount = (product.v2p_persen / 100) * hargaSetelahDiskon;
    } else if (product.v2p_kategori_voucher === 2 && product.v2p_nominal_diskon) {
        // Kategori 2: diskon nominal per satuan
        let totalPieces = 0;

        if (mode === "realisasi") {
            totalPieces = product.realisasi || 0;
        } else {
            const piecesPerBox = product.konversi_level2 || 1;
            const piecesPerKarton = product.konversi_level3 || 1;

            // Pilih field yang sesuai berdasarkan mode
            const pieces =
                mode === "order" ? product.pieces_order : product.pieces_picked;
            const box = mode === "order" ? product.box_order : product.box_picked;
            const karton =
                mode === "order" ? product.karton_order : product.karton_picked;

            totalPieces =
                (pieces || 0) +
                (box || 0) * piecesPerBox +
                (karton || 0) * piecesPerKarton;
        }

        discount = product.v2p_nominal_diskon;
    }

    return discount;
};

/**
 * Menghitung diskon untuk Voucher Produk 3 (v3p)
 * @param {Object} product - Data produk dan voucher
 * @param {number} hargaSetelahDiskon - Harga setelah diskon voucher sebelumnya
 * @param {boolean} isActive - Status voucher aktif atau tidak
 * @param {string} mode - Mode perhitungan: "order", "delivered", "picked", "realisasi"
 * @returns {number} Nilai diskon
 */
export const calculateVoucher3pDiscount = (
    product,
    hargaSetelahDiskon,
    isActive = true,
    mode = "order"
) => {
    if (!isActive) return 0;

    // Hitung diskon
    let discount = 0;

    if (product.v3p_kategori_voucher === 1 && product.v3p_persen) {
        // Kategori 1: diskon persentase
        discount = (product.v3p_persen / 100) * hargaSetelahDiskon;
    } else if (product.v3p_kategori_voucher === 2 && product.v3p_nominal_diskon) {
        // Kategori 2: diskon nominal per satuan
        let totalPieces = 0;

        if (mode === "realisasi") {
            totalPieces = product.realisasi || 0;
        } else {
            const piecesPerBox = product.konversi_level2 || 1;
            const piecesPerKarton = product.konversi_level3 || 1;

            // Pilih field yang sesuai berdasarkan mode
            const pieces =
                mode === "order" ? product.pieces_order : product.pieces_picked;
            const box = mode === "order" ? product.box_order : product.box_picked;
            const karton =
                mode === "order" ? product.karton_order : product.karton_picked;

            totalPieces =
                (pieces || 0) +
                (box || 0) * piecesPerBox +
                (karton || 0) * piecesPerKarton;
        }

        discount = product.v3p_nominal_diskon ;
    }

    return discount;
};

/**
 * Menghitung total diskon dari semua voucher dan harga akhir
 * Urutan perhitungan baru: v1r → v2r → v3r → v2p → v3p
 * @param {Object} product - Data produk
 * @param {Object} voucherStatus - Status voucher (aktif/tidak)
 * @param {number} totalOrderSubtotal - Total subtotal seluruh pesanan
 * @returns {Object} Hasil perhitungan diskon
 */
export const calculateProductDiscounts = (
    product,
    voucherStatus = null,
    totalOrderSubtotal = 0,
    mode = "order"
) => {
    const round2 = (val) => Number(parseFloat(val || 0).toFixed(2));

    // Default semua voucher aktif jika tidak ada status
    const defaultStatus = {
        v1r_active: true,
        v2r_active: true,
        v3r_active: true,
        v2p_active: true,
        v3p_active: true,
    };

    // Gabungkan dengan status yang diberikan
    const status = { ...defaultStatus, ...(voucherStatus || {}) };

    // Hitung subtotal yang benar terlebih dahulu dengan parameter mode
    const subtotal = round2(calculateProductSubtotal(product, mode));

    // Jika total subtotal pesanan tidak diberikan, gunakan subtotal produk ini
    if (!totalOrderSubtotal) {
        totalOrderSubtotal = subtotal;
    }

    // Langkah 1: Hitung diskon voucher reguler 1 (v1r)
    const diskon1r = round2(
        calculateVoucher1rDiscount(product, status.v1r_active, totalOrderSubtotal, mode)
    );
    const hargaSetelahDiskon1r = round2(subtotal - diskon1r);

    // Langkah 2: Hitung diskon voucher reguler 2 (v2r)
    const diskon2r = round2(
        calculateVoucher2rDiscount(product, hargaSetelahDiskon1r, status.v2r_active, totalOrderSubtotal, mode)
    );
    const hargaSetelahDiskon2r = round2(hargaSetelahDiskon1r - diskon2r);

    // Langkah 3: Hitung diskon voucher reguler 3 (v3r)
    const diskon3r = round2(
        calculateVoucher3rDiscount(product, hargaSetelahDiskon2r, status.v3r_active, totalOrderSubtotal, mode)
    );
    const hargaSetelahDiskon3r = round2(hargaSetelahDiskon2r - diskon3r);

    // Langkah 4: Hitung diskon voucher produk 2 (v2p)
    const diskon2p = round2(
        calculateVoucher2pDiscount(product, hargaSetelahDiskon3r, status.v2p_active, mode)
    );
    const hargaSetelahDiskon2p = round2(hargaSetelahDiskon3r - diskon2p);

    // Langkah 5: Hitung diskon voucher produk 3 (v3p)
    const diskon3p = round2(
        calculateVoucher3pDiscount(product, hargaSetelahDiskon2p, status.v3p_active, mode)
    );
    const hargaSetelahDiskon3p = round2(hargaSetelahDiskon2p - diskon3p);

    // Hitung total diskon
    const totalDiskon = round2(diskon1r + diskon2r + diskon3r + diskon2p + diskon3p);

    // Hitung PPN
    const ppnRate = product.ppn ? product.ppn / 100 : 0;
    const ppnValue = round2(hargaSetelahDiskon3p * ppnRate);

    return {
        subtotal,
        diskon1r,
        diskon2r,
        diskon3r,
        diskon2p,
        diskon3p,
        totalDiskon,
        hargaSetelahDiskon: hargaSetelahDiskon3p,
        ppnValue,
    };
};


export const statusFakturText = (status) => {
    const statusText = {
        "-1": "denied",
        0: "draft",
        1: "printed",
        2: "unpaid",
        3: "paid",
        4: "canceled",
    };

    return statusText[status] || "Tidak Diketahui";
};

export const statusOrderText = (status) => {
    const statusText = {
        "-1": "denied",
        0: "draft",
        1: "booked",
        2: "scheduled",
        3: "picked",
        4: "shipping",
        5: "revision",
        6: "delivered",
        7: "canceled",
        8: "return",
        9: "reschedule",
        10: "rescheduled",
        11: "reshipping",
    };

    return statusText[status] || "Tidak Diketahui";
};


export const calculateKonversi = (value, data_konversi) => {
    const konversi = {
        pieces: 0,
        box: 0,
        karton: 0
    };
    const level1 = data_konversi.find(
        (val) => val.level === 1
    );
    const level2 = data_konversi.find(
        (val) => val.level === 2
    );
    const level3 = data_konversi.find(
        (val) => val.level === 3
    );
    konversi.pieces = value.pieces + (value.box * level2.faktor_konversi) + (value.karton * level3.faktor_konversi);
    konversi.box = Math.floor(konversi.pieces / level2.faktor_konversi);
    konversi.karton = Math.floor(konversi.pieces / level3.faktor_konversi);

    return konversi;
};

export const ToParams = (obj = {}) => {
  return new URLSearchParams(obj).toString();
};